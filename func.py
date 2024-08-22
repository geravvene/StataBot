from tabulate import tabulate
from aiogram.utils.markdown import bold

def even(num):
    if int(num*2*100)%10==0:
        return round(num*2, 2)
    else:
        return round(num*2-0.01, 2)
def rec_order(row, pnl, volume, array, col):
    if 'slices' in row:
        slice_pnl = float(row['slices']['PROFIT']) + float(row['slices']['COMMISSION'])+float(row['slices']['SWAP'])
        array.append({'.':'', 'dt':row['slices']['DATE'].strftime('%d.%m'), 'vl': row['slices']['VOLUME'], '!': '', '$': int(slice_pnl), 'k/p': ''})
        return rec_order(row['slices'], pnl+slice_pnl, volume+row['slices']['VOLUME'], array, col+1)
    else:       
        return [pnl, volume, col]
def count(collection, date1, date2):
    pnl = 0
    symbol = {}
    length = 0
    winrate = 0
    orders = collection.find({"DATE": {"$gte": date1, "$lte": date2}})if date1 and date2 else collection.find(
        {"DATE": {"$gte": date1}}) if date1 and not date2 else collection.find(
            {"DATE": {"$lte": date2}}) if not date1 and date2 else collection.find()
    for row in orders:
        length+=1
        order_pnl = float(row['PROFIT']) + float(row['COMMISSION'])+float(row['SWAP'])
        winrate += 1 if order_pnl > 0 else 0
        symbol[row['SYMBOL']] = symbol[row['SYMBOL']
                                       ] if row['SYMBOL'] in symbol else {'all':{'PNL': 0, 'Winrate': 0, 'k/p':0, 'Количество сделок':0}, 'Сделки': []}
        typ_flag=type(row['end']) is str
        typ=f"{row['TYPE']}{('/'+row['end']) if typ_flag else ''}"  
        if not 'slices' in row and typ_flag:    
            volume = float(row['VOLUME'])
            risk = volume*10*18
            symbol[row['SYMBOL']]['Сделки'].append(
            {'.':typ,'dt':row['DATE'].strftime('%d.%m'), 'vl': volume, '!': int(risk), '$': int(order_pnl), 'k/p': round(order_pnl/risk, 2) })
        else:
            
            symbol[row['SYMBOL']]['Сделки'].append(
            {'.':'','dt':row['DATE'].strftime('%d.%m'), 'vl': float(row['VOLUME']), '!': '', '$': int(order_pnl), 'k/p': '' })
            [order_pnl, volume, col]=rec_order(row, order_pnl, float(row['VOLUME']), symbol[row['SYMBOL']]['Сделки'], 1)
            volume = volume if typ_flag else '?'  
            risk = volume*10*18 if typ_flag else 0
            order_pnl=order_pnl if typ_flag else 0 
            k_p=round(order_pnl/risk, 2)if typ_flag else 0 
            symbol[row['SYMBOL']]['Сделки'].insert(0-col,
            {'.':typ,'dt':'', 'vl': volume, '!': int(risk), '$': int(order_pnl) if typ_flag else 0, 'k/p': k_p })           
        symbol[row['SYMBOL']]['all']['PNL'] += order_pnl
        symbol[row['SYMBOL']]['all']['Winrate'] += 1 if order_pnl > 0 else 0
        symbol[row['SYMBOL']]['all']['Количество сделок'] +=1
        pnl += order_pnl

    risk = 0
    for key in symbol:
        len_symbol=0
        risk_symbol = 0
        for order in symbol[key]['Сделки']:
            if order['!']:
                risk_symbol += order['!']
                len_symbol+=1
        risk += risk_symbol
        symbol[key]['all']['k/p'] = f"{round(symbol[key]['all']['PNL']/risk_symbol, 2)}"
        symbol[key]['all']['PNL'] = f"{round(symbol[key]['all']['PNL'], 2)} $"
        symbol[key]['all']['Winrate'] = f"{round(symbol[key]['all']['Winrate']/len_symbol*100, 2)} %"

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

def get_count_many(collection, date1=False, date2=False):
    data = count(collection, date1, date2)
    all=data['all']
    str_arr=[]
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
        if len(orders)<40:
            str += f"```{tabulate(orders, headers='keys', stralign='center')}```"
            str += "\n\n"
            str_arr.append(str)
        str=''
        
    return str_arr


def string_range_date(date1, date2):
    return f"{date1.strftime('%d.%m.%Y')} – {date2.strftime('%d.%m.%Y')}\n\n" if date1 else f"До {date2.strftime('%d.%m.%Y')}\n\n"
