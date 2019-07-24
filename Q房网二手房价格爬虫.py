import requests
import csv
import time
from lxml import etree


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.131 Safari/537.36',
    'Referer':'https://shenzhen.qfang.com/sale',
    'cookie':'language=SIMPLIFIED; _ga=GA1.2.1159469757.1563260151; acw_tc=3afa7f9e15632601689166541e4627da71979cc13ad8d1f85b45f564ac; sid=5801d5f2-5315-48ef-9b43-37746a59341f; qchatid=2f4ea6d9-ddab-485e-8cc7-d52b1f6ce94a; _ga=GA1.3.1159469757.1563260151; WINDOW_DEVICE_PIXEL_RATIO=1; CITY_NAME=SHENZHEN; _gid=GA1.3.1067223603.1563346952; _gid=GA1.2.563470803.1563453842; cookieId=16bc3af1-7963-4dd7-9533-b0188356d653; Hm_lvt_de678bd934b065f76f05705d4e7b662c=1563455686,1563456746,1563459380,1563502575; LXB_REFER=www.baidu.com; JSESSIONID=aaa2XK8fmawX7-sZ-aiWw; Hm_lvt_4d7fad96f5f1077431b1e8d8d8b0f1ab=1563455688,1563456746,1563459383,1563502576; SALEROOMREADRECORDCOOKIE=100651008%23100652778%23100553147%23100657467%23100419827; looks=GARDEN%2C58669%2C58669%7CSALE%2C100657467%2C56383%7CSALE%2C100419827%2C57493; acw_sc__v2=5d3142b9de1bb72cfc83f39c53e915f08bdb95b5; ROOM_SALE=%2Fsale%2Fdapengxinqu%5E%20%E5%A4%A7%E9%B9%8F%E6%96%B0%E5%8C%BA; Hm_lpvt_4d7fad96f5f1077431b1e8d8d8b0f1ab=1563509841; Hm_lpvt_de678bd934b065f76f05705d4e7b662c=1563509841'
}


def getonepage(url):

    r=requests.get(url,headers = headers).text
    html = etree.HTML(r)

    house_all = html.xpath('//*[@id="cycleListings"]/ul/li')
    for house_one in house_all:
        try:
            Region = house_one.xpath('./div[1]/p[3]/span[2]/a[1]/text()')[0]
            Layout = house_one.xpath('./div[1]/p[2]/span[2]/text()')[0]
            Size = house_one.xpath('./div[1]/p[2]/span[4]/text()')[0]
            Renovation = house_one.xpath('./div[1]/p[2]/span[6]/text()')[0]
            Floor = house_one.xpath('./div[1]/p[2]/span[8]/text()')[0].strip()
            Direction = house_one.xpath('./div[1]/p[2]/span[10]/text()')[0]
            Year = house_one.xpath('./div[1]/p[2]/span[12]/text()')[0]
            Price = house_one.xpath('./div[2]/span[1]/text()')[0]
            house_info = [Region, Layout, Size, Renovation, Floor, Direction, Year, Price]
            filesave(house_info)
        except Exception as e:
            pass
        continue


def filesave(item):
    with open(r'F:\pythoncode\Q房网二手房源价格.csv', 'a+', encoding = 'utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(item)


def main():
    house_title = ['Region','Layout','Size','Renovation','Floor','Direction','Year','Price']
    filesave(house_title)

    Destrict = ['nanshan','futian','luohu','baoan','longgang','longhuaa','guangmingqu','yantiana','pingshanab','dapengxinqu']
    for d in Destrict:
        for t in range(1,100):
            url = 'https://shenzhen.qfang.com/sale/' + d + '/f' + str(t)
            getonepage(url)
            time.sleep(2)


if __name__ == '__main__':
    main()