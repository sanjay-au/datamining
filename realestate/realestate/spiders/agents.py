import scrapy


class AgentSpider(scrapy.Spider):
    name = 'agents'
    start_urls=['https://www.bhhsamb.com/bio/Agents']

    def parse(self, response):
        for ag in response.css('a.cms-int-roster-card-image-container.site-roster-card-image-link').attrib['href']:
            details=response.css('section.rng-agent-profile.bio1')
            yield {
                'name':'',
                'job_title':'',
                'image_url':'',
                'address':'',
                'contact_details':{
                    'Office':'',
                    'Cell':'',
                    'Fax':'',
                },
                'social_accounts':{
                    'facebook':'',
                    'twitter':'',
                    'linkedin':'',
                    'youtube':'',
                    'pinterest':'',
                    'instagram':''
                },
                'offices':[],
                'languages':'',
                'description':''
            }
