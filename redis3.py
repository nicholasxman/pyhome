#! /usr/bin/python3
import redis
import pymysql
from multiprocessing import Process

# mysql中数据更新后同步到redis
'''
流程：
1. mysql更新数据
2. redis更新数据
'''


class Update(Process):
    # 连接redis和mysql,创建mysql游标对象
    def __init__(self):
        Process.__init__(self)
        self.r = redis.Redis(host='localhost', password='123456', port=6379, db='7')
        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, database='userdb',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    # mysql更新数据事件子进程
    def update_mysql(self, score=None, username=None):
        upd = 'update user set score=%s where name=%s'
        try:
            self.cursor.execute(upd,[score,username])
            self.db.commit()
            # self.cursor.close()
            # self.db.close()

            # 做一个更新成功的标记
            return True
        except Exception as e:
            self.db.rollback()
            print('Failed', e)


    # redis更新数据事件子进程
    def update_redis(self, score=None, username=None):
        # redis更新数据: hmset(key,{mapping})
        self.r.hmset(username, {'score': score})
        # 设置过期时间
        self.r.expire(username, 30)

    # run()是Process父类提供的接口函数，启动时自动调用子进程
    # def run(self):
        # username = 'klpll'
        # username = input('请输入用户名：')
        # score = float(input('请输入成绩:'))
        # score = 69
        # 创建子进程对象并传参
        # p1 = Process(target=self.update_mysql, args=(username, score))
        # p2 = Process(target=self.update_redis, kwargs={'username': username, 'score': score})
        #
        #     #正式生成子进程并执行
        #     #确保mysql更新成功后(mysql更新子进程返回True)再更新redis
        # p1.start()
        # p2.start()
    #
    #     # #回收子进程
    #     # p1.join()
    #     # p2.join()


if __name__ == '__main__':
    # 创建对象
    upda = Update()
    # upda.run()
    username = 'neo'
    score = 75632
    p1 = Process(target=upda.update_mysql, args=(score, username ))
    p1.run()
