# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TxTvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 剧集壳id
    tv_id = scrapy.Field()
    # 内容名称
    tv_name = scrapy.Field()
    # 本站评分
    score = scrapy.Field()
    # 豆瓣评分
    douban_score = scrapy.Field()
    # 评论量
    comment = scrapy.Field()
    # 点赞量
    likes = scrapy.Field()
    # 地区
    area = scrapy.Field()
    # 年代
    years = scrapy.Field()
    # 标签
    label_list = scrapy.Field()
    # 导演
    director_list = scrapy.Field()
    # 主演
    starring_list = scrapy.Field()
    # 热度
    heat = scrapy.Field()
    # 内容简介
    content_info = scrapy.Field()
    # 频道
    channel = scrapy.Field()
    # 站点来源
    site_source = scrapy.Field()
    # 爬取时间
    dayid = scrapy.Field()
