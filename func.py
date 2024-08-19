from tabulate import tabulate
from aiogram.utils.markdown import bold

def count(collection, date1, date2):
    pnl = 0
    symbol = {}
    length = 0
    winrate = 0
    orders = collection.find({"DATE": {"$gte": date1, "$lte": date2}})if date1 and date2 else collection.find(
        {"DATE": {"$gte": date1}}) if date1 and not date2 else collection.find(
            {"DATE": {"$lte": date2}}) if not date1 and date2 else collection.find()
    for row in orders:
        order_pnl = float(row['PROFIT']) + float(row['COMMISSION'])
        pnl += order_pnl
        winrate += 1 if order_pnl > 0 else 0
        symbol[row['SYMBOL']] = symbol[row['SYMBOL']
                                       ] if row['SYMBOL'] in symbol else {'all':{'PNL': 0, 'Winrate': 0, 'k/p':0}, 'Сделки': []}
        symbol[row['SYMBOL']]['all']['PNL'] += order_pnl
        symbol[row['SYMBOL']]['all']['Winrate'] += 1 if order_pnl > 0 else 0
        volume = float(row['VOLUME'])
        risk = volume*10*20
        symbol[row['SYMBOL']]['Сделки'].append(
            {'dt':row['DATE'].strftime('%d.%m'), 'vl': volume, '!': risk, '$': round(order_pnl,2), 'k/p': round(order_pnl/risk, 2)})
        length+=1

    risk = 0
    for key in symbol:
        risk_symbol = 0
        for order in symbol[key]['Сделки']:
            risk_symbol += order['!']
        risk += risk_symbol
        symbol[key]['all']['k/p'] = f"{round(symbol[key]['all']['PNL']/risk_symbol, 2)}"
        symbol[key]['all']['PNL'] = f"{round(symbol[key]['all']['PNL'], 2)} $"
        symbol[key]['all']['Winrate'] = f"{round(symbol[key]['all']['Winrate']/len(symbol[key]['Сделки'])*100, 2)} %"

    return {'all': {'PNL': f"{round(pnl, 2)} $", 'Winrate': f"{round(winrate/length*100, 2)} %", 'Всего сделок': length, 'k/p': round(pnl/risk, 2)}, 'symbol': symbol}


def get_count(collection, date1=False, date2=False):
    data = count(collection, date1, date2)
    all=data['all']
    str=f"{bold('Общее:', '') }\n"
    for key in all:
        str += f"{key} = {all[key]}\n"
    str+="\n"
    currencies = data['symbol']
    for currency in currencies:
        str += f"{bold(currency+':', '')}\n"
        for key in currencies[currency]['all']:
            str += f"{key} = {currencies[currency]['all'][key]}\n"
        str += "\n"
        orders= currencies[currency]['Сделки']
        str += f"```{tabulate(orders, headers='keys', stralign='center')}```"
        str += "\n\n"
        
    return str


def string_range_date(date1, date2):
    return f"{date1.strftime('%d.%m.%Y')} – {date2.strftime('%d.%m.%Y')}\n\n" if date1 else f"До {date2.strftime('%d.%m.%Y')}\n\n"
