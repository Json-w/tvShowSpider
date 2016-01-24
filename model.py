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


class TvShowDao(object):
    def __init__(self):
        self.conn = connector.connect(user='root', password='', database='tvShows')

    def save_TvShow(self, tvshow):
        cursor = self.conn.cursor()
        cursor.execute('insert into tvShows (name,showTime,showPlatform,type,originName,picture,introduction,comments) '
                       'values (%s,%s,%s,%s,%s,%s,%s,%s)',
                       [tvshow.get_name(), tvshow.get_showTime(), tvshow.get_showPlatform(), tvshow.get_type(),
                        tvshow.get_originName(), tvshow.get_picture(), tvshow.get_introduction(),
                        tvshow.get_comments()])
        self.conn.commit()
        cursor.close()
