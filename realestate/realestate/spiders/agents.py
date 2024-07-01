import scrapy
from scrapy_splash import SplashRequest

class AgentSpider(scrapy.Spider):
    name = 'agents'
    script = """
        function main(splash)
            local scroll_delay = 10
            local num_scrolls = 100

            splash:set_viewport_full()

            for _ = 1, num_scrolls do
                splash:runjs("window.scrollTo(0, document.body.scrollHeight);")
                splash:wait(scroll_delay)
            end

            return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
            }
        end
        """

    def start_requests(self):
        url= 'https://www.bhhsamb.com/roster/Agents'
        yield SplashRequest(url=url,callback=self.parse,args={'lua_source':self.script,'timeout':90})
    def parse(self, response):
        profile_links=response.css('a.cms-int-roster-card-image-container.site-roster-card-image-link::attr(href)').getall()
        for links in profile_links:
            yield response.follow(links,self.parse_details)

    def parse_details(self,response):
        profile=response.css('section.rng-agent-profile')

        yield {
            'name':profile.css('p.rng-agent-profile-contact-name::text').get(),
            'job_title':profile.css('span.rng-agent-profile-contact-title::text').get(),
            # 'image_url':profile.css('img.rng-agent-profile-photo::attr(src)').get(),
            'address':profile.css('li.rng-agent-profile-contact-address::text').get(),
            'contact_details':{
                'phone':profile.css('i.rni-profile::text').get(),
                'website':profile.css('rng-agent-profile-contact-website.a::attr(href)').get(),
                'email':profile.css('rng-agent-profile-contact-email.a::attr(href)').get(),
            },
            # 'social_accounts':{
            #     'facebook':'',
            #     'twitter':'',
            #     'linkedin':'',
            #     'youtube':'',
            #     'pinterest':'',
            #     'instagram':''
            # },
            # 'offices':[],
            # 'languages':profile.css('p.rng-agent-profile-languages::text').get().strip(),
            'description':profile.xpath('//*[@id="body-text-1-preview-5500-4559646"]/text()').get()
        }
