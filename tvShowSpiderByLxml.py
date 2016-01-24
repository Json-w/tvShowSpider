import requests
from mysql import connector
from lxml import etree


class DBManager:
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = 'password'
    db = 'tvShows'

    def get_connector(self):
        return connector.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                 database=self.db)


response = requests.get('http://cn163.net/cwmeiju/')

selector = etree.HTML(response.text)

for e in selector.xpath('//div[@id="post-3807"]/table/tbody/tr'):
    content = e.xpath('string(.)')
    str(content).replace('\n', '')
    print(content)
