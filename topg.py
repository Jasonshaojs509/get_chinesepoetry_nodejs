'''
Descripttion: 
version: 
Author: shaojinxin
Date: 2021-07-26 13:49:51
LastEditors: shaojinxin
LastEditTime: 2021-07-26 16:20:13
'''
# coding=utf-8
import re
import json
from datetime import datetime
import logging
import os
import psycopg2
import time
from io import BytesIO
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collections import Counter #引入Counter

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
today = time.strftime("%Y%m%d", time.localtime())
logfile = f'log/topg-{today}.txt'
fh = logging.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
# 第四步，定义handler的输出格式
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

conn = psycopg2.connect(database="data",user="postgres",password="zjhzmcm2839667",host="127.0.0.1",port="5432")
logger.info("Opened database successfully")
cur = conn.cursor()
global_index = 0

def scan_shi():
    for files in os.listdir('json'):
        if re.search('json', files) and re.search('poet', files) and re.search('tang', files):
            path = os.path.join('json',files)
            import_shi(path,'唐')
        elif re.search('json', files) and re.search('poet', files) and re.search('tang', files):
            import_shi(path,'宋')

def import_shi(path,age):
    global global_index
    with open(path, encoding='utf-8') as f:
        d = json.loads(f.read())
        for item in d:
            author = item['author']
            paragraphs = item['paragraphs']
            title = item['title']
            id = item['id']
            if len(paragraphs)>0:
                sql = f"INSERT INTO poetry.shi (id,author,title,paragraphs,collect,age) select '{id}', '{author}','{title}',ARRAY {paragraphs},FALSE,'{age}' where not exists (select * from poetry.shi where id = '{id}');"
                cur.execute(sql)
                conn.commit()
                logger.info(f"{global_index}:{title} is storage!")
            global_index+=1
        f.close()

def scan_ci():
    for files in os.listdir('ci'):
        if re.search('json', files) and re.search('ci', files) and re.search('song', files):
            path = os.path.join('ci',files)
            import_ci(path,'宋')

def import_ci(path,age):
    global global_index
    with open(path, encoding='utf-8') as f:
        d = json.loads(f.read())
        for item in d:
            author = item['author']
            paragraphs = item['paragraphs']
            rhythmic = item['rhythmic']
            if len(paragraphs)>0:
                sql = f"INSERT INTO poetry.ci (author,rhythmic,paragraphs,collect,age) select '{author}','{rhythmic}',ARRAY {paragraphs},FALSE,'{age}' where not exists (select * from poetry.ci where paragraphs = ARRAY {paragraphs});"
                cur.execute(sql)
                conn.commit()
                logger.info(f"{global_index}:{rhythmic} is storage!")
            global_index+=1
        f.close()

if __name__ == '__main__':
    scan_ci()