# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pymysql


class TxTvPipeline(object):

    def __init__(self):
        ""
        try:
            self.connect = pymysql.connect(
                host='localhost',  # 数据库地址
                port=3306,  # 数据库端口
                db='migu',  # 数据库名
                user='root',  # 数据库用户名
                passwd='123456',  # 数据库密码
                charset='utf8',  # 编码方式
                use_unicode=True)

            # 通过cursor执行增删查改
            self.cursor = self.connect.cursor()
            print('------------------------------------------------------------------连接成功')
        except:
            print('--------------------------------------------------------------连接失败')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into tv_d_tx(
                                tv_id,
                                tv_name,
                                score,
                                douban_score,
                                comment,
                                likes,
                                area,
                                years,
                                label_list,
                                director_list,
                                starring_list,
                                heat,
                                content_info,
                                channel,
                                site_source,
                                dayid) 
                value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['tv_id'],
                    item['tv_name'],
                    item['score'],
                    item['douban_score'],
                    item['comment'],
                    item['likes'],
                    item['area'],
                    item['years'],
                    item['label_list'],
                    item['director_list'],
                    item['starring_list'],
                    item['heat'],
                    item['content_info'],
                    item['channel'],
                    item['site_source'],
                    item['dayid'],
                ))
            # 提交sql语句
            self.connect.commit()
            # self.cursor.close()
            print('---------------------------------------------插入成功')
        except:
            print("-------------------------------------------------------------------------插入失败")

        return item  # 必须实现返回

    def close_spider(self, spider):
        self.cursor.close()


