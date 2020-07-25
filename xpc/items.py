# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class XpcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PostItem(scrapy.Item):
    """保存视频信息的item"""
    table_name = 'posts'
    vid = Field()
    title = Field()
    cover = Field()
    video = Field()
    tags = Field()
    duration = Field()
    category = Field()
    update_time = Field()
    play_counts = Field()
    like_counts = Field()
    description = Field()


class CommentItem(scrapy.Item):
    table_name = 'comments'
    cid = Field()
    avatar = Field()
    uname = Field()
    add_time = Field()
    content = Field()


