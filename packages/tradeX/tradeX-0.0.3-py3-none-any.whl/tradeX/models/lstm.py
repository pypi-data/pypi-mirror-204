import torch
from pytorch_lightning import LightningModule
from torch.nn import Module, LSTM, Linear, ReLU


class IT_LSTM(LightningModule):
    def __init__(self, input_size, hidden_size, output_size, drop_out=0):
        super(IT_LSTM, self).__init__()
        self.lstm = LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True, dropout=drop_out)
        self.output_size = output_size
        self.fc = Linear(hidden_size, output_size)

    def set_loss(self, loss_func):
        self.loss_func = loss_func

    def forward(self, input):
        output, (hn, cn) = self.lstm(input)
        hn = torch.squeeze(hn, 0)  # BS,hidden
        out = self.fc(hn)  # BSxout
        return out

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.0001)
        return optimizer

    def training_step(self, batch, batch_id):
        input = batch["input"].float()  # B x L x input_size
        gt = batch["gt"].float()  # B x output_size
        output = self(input)  # B x output_size
        loss = self.loss_func(output, gt)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_id):
        input = batch["input"].float()  # B x L x input_size
        gt = batch["gt"].float()  # B x output_size
        output = self(input)  # B x output_size
        loss = self.loss_func(output, gt)
        self.log("val_loss", loss)
        return loss
