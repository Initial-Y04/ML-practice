import requests
from lxml import etree


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Referer': 'https://shenzhen.qfang.com/sale',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'acw_tc=b7d6989915548939845948844eeffab572b5a26afc085c57b6f38e387a; sid=652965b3-8f52-40dd-b9c1-6962ea42a339; cookieId=5c38f6e1-affc-4f00-8c4c-abb3c912ca9c; qchatid=27f0e864-7c8e-45e5-a508-76a3688fd464; language=SIMPLIFIED; _ga=GA1.3.915622741.1554893919; _gid=GA1.3.339519498.1554893919; WINDOW_DEVICE_PIXEL_RATIO=1; _jzqy=1.1554959610.1554959610.1.jzqsr=baidu|jzqct=%E4%BA%8C%E6%89%8B%E6%88%BF.-; _ga=GA1.2.423311346.1554972187; _gid=GA1.2.1781558179.1554972187; CITY_NAME=SHENZHEN; Hm_lvt_de678bd934b065f76f05705d4e7b662c=1554954249,1554959610,1554972187,1555030164; LXB_REFER=sp0.baidu.com; JSESSIONID=aaaMyFRpP9VNkhshMbpOw; _jzqc=1; sec_tc=AQAAAIPTbS2VFwAAeOozJhHzN3Ji1nQ3; acw_sc__v2=5cb03c43d56f9eb09c2ee1c5bf52fd971d0702a3; _jzqa=1.1902658096639036700.1554954249.1555033262.1555053569.7; _jzqx=1.1554954249.1555053569.1.jzqsr=shenzhen%2Eqfang%2Ecom|jzqct=/sale.-; _jzqckmp=1; _qzja=1.1489688666.1554954248971.1555033262484.1555053568980.1555053568980.1555053577870.0.0.0.17.7; _qzjb=1.1555053568980.2.0.0.0; _qzjc=1; _qzjto=5.3.0; _jzqb=1.2.10.1555053569.1; Hm_lpvt_de678bd934b065f76f05705d4e7b662c=1555053578'
    }


def getonepage(url):

    r = requests.get(url,headers = headers).text
    html = etree.HTML(r)

    sale = html.xpath('//*[@id="cycleListings"]/ul/li/div[2]/span[1]/text()')
    price = html.xpath('//*[@id="cycleListings"]/ul/li/div[2]/p/text()')
    bathroom = html.xpath('//*[@id="cycleListings"]/ul/li/div[1]/p[2]/span[2]/text()')
    sq_ft = html.xpath('//*[@id="cycleListings"]/ul/li/div[1]/p[2]/span[4]/text()')
    decoration = html.xpath('//*[@id="cycleListings"]/ul/li/div/p[2]/span[6]/text()')
    floor = html.xpath('//*[@id="cycleListings"]/ul/li/div[1]/p[2]/span[8]/text()')
    direction = html.xpath('//*[@id="cycleListings"]/ul/li/div[1]/p[2]/span[10]/text()')
    year = html.xpath('//*[@id="cycleListings"]/ul/li/div[1]/p[2]/span[12]/text()')

    return sale,price,bathroom,sq_ft,decoration,floor,direction,year


def filesave(sale,price,bathroom,sq_ft,decoration,floor,direction,year):
    for i in range(len(sale)):
        with open(r'D:\Scraping practice\二手房.csv','a',encoding = 'utf-8-sig') as f:
            f.write('%s,%s,%s,%s,%s,%s,%s,%s' % (sale[i],price[i],bathroom[i],sq_ft[i],decoration[i],floor[i].strip(),direction[i],year[i])+'\n')
            f.flush()

if __name__  == '__main__':

    for t in range(1,100):

        url = 'https://shenzhen.qfang.com/sale/f'+str(t)
        sale,price,bathroom,sq_ft,decoration,floor,direction,year = getonepage(url)
        filesave(sale,price,bathroom,sq_ft,decoration,floor,direction,year)


