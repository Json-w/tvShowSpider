import DBUtil
from mysql import connector

class TvShow(object):
    def __init__(self, name, showTime, showPlatform, type, originName, picture, introduction, comments):
        self.name = name
        self.showTime = showTime
        self.showPlatform = showPlatform
        self.type = type
        self.originName = originName
        self.picture = picture
        self.introduction = introduction
        self.comments = comments
    def __init__(self):
        self.name = ''
        self.showTime = ''
        self.showPlatform = ''
        self.type = ''
        self.originName = ''
        self.picture = ''
        self.introduction = ''
        self.comments = ''

    def set_name(self, name):
        self.name = name

    def set_showTime(self, showTime):
        self.showTime = showTime

    def set_showPlatform(self, showPlatform):
        self.showPlatform = showPlatform

    def set_type(self,type):
        self.type = type

    def set_originName(self, originName):
        self.originName = originName

    def set_picture(self, picture):
        self.picture = picture

    def set_introduction(self, introduction):
        self.introduction = introduction

    def set_comments(self, comments):
        self.comments = comments

    def get_name(self):
        return self.name

    def get_showTime(self):
        return self.showTime

    def get_showPlatform(self):
        return self.showPlatform

    def get_type(self):
        return self.type

    def get_originName(self):
        return self.originName

    def get_picture(self):
        return self.picture

    def get_introduction(self):
        return self.introduction

    def get_comments(self):
        return self.comments


class TvShowDao(object):
    def __init__(self):
        self.conn = connector.connect(user='root', password='', database='tvShows')

    def save_TvShow(self, tvshow):
        cursor = self.conn.cursor()
        cursor.execute('insert into tvShows (name,showTime,showPlatform,type,originName,picture,introduction,comments) '
                       'values (%s,%s,%s,%s,%s,%s,%s,%s)',
                       [tvshow.get_name(), tvshow.get_showTime(), tvshow.get_showPlatform(), tvshow.get_type(),
                        tvshow.get_originName(), tvshow.get_picture(), tvshow.get_introduction(), tvshow.get_comments()])
        self.conn.commit()
        cursor.close()
