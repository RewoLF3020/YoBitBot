https://jsonviewer.stack.hu/

ticker: инфа по нужным парам
depth: инфа по ордерам покупка/продажа
    coin1_coin2:
        asks(продажа):
            []:
                0(price): xxxx
                1(кол-во монет на продажу)
        bids(покупка):
            []:
                0(price): xxxx
                1(кол-во монет на покупку)
trades: совершенные сделки по покупке и продаже


todo:
    send requests every {n} time, save data in database, compare amount and after big increase -> sygnal