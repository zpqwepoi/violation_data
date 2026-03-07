# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import threading
#import logging
import os
import json
import requests
import time
import violation_contents
from datetime import datetime
from pathlib import Path
from wxwork_func import msg_poster
from data_clean import Controller
import pymysql
from pymysql import Error
#engine = create_engine("") #此为测试用数据库，非生产环境
#sql_password = os.environ.get('')
#engine = create_engine("")  # 执行连接前检查有效性（推荐）)
#Session = sessionmaker(engine)
#session = Session()
webhook_qywx = "" # 企业微信群机器人提醒的webhook，需要自行配置
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#print(f"开始启动12123违章查询服务，本次启动时间:{start_time}，使用详情请查看README.md")

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def query():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        data = request.json
        controller = Controller()
        #rollback_status = False
        raw_data = controller.execute(data)
        #for item in raw_data:
        #    print(item['car_no'],item['violation_time'],item['violation_address'])
        if len(raw_data)<1:
            return "200"
        else:
            try:
                
                #此处需要配置数据库
                
                connection = pymysql.connect(
                        host='',
                        user='',
                        password='',
                        database='',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor
                    )
                with connection.cursor() as cursor:
                    # 提取所有vid
                    vids = [item['vid'] for item in raw_data]
                    company_name = raw_data[0]['company']
                    car_no_this_page = raw_data[0]['car_no']
                    existing = {}
                    existing_proccess = {}
                    if vids:
                        # 构造IN查询，获取存在的vid和pay_status
                        in_clause = ','.join(['%s'] * len(vids))
                        select_sql = f"SELECT vid, pay_status,proccess_status FROM violation_data WHERE vid IN ({in_clause})"
                        cursor.execute(select_sql, vids)
                        query = cursor.fetchall()
                        existing = {row['vid']: row['pay_status'] for row in query}
                        existing_proccess = {row['vid']: row['proccess_status'] for row in query}
                    # 分离需要插入和更新的数据
                    to_insert = []
                    to_update = []
                    for item in raw_data:
                        vid = item['vid']
                        car_no = item['car_no']
                        violation_time = item['violation_time']
                        violation_address = item['violation_address']
                        violation_content=item['violation_content']
                        #print(car_no,violation_time,violation_address,violation_content)
                        if violation_content not in violation_contents.violation_content_type:
                            try:
                                msg_poster(webhook_qywx,f"{now}告警：\n新的违章类型：{violation_content}\n车牌号：{car_no}")
                                continue
                            except Exception as e:
                                print(f"{now}告警：\n新的违章类型：{violation_content}\n车牌号：{car_no}")
                                
                        if vid not in existing:
                            to_insert.append(item)
                        else:
                            if (item['pay_status'] != existing[vid]) or (item['proccess_status'] != existing_proccess[vid]):
                                to_update.append(item)
    
                    # 批量插入数据
                    if to_insert:
                        insert_sql = f"""
                            INSERT INTO violation_data (
                                vid, car_no, proccess_time, violation_time, violation_address,
                                violation_content, proccess_status, pay_status, violation_points,
                                violation_fines, company, resource,refresh_time
                            ) VALUES (
                                %(vid)s, %(car_no)s, %(proccess_time)s, %(violation_time)s,
                                %(violation_address)s, %(violation_content)s, %(proccess_status)s,
                                %(pay_status)s, %(violation_points)s, %(violation_fines)s,
                                %(company)s, %(resource)s,NOW()
                            )
                        """
                        cursor.executemany(insert_sql, to_insert)
                        rematch_sql = """
                            UPDATE violation_data
                            LEFT JOIN (
                                SELECT 
                                    `violation_time`, 
                                    `car_no`, 
                                    `司机姓名`, 
                                    `身份证号码`, 
                                    `母单号`
                                FROM (
                                    SELECT 
                                        violation_data.violation_time,
                                        violation_data.car_no,
                                        rent_period.`司机姓名`,
                                        rent_period.`身份证号码`,
                                        rent_period.`母单号`,
                                        ROW_NUMBER() OVER (
                                            PARTITION BY violation_data.car_no, violation_data.violation_time 
                                            ORDER BY ABS(TIMESTAMPDIFF(SECOND, rent_period.`签约时间`, NOW()))
                                        ) AS rn
                                    FROM violation_data
                                    JOIN rent_period ON violation_data.car_no = rent_period.`车牌号`
                                        AND violation_data.violation_time BETWEEN rent_period.start_time AND rent_period.end_time
                                ) ranked
                                WHERE rn = 1
                            ) matched ON violation_data.car_no = matched.car_no 
                                AND violation_data.violation_time = matched.violation_time
                            SET 
                                violation_data.driver_name = matched.`司机姓名`,
                                violation_data.driver_id = matched.`身份证号码`,
                                violation_data.contract_sn = matched.`母单号`
                            WHERE
                                matched.car_no IS NOT NULL;
                        """
                        cursor.execute(rematch_sql)
                        
                    # 批量更新数据（所有字段）
                    if to_update:
                        update_sql = f"""
                            UPDATE violation_data SET
                                proccess_time = %(proccess_time)s,
                                violation_time = %(violation_time)s,
                                violation_address = %(violation_address)s,
                                violation_content = %(violation_content)s,
                                proccess_status = %(proccess_status)s,
                                pay_status = %(pay_status)s,
                                violation_points = %(violation_points)s,
                                violation_fines = %(violation_fines)s,
                                company = %(company)s,
                                resource = %(resource)s,
                                refresh_time = NOW()
                            WHERE vid = %(vid)s
                        """
                        cursor.executemany(update_sql, to_update)

                    update_info = f"update `company_status` set `last_update_time`=NOW(),`last_carno`='{car_no_this_page}' where `company_name`='{company_name}'"
                    cursor.execute(update_info)
                    # 提交事务
                    connection.commit()
                    #print(f"**********本页数据已更新至数据库**********\n{now} {company_name} {car_no_this_page}本次请求处理完成，已更新{len(raw_data)}条数据")
                    print(f"{now} {company_name} {car_no_this_page}本次请求处理完成，已更新{len(raw_data)}条数据")
                    if to_update or to_insert:
                        try:
                            requests.post("https://violatiily-task-dxydhexsos.cn-hangzhou.fcapp.run")
                        except Exception as e:
                            print(f"{now}告警：\n更新数据失败：{e}")
            except Error as e:
                print(f"数据库错误: {e,e.__traceback__.tb_lineno}")
                
                if connection:
                    connection.rollback()
            finally:
                if connection:
                    connection.close()                
    except Exception as e:
        print(f"Unexpected error: {e}{e.__traceback__.tb_lineno}")
        
    return "200"
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)