# region imports
from AlgorithmImports import *
from reader import IBData
from CustomFeeModel import CustomFeeModel
# endregion


class Ibloader(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)  # Set Start Date
        self.SetEndDate(2023, 11, 30)  # Set End Date
        self.SetAccountCurrency("AUD")
        self.SetCash(1000000)  # Set Strategy Cash
        customFeeModel = CustomFeeModel()
        symbol = self.AddData(IBData, "STW", Resolution.Daily).Symbol
        self.SetBenchmark(symbol)
        # this line will be modified on the frontend
        self.symbol = self.AddData(IBData, "WBCPI", Resolution.Daily).Symbol
        self.Securities[self.symbol].SetFeeModel(customFeeModel)

        # Schedule the BuyStock method to run every Monday
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Monday), self.TimeRules.At(9, 59), self.BuyStock)

        # Schedule the SellStock method to run every Friday
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Friday), self.TimeRules.At(9, 59), self.SellStock)

    def BuyStock(self):
        # Check if there's enough cash and price data before buying the stock
        if self.Portfolio.Cash > self.Securities[self.symbol].Price and self.Securities[self.symbol].Price != 0:
            self.SetHoldings(self.symbol, 1)
            # Get the number of shares bought
            shares_bought = self.Portfolio[self.symbol].Quantity
            # Get the current price
            price = self.Securities[self.symbol].Price
            # Get the current date
            date = self.Time
            self.Debug(f'Purchased {shares_bought} shares of {self.symbol.Value} on {date} at a price of {price}')

    def SellStock(self):
        # Check if the stock is in the portfolio and price data is available before selling it
        if self.Portfolio[self.symbol].Invested and self.Securities[self.symbol].Price != 0:
            # Store the number of shares sold
            shares_sold = self.Portfolio[self.symbol].Quantity
            # Get the current price
            price = self.Securities[self.symbol].Price
            date = self.Time
            self.Liquidate(self.symbol)
            self.Debug(f'Sold {shares_sold} shares of {self.symbol.Value} on {date} at a price of {price}')

    def OnData(self, data: Slice):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """

        # keep track of values
        # self.Debug(f"{self.symbol.Value} - {self.Time}: Close={data[self.symbol].Close}")