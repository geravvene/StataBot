def calc(collection):
    pnl = 0
    pnl_symbol = {}

    
    for row in collection.find():
        pnl += float(row['PROFIT']) + float(row['COMMISSION'])
        pnl_symbol[row['SYMBOL']] = pnl_symbol[row['SYMBOL']] + \
            float(row['PROFIT']) + float(row['COMMISSION'])  if row['SYMBOL'] in pnl_symbol else float(
                row['PROFIT']) + float(row['COMMISSION'])
            
    for key in pnl_symbol:
        pnl_symbol[key] = round(pnl_symbol[key], 2)
        
    return {'pnl': round(pnl, 2), 'pnl_symbol': pnl_symbol}
