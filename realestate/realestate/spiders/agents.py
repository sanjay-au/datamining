import scrapy


class AgentSpider(scrapy.Spider):
    name = 'agents'
    start_urls=['https://www.bhhsamb.com/bio/Agents']

    def parse(self, response):
            profile_links=response.css('a.cms-int-roster-card-image-container::attr(href)').getall()
            for links in profile_links:
                yield response.follow(links,self.parse_details)

    def parse_details(self,response):
        profile=response.css('section.rng-agent-profile').get()
        languages=profile.css('p.rng-agent-profile-languages::text').get()

        yield {
            'name':profile.css('p.rng-agent-profile-contact-name::text').get(),
            'job_title':profile.css('span.rng-agent-profile-contact-title::text').get(),
            'image_url':profile.css('img.rng-agent-profile-photo::attr(src)').get(),
            'address':profile.css('li.rng-agent-profile-contact-address::text').get(),
            'contact_details':{
                'phone':profile.css('i.rni-profile::text').get(),
                'website':profile.css('rng-agent-profile-contact-website.a::attr(href)').get(),
                'email':profile.css('rng-agent-profile-contact-email.a::attr(href)').get(),
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
            'languages':profile.css('p.rng-agent-profile-languages::text').get(),
            'description':''
        }
