import requests
from bs4 import BeautifulSoup
import time
import re
import threading
import MySqlCtrl
#import HiveCtrl
class spider:
    def __init__(self,cookie,sql) -> None:
        '''
        爬虫初始化,提供cookie参数和mysql数据库操作类
        '''
        self.sql=sql
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        "Cookie":cookie
        }
    def get_hot(self):
        '''
        获取榜单和热度,提供榜单参数
        realtimehot:热搜总榜
        entrank:文娱榜
        sport:体育榜
        game:游戏榜
        '''
        postDict={}
        historyValue={
            "realtimehot":0,
            "sport":0,
            "game":0,
            "entrank":0,
        }
        for hotType in ["realtimehot","sport","game","entrank"]:
            url = 'https://s.weibo.com/top/summary?cate='+hotType
            response = requests.get(url, headers=self.headers)#get方法发送请求
            try:response.raise_for_status()  # 检查请求是否成功
            except Exception as e:print(e)
            soup = BeautifulSoup(response.content, 'html.parser')#BS筛选
            self.sql.delete("weibo_"+hotType,"all")#清空原表
            table=self.sql.getTable()
            table=set(map(lambda x:x[0],table))
            try:#因为可能存在广告和一些无热度值的项,为保证程序鲁棒性添加异常处理
                items=0
                for i in soup.select("tbody tr"):#找到每个热搜项
                    if(items==10):
                         break
                    if hotType=="entrank" :items+=1
                    if  not i.select(".td-01")[0].get_text().isdigit():#检查项前标志是否为数字以过滤非热搜项
                            continue
                    hotName=i.select("a")[0].get_text().replace(" ","_").replace("@","at").replace("%","百分比").replace(".","点")#获取热搜词条
                    hotValue=eval(re.compile("(\d+)").findall(i.select("span")[0].get_text())[0])
                    hotUrl="https://s.weibo.com"+i.select("a")[0]["href"]
                    if hotName not in table:
                        postDict[hotName]=hotUrl

                    historyValue[hotType]+=hotValue
                    #获取热度，热度字段可能包含其他字符，使用正则表达式清洗
                    self.sql.insert("weibo_"+hotType,(hotName,hotValue))#向mysql写入热度
                    
            except Exception as e:
                print(e)
        print(historyValue)
        return {"post":postDict,"totalValue":historyValue}

    def get_post(self,postDict):
        '''
        获取帖子
        '''
        for hotName in postDict:
            url=postDict[hotName]
            self.sql.create(hotName,{"post":"varchar(5000)"})
            for j in range(10):#每个热搜爬10页帖子
                    try:#异常处理
                        postUrl=url+"&nodup=1&page=%d"%j #构造爬取帖子的url
                        print(postUrl+"--------------")
                        response = requests.get(postUrl, headers=self.headers)
                        try:response.raise_for_status()  # 检查请求是否成功
                        except Exception as e:print(e)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        for p in soup.select(".txt"):#获取帖子
                            for t in re.compile("(#.*#)").findall(p.get_text()):#去tag
                                post=p.get_text().replace(t,"")
                            self.sql.insert(hotName,(post,))
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(e)

    def hotAndWordThread(self):
        while(True):   
            post=self.get_hot()["post"]
            self.get_post(post)
            time.sleep(120)#2分钟一更新
    def hitstoryThread(self):
        while(True):
            totalValue=self.get_hot()["totalValue"]
            t=time.gmtime()
            h=t.tm_hour+8 if t.tm_hour+8<24 else t.tm_hour+8-24
            d=t.tm_mday if t.tm_hour+8<24 else t.tm_mday+1
            Time="%d-%d-%d %d:%d"%(t.tm_year,t.tm_mon,t.tm_mday,h,t.tm_min)
            for Type in ["realtimehot","sport","game","entrank"]:
                self.sql.insert("weibo_%s_history"%Type,(Time,totalValue[Type]))
            time.sleep(360)#六分钟一记录
    def start_spider(self):
        spider1=threading.Thread(target=self.hitstoryThread)
        spider2=threading.Thread(target=self.hotAndWordThread)
        spider2.start()
        time.sleep(2)
        spider1.start()



              
         
