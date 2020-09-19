# -*- coding: utf-8 -*-
import scrapy


class ChinaweatherSpider(scrapy.Spider):
    name = 'ChinaWeather'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://www.weather.com.cn/textFC/hb.shtml']

    def parse(self, response):

        #获得页面上的链接
        sections = response.xpath("//div[@class='contentboxTab1']/div/ul/li/span/a/@href")
        base_url = "http://www.weather.com.cn"
        #搜集不同地区的天气情况
        for section in sections:
            yield scrapy.Request(base_url + section.get(), callback=self.weather_parse)

    def weather_parse(self, response):

        # 近7天的天气情况
        sections = response.xpath("//div[@class='conMidtab']")
        #搜集明天的天气情况
        rows = section[1].xpath("./div[@class='conMidtab2']//tr")

        # print(response.url)

