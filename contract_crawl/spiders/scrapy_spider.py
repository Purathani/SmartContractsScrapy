import scrapy

import requests
import json
from urllib.request import urlopen, Request
import urllib
from .google_url_shortner import GooglException
import os

class ContractsSpider(scrapy.Spider):
    name = 'contracts'
    allowed_domains = ['www.etherscan.io', 'goo.gl', 'www.googleapis.com']
    #start_urls = ['https://etherscan.io/contractsVerified']

    def start_requests(self):
        #Loop for all pages in the table of verified smart contracts in EtherScan
        
        urls = ['https://etherscan.io/contractsVerified/' + format(i) for i in range(1, 1170, 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        address = response.css('.address-tag::text').extract()
       
        #Give the extracted content row wise
        #for item in zip(address):
        for addr in address:
            #create a dictionary to store the scraped info
            #scraped_info = {
            #    'address' : item[0]
            #}

            #yield or give the scraped info to scrapy
            #yield scraped_info
            
            contract_url = 'https://etherscan.io/address/' +  addr + '#code'

            url = [contract_url]
            
            next_page = str(url)
            print('next page is ', next_page)

            obj = GooglException(next_page)
            print(print(obj.shortenURL('https://www.google.com.au')))
            short = self.goo_shorten_url_2('https://www.google.com.au/')
            short_url = 'https://' + str(short)
            print(short_url)
            
            #yield scrapy.Request('https://goo.gl/F3dWxM', self.parse_contract, dont_filter=True, meta={'address': addr})
            yield scrapy.Request(short_url, self.parse_contract, dont_filter=True, meta={'address': addr})

            #scraped_info = {
            #    'address' : addr,
            #    'content' : next_page
            #}
           
            #yield scraped_info
        
        
        here = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(here, 'shorturl.txt')
        self.read_url_text_file(filename)
        # Open the file with read only permit


        f = open(filename)
        line = f.readline()

        lines = list(f)
       
        for li in lines:
            print(li)
            yield scrapy.Request(li.strip(), self.parse_short_url, dont_filter=True)

        f.close() 


    def read_url_text_file(self, text_file):
        # Open the file with read only permit
        f = open(text_file)
        # use readline() to read the first line 
        line = f.readline()
        

        # use the read line to read further.
        # If the file is not empty keep reading one line
        # at a time, till the file is empty
        while line:
            shorturl = line
            yield scrapy.Request(shorturl, self.parse_short_url, dont_filter=True)
            # use realine() to read next line
            line = f.readline()
        f.close() 

    def parse_short_url(self, response):
        #Extracting the content using css selectors
        print('test1')
        content = response.xpath('//div[@id ="verifiedbytecode2"]/text()').extract_first(default='not-found') # To get bytecode
        #content = response.css('.js-sourcecopyarea::text').extract() # To get source code
        #content = response.css('.wordwrap::text').extract() # To get abi code
        print('after short url parse')

        scraped_info = {
            'content' : content
        }
        yield scraped_info


    def parse_contract(self, response):
        #Extracting the content using css selectors
        print('test1')
        address = response.meta['address']
        content = response.xpath('//div[@id ="verifiedbytecode2"]/text()').extract_first(default='not-found')
        #content = response.css('.address-tag::text').extract()
        print('after parse')
        print('parse address' , address)
                
        scraped_info = {
            'address' : address,
            'content' : content
        }
        yield scraped_info

    #function to shorten the url
    def urlShotern(self, url):
        key="AIzaSyDZ969uwlIruVDkkijIFqtCQppnCcGvqa8" # replace with your api key
        gurl="https://www.googleapis.com/urlshortener/v1/url"
        data={}
        data['longUrl']=url
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(gurl, data=data_json, headers=headers)
        a=response.json()
        print(a)
        return a['id']

    def goo_shorten_url(self, url):
        key="AIzaSyDZ969uwlIruVDkkijIFqtCQppnCcGvqa8" # replace with your api key
        post_url = 'https://www.googleapis.com/urlshortener/v1/url'+key
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        print (r.text)

    def goo_shorten_url_2(self, url):
        d = dict(parameter1="value1", parameter2="value2")
        data = urllib.parse.urlencode(d).encode("utf-8")

        post_url = 'https://www.googleapis.com/urlshortener/v1/url'
        postdata = {'longUrl':url}
        headers = {'Content-Type':'application/json'}
        req = Request(
            post_url,
            json.dumps(postdata),
            headers
        )
        ret = urlopen(req, data=data).read()
        print(ret)
        return json.loads(ret)['id']
