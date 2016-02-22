import requests
import logging
import os
from mysql import connector
from lxml import etree

log_filename = 'tvShowSpider.log'
log_format = '%(filename)s [%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format,datefmt='%Y-%m-%d %H:%M:%S %p',level=logging.INFO,filename=log_filename)

class DBManager:
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = '123456'
    db = 'tvShows'

    def get_connector(self):
        return connector.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                 database=self.db)

#s = requests.session()
#s.keep_alive = False
response = requests.get('http://cn163.net/cwmeiju/')
selector = etree.HTML(response.text)


class TvShow:
    def __init__(self):
        pass


def download(url, tvShow):
    picName = url.split('/')[len(url.split('/')) - 1]
    picFilePath = './pics/{0}'.format(picName)
    modifyUrl = url.split('//')[0]+'//o'+url.split('//')[1]
    if not os.path.exists(os.path.dirname(picFilePath)):
        os.mkdir(os.path.dirname(picFilePath))
    tvShow.picture = picFilePath
    with open(picFilePath, 'wb') as picFile:
        while(True):
            try:
                print('原始图片url:'+url)
                picFile.write(requests.get(url,timeout=10).content)
                break
            except requests.exceptions.ConnectionError as connectError:
                print("修正后的图片url:"+modifyUrl)
                try:
                    picFile.write(requests.get(modifyUrl,timeout=10).content)
                    break
                except requests.exceptions.ConnectionError as connectError:
                    continue

def saveTvShow(tvShow):
    db_manager = DBManager()
    connec = db_manager.get_connector()
    cursor = connec.cursor()
    picPath = ''
    introduction = ''
    if hasattr(tvShow, 'picture'):
        picPath = tvShow.picture
    if hasattr(tvShow, 'introduction'):
        introduction = tvShow.introduction.replace('\'',' ')
        introduction = introduction.replace('\"',' ')
    cursor.execute(
            "insert into `tv_shows` (name,show_time,show_platform,type,origin_name,picture,introduction) values(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\")".format(
                    tvShow.name, tvShow.showTime, tvShow.showPlatform, tvShow.type, tvShow.originName, picPath,
                    introduction))
    cursor.close()
    connec.commit()
    connec.close


flag = 0
for e in selector.xpath('//div[@id="post-3807"]/table/tbody/tr'):
    index = 0
    if flag == 0:
        flag += 1
        continue
    tvShow = TvShow()
    for td in e.getchildren():
        if len(td.getchildren()) > 0:
            if td.getchildren()[0].tag == 'a':
                logging.info(td.getchildren()[0].get('href'))
                res = requests.get(td.getchildren()[0].get('href'))
                sel = etree.HTML(res.text)
                con = sel.xpath('//div[@id="entry"]/p')[0].xpath('string(.)')
                tvShow.introduction = con
                logging.info('介绍:' + con)
                if len(sel.xpath('//div[@class="wp-caption alignnone"]/img/@src')) > 0:
                    logging.info('图片地址:' + sel.xpath('//div[@class="wp-caption alignnone"]/img/@src')[0])
                    download(sel.xpath('//div[@class="wp-caption alignnone"]/img/@src')[0], tvShow)
        content = td.xpath('string(.)')
        print(content)
        if index == 0:
            tvShow.showTime = content
        elif index == 1:
            tvShow.showPlatform = content
        elif index == 2:
            tvShow.type = content
        elif index == 3:
            tvShow.originName = content
        elif index == 4:
            tvShow.name = content
        index += 1
    saveTvShow(tvShow)
# content = e.xpath('string(.)')
# str(content).replace('\n', '')
# print(content)



# download('http://i66.tinypic.com/f524d2.jpg')
