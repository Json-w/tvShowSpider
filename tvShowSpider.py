import requests
from bs4 import BeautifulSoup
from bs4 import element
import model


class TVShowSpider:
    def __init__(self, parser, dataStruct, url):
        self.parser = parser
        self.dataStruct = dataStruct
        self.url = url

    def doParse(self):
        self.parser.parse(self.dataStruct, self.url);


class TvShowParser:
    def parse(self, tvShow, url):
        tvShowDao = model.TvShowDao()
        flag = 0
        for tr in LoadCotent().get_content_from_internet(url).body.tbody.contents[1].next_siblings:
            if (type(tr) == element.Tag):
                index = 0
                for td in tr.contents:
                    if (type(td) == element.Tag):
                        if index == 0:
                            tvShow.set_showTime(str(td.string))
                        elif index == 1:
                            tvShow.set_showPlatform(str(td.string))
                        elif index == 2:
                            tvShow.set_type(str(td.string))
                        elif index == 3:
                            tvShow.set_originName(str(td.string))
                        elif tvShow == 4:
                            tvShow.set_name(str(td.string))
                        index = index + 1
                        if type(td.find('a')) == element.Tag:
                            url = td.find('a').get('href')
                            print(url)
                            self.get_tvshow_detail(url, tvShow)
                tvShowDao.save_TvShow(tvShow)
                print("当前下载数:")
                print(flag)
                flag = flag + 1

    def get_tvshow_detail(self, url, tvShow):
        detailSoup = LoadCotent().get_content_from_internet(url)
        for entry in detailSoup.find_all(id='entry'):
            for entryChild in entry.children:
                # print(type(entryChild))
                if entryChild.name == 'p':
                    if type(entryChild) == element.Tag:
                        # print(entryChild.contents[2])
                        i = 0
                        s = ''
                        for pChild in entryChild.contents:
                            if type(pChild) == element.NavigableString:
                                s = s + pChild.string
                                i = i + 1
                                if i > 2:
                                    break
                        tvShow.set_introduction(s)


class LoadCotent:
    def get_content_from_internet(self, url):
        return BeautifulSoup(requests.get(url).text, 'html.parser')


if __name__ == '__main__':
    TVShowSpider(TvShowParser(), model.TvShow(), 'http://cn163.net/cwmeiju/').doParse()
