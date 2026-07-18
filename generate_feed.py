import requests


urls = [
    "https://news.google.com/rss/search?q=site%3Arouleur.cc",
    "https://www.google.com/search?q=site%3Arouleur.cc",
]


for url in urls:

    print("\nTEST:", url)

    try:

        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        print("STATUS:", r.status_code)
        print(r.text[:1000])


    except Exception as e:

        print("ERRORE:", e)
