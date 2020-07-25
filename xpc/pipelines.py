# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class XpcPipeline:
    def process_item(self, item, spider):
        return item


class MySQLPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            user='root',
            password='*',
            host='*.*.*.*',
            port=3306,
            charset='utf8mb4',
            database='xpc'
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        keys, values = zip(*item.items())
        sql = 'insert into {}({}) values({})'.format(
            item.table_name,
            ', '.join(keys),
            ', '.join(['%s'] * len(keys))
        )
        self.conn.commit()
        self.cursor.execute(sql, values)
        print(self.cursor._last_executed)
        return item
