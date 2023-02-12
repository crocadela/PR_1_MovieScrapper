import scrapy
from scrapy.crawler import CrawlerProcess
import json
from scrapy.item import Item, Field
import time
import random

# Create spider
class movies_spider(scrapy.Spider):

    # Assign name to spider
    name = "movies_spider"

    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"
    ]
    
    # Output
    custom_settings = {
        'FEEDS': { 'data_wikiM.json': {'format': 'json', 'overwrite': True, 'encofing':'utf-8'}}
        }

          
    # Extract film info from first URL        
    def parse(self, response):
        for name in response.xpath('//table[@class="wikitable sortable"]//tr'):
            time.sleep(random.uniform(0.20, 0.70))
            # Was this movie the Best Film winner?
            if name.xpath('.//b').get() is not None:
                best_movie = True
            else:
                best_movie = False
            yield {
               'title': name.xpath('.//i//text()').get(),
               'year': name.xpath('(.//a)[2]/text()').get(),
               'best movie': best_movie,
               'awards': name.xpath('(./td)[3]/text()').get(),
               'nominations': name.xpath('(./td)[4]/text()').get(),
               'linkMovie': str(name.xpath('.//i//a/@href').get())
            }   
        
        # Iterate over each movie link
        for item in response.xpath('//table[@class = "wikitable sortable"]//i//a/@href'):
            time.sleep(random.uniform(0.20, 0.70))
            if item is not None:
                yield response.follow(item.get(), callback=self.parse_movies)
                
            
    def parse_movies(self, response):
        # Is this a documentary film?
        if response.xpath('//div[@class="catlinks"]') is None:
            documentary = None  
        elif response.xpath('//div[@class="catlinks"]//a[contains(text(), "documentary") or contains(text(), "Documentary")]').get() is not None:
            documentary = True
        else:
            documentary = False
        
        # Dict with movie name + link + documentary
        dict_movie = {'movie': response.xpath('//h1[@id="firstHeading"]/i/text()').get(),
                     'link': response.request.url, 
                      'documentary': documentary
                     }
        
                # Information we'll get
        response_type = ['Directed', 'Screenplay', 
                         'Starring', 'Produced', 
                         'Cinematography', 'Edited',
                         'Music', 'Production',
                         'Distributed', 'Release date',
                         'Running time', 'Countr',
                         'Language', 'Budget',
                         'Box office'
                        ]
        
        # Gather all response_type info in URL
        for tipo in response_type:
            path_template = '//table[@class="infobox vevent"]//th[contains(., "{}")]/following-sibling::td'.format(tipo)
            crew = []
            if response.xpath(path_template+'//ul').get() is not None:
                path_template = path_template+'//li'
            for name in response.xpath(path_template):
                crew.append(name.xpath('.//text()').get())
            dict_movie[tipo] = crew
            time.sleep(random.uniform(0.20, 0.70))

        # Yield full dictionary   
        yield dict_movie

        # Get all available URLs for the cast
        path_template = '//table[@class="infobox vevent"]//th[contains(text(), "Starring")]/following-sibling::td'
        if response.xpath(path_template+'//ul').get() is not None:
            path_template = path_template+'//li'
        
        for item in response.xpath(path_template+'//@href'):
            if item is not None:
                yield response.follow(item.get(), callback=self.parse_cast)
                time.sleep(random.uniform(0.20, 0.70))
                
            
     # Get cast details
    def parse_cast(self, response):
        time.sleep(random.uniform(0.20, 0.70))
        
        # Is this person a woman?
        females_sum = 0
        males_sum = 0
        female_list = ['" her "', '"Her "', 
                       '" she "', '"She "', 
                       '" female "', 
                       '" actress "', 
                       '" woman "']
        male_list = ['" his "', '"His "', 
                     '" he "', '"He "', 
                     '" male "', 
                     '" man "']
        
        if response.xpath('//div[@class="catlinks"]//a[contains(text(), "women") or contains(text(), "actresses") or contains(text(), "females")]').get() is not None:
            female = True
        elif response.xpath('//div[@class="catlinks"]//a[contains(text(), "men") or contains(text(), "actors") or contains(text(), "males")]').get() is not None:
            female = False 
        else:
            for e in response.xpath('//p'):
                for word_fem in female_list:
                    path = 'count(.//text()[contains(.,{})])'.format(word_fem)
                    females_sum = females_sum + float(e.xpath(path).get())
                    
                for word_male in male_list:
                    path = 'count(.//text()[contains(., {})])'.format(word_male)
                    males_sum = males_sum + float(e.xpath(path).get())

            if females_sum > males_sum:
                female = True
            elif females_sum < males_sum:
                female = False
            else:
                female = 'NA'
            
        yield {'name': response.xpath('//h1[@id="firstHeading"]//text()').get(),
               'female': female,
              'birthdate': response.xpath('//span[@class="bday"]/text()').get(),
               'birthplace': response.xpath('//div[@class="birthplace"]//text()').getall(),
               'link': response.request.url
              }
                     
            
if __name__ == "__main__":
# Crawler creation
  process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                    'DOWNLOAD_HANDLERS': {'s3': None},
                    'LOG_ENABLED': True
                })

# Crawler star
process.crawl(movies_spider)

# Launch spider
process.start()
