import random
import time

import scrapy
import re
import json
from pprint import pprint
from scrapy import Request
import string

from xpc.items import PostItem
from scrapy_redis.spiders import RedisSpider
from xpc.items import CommentItem


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com', 'qiniu-xpc15.xpccdn.com', 'openapi-vtom.vmovier.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/']
    cookies = dict(
        Authorization='E54312FD3785C68D73785C4A583785C9CF23785CDADD3204EBC0',
    )

    def parse(self, response):
        articleid = response.css('.enter-filmplay::attr(data-articleid)').extract()
        video_url = response.css('.enter-filmplay::attr(data-videourl)').extract()
        for id, v_url in zip(articleid, video_url):
            # https://www.xinpianchang.com/a10845710?from=ArticleList
            link = "/a" + id + ("?from=" + v_url if v_url else "")
            cookies = dict(
                PHPSESSID=''.join(random.sample(string.ascii_lowercase + string.digits, 26))
            )
            yield response.follow(link, self.parse_post, cookies=cookies)
        # 下一页
        next_page = response.css('div[class="page"] a:last-child::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse, cookies=self.cookies)

    def parse_post(self, response):
        post = PostItem(
            title=response.css('.title::text').extract_first(),
            category='-'.join(response.css('.cate a::text').extract()).replace('\t', '').replace('\n', ''),
            update_time=response.css('.update-time i::text').extract_first(),
            play_counts=response.css('.play-counts::text').extract_first().replace(',', ''),
            like_counts=response.css('.like-counts::text').extract_first().replace(',', ''),
            tags=', '.join(response.css('.tag-wrapper a::text').extract()),
            description=response.css('.filmplay-info-desc p::text').extract_first()
        )

        # 解析视频信息
        vid, = re.findall(r'var vid = "(\w+)";?', response.text)
        post['vid'] = vid
        app_key, = re.findall(r'var modeServerAppKey = "(\w+)";?', response.text)
        url_format = 'http://openapi-vtom.vmovier.com/v3' \
                     '/video/%s?expand=resource&usage=xpc_web&appKey=%s'
        # https://openapi-vtom.vmovier.com/v3/video/5F0C33F784BB4?expand=resource&usage=xpc_web&appKey=61a2f329348b3bf77
        url = url_format % (vid, app_key)
        request = Request(url=url, callback=self.parse_video)
        request.meta['post'] = post
        yield request
        # 解析评论信息
        # https://app.xinpianchang.com/comments?resource_id=10847731&type=article
        resource_id, = re.findall(r"article_id: '(\d+)'", response.text)
        url_format = 'http://app.xinpianchang.com/comments?resource_id=%s&type=article&page=1'
        url = url_format % resource_id
        request = Request(url, callback=self.parse_comment)
        yield request

    def parse_video(self, response):
        post = response.meta['post']
        video = json.loads(response.text)['data']['video']
        post['video'] = video['source_link']
        post['cover'] = video['cover']
        post['duration'] = video['duration']
        yield post

    def parse_comment(self, response):
        res = json.loads(response.text)
        comment = CommentItem()
        if res['data']:
            comment_list = res['data']['list']
            for ct in comment_list:
                comment['cid'] = ct['id']
                comment['content'] = ct['content']
                comment['avatar'] = ct['userInfo']['avatar']
                comment['uname'] = ct['userInfo']['username']
                comment['add_time'] = time.strftime('%Y-%m-%d %H-%M', time.localtime(ct['addtime']))
                yield comment
            next_url = res['data']['next_page_url']
            if next_url:
                response.follow(next_url, self.parse_comment)
