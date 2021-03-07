import requests
from bs4 import BeautifulSoup
import re

#取得網站資料

payload = {'billcode': '900875026491'}
# 將查詢參數加入 GET 請求中
org_web = requests.get("https://member.songshuguoji.com/track.php", params=payload)
org_web.encoding = 'utf-8'
# For test
# print(org_web.url) # https://member.songshuguoji.com/track.php?billcode=value1

soup = BeautifulSoup(org_web.text, 'html.parser')
# print(soup.prettify())
# status = soup.find("span", {"class": "price-text__current"}).getText()[7:]  #取得文字中的價格部分

# sel = soup.select(".bottom-tr")    #取得主要文字
# print(sel)

time = soup.select(".left")
data = soup.select(".right")

for status in range(len(time)):
        print(time[status].text.strip())
        print(data[status].text.strip())
        print("\n")

rec = open('rec.txt', 'r+')
last = rec.read()
now = len(time)


if int(now) > int(last):
    headers = {
        "Authorization": "Bearer " + "fCmE4weuuF4dUQrdOz7Dr9MDHtRR6XujdAIT65BfpUz",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": "物流狀態推播 \n最新時間:"+ time[0].text.strip() + "\n目前狀態:"+ data[0].text.strip() }

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  # 200
    rec = open('rec.txt', 'w+')
    rec.write(str(now))
