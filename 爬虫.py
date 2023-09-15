import time
import bs4
import re
import os
import random
import urllib.request
import urllib.error
import jsonpath
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup
savePath = "D:\luogu"
start = 1000
end = 1049
difficulty=[]
def main():
    p_baseurl = "https://www.luogu.com.cn/problem/P"
    s_baseurl = "https://www.luogu.com.cn/problem/solution/P"
    get_diff()
    print("计划爬取到P{}".format(end))
    for i in range(start, end):
        print("正在爬取P{}...".format(i), end="")
        html = getHTML(p_baseurl + str(i))
        if html == "error":
            print("爬取失败，可能是不存在该题或无权查看")
            time.sleep(random.randint(0, 5))#访问不能太频繁
        else:
            problemMD = getMD(html)
            solutionMD =getData(s_baseurl+str(i))
            print("爬取成功！正在保存...", end="")
            saveData(problemMD, r"P" + str(i) + str(difficulty[i - start]) + ".md")
            saveData(solutionMD, r"P" + str(i) + "题解" + ".md")
            print("保存成功!")
            time.sleep(random.randint(0, 5))
    print("爬取完毕")

def get_diff():

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Cookie": "__client_id=3a13b6f10a22489fb0432f44a60b2fff58cdd681; _uid=570994"
  }
  tag_url = 'https://www.luogu.com.cn/_lfe/tags'
  tag_html = requests.get(url=tag_url, headers=headers).json()
  tags_dicts = []
  tags_tag = list(jsonpath.jsonpath(tag_html, '$.tags')[0])
  for tag in tags_tag:
    if jsonpath.jsonpath(tag, '$.type')[0] != 1 or jsonpath.jsonpath(tag, '$.type')[0] != 4 or \
            jsonpath.jsonpath(tag, '$.type')[0] != 3:
      tags_dicts.append({'id': jsonpath.jsonpath(tag, '$.id')[0], 'name': jsonpath.jsonpath(tag, '$.name')[0]})

  a = ["入门","普及-","普及","普及+","提高+","省选","NOI","题解"]
  url = 'https://www.luogu.com.cn/problem/list?page={1}'
  html = requests.get(url=url, headers=headers).text
  urlParse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
  htmlParse = json.loads(urllib.parse.unquote(urlParse)[1:-1])
  result = list(jsonpath.jsonpath(htmlParse, '$.currentData.problems.result')[0])
  for res in result:
    difficulty.append(a[int(jsonpath.jsonpath(res, '$.difficulty')[0])])
def getData(baseurl):
        html= getsolution(baseurl)
        text=str(urllib.parse.unquote(html,encoding='unicode_escape'))
        bs=bs4.BeautifulSoup(text,"html.parser")
        core=bs.find("script")
        md=str(core)
        # 查找"type"之前的内容的索引位置
        type_index = md.find("type")

        # 截取"type"之前的内容
        if type_index != -1:
            content_before_type = md[:type_index]
        else:
            content_before_type = md
        content_before_type = content_before_type[:-3]
        content_before_type = re.sub("<h1>", "# ", md)
        content_before_type = re.sub("<h2>", "## ", md)
        content_before_type = re.sub("<h3>", "#### ", md)
        content_before_type = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
        #print(content_before_type)
        return content_before_type
def getsolution(url):
    header = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 116.0.0.0Safari / 537.36Edg / 116.0.1938.76",
        "Cookie": "__client_id=233f84c5348a8a4ab8a8bc2c8f05a851e4339afc; _uid=1090613"
    }
    request = requests.get(url=url,headers=header)
    reseponse=request.text
    return reseponse

def getHTML(url):
    header = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 116.0.0.0Safari / 537.36Edg / 116.0.1938.76",
        "Cookie": "__client_id=233f84c5348a8a4ab8a8bc2c8f05a851e4339afc; _uid=1090613"
    }
    request = urllib.request.Request(url = url , headers = header)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if str(html).find("Exception") == -1:
        return html
    else:
        return "error"

def getMD(html):
    bs = bs4.BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    return md

def saveData(data,filename):
    file_name = os.path.join(savePath, filename)  #  最开始直接file_name = savePath + filename，结果文件保存位置不对
    with open(file_name, "w", encoding="utf-8") as file:
        for d in data:
            file.write(d)

if __name__ == '__main__':
    main()