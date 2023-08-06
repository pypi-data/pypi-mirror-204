


class EModel:
    def __init__(self, model):
        self.model = model

    def load_model(self, ckpt_path):
        raise "Not implement yet"

    def predict(self, input, *args, **kargs):
        """
        :param input: The last 100-interval raw trading data
        :return: predictions for High price, Low price, Close price for next interval based on history data
        """
        data, mms = process_input(input, len(input))

        if "ahead" in kargs:
            ahead = kargs["ahead"]
        else:
            ahead = 1

        # predict and unnorm predictions
        predict = self.model(data, ahead=ahead).view(3)

        predict = un_norm_output(predict, mms[1:]).tolist()

        # pred high, low, close price
        php, plp, pcp = predict[:3]
        return php, plp, pcp
