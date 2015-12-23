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
        for tr in LoadCotent().get_content_from_internet(url).body.tbody.contents[1].next_siblings:
            if (type(tr) == element.Tag):
                for td in tr.contents:
                    if (type(td) == element.Tag):
                        if type(td.find('a')) == element.Tag:
                            url = td.find('a').get('href')
                            print(url)
                            self.get_tvshow_detail(url)

    def get_tvshow_detail(self, url):
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
                        print(s)


class LoadCotent:
    def get_content_from_internet(self, url):
        return BeautifulSoup(requests.get(url).text, 'html.parser')


if __name__ == '__main__':
    TVShowSpider(TvShowParser(), model.TvShow(), 'http://cn163.net/cwmeiju/').doParse()
