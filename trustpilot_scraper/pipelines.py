# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import logging
import json
class TrustpilotScraperPipeline:
    # each time yield is called from the spider, the items go here
    def __init__(self):
        self.con = sqlite3.connect('trustpilot.db')  # create/connect to database
        self.cur = self.con.cursor()  # create cursor, used to execute commands
        self.create_table()
        logging.info(f'SQLite pipeline is enabled')

    def create_table(self):
        # self.cur.execute('''DROP trustpilot_table''')  # if the table already exists, it deletes the
        # previous table and creates a new one
        self.cur.execute('''CREATE TABLE IF NOT EXISTS trustpilot_table(
                        title TEXT,
                        trust_score REAL,
                        location TEXT,
                        services TEXT)''')


    def process_item(self, item, spider):
        services = json.dumps(item['services'])
        self.cur.execute('''INSERT OR IGNORE INTO trustpilot_table VALUES (?,?,?,?)''',
                         (
                             item['title'],
                             item['trust_score'],
                             item['location'],
                             services
                         ))
        self.con.commit()  # command used to insert the data
        return item

    def spider_closed(self, spider):
        self.con.close()


