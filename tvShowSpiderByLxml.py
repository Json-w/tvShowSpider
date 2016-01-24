import requests
import os
from mysql import connector
from lxml import etree


class DBManager:
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = ''
    db = 'tvShows'

    def get_connector(self):
        return connector.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                 database=self.db)


response = requests.get('http://cn163.net/cwmeiju/')
selector = etree.HTML(response.text)


class TvShow:
    def __init__(self):
        pass


def download(url, tvShow):
    picName = url.split('/')[len(url.split('/')) - 1]
    picFilePath = './pics/{0}'.format(picName)
    if not os.path.exists(os.path.dirname(picFilePath)):
        os.mkdir(os.path.dirname(picFilePath))
    tvShow.picture = picFilePath
    with open(picFilePath, 'wb') as picFile:
        picFile.write(requests.get(url).content)


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
            "insert into `tvShows` (name,showTime,showPlatform,type,originName,picture,introduction) values(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\")".format(
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
                print(td.getchildren()[0].get('href'))
                res = requests.get(td.getchildren()[0].get('href'))
                sel = etree.HTML(res.text)
                con = sel.xpath('//div[@id="entry"]/p')[0].xpath('string(.)')
                tvShow.introduction = con
                print('介绍:' + con)
                if len(sel.xpath('//div[@class="wp-caption alignnone"]/img/@src')) > 0:
                    print('图片地址:' + sel.xpath('//div[@class="wp-caption alignnone"]/img/@src')[0])
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
