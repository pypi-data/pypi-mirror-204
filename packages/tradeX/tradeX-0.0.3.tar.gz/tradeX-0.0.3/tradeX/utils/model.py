import torch

from tradeX.models.RegressionModel import ITTransformer


def get_model(ckpt, dmodel=60, nhead=6, dimff=128, inputd=9, outputd=3, decoder_d=4, position_encode=False,
              device="cuda:0"):
    model = ITTransformer(d_model=dmodel, nhead=nhead, dim_feedforward=dimff, input_d=inputd, output_d=outputd,
                          d_in_decoder=decoder_d,
                          position_encode=position_encode)
    model.load_state_dict(torch.load(ckpt, map_location="cpu")['state_dict'])
    model.eval()
    model.to(device)
    return model
