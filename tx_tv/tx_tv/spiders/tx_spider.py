# -*- coding: utf-8 -*-
import random
import re
import time
import scrapy

from tx_tv.items import TxTvItem


class TxSpiderSpider(scrapy.Spider):
    name = 'tx_spider'
    allowed_domains = ['v.qq.com']
    # start_urls = ['http://v.qq.com/']
    base_url1 = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=tv&listpage=2&offset="
    base_url2 = "&pagesize=30&sort=18"
    offset = 0
    start_urls = [base_url1 + str(offset) + base_url2]

    def parse(self, response):
        a_list = re.findall('(?<=<a href=")https://v.qq.com/x/cover/.*?\.html', response.body.decode())

        # 退出条件
        if len(a_list) == 0:
            return
        for a in a_list:
            # 休眠时间
            t1 = max(2, int(random.random() * 5))
            time.sleep(t1)
            yield scrapy.Request(
                a,
                callback=self.parse_tv_detail,
                # meta={"item": item}
            )

        self.offset += 30
        print('--------------------------------------------------------------------------current page ', self.offset)
        yield scrapy.Request(self.base_url1 + str(self.offset) + self.base_url2, callback=self.parse)

    def parse_tv_detail(self, response):
        item = TxTvItem()

        # 剧集壳id
        item["tv_id"] = response.url.split('/')[-1].split('.')[0]

        # 电视剧名字
        try:
            item['tv_name'] = response.xpath(
                "//*[@id='container_player']/div/div[2]/div[1]/div[1]/h1/a/text()").extract_first()
        except:
            item['tv_name'] = ''

        # 本站评分
        try:
            score1 = response.xpath(
                "//*[@id='container_player']/div/div[2]/div[1]/div[1]/span/span[1]/text()").extract_first()
            score2 = response.xpath(
                "//*[@id='container_player']/div/div[2]/div[1]/div[1]/span/span[2]/text()").extract_first()
            item['score']= '{}{}'.format(score1, score2)
        except:
            item['score'] = ""

        # 豆瓣评分
        try:
            item['douban_score'] = response.xpath(
                "//*[@id='container_player']/div/div[2]/div[1]/div[1]/span/span[3]/span/span/text()").get()
        except:
            item['douban_score'] = ''

        # 年代
        try:
            years = response.xpath("//*[@class='video_tags _video_tags']/span/text()").extract_first()
            if '\n' in years:
                years = ''
            item['years'] = years
        except:
            item['years'] = ""

        #   标签合集
        try:
            labels = response.xpath("//*[@class='video_tags _video_tags']/a")

            # 地区
            item['area'] = labels[0].xpath('./text()').extract_first()

            number = 1
            # 对于个别年份，在labels里面。
            if item['years'] == "" and labels[number].xpath('./text()').get().isdigit():
                item['years'] = labels[number].xpath('./text()').get()
                number = 2

            tmp_list = []
            for label in labels[number:]:
                tmp_list.append(label.xpath("./text()").extract_first())
            item['label_list'] = '/'.join(tmp_list)
        except:
            item['area'] = ""
            item['label_list'] = ""

        # .//*[@class='director']
        # 求出导演和演员的分界线
        try:
            line_list = response.xpath(".//*[@class='director']/text()").extract()

            line_index = line_list.index("演员: ")

            # 求出所有的导演和演员的名字
            people_names = response.xpath(".//*[@class='director']/a/text()").extract()
            item['director_list'] = '/'.join(people_names[:line_index - 1])
            item['starring_list'] = '/'.join(people_names[line_index - 1:])
        except:
            item['director_list'] = ""
            item['starring_list'] = ""

        # 内容简介
        try:
            info_tmp = response.xpath(".//p[@class='summary']/text()").extract_first()
            if '\r\n' in info_tmp:
                info_tmp = info_tmp.replace('\r\n', '    ')
            elif '\r' in info_tmp:
                info_tmp = info_tmp.replace('\r', '    ')
            elif '\n' in info_tmp:
                info_tmp = info_tmp.replace('\n', '    ')
            item['content_info'] = info_tmp
        except:
            item['content_info'] = ""

        # 入库日期
        try:
            item['dayid'] = time.strftime("%Y%m%d", time.localtime())
        except:
            item['dayid'] = ""

        try:
            # 评论量
            item['comment'] = response.xpath('//*[@id="container_player"]/div/div[1]/div[1]/div[2]/div[2]/div/@title').get()
        except:
            item['comment'] = ''

        # 点赞数
        item['likes'] = ''

        # 热度
        item['heat'] = ''

        # 频道
        item['channel'] = u'电视剧'

        # 站点来源
        item['site_source'] = u'腾讯视频'

        return item



