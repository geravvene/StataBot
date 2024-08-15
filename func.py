def count(collection, date1, date2):
    pnl = 0
    pnl_symbol = {}
    orders = collection.find({"DATE": {"$gte": date1, "$lte": date2}})if date1 and date2 else collection.find(
        {"DATE": {"$gte": date1}}) if date1 and not date2 else collection.find(
            {"DATE": {"$lte": date2}}) if not date1 and date2 else collection.find()
    for row in orders:
        pnl += float(row['PROFIT']) + float(row['COMMISSION'])
        pnl_symbol[row['SYMBOL']] = pnl_symbol[row['SYMBOL']] + \
            float(row['PROFIT']) + float(row['COMMISSION']) if row['SYMBOL'] in pnl_symbol else float(
                row['PROFIT']) + float(row['COMMISSION'])

    for key in pnl_symbol:
        pnl_symbol[key] = round(pnl_symbol[key], 2)

    return {'pnl': round(pnl, 2), 'pnl_symbol': pnl_symbol}


def get_count(collection, date1=False, date2=False):
    data = count(collection, date1, date2)
    str = f"<b>PNL = {data['pnl']}</b>\n\n"
    for key in data['pnl_symbol']:
        str += f"{key} = {data['pnl_symbol'][key]}\n"
    return str


def string_range_date(date1, date2):
    return f'{date1.strftime("%d.%m.%Y")} - {date2.strftime('%d.%m.%Y')}\n\n' if date1 else f"До {date2.strftime("%d.%m.%Y")}\n\n"
