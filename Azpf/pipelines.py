# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from openpyxl import Workbook
import time

class excelPipeline(object):
#定义一个类，负责处理item
    def open_spider(self,spider):
        print("创建表格")
        self.wb = Workbook()
        self.wb.create_sheet ("爬取")
        self.ws = self.wb["爬取%d"%(spider)]
        self.ws.append(['类别', '名称', '网址', '推特', '投资机构',"spider"])
        #用append函数往表格添加表头

    def process_item(self, item, spider):
    #process_item是默认的处理item的方法，就像parse是默认处理response的方法
        print("开始写入")
        self.ws.append(item['category'], item['name'], item['url'], item['twitter'], item['funds'], spider)
        #用append函数把数据都添加进表格
        return item
        #将item丢回给引擎，如果后面还有这个item需要经过的itempipeline，引擎会自己调度

    def close_spider(self, spider):
    #close_spider是当爬虫结束运行时，这个方法就会执行
        time_1 = time.strftime("%Y-%m-%D",time.localtime())
        #file_name = (r"%d爬虫%d爬取.xlsx"%(str(time_1),spider))
        # file_name = str(time_1+spider+".xlsx")
        print("储存结束")
        self.wb.save(spider)
        #保存文件
        self.wb.close()
        #关闭文件