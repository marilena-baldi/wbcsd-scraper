""" Scrapy spiders """

import urllib
import scrapy
from core.items import CourseItem


class WbcsdSpider(scrapy.Spider):
    """ Wbcsd spider """

    name = "wbcsd"
    url_page = {
            "https://www.wbcsd.org/Overview/News-Insights/Insider-perspective":
            "https://www.wbcsd.org/Overview/News-Insights/Insider-perspective",
            "https://www.wbcsd.org/Overview/News-Insights/WBCSD-insights":
            "https://www.wbcsd.org/bm/ajax/block/1297/en_GB/default?_hash=PKWBoLWVFe3rPf78M0CayB%"\
            "2BHzkZiThRDo0zTWO7m4Q8%3D&ngbmContext[ez_location_id]=6565"
        }
    start_urls = list(url_page.keys())

    def build_page_url(self, url, index):
        """ Process an url updating its page number

        :param url: the url to parse
        :type url: str
        :param index: the page number
        :type index: int
        :return: the parsed url
        :rtype: str
        """

        params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        base_url = urllib.parse.urlparse(url)
        params.update({"page": index})

        return base_url.scheme + "://" + base_url.netloc + base_url.path + "?" + \
            urllib.parse.urlencode(params, doseq=True)

    def parse(self, response): # pylint: disable=arguments-differ
        """ Parse a url response to get its pages urls """

        last_page_url = response.css('ul.pagination li.visible-xs-inline a::attr(href)').get()

        if last_page_url is not None:
            last_page_num = int(
                    urllib.parse.parse_qs(urllib.parse.urlparse(last_page_url).query)["page"][0]
                )

        else:
            last_page_num = int(
                    response.css('nav.ajax-navigation::attr(data-total-pages)').extract()[0]
                )

        for i in range(1, last_page_num + 1):
            yield scrapy.Request(
                    url=self.build_page_url(self.url_page[response.url], i),
                    callback=self.parse_page
                )


    def parse_page(self, response): # pylint: disable=arguments-differ
        """ Parse a page url response to get the courses urls """

        for course in response.css('div.info'):
            url = course.css('h2.title a::attr(href)').get()

            yield response.follow(url, callback=self.parse_course)

        next_page = response.css('navigation ul.pagination li a.ajax-nav-last::attr("href")').get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_course(self, response):
        """ Parse a course url response to extract the course information """

        yield CourseItem(
                url=response.url,
                title=response.css('h1.page-title span.ezstring-field::text').get(),
                image_url=urllib.parse.urljoin(
                    response.url,
                    response.css('figure.featured-image img.ezimage-field::attr(src)').get()
                ),
                publication_date=response.css('div.date::text').re_first(r'(\d{1,2} \w{3} \d{4})'),
                tags=response.css('div.tags a::text').getall()
        )
