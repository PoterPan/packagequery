import requests
from bs4 import BeautifulSoup
import re
import pymysql

db_settings = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "",
            "db": "package",
            "charset": "utf8"
        }

class Package:
    def __init__(self, *package_nums):
        self.package_nums = package_nums

    def capture(self):

        result = list()

        for package_num in self.package_nums:

            # 取得網站資料
            payload = {'billcode': package_num}
            # 將查詢參數加入 GET 請求中
            org_web = requests.get("https://member.songshuguoji.com/track.php", params=payload)
            org_web.encoding = 'utf-8'
            soup = BeautifulSoup(org_web.text, 'html.parser')
            time = soup.select(".left")
            info = soup.select(".right")
            result.append((package_num,)+(time[0].text.strip(),) + (info[0].text.strip(),) + (time[1].text.strip(),) + (info[1].text.strip(),))
        return result

    def readlocal(self):

        loacldata = list()

        try:
            conn = pymysql.connect(**db_settings)
            with conn.cursor() as cursor:
                cursor.execute("SELECT time_last FROM status")
                localdata = cursor.fetchall()
            return localdata

        except Exception as ex:
            print("Exception:", ex)


    def save(self, packages):

        try:
            conn = pymysql.connect(**db_settings)

            with conn.cursor() as cursor:
                sql = """
                        INSERT INTO status(
                                number,
                                time_last,
                                info_last,
                                time_seclast,
                                info_seclast)
                        VALUES(%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        time_last = VALUES(time_last),
                        info_last = VALUES(info_last),
                        time_seclast = VALUES(time_seclast),
                        info_seclast = VALUES(info_seclast)
                        """

                for package in packages:
                    cursor.execute(sql, package)
                conn.commit()
        except Exception as ex:
            print("Exception:", ex)

    def pushnofify(self, packages):
        headers = {
            "Authorization": "Bearer " + "fCmE4weuuF4dUQrdOz7Dr9MDHtRR6XujdAIT65BfpUz",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        for package in packages:
            params = {"message": "物流狀態推播 \n最新時間:" + package[1] + "\n目前狀態:" + package[2]}

            r = requests.post("https://notify-api.line.me/api/notify",
                          headers=headers, params=params)
            print(r.status_code)  # 200


''' 印出所有歷程
            for status in range(len(time)):
                print(time[status].text.strip())
                print(info[status].text.strip())
                print("\n")
'''


package = Package("01705500075")  #建立package物件並導入package_num
print(package.capture())  #印出爬取結果

lastdata = package.readlocal()

package.save(package.capture())  #將爬取的結果存入MySQL資料庫中

nowdata = package.readlocal()

if nowdata != lastdata:
    package.pushnofify(package.capture())



'''
rec = open('rec.txt', 'r+')
last = rec.read()
now = len(time)


if int(now) > int(last):
    headers = {
        "Authorization": "Bearer " + "fCmE4weuuF4dUQrdOz7Dr9MDHtRR6XujdAIT65BfpUz",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": "物流狀態推播 \n最新時間:"+ time[0].text.strip() + "\n目前狀態:"+ info[0].text.strip() }

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  # 200
    rec = open('rec.txt', 'w+')
    rec.write(str(now))
'''