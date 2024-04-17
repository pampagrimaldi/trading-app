from QuantConnect.Orders.Fees import FeeModel, OrderFee
from QuantConnect.Orders import Order
from QuantConnect.Securities import CashAmount


class CustomFeeModel(FeeModel):
    def __init__(self, minimum_fee=5.0, percentage_fee=0.0008):
        '''
        Custom Fee Model
        Args:
            minimum_fee: Minimum fee in AUD
            percentage_fee: Percentage of trade value (0.08% = 0.0008)
        '''
        self.minimum_fee = minimum_fee
        self.percentage_fee = percentage_fee

    def GetOrderFee(self, parameters):
        '''
        Get the fee for an order.
        Args:
            parameters: An OrderFeeParameters object containing the order and security details.
        Returns:
            An OrderFee object representing the fee for the order in AUD.
        '''
        order_value = parameters.Security.Price * parameters.Order.AbsoluteQuantity
        fee_in_percentage = order_value * self.percentage_fee
        fee = max(self.minimum_fee, fee_in_percentage)

        # Return the fee as an OrderFee object with the currency set to AUD
        return OrderFee(CashAmount(fee, "AUD"))
