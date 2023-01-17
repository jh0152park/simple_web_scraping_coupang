import requests
import re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
coupang = "https://www.coupang.com/"

for i in range(1, 6):
    url = "https://www.coupang.com/np/search?q=%EB%A7%A5%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=" + str(
        i) + "&rocketAll=false&searchIndexingToken=1=6&backgroundColor="
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("li", attrs={"class": re.compile("^search-product")})
    for item in items:
        product = item.find("div", attrs={"class": "name"}).get_text()
        ad = item.find("span", attrs={"class": "ad-badge-text"})
        pattern = re.compile("^Apple")

        if ad:
            # print(f"{product} 해당 제품은 광고 제품 으로, 확인하지 않고 넘어갑니다.\n")
            continue

        if pattern.match(product):
            price = item.find("strong", attrs={"class": "price-value"})
            price = price.get_text() if price else "None"
            if price == "None":
                continue

            rate = item.find("em", attrs={"class": "rating"})
            rate = rate.get_text() if rate else "0.0"

            rate_count = item.find("span", attrs={"class": "rating-total-count"})
            rate_count = rate_count.get_text()[1:-1] if rate_count else "0"

            link = item.find("a", attrs={"class": "search-product-link"})["href"]

            if int(price.replace(",", "")) <= 2500000 and float(rate) >= 4.5 and int(rate_count) >= 1500:
                print(f"product : {product}\nprice : {price}\nrate : {rate} / {rate_count}")
                print("link : {}\n".format(coupang + link))
