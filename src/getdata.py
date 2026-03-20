import MySqlCtrl
import jieba.analyse
import jieba

class getdata:
    def __init__(self,sql):
      '''
      初始化数据展示:提供需要展示的榜单和词云目标
      '''
      self.ss=sql
    def getValue(self):
        num_sport=self.ss.select("weibo_sport")
        num_entrank=self.ss.select("weibo_entrank")
        num_game=self.ss.select("weibo_game")
        total=self.ss.select("weibo_realtimehot")
        hotValue={
            "sport":0,
            "game":0,
            "entrank":0
        }
        
        for i in range(10):
            hotValue["sport"]+=num_sport[i][1]
            hotValue["game"]+=num_game[i][1]
            hotValue["entrank"]+=num_entrank[i][1]
        hot={
            "sport":[(i[0],i[1]) for i in num_sport],
            "game":[(i[0],i[1]) for i in num_game],
            "entrank":[(i[0],i[1]) for i in num_entrank],
            "realtimehot":[(i[0],i[1]) for i in total]
        }
        return (hotValue,hot)
    def getWord(self,name):
        
        results=self.ss.select(name)
        # 提取文本数据
        texts = [row[0] for row in results]
        all_text = " ".join(texts)
        stopwords = []
        stopwords_path = 'STOPWORD.txt' #屏蔽词
        words = jieba.lcut(all_text) #分词，精准模式
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            for line in f:
                if len(line) > 0:
                    stopwords.append(line.strip())
        self.word_set=set()
        for word in words:
            if word not in stopwords and len(word)!=1:
                self.word_set.add((word,words.count(word)))
            else:
                continue
        return self.word_set
    def getPost(self,name):
        results=self.ss.select(name)
        # 提取文本数据
        texts = [row[0].replace("收起d","").replace("展开c","") for row in results if (not "\n \u200b"in row[0]) and (not "\n\xa0\u200b" in row[0])]
        print(texts)
        return texts
    def getLine(self,sep):#获取折线图数据，以sep为间隔，每个sep为6min
        sport_history=self.ss.select("weibo_sport_history")[-10*sep::sep]
        entrank_history=self.ss.select("weibo_entrank_history")[-10*sep::sep]
        game_history=self.ss.select("weibo_game_history")[-10*sep::sep]
        realtimehot_history=self.ss.select("weibo_realtimehot_history")[-10*sep::sep]
        linedata={
            "xline":list(map(lambda x:"6-19 "+str(x[0])[11:16],realtimehot_history)),
            "realtimehotline":list(map(lambda x:x[1]//1000,realtimehot_history)),
            "entrankline":list(map(lambda x:x[1]//1000,entrank_history)),
            "sportline":list(map(lambda x:x[1]//1000,sport_history)),
            "gameline":list(map(lambda x:x[1]//1000,game_history)),
        }
        return linedata
    def gethdfs(self):
        hdfs=self.ss.select("weibo_hdfs")
        return list(map(lambda x:x[0],hdfs))
        
        
        
        
