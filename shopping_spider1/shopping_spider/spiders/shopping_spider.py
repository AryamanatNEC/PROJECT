import scrapy
import json

class GoogleShoppingSpider(scrapy.Spider):
    name = 'google_shopping'
    allowed_domains = ['google.com']

    def __init__(self, search_query=None, *args, **kwargs):
        super(GoogleShoppingSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.google.com/search?q={self.format_search_query(search_query)}&tbm=shop&gl=ind']

    def format_search_query(self, search_query):
        formatted_query = search_query.replace("'", '').lower().replace('"', '').replace(' ', '+')
        return formatted_query

    def parse(self, response):
        ads_data = []
        shopping_results_data = []

        for el in response.css(".sh-np__click-target"):
            ad = {
                "title": el.css(".sh-np__product-title::text").get(),
                "link": "https://google.com" + el.css("::attr(href)").get(),
                "source": el.css(".sh-np__seller-container::text").get(),
                "price": el.css(".hn9kf::text").get(),
                "delivery": el.css(".U6puSd::text").get(),
            }
            extensions = el.css(".rz2LD::text").get()
            if extensions:
                ad["extensions"] = extensions
            ads_data.append(ad)

        for el in response.css(".sh-dgr__gr-auto"):
            result = {
                "title": el.css("h3.tAxDx::text").get(),
                "link": el.css(".zLPF4b .eaGTj a.shntl::attr(href)").get()[el.css("a.shntl::attr(href)").get().index("=") + 1:],
                "source": el.css(".IuHnof::text").get().replace(".aULzUe{.*?}.aULzUe::after{.*?}", "") if el.css(".IuHnof::text").get() else None,
                "price": el.css(".XrAfOe .a8Pemb::text").get(),
                "rating": None,
                "reviews": None,
                "delivery": el.css(".vEjMR::text").get(),
            }

            rating_element = el.css(".NzUzee .QIrs8")
            if rating_element:
                rating_text = rating_element.css("::text").get().strip()
                if "out" in rating_text:
                    try:
                        result["rating"] = float(rating_text.split("out")[0].strip())
                        result["reviews"] = self.extract_number_from_string(rating_text)
                    except ValueError:
                        pass

            extensions = el.css(".Ib8pOd::text").get()
            if extensions:
                result["extensions"] = extensions
            shopping_results_data.append(result)

        for ad in ads_data:
            ad.pop("", None)

        for result in shopping_results_data:
            result.pop("", None)

        yield {
            "ads_data": ads_data,
            "shopping_results_data": shopping_results_data
        }

    def extract_number_from_string(self, s):
        parts = s.split()
        for i in range(len(parts)):
            if parts[i] == 'stars.':
                return parts[i+1]
