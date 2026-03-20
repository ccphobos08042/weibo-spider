import json
import web
import MySqlCtrl
import getdata
import spider

urls = (
    '/','hello',
    '/post','postdata',
    '/postline','linedata',
    '/postword','worddata',
    '/posthdfs','hdfs',

)
app = web.application(urls, globals())
render=web.template.render('./')
mysqldataCtrl=MySqlCtrl.database("192.168.217.10","root","Bp.33331371","cauc")
#改为自己的sql链接
cookie="SINAGLOBAL=3605935749406.111.1718327398211; SUB=_2A25LajsSDeRhGeBL7FYZ-S3Myj-IHXVoBjLarDV8PUNbmtAGLUTXkW9NRsi1vTgHcf2ub_g4TIbMFitgm-ylVcf2; _s_tentry=-; Apache=2292507388789.351.1718630007170; ULV=1718630007176:16:16:9:2292507388789.351.1718630007170:1718614771428"
#改为自己的cookie
class postdata:
    global mysqldataCtrl
    def POST(self):
        data = json.loads(web.data())
        hotName = data.get('hotName')
        data=getdata.getdata(mysqldataCtrl)
        x=data.getPost(hotName)
        new=[
            { "name": o[0], "value": o[1] }for o in data.getWord(hotName)
            ]
        web.header('Content-Type', 'application/json')
        return json.dumps({'newData': new})

class hello:
    def GET(self):
        data=getdata.getdata(mysqldataCtrl)
        hotValue=data.getValue()[0]
        hotName=data.getValue()[1]
        return render.index(hotValue,hotName)
class linedata:
    def POST(self):
        data = json.loads(web.data())
        sep = data.get('sep')
        data=getdata.getdata(mysqldataCtrl)
        line=data.getLine(sep)
        web.header('Content-Type', 'application/json')
        return json.dumps({'newData': line})
class worddata:
    def POST(self):
        data = json.loads(web.data())
        hotName = data.get('hotName')
        data=getdata.getdata(mysqldataCtrl)
        x=data.getPost(hotName)
        web.header('Content-Type', 'application/json')
        return json.dumps({'newData': x})
class hdfs:
    def POST(self):
        data=getdata.getdata(mysqldataCtrl)
        x=data.gethdfs()
        print(x)
        web.header('Content-Type', 'application/json')
        return json.dumps({'newData': x})
if __name__ == "__main__":
    sql=mysqldataCtrl
    spider.spider(cookie=cookie,sql=sql).start_spider()
    app.run()