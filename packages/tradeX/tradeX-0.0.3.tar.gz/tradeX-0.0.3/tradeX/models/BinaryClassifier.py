import mlflow
import torch
from pytorch_lightning import LightningModule
from torch.nn import TransformerEncoder, TransformerEncoderLayer, LayerNorm, Linear
from torch.nn.functional import leaky_relu, binary_cross_entropy_with_logits, cross_entropy


class BinaryClassifier(LightningModule):
    """
    Predict at this point will coin price bump, dump or keep stable.
    """

    def __init__(self, d_in=9, d_out=3, d_model=64, nhead=8, dim_ff=64, look_back=100):
        super(BinaryClassifier, self).__init__()
        self.d_model = d_model
        self.in_fc = Linear(d_in, d_model)
        encoder_layer = TransformerEncoderLayer(d_model, nhead, dim_ff, batch_first=True)
        encoder_norm = LayerNorm(d_model)
        self.lookback = look_back
        self.encoder = TransformerEncoder(encoder_layer, 6, encoder_norm)
        self.fc_out = Linear(d_model * look_back, d_out)

    def forward(self, x):
        """
        :param x: B x L x  d_in
        :return:
        """
        x = self.in_fc(x)  # B x L x d_model
        x = self.encoder(x)  # B x L x d_model
        x = x.view(x.shape[0], -1)  # B x E where E = d_model x L
        x = leaky_relu(x)
        x = self.fc_out(x)  # B x d_out
        return x

    def training_step(self, batch, batch_idx):
        mlflow.log_metric("learning_rate", self.lr_scheduler.get_lr()[0])
        input = batch["input"]  # B x L x D
        event = batch["event"]  # B x 3
        x = self(input)  # B x 3
        loss = binary_cross_entropy_with_logits(x.view(-1), event, reduction="mean")
        mlflow.log_metric("train_loss", loss.item())
        return loss #np.hstack((x.sigmoid().cpu().detach().numpy(),event.detach().cpu().numpy().reshape(-1,1)))

    def validation_step(self, batch, batch_idx):
        input = batch["input"]  # B x L x D
        event = batch["event"]  # B x 3
        x = self(input)  # B x 3
        loss = binary_cross_entropy_with_logits(x.view(-1), event, reduction="mean")
        self.log("val_loss", loss.item())
        mlflow.log_metric("val_loss", loss.item())
        return loss

    def set_optimizer(self, optimizer, lr_scheduler):
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def configure_optimizers(self):
        assert self.optimizer is not None and self.lr_scheduler is not None
        return [self.optimizer], [self.lr_scheduler]
