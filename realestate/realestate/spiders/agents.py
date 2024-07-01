import scrapy
from scrapy_splash import SplashRequest

class AgentSpider(scrapy.Spider):
    name = 'agents'
    script = """
        function main(splash,args)
            local num_scrolls = 10
            local scroll_delay = 1
            
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)
            
            for _ = 1, num_scrolls do
                scroll_to(0, get_body_height())
                splash:wait(scroll_delay)
            end        
            return splash:html()
        end
        """
    def start_requests(self):
        url= 'https://www.bhhsamb.com/roster/Agents'
        yield SplashRequest(url=url,callback=self.parse,endpoint='execute',args={'lua_source':self.script,'wait':10000000})
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
        phone=phone.strip()
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
