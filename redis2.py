#! /usr/bin/python3
import redis
import pymysql
# 模拟用户查询过程
'''
1. 先到redis中查询
2. redis中没有，到Mysql中查询，并将数据缓存到redis(设置过期时间)
3. 再查询一次，此时就从redis中直接拿
4. 过期时间到，redis中缓存的数据没了，重复第二步
'''
#1111111111
# 连接redis
r = redis.Redis(host='192.168.232.132',password='123456', port=6379, db='4')

# 连接mysql
db = pymysql.connect(host='192.168.232.132', user='root', password='123456', port=3306, database='userdb', charset='utf8')

# 创建pymysql游标对象
cursor = db.cursor()

# 用户开始查询
username = input('请输入用户名:')
# 1.redis查
# hgetall(key):获取该key的所有field和value
# 将mysql数据表中的字段username当做redis的key
result = r.hgetall(username)

if result:
    print('redis:', result)
    # 2.到mysql中查询，再缓存到redis,打印输出
else:
    sel = 'select age,score from user where name="%s"' % username
    print(sel)
    cursor.execute(sel)
    # 获取查到的结果：fetchone():返回的结果是 (age_value,score_value) 元组
    userinfo = cursor.fetchone()
    print('mysql:', userinfo)
    # 3.缓存到redis
    r.hmset(username, {'age': userinfo[0], 'score': userinfo[1]})
    # 设置过期时间：expire(key,time)
    r.expire(username, 300)

cursor.close()
db.close()
