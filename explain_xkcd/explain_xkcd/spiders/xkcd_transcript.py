import scrapy
import string

class XKCD_transcript(scrapy.Spider):
    name = "XKCD_transcript"
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "BOT_NAME":'inv',
#        "DEPTH_LIMIT":'3',
        "ROBOTSTXT_OBEY":False}

#scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=2014'
#scrapy crawl XKCD_transcript -o xkcd_transcript.json

    def start_requests(self):        
        start_url = "http://www.explainxkcd.com/wiki/index.php/1"
        yield scrapy.Request(url=start_url, callback = self.getComics)

    def getComics(self, response):
        comic_name = response.xpath('//h1[@id="firstHeading"]/span/text()').extract_first()
        flag = False
#        for trow in response.xpath('//div[@id="mw-content-text"]/dl'):
        for trow in response.xpath('//div[@id="mw-content-text"]/*'):
            if(flag == False):
                try:
                    flag = trow.xpath('./span/@id').extract_first() == 'Transcript'
                except:
                    continue
            else:
                try:
                    transcript_line = trow.xpath('./dd/text()').extract()
                    if(transcript_line):
                        yield {comic_name :[comic_name, transcript_line]}
                except:
                    continue
        for trow2 in response.xpath('//ul/li/a'):
            try:
                if(trow2.xpath('.//span/text()').extract_first()[:-2]=="Next"):
                    next_url = trow2.xpath('.//@href').extract_first()
                    yield scrapy.Request(url='http://www.explainxkcd.com' + next_url, callback = self.getComics)
            except:
                continue