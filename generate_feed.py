import requests


URL = "https://www.rouleur.cc/news-sitemap.xml"


headers = {
    "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
}


response = requests.get(
    URL,
    headers=headers,
    timeout=30
)


print(
    "STATUS:",
    response.status_code
)


print(
    response.text[:2000]
)
