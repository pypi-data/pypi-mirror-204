import mlflow
from pytorch_lightning import LightningModule
from torch.nn import LSTM, Linear
from torch.nn.functional import l1_loss
from torch import tanh


class FCLSTM_RegressionModel(LightningModule):
    def __init__(self, d_model: int = 512, output_d=3, input_d=9):
        super(FCLSTM_RegressionModel, self).__init__()

        # modules
        self.fc_in_en = Linear(input_d, d_model)
        self.lstm = LSTM(input_size=d_model, hidden_size=d_model, batch_first=True, dropout=0.1)

        self.fc_reg = Linear(d_model, output_d)
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
        x = self.fc_in_en(src)
        x = tanh(x)
        o, (h, c) = self.lstm(x)
        x = h[0]
        x = self.fc_reg(x)
        return x

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
