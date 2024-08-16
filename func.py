def count(collection, date1, date2):
    pnl = 0
    symbol = {}
    length = 0
    orders = collection.find({"DATE": {"$gte": date1, "$lte": date2}})if date1 and date2 else collection.find(
        {"DATE": {"$gte": date1}}) if date1 and not date2 else collection.find(
            {"DATE": {"$lte": date2}}) if not date1 and date2 else collection.find()
    for row in orders:
        pnl += float(row['PROFIT']) + float(row['COMMISSION'])
        symbol[row['SYMBOL']] = symbol[row['SYMBOL']
                                       ] if row['SYMBOL'] in symbol else {'PNL': 0, 'Кол-во': 0}
        symbol[row['SYMBOL']]['PNL'] = symbol[row['SYMBOL']]['PNL'] + \
            float(row['PROFIT']) + float(row['COMMISSION'])
        symbol[row['SYMBOL']]['Кол-во'] = symbol[row['SYMBOL']]['Кол-во'] + 1
        length += 1

    for key in symbol:
        piece = symbol[key]['Кол-во']/length
        symbol[key]['Кол-во'] = f"{symbol[key]
                                   ['Кол-во']} | {round(piece*100, 2)} %"
        symbol[key]['KPD'] = symbol[key]['PNL']/piece
        symbol[key]['PNL'] = round(symbol[key]['PNL'], 2)
        symbol[key]['KPD'] = round(symbol[key]['KPD'], 2)

    return {'pnl': round(pnl, 2), 'symbol': dict(
        sorted(symbol.items(), key=lambda item: item[1]['KPD'], reverse=True)), 'length': length}


def get_count(collection, date1=False, date2=False):
    data = count(collection, date1, date2)
    currencies = data['symbol']
    str = f"<b>PNL = {data['pnl']}</b>\nВсего сделок: {data['length']}\n\n"
    for currency in currencies:
        str += f"<b>{currency}:</b>\n"
        for key in currencies[currency]:
            str += f"{key} = {currencies[currency][key]}\n"
        str += "\n"
    return str


def string_range_date(date1, date2):
    return f"{date1.strftime('%d.%m.%Y')} – {date2.strftime('%d.%m.%Y')}\n\n" if date1 else f"До {date2.strftime('%d.%m.%Y')}\n\n"
