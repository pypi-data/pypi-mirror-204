import math
from torch import tanh

import mlflow
import torch
from pytorch_lightning import LightningModule
from torch import Tensor
from torch.nn import Linear, TransformerEncoderLayer, LayerNorm, TransformerEncoder, \
    TransformerDecoderLayer, TransformerDecoder, Module, Dropout
from torch.nn.functional import l1_loss, max_pool1d, relu

from tradeX.utils.losses import log_return_loss


class ITTransformer(LightningModule):
    def __init__(self, d_model: int = 512, nhead: int = 1, dim_feedforward: int = 2048,
                 output_d=9, input_d=9, d_in_decoder=4, position_encode=False):
        super(ITTransformer, self).__init__()

        # modules
        self.fc_in_en = Linear(input_d, d_model)
        self.pos_encoder = PositionalEncoder(max_seq_len=1000, d_model=d_model)

        encoder_layer = TransformerEncoderLayer(d_model, nhead, dim_feedforward, batch_first=True)
        encoder_norm = LayerNorm(d_model)
        self.encoder = TransformerEncoder(encoder_layer, 6, encoder_norm)

        # self.fc_in_de = Linear(4, d_model)
        # decoder_layer = TransformerDecoderLayer(d_model, nhead, dim_feedforward, batch_first=True)
        # decoder_norm = LayerNorm(d_model)
        # self.decoder = TransformerDecoder(decoder_layer, 6, decoder_norm)

        self.fc_reg = Linear(d_model, output_d)

        self.position_encode = position_encode
        self.init_weights()

    def init_weights(self) -> None:
        initrange = 0.1
        for layer in [self.fc_in_en, self.fc_reg]:
            layer.weight.data.uniform_(-initrange, initrange)
            layer.bias.data.zero_()
            layer.weight.data.uniform_(-initrange, initrange)

    def forward(self, src):
        """
        :param src: B x L x D_in
        :param tgt: B x W x D_out
        :param tgt_y: same as $tgt
        :return: shifted right of $tgt in shape of B x W x D_out
        """
        target = src[:, -1:, :4]
        x = self.fc_in_en(src)  # B x L x D
        x = relu(x)
        if self.position_encode:
            x = self.pos_encoder(x)
        mem = self.encoder(x)  # B x L x D
        mem = relu(mem)  # B x L x D
        out = self.fc_reg(mem[:,-1]) # B x D_out
        return out
        # decoder_in = self.fc_in_de(target)  # B x 1 x D
        # decoder_in = relu(decoder_in)
        # out = self.decoder(decoder_in, mem)  # B x 1 x D
        # out = relu(out)
        # out = self.fc_reg(out)  # B x 1 x D_out
        # return out.view(len(out), -1)

    def train_val_step(self, batch, batch_id, key_log):
        input = batch["input"].float()  # B x L_back x D_in
        gt_reg = batch["log_return"].float()  # B x L_ahead x D_in
        log_return_pred = self(input)  # B x 3

        loss = l1_loss(log_return_pred, gt_reg, reduction="mean")

        self.log(f"{key_log}_loss", loss.item())
        mlflow.log_metric(f"{key_log}_loss", loss.item())
        return loss

    def training_step(self, batch, batch_id):
        self.log("learning_rate", self.lr_scheduler.get_last_lr()[0])
        return self.train_val_step(batch, batch_id, "train")

    def validation_step(self, batch, batch_id):
        return self.train_val_step(batch, batch_id, "val")

    def set_optimizer(self, optimizer, lr_scheduler):
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def configure_optimizers(self):
        return [self.optimizer], [self.lr_scheduler]


class PositionalEncoder(Module):
    """
    The authors of the original transformer paper describe very succinctly what
    the positional encoding layer does and why it is needed:

    "Since our model contains no recurrence and no convolution, in order for the
    model to make use of the order of the sequence, we must inject some
    information about the relative or absolute position of the tokens in the
    sequence." (Vaswani et al, 2017)
    Adapted from:
    https://pytorch.org/tutorials/beginner/transformer_tutorial.html
    """

    def __init__(
            self,
            dropout: float = 0.1,
            max_seq_len: int = 5000,
            d_model: int = 512,
            batch_first: bool = False
    ):
        """
        Parameters:
            dropout: the dropout rate
            max_seq_len: the maximum length of the input sequences
            d_model: The dimension of the output of sub-layers in the model
                     (Vaswani et al, 2017)
        """

        super().__init__()

        self.d_model = d_model

        self.dropout = Dropout(p=dropout)

        self.batch_first = batch_first

        self.x_dim = 1 if batch_first else 0

        # copy pasted from PyTorch tutorial
        position = torch.arange(max_seq_len).unsqueeze(1)

        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))

        pe = torch.zeros(max_seq_len, 1, d_model)

        pe[:, 0, 0::2] = torch.sin(position * div_term)

        pe[:, 0, 1::2] = torch.cos(position * div_term)

        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: Tensor, shape [batch_size, enc_seq_len, dim_val] or
               [enc_seq_len, batch_size, dim_val]
        """

        x = x + self.pe[:x.size(self.x_dim)]

        return self.dropout(x)
