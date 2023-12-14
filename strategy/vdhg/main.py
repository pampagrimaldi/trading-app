# region imports
from AlgorithmImports import *
from reader import IBData
# endregion


class VDHG(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)  # Set Start Date
        self.SetEndDate(2023, 11, 30)  # Set End D  ate
        self.SetAccountCurrency("AUD")
        self.SetCash(10000)  # Set Strategy Cash
        symbol = self.AddData(IBData, "STW", Resolution.Daily).Symbol
        self.SetBenchmark(symbol)
        self.symbol = self.AddData(IBData, "VDHG", Resolution.Daily).Symbol


    def OnData(self, data: Slice):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """

        if not self.Portfolio.Invested:
            self.SetHoldings(self.symbol, 1)
            self.Debug('Purchased Stock')

        # keep track of values
        self.Debug(f"{self.symbol.Value} - {self.Time}: Close={data[self.symbol].Close}")