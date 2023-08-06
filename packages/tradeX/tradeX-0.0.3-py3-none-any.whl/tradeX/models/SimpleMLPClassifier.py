from pytorch_lightning import LightningModule
from torch.nn import Linear, Sequential, LeakyReLU, Dropout, Tanh
from torch.nn.functional import leaky_relu, cross_entropy, binary_cross_entropy_with_logits
import mlflow


class SimpleMLPClassifier(LightningModule):
    """
    Predict at this point will coin price bump, dump or keep stable.
    """

    def __init__(self, d_in=9, d_out=3, stack=3, d_model=64, look_back=100, drop_out=0.2):
        super(SimpleMLPClassifier, self).__init__()
        self.d_model = d_model
        self.in_fc = Linear(d_in, d_model)

        self.lookback = look_back
        self.encoder = Sequential()
        for i in range(stack):
            self.encoder.append(Dropout(p=drop_out))
            self.encoder.append(Tanh())
            self.encoder.append(Linear(in_features=d_model, out_features=d_model))
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
        self.log("learning_rate", self.lr_scheduler.get_last_lr()[0])
        input = batch["input"]  # B x L x D
        event = batch["event"]  # B x 3
        x = self(input)  # B x 3loss = binary_cross_entropy_with_logits(x, event)
        # loss = binary_cross_entropy_with_logits(x, event)
        loss = binary_cross_entropy_with_logits(x.view(-1), event).sum()
        self.log("train_loss", loss.item())
        mlflow.log_metric("train_loss", loss.item())
        return loss

    def validation_step(self, batch, batch_idx):
        input = batch["input"]  # B x L x D
        event = batch["event"]  # B x 1
        x = self(input)  # B x 3

        # weight=torch.tensor([0.36615189, 2.29188975, 2.58988648], device=x.device)
        loss = binary_cross_entropy_with_logits(x.view(-1), event).sum()
        self.log("val_loss", loss.item())
        mlflow.log_metric("val_loss", loss.item())
        return loss

    def set_optimizer(self, optimizer, lr_scheduler):
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def configure_optimizers(self):
        assert self.optimizer is not None and self.lr_scheduler is not None
        return [self.optimizer], [self.lr_scheduler]
