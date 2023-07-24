import scrapy
from bs4 import BeautifulSoup

def extract_number_from_string(s):
    # Helper function to extract numeric part from a string
    return float("".join(filter(str.isdigit, s)))

class ShoppingSpider(scrapy.Spider):
    name = 'shopping_spider'
    start_urls = ['https://www.google.com/search?q=nike+shoes&tbm=shop&gl=us']

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        ads = []
        for el in soup.select(".sh-np__click-target"):
            ad = {
                "title": el.select_one(".sh-np__product-title").get_text() if el.select_one(".sh-np__product-title") else None,
                "link": "https://google.com" + el.get("href"),
                "source": el.select_one(".sh-np__seller-container").get_text() if el.select_one(".sh-np__seller-container") else None,
                "price": el.select_one(".hn9kf").get_text() if el.select_one(".hn9kf") else None,
                "delivery": el.select_one(".U6puSd").get_text() if el.select_one(".U6puSd") else None,
            }
            extensions = el.select_one(".rz2LD")
            if extensions:
                ad["extensions"] = extensions.get_text()
            ads.append(ad)

        for ad in ads:
            ad.pop("", None)

        shopping_results = []
        for el in soup.select(".sh-dgr__gr-auto"):
            result = {
                "title": el.select_one("h3.tAxDx").get_text() if el.select_one("h3.tAxDx") else None,
                "link": el.select_one(".zLPF4b .eaGTj a.shntl")["href"][el.select_one("a.shntl")["href"].index("=") + 1:] if el.select_one(".zLPF4b .eaGTj a.shntl") else None,
                "source": el.select_one(".IuHnof").get_text().replace(".aULzUe{.*?}.aULzUe::after{.*?}", "") if el.select_one(".IuHnof") else None,
                "price": el.select_one(".XrAfOe .a8Pemb").get_text() if el.select_one(".XrAfOe .a8Pemb") else None,
                "rating": None,
                "reviews": None,
                "delivery": el.select_one(".vEjMR").get_text() if el.select_one(".vEjMR") else None,
            }
            rating_element = el.select_one(".NzUzee .QIrs8")
            if rating_element:
                rating_text = rating_element.get_text().strip()
                if "out" in rating_text:
                    try:
                        result["rating"] = float(rating_text.split("out")[0].strip())
                        result["reviews"] = extract_number_from_string(rating_text)
                    except ValueError:
                        pass

            extensions = el.select_one(".Ib8pOd")
            if extensions:
                result["extensions"] = extensions.get_text()
            shopping_results.append(result)

        for result in shopping_results:
            result.pop("", None)

        yield {
            "ads": ads,
            "shopping_results": shopping_results
        }
