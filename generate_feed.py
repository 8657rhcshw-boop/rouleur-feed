import requests


urls = [
    "https://www.rouleur.cc/feed",
    "https://www.rouleur.cc/rss",
    "https://www.rouleur.cc/blog/rss.xml",
    "https://www.rouleur.cc/news/rss.xml"
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

        print(r.text[:300])


    except Exception as e:

        print("ERRORE:", e)
