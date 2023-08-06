import asyncio

import plotly.graph_objects as go
import streamlit as st
import numpy as np
from tradeX.bots import BinanceDataBot


class StreamListView(BinanceDataBot):
    def __init__(self, *args, **kwargs):
        super(StreamListView, self).__init__(*args, **kwargs)

    async def render(self):
        st.title("TradeX")
        await self.loop()

    def on_new_interval(self, past_data):
        # process data
        # make prediction
        prediction = self.predict(np.array(past_data))
        # plot
        self.plot_prediction_on_chart(np.array(past_data), prediction)

    def on_start(self):
        prediction = self.predict(self.data)
        # plot
        self.plot_prediction_on_chart(np.array(self.data), prediction)

    def plot_prediction_on_chart(self, raw_data, prediction):
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=raw_data[:, 0], open=raw_data[:, 1], high=raw_data[:, 2], low=raw_data[:, 3],
                                     close=raw_data[:, 4], name="candle_stick"))
        # Set the chart layout
        fig.update_layout(title="Bitcoin Price",
                          xaxis_title="Date",
                          yaxis_title="Price",
                          hovermode="x unified")

        # Set the Plotly layout options, including scrollZoom and dragmode
        layout = go.Layout(uirevision="foo", dragmode="pan", hovermode="closest")

        # Create a FigureWidget from the chart and layout
        fig_widget = go.FigureWidget(fig, layout=layout)

        # Render the chart using Streamlit
        st.plotly_chart(fig_widget)

    def predict(self, data):
        return 1


if __name__ == '__main__':
    view = StreamListView(interval="1m", look_back=1000, symbol="btcusdt")
    asyncio.run(view.render())
