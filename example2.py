import requests
import bs4
import re
kuaidi = []
url='http://m.46644.com/express/result.php?typetxt=%D6%D0%CD%A8&type=zto&number=你的单号'
response = requests.get(url)
response.encoding = 'gb18030'
response = response.text
soup = bs4.BeautifulSoup(response,'html.parser',from_encoding="utf8")
for i in soup.findAll(name='div',attrs = {'class':'icontent'}):
    kuaidi.append(i.get_text())
    print(i.get_text())


def express_type_get():
    express_type = ('sfexpress', 'yunda', 'sto', 'yto', 'zto', 'ems', 'ttdex', 'htky', 'qfkd', 'chinapost')
    print(
        '////////////////快递公司////////////////\n1.顺丰 2.韵达 3.申通 4.圆通 5.中通\n6.EMS 7.天天 8.汇通 9.全峰 10.邮政\n////////////////////////////////////////')
    while True:
        express = int(input('请选择快递公司(数字):'))
        if express:
            if express <= 10 and express >= 1:
                break
            else:
                print("错误的选择!")
        else:
            print("不能为空!")
    return express_type[express - 1]


def get_url(code, id):
    url = 'http://m.46644.com/express/result.php?typetxt=%D6%D0%CD%A8&type=' + code + '&number=' + id

    return url