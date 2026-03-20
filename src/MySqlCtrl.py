# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-

import pymysql

class database:#数据库类
    '''数据库操作类'''
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
    def __getConnect(self):
        '''
        获取数据库链接
        '''
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4'
        )
        return conn
    def select(self,table,item="*",where=""):
        '''
        提供需要查找的表和项及限制条件,项以列表或元组形式传入,缺省值为*，限制条件缺省值为空
        '''
        item="*" if item=="*" else ",".join(item)
        where="" if where=="" else " WHERE "+where
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("SELECT "+item+" FROM "+table+where)
        cursor.execute("SELECT "+item+" FROM "+table+where)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    def insert(self,table,item,itemname=" "):
        '''
        提供需要插入的表\数据项\数据项字段名(可选),项或字段名以列表或元组形式传入
        '''
        #print("________________________________________________________________________________")
        itemname=" " if itemname==" " else " ("+",".join(itemname)+") "
        item1=""
        for i in item:
            if isinstance(i,str):
                item1+="'"+i+("'," if i is not item[-1] else "'")
            else:
                item1+=str(i)+("," if i is not  item[-1] else " ")
        item=" ("+item1+") "
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("INSERT INTO "+table+itemname+"VALUES"+item)
        cursor.execute("INSERT INTO "+table+itemname+"VALUES"+item)
        conn.commit()
        cursor.close()
        conn.close()
    def delete(self,table,where):
        '''
        提供需要删除的表及其条件,若要清空整张表,请使用where="all"参数
        '''
        where="" if where=="all" else " WHERE "+where
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("DELETE FROM "+table+where)
        cursor.execute("DELETE FROM "+table+where)
        conn.commit()
        cursor.close()
        conn.close()
    def create(self,table,item):
        '''
        创建表:提供表名,并以字典形式传入表项(key为项名,value为类型)
        '''
        it=""
        for i in item:
            it+=i+" "
            it+=item[i]+","
        it=it[:-1:]
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("CREATE TABLE IF NOT EXISTS "+table+" ("+it+")")
        cursor.execute("CREATE TABLE IF NOT EXISTS "+table+" ("+it+")")
        conn.commit()
        cursor.close()
        conn.close()
    def update(self,table,data,where):
        '''
        提供需要更新的表\数据\限制条件,数据以列表或元组形式传入,若要修改整张表,请使用where="all"参数
        '''
        where="" if where=="all" else " WHERE "+where
        data=" "+",".join(data)+" "
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("UPDATE "+table+" SET "+data+where)
        cursor.execute("UPDATE "+table+" SET "+data+where)
        conn.commit()
        cursor.close()
        conn.close()
    def drop(self,table):
        '''
        删除表:提供表名
        '''
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("DROP TABLE "+table)
        cursor.execute("DROP TABLE "+table)
        conn.commit()
        cursor.close()
        conn.close()
    def getTable(self):
        '''
        获取表
        '''
        conn=self.__getConnect()
        cursor =conn.cursor()
        print("SHOW TABLES")
        cursor.execute("SHOW TABLES")
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.fetchall()

