# coding=utf-8
# filename: CheckXLOBOExpressStatus.py
from __future__ import unicode_literals
from BeautifulSoup import BeautifulSoup
import urllib2
import re

url = r'http://www.xlobo.com/Public/PubB.aspx?code=DB111111111US'  # DBxxxUS is the express number to be queried
req = urllib2.Request(url)
resp = urllib2.urlopen(req)
page = resp.read()
from os import linesep

page = page.strip(linesep)
soup = BeautifulSoup(page)
result = []
temp = []
# using two 'for' block to make all info in the same line in one list
for block in soup.findAll('div', {'class': 'ff_row'}):
    for tag in block.findAll('span', {'class': re.compile(r'ff_\d{3} in_bk')}):
        temp.append(tag.text)
    result.append(temp)
    temp = []

from sys import getfilesystemencoding

for i, v in enumerate(result):
    if i == 0:
        print
        '{0[0]:<s}\t\t\t{0[1]:<s}\t\t\t\t{0[2]:<s}'.format(v).encode(getfilesystemencoding())
    else:
        print
        '{0[0]:<s}\t{0[1]:<s}\t{0[2]:<s}\t{0[3]:s}'.format(v).encode(getfilesystemencoding())




if int(price) < 500:  # 將爬取的價格字串轉型為整數
    headers = {
        "Authorization": "Bearer " + "你的權杖(token)",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": "Python基礎課程和網路爬蟲入門實戰 已降價至" + price + "元"}

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  # 200