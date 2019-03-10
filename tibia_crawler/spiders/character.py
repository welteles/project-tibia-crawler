# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CharacterSpider(CrawlSpider):
    name = 'character'
    allowed_domains = ['tibia.com']
    start_urls = ['https://www.tibia.com/community/?subtopic=characters&name=']

    def __init__(self, name=None, *args, **kwargs):
        super(CharacterSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.start_urls[0] + '%s' % name]

    def parse(self, response):
        yield {
            'character_information': self.character_information(response),
            'account_information': self.account_information(response)
        }

    def character_information(self, response):
        character_information = {}
        for line in response.css('.BoxContent table:first-child tr'):
            lineArray = line.css('td::text').getall()
            if len(lineArray) == 2:
                character_information[lineArray[0]] = lineArray[1];
        return character_information

    def account_information(self, response):
        player_status = {}
        for line in response.css('.BoxContent table:first-child tr'):
            lineArray = line.css('td::text').getall()
            if len(lineArray) == 2:
                keyName = lineArray[0]
                value = lineArray[1]
                player_status[keyName] = value;
        return player_status
