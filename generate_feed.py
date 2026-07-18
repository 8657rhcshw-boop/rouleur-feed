import requests


urls = [
    "https://www.rouleur.cc/news-sitemap.xml?output=1",
    "https://www.rouleur.cc/sitemap-news.xml",
    "https://www.rouleur.cc/sitemap_index.xml",
    "https://www.rouleur.cc/wp-sitemap.xml"
]


for url in urls:

    print("\nTEST:", url)

    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        print("STATUS:", r.status_code)
        print(r.text[:200])

    except Exception as e:
        print("ERRORE:", e)
