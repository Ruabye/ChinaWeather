# -*- coding: utf-8 -*-
import scrapy
import time

def decorate(func):
    def improve_func(*args, **kwargs):
        print("------------------------start------------------------")
        ret = func(*args, **kwargs)
        print("-------------------------end-------------------------")
        return ret
    return improve_func


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

    # @decorate
    def weather_parse(self, response):

        # 近7天的天气情况
        sections = response.xpath("//div[@class='conMidtab']")
        #明天各地区的天气情况
        areas = sections[1].xpath("./div[@class='conMidtab2']")
        #不同信息的width值不同
        dic = {
                "83":"城市", "89":"天气现象(白天)", "162":"风向风力(白天)","92":"最高气温(白天)",
               "98":"天气现象(夜间)", "177":"风向风力(夜间)","86":"最高气温(夜间)"
            }
        #最终结果数组
        result_data = []
        #分地区解析信息，各地区前两个tr都是表头
        for area in areas:
            #跳过区域的表头
            citys = area.xpath(".//tr")[2:]
            for city in citys:

                city_data = {}
                for k in dic.keys():
                    #表格中的文本数据
                    d = city.xpath(".//td[@width=%s]//text()" % k)
                    #这里需使用getall(),风向风力列表中有"\n"字符
                    d = ''.join(d.getall()).replace("\n", " ").strip()
                    city_data[ dic[k] ] = d
                #详情链接
                url = city.xpath("./td/a/@href").get()
                city_data[ "url" ] = url
                #爬取日期
                city_data[ "update_data" ] =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                result_data.append(city_data)
        #返回结果
        return result_data



