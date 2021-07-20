# %% %%
import scrapy

# %%
"""This class provides a crawl request and returns the response as a csv file."""


class LinearOptSpider(scrapy.Spider):

    name = 'linear_opt'
    # Domain of webpage we using to crawling data
    allowed_domains = ['www.oto-xemay.vn']
    # Start url of the first page in the crawling website
    start_urls = [
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=1',
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=2',
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=3',
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=4',
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=5',
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=6',
        'http://oto-xemay.vn/ben-xe/my-dinh-122.html?adodb_next_page=7', ]

    custom_settings = {'FEED_URI': "scraped_%(time)s.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):

        print("Processing: " + response.url)

        # Xpath of all data we want to crawl
        company = response.xpath(
            ".//a[@class = 'cls_diachiben']/text()")
        journeys = response.xpath(
            ".//td[2]/b/font/text()")
        times_per_day = response.xpath(
            "//td[3]/b[2]/text()")
        times_start = response.xpath(
            ".//td[5]/ul/li[2]/select[@name = 'tgxuatphat']/option/text()")
        times_end = response.xpath(
            ".//td[6]/ul/li[2]/select[@name = 'tgvedich']/option/text()")
        total_time = response.xpath(
            ".//td[6]/ul/li[3]/a[@class = 'tongtg']/b/text()")
        payments = response.xpath(
            ".//td[7]/ul/li[1][@class = 'giave']/text()")

        row_data = zip(company, journeys, times_per_day,
                       times_start, times_end, total_time, payments)

        # Making extracted data row wise
        for element in row_data:
            # Create a dictionary to store the scraped info
            scraped_info = {
                #key: value
                # element[0] means product in the list and so on, index tells what value to assign
                'Company': element[0],
                'Journeys': element[1],
                'Times_per_day': element[2],
                'Times_start': element[3],
                'Times_end': element[4],
                'Total_time': element[5],
                'Payment': element[6],
            }
            # Yield all data crawling from xpath in one tuple
            yield scraped_info

            NEXT_PAGE_SELECTOR = ".//tr[32]//a/@href"
            next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
            if next_page is not None:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )

# %%
