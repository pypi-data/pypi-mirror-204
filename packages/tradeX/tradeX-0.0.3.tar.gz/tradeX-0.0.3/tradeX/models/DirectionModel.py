import mlflow
import torch
from pytorch_lightning import LightningModule
from torch.nn import TransformerEncoder, TransformerEncoderLayer, LayerNorm, Linear
from torch.nn.functional import leaky_relu

from tradeX.utils.losses import orientation_loss


class DirectionModel(LightningModule):
    """
    Predict at this point will coin price bump, dump or keep stable.
    """

    def __init__(self, sequence_length, d_in=9, d_model=64, nhead=8, dim_ff=64):
        super(DirectionModel, self).__init__()
        self.d_model = d_model
        self.in_fc = Linear(d_in, d_model)
        encoder_layer = TransformerEncoderLayer(d_model, nhead, dim_ff, batch_first=True)
        encoder_norm = LayerNorm(d_model)

        self.encoder = TransformerEncoder(encoder_layer, 6, encoder_norm)
        self.fc_theta = Linear(d_model * sequence_length, 2)

    def forward(self, x):
        """
        :param x: B x L x  d_in
        :return:
        """
        x = self.in_fc(x)  # B x L x d_model
        x = self.encoder(x)  # B x L x d_model
        x = x.view(x.shape[0], -1)  # B x E where E = d_model x L
        x = leaky_relu(x)
        sin_cos = self.fc_theta(x)  # B x 2
        sin_cos = torch.nn.functional.normalize(sin_cos, p=2, dim=-1)  # B x 2

        return sin_cos

    def training_step(self, batch, batch_idx):
        mlflow.log_metric("learning_rate", self.lr_scheduler.get_lr()[0])
        inp = batch["input"]  # B x L x D

        gt_theta = batch["theta"]  # B x 1 in radian
        sin_cos = self(inp)

        coss_loss = orientation_loss(sin_cos, gt_theta).mean()
        sin_loss = torch.zeros(1).item()
        gt_sin = torch.sin(gt_theta)
        pred_sin = sin_cos[:, 0]
        pos_sin_loss_idx = torch.logical_and(gt_sin > 0, pred_sin < gt_sin)
        neg_sin_loss_idx = torch.logical_and(gt_sin < 0, pred_sin > gt_sin)
        if torch.count_nonzero(pos_sin_loss_idx) > 0:
            sin_loss += (gt_sin - pred_sin)[pos_sin_loss_idx].mean()
        if torch.count_nonzero(neg_sin_loss_idx) > 0:
            sin_loss += (pred_sin - gt_sin)[neg_sin_loss_idx].mean()

        mlflow.log_metric("train_loss", coss_loss.item())
        mlflow.log_metric("sin_loss", sin_loss.item())
        self.log("train_loss", coss_loss.item())
        return coss_loss + sin_loss

    def validation_step(self, batch, batch_idx):
        inp = batch["input"]  # B x L x D
        gt_theta = batch["theta"]  # B x 1 in radian
        sin_cos = self(inp)

        loss = orientation_loss(sin_cos, gt_theta).mean()
        mlflow.log_metric("val_loss", loss.item())
        self.log("val_loss", loss.item())
        return loss

    def set_optimizer(self, optimizer, lr_scheduler):
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def configure_optimizers(self):
        assert self.optimizer is not None and self.lr_scheduler is not None
        return [self.optimizer], [self.lr_scheduler]
