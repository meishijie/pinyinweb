#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask
from pypinyin import pinyin, lazy_pinyin, Style
# print (pinyin(u'蹒跚',style=Style.FINALS))
import sqlite3

app = Flask(__name__)

# 兼容python2.7
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
all = []


def search(temp):
    chr_len = len(temp)
    # search_temp = temp.decode('UTF-8')
    search_pinyin = pinyin(temp, style=Style.FINALS)
    # print search_pinyin
    conn = sqlite3.connect('allclean.db')
    c = conn.cursor()

    i = 0
    x = 0
    want = 10
    allcount = c.execute("SELECT COUNT(*) FROM lyc")

    print(len(allcount.fetchall()))
    can = True
    while can:
        print(x)
        if i > len(allcount.fetchall()) or x >= want:
            return
        # num = i * 20
        offset = 1000
        cursor = c.execute("SELECT * from lyc limit " + str(i) + "," + str(i + offset))
        # LIMIT 5 OFFSET 10
        # cursor = c.execute("SELECT * from lyc ")
        for row in cursor:
            if x >= want:
                return
            i += 1
            content = row[1]
            # print (content)
            # item 一句歌词
            item_temp = content[-1 * chr_len:]
            # print ("item_temp = ",item_temp)
            pinyin_temp = pinyin(item_temp, style=Style.FINALS)[-1 * chr_len:]
            # print ("pinyin_temp",pinyin_temp)
            if (search_pinyin == pinyin_temp):
                x += 1
                all.append(content)
                # print ("all = ",all)
    conn.close()


@app.route('/s/<username>')
def show_yunmu(username):
    # show the user profile for that user
    # return '搜索文字是 %s' % username
    global all
    all = []
    search(username)
    print (type(username))
    return "搜索 %s <br /> %s " % (username, '<br/>'.join(all))


@app.route('/')
def index():
    all = []
    st = '意义'
    search(st)
    return "搜索 %s <br /> %s " % (st, '<br/>'.join(all))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
