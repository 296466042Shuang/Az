import scrapy
from scrapy.crawler import CrawlerProcess
import bs4
from Azpf.items import AzpfItem
from Azpf.pipelines import excelPipeline
from scrapy.utils.project import get_project_settings

def GetMiddleStr(content,startStr,endStr):
    # startIndex = content.indexA(startStr)
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
        endIndex = content.index(endStr)
    return content[startIndex:endIndex]

def judge(web):
    a =  GetMiddleStr(web,'//','.')
    if a == 'www':
        b = web.split('.')[1]
    else:
        b = GetMiddleStr(web,'//','.')
    return b

class Web1Spider(scrapy.Spider):
    name = 'Web1'
    allowed_domains = ['spartangroup.io']
    start_urls = ['http://spartangroup.io/management.html/']
    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        div_all = bs.find_all('div',class_="portfolio")
        for div in div_all:
            a_list = div.find_all('a')
            for a in a_list:
                com_url = a['href']
                item = AzpfItem()
                item['url'] = com_url
                com_name = judge(com_url)
                item['name'] = com_name
                item['funds'] = ('spartangroup')
                yield item

class Web2Spider(scrapy.Spider):
    name = 'Web2'
    allowed_domains = ['ldcap']
    start_urls = ['https://dashboard.ldcap.sekai.me/api/v1/portfolio']
    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')        
        com_all = bs.find_all('div',class_= "Portfolio__StyledProjectGroup-sc-4wu4eb-0 gqghUN scale-1")
        for com in com_all:
            a_list = com.find_all('a')
            for a in a_list:
                item = AzpfItem()
                item['name'] = a.find('div',class_="project-name").text
                item['funds'] = ('ldcap')
            yield item

class Web3Spider(scrapy.Spider):
    name = 'Web3'
    allowed_domains = ['multicoin.capital']
    start_urls = ['https://multicoin.capital/portfolio/']
    #excelPipeline.open_spider()
    #名称，板块、推特、网页
    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        div_all = bs.find_all('div',class_= "sc-bdVaJa Project__StyledProject-sc-1vpvqcu-1 eGAFwi sc-bwzfXH bydaod")
        for div in div_all:
            item = AzpfItem()
            if len(div.find(class_='collapsed links')) != 0:
                com_url = div.find(class_='collapsed links').find_all('a')[0]['href']
                item['twitter'] = div.find(class_='collapsed links').find_all('a')[1]['href']
                item['url'] = com_url
                com_name = judge(com_url)
                item['name'] = com_name
                item['category'] = div.find(class_='categories').text
                item['funds'] = ('multicoin')
                yield item

class Web4Spider(scrapy.Spider):
    name = 'Web4'
    allowed_domains = ['dcg.co']
    start_urls = ['https://dcg.co/portfolio/']
    #名称，板块、推特、网页
    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        div_all = bs.find_all('div',class_= "company-info")
        for div in div_all:
            item = AzpfItem()
            com_url = div.find(class_='description').find('a').text
            item['url'] = com_url
            item['name'] = div.find(class_='name').find('h6').text
            item['funds'] = ('dcg')
            yield item

class Web5Spider(scrapy.Spider):
    name = 'Web5'
    allowed_domains = ['a16z.com']
    start_urls = ['https://a16z.com/portfolio/']
    #名称，板块、推特、网页
    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        div_all = bs.find_all('div',class_='company__thumbnail company__thumbnail-link')
        for div in div_all:
            item = AzpfItem()
            if div.find('a') != None:
                com_url = div.find('a')['href']
                item['url'] = com_url
                com_name = judge(com_url)
                item['name'] = com_name
                item['funds'] = ('a16z')
                yield item

#实例化多进程并运行
setting = get_project_settings()
process = CrawlerProcess(settings=setting)
# process.crawl(Web1Spider)
# print("Web 1 end to scrapy")
# process.crawl(Web2Spider)
# print("Web 2 end to scrapy")
process.crawl(Web3Spider)
print("Web 3 end to scrapy")
# process.crawl(Web4Spider)
# print("Web 4 end to scrapy")
# process.crawl(Web5Spider)
# print("Web 5 end to scrapy")
process.start()