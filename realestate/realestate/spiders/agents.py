import scrapy
from scrapy_splash import SplashRequest

class AgentSpider(scrapy.Spider):
    name = 'agents'
    script = """
        function main(splash, args)
            splash.images_enabled = false
            splash:go(args.url)
            splash:wait(2)
            local previous_height = 0
            local current_height = splash:evaljs("document.body.scrollHeight")
            local max_scrolls = 35
            local scrolls = 0
            
            -- simulate scrolling
            while scrolls < max_scrolls and current_height > previous_height do
                previous_height = current_height
                splash:runjs("window.scrollTo(0, document.body.scrollHeight);")
                splash:wait(2)
                current_height = splash:evaljs("document.body.scrollHeight")
                scrolls = scrolls + 1
            end
            return splash:html()
        end
        """
    def start_requests(self):
        url= 'https://www.bhhsamb.com/roster/Agents'
        yield SplashRequest(url=url,callback=self.parse,endpoint='execute',args={'lua_source':self.script,'timeout':90})
    def parse(self, response):
        profile_links=response.css('a.cms-int-roster-card-image-container.site-roster-card-image-link::attr(href)').getall()
        for links in profile_links:
            yield response.follow(links,self.parse_details)

    def parse_details(self,response):
        profile=response.css('section.rng-agent-profile')
        name=profile.css('p.rng-agent-profile-contact-name::text').get()
        name=name.strip()
        address=profile.css('ul.rng-agent-profile-contact li.rng-agent-profile-contact-address::text').getall()
        address="".join(address).strip()
        phone=profile.css('ul.rng-agent-profile-contact li.rng-agent-profile-contact-phone a::text').get()
        if phone:
            phone=phone.strip()
        else:
            phone=None
        website=profile.css('ul.rng-agent-profile-contact li.rng-agent-profile-contact-website a::attr(href)').get()
        email=profile.css('ul.rng-agent-profile-contact li.rng-agent-profile-contact-email a::attr(href)').get()
        description=profile.css('article.rng-agent-profile-content div p::text').get()
        facebook=profile.css('ul.rng-agent-profile-contact li.social-facebook a::attr(href)').get()
        twitter=profile.css('ul.rng-agent-profile-contact li.social-twitter a::attr(href)').get()
        linkedin=profile.css('ul.rng-agent-profile-contact li.social-linkedin a::attr(href)').get()
        youtube=profile.css('ul.rng-agent-profile-contact li.social-youtube a::attr(href)').get()
        pinterest=profile.css('ul.rng-agent-profile-contact li.social-pinterest a::attr(href)').get()
        instagram=profile.css('ul.rng-agent-profile-contact li.social-instagram a::attr(href)').get()
        language=profile.css('article.rng-agent-profile-main p.rng-agent-profile-languages::text').getall()
        if not language:
            language=None
        image=profile.css('article.rng-agent-profile-main img::attr(src)').get()

        yield {
            'name':name,
            'job_title':profile.css('span.rng-agent-profile-contact-title::text').get(),
            'image_url':image,
            'address':address,
            'contact_details':{
                'phone':phone,
                'website':website,
                'email':email,
            },
            'social_accounts':{
                'facebook':facebook,
                'twitter':twitter,
                'linkedin':linkedin,
                'youtube':youtube,
                'pinterest':pinterest,
                'instagram':instagram
            },
            # 'offices':[],    # no office address
            'languages':language,
            'description':description
        }
