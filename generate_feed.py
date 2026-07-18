print("FILE GIUSTO ESEGUITO")

from playwright.sync_api import sync_playwright

print("PLAYWRIGHT IMPORT OK")


with sync_playwright() as p:
    print("PLAYWRIGHT AVVIATO")

print("FINE")
