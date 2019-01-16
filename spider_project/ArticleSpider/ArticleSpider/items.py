# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader实现默认提取第一个
    default_output_processor = TakeFirst()


def handle_create_data(value):
    #处理时间函数
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()  # 转换为时间类型
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date



def return_value(value):
    #返回列表值
    return value

def get_nums(value):
    """

    去除评论,点赞,收藏数的正则表达式,只取数字
    """
    match_re = re.match(".*?(\d+).*?", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    """
    处理标签函数，去除评论两个字
    """
    if "评论" in value:
        return ""
    else:
        return value



class JoBoleArticleItem(scrapy.Item):  #伯乐Item
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(handle_create_data)  # 预先处理,自定义函数，从左到右顺序执行
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)  #output_processor取值的函数
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(",")  #连接符来连接列表
    )