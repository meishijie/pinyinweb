#-*- coding:utf-8 -*-
from flask import Flask
from pypinyin import pinyin, lazy_pinyin, Style
import sqlite3

# 兼容python2.7
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#
all = []
def search(temp):
    
    search_temp = temp.decode('UTF-8')
    search_pinyin = pinyin(search_temp,style=Style.FINALS)
    # print search_pinyin
    conn = sqlite3.connect('e.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * from lyc")
    for row in cursor:
        content = row[1]
        lyc_name = row[6]
        contents = content.split('|')
        for item in contents:
            item_temp = item[-2:]
            pinyin_temp = pinyin(item,style=Style.FINALS)[-2:]
            if(search_pinyin == pinyin_temp):
                # print (u'歌曲:'+lyc_name)
                print (item)
                # print ('-----')
                all.append(item)
    conn.close()

# @app.route('/')
def index():
    st = '意义'
    search(st);
    # return "搜索 %s <br /> %s " % (st,'<br/>'.join(all))
    print "搜索 %s <br /> %s " % (st,'<br/>'.join(all))
    
index()
# if __name__ == '__main__':
    # app.run()
