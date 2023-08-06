import torch.nn
from torch.nn.functional import cross_entropy, binary_cross_entropy_with_logits, l1_loss


def log_return_loss(input, target, last, mean, std):
    """
    :param input: B x 3 Prediction of high, low, close
    :param target: B x 3 GT high, low, close
    :param last: B x 3 = last high, low, close
    :return:
    """
    input = input * std + mean
    last = last * std + mean
    target = target * std + mean
    log_return_gt = torch.log(target / last)
    log_return_pred = torch.log(input / last)
    return l1_loss(log_return_gt, log_return_pred).mean()


def bce_loss(input, target, alpha=4):
    bce = binary_cross_entropy_with_logits(input, target, reduction="none")

    positives = target != 0
    negatives = target == 0
    prob = torch.exp(-bce)

    negative_loss = bce[negatives] * (1 - prob[negatives]) ** alpha
    positive_loss = bce[positives] * (1 - prob[positives]) ** alpha
    loss = negative_loss.sum() + positive_loss.sum()
    return loss.sum()


def focal_loss(input, target, pos_neg_weight=(1, 0), alpha=4):
    """
    :param input:
    :param target:
    :param alpha:
    :return:
    """
    ce_loss = cross_entropy(input, target, reduction="none")

    prob = torch.exp(-ce_loss)

    # positives = target != 0
    # negatives = target == 0

    loss = (1 - prob) ** alpha * ce_loss
    return loss.sum()
    # negative_loss = ce_loss[negatives] * pos_neg_weight[1]
    # return positive_loss.sum() + negative_loss.sum()


def unscaled_l1_loss(input, target, *args, **kwargs):
    """
    :param input: B x 3
    :param target: B x 3
    :param args:
    :param kwargs:
    :return:
    """
    mm = None
    if len(args) > 0:
        mm = args[0]
    if "mm" in kwargs:
        mm = kwargs["mm"]
    assert mm is not None
    min = torch.concat([item["min"].view(-1, 1) for item in mm[:3]], dim=-1)  # B x 3
    max = torch.concat([item["max"].view(-1, 1) for item in mm[:3]], dim=-1)  # B x 3
    if input.shape != target.shape:
        target = target[..., :input.shape[-1]]
    target = target * (max - min) + min
    input = input * (max - min) + min

    if "reduction" in kwargs:
        reduction = kwargs["reduction"]
    else:
        reduction = "sum"
    return torch.nn.functional.l1_loss(input, target, reduction=reduction)


def l1_loss(input, target, *args, **kwargs):
    """
    :param input:  B x 8
    :param target: B x 8
    :return:
    """
    if input.shape != target.shape:
        target = target[..., :input.shape[-1]]
    if "reduction" in kwargs:
        reduction = kwargs["reduction"]
    else:
        reduction = "sum"
    return torch.nn.functional.l1_loss(input, target, reduction=reduction)


def l2_loss(input, target, *args, **kwargs):
    """
    :param input:  B x 8
    :param target: B x 8
    :return:
    """
    if input.shape != target.shape:
        target = target[..., :input.shape[-1]]
    if "reduction" in kwargs:
        reduction = kwargs["reduction"]
    else:
        reduction = "sum"
    return torch.nn.functional.mse_loss(input, target, reduction=reduction)


def orientation_loss(pred_theta, gt_theta):
    """
    pred_theta : B x 2 presenting sin and cos
    gt_theta: B x 1 # in radian
    """

    theta_diff = torch.atan2(pred_theta[:, 0], pred_theta[:, 1])  # B

    return -1 * torch.cos(theta_diff - gt_theta).mean()
