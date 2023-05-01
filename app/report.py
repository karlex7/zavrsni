
class report:
    def __init__(self, buy_times=0, avg_btc_buy=0, sell_times=0, avg_btc_sell=0, stop_loss_times=0, btc_bag=0, btc_price=0, money=-1, starting_money=0, avg_buy=0):
        self.buy_times = buy_times
        self.avg_btc_buy = round(avg_btc_buy,2)
        self.sell_times = sell_times
        self.avg_btc_sell = round(avg_btc_sell,2)
        self.stop_loss_times = stop_loss_times
        self.btc_bag = round(btc_bag,5)
        self.btc_price = btc_price
        self.money = round(money,2)
        self.starting_money = starting_money
        self.avg_buy = avg_buy
        
