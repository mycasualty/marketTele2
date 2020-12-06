import requests, MySQLdb

url = 'https://yar.tele2.ru/api/exchange/lots'
urlParams = {'trafficType': 'data', 'volume': 1, 'cost': 15, 'offset': 0, 'limit': 1000}
urlHeaders = {
    'Tele2-User-Agent': 'web',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.106 Safari/537.36',
    'Referer': 'https://yar.tele2.ru/stock-exchange/internet'
}

def getLot (urlParams , urlHeaders):
    requests = requests.get(url=target_url, headers=urlHeaders, params=urlParams)
    return requests.json()
    
def saveDB (data, dbParam):
         con = MySQLdb.connect(host=sqlurl, user=user, passwd=pw, db=mydb)
         cur = con.cursor()
         dataPrepared = map(
             lambda x: {**x, 'commission': str(x['commission']), 'cost': x['cost']['amount'], 'my': str(x['my']),
                        'seller': str(x['seller']), 'volume': str(x['volume']), 'timein': timeRequest}, data['data'])
         cur.executemany("""
         INSERT OR IGNORE INTO saler (
         commission, cost, hash, id, my, seller, status, trafficType, volume, timein
         )
         VALUES (
         :commission, :cost, :hash, :id, :my, :seller, :status, :trafficType, :volume, :timein
          )
          """, dataPrepared)
         con.commit()
         dataPrepared = map(lambda x: {'time': timeRequest, 'hash': x[1]['hash'] , 'id': x[1]['id'], 'position': x[0]}, enumerate(data['data']))
         cur.executemany("""
         INSERT  INTO  lots ( id, hash, time , position) VALUES (:id , :hash, :time , :position)
         """, dataPrepared)
         con.commit()
         con.close()
