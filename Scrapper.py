import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_all_stoic_quotes():
    quotes_data = []
    page = 1
    base_url = "https://www.goodreads.com/quotes/tag/stoicism?page={}"

    while True:
        print(f"Scraping page {page}...")
        url = base_url.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        quotes = soup.find_all("div", class_="quote")
        if not quotes:
            print(f"No more quotes found. Scraping complete. Total pages scraped: {page - 1}")
            break

        for quote in quotes:

            text_element = quote.find("div", class_="quoteText")
            text = text_element.get_text(separator=" ").strip().split("―")[0].strip().replace("\n", " ") if text_element else "N/A"


            author_tag = text_element.find("span", class_="authorOrTitle") if text_element else None
            author = author_tag.get_text(strip=True) if author_tag else "Unknown"


            book_tag = text_element.find("a", class_="authorOrTitle") if text_element else None
            book = book_tag.get_text(strip=True) if book_tag else "N/A"


            tag_section = quote.find("div", class_="greyText smallText left")
            tags = [tag.get_text(strip=True) for tag in tag_section.find_all("a")] if tag_section else []

            quotes_data.append({
                "Quote": text,
                "Author": author,
                "Book": book,
                "Tags": ", ".join(tags)
            })

        page += 1
        time.sleep(2)  


    df = pd.DataFrame(quotes_data)
    print(f"Scraped {len(df)} quotes across all pages.")
    df.to_csv("stoic_quotes_full.csv", index=False)
    print("Dataset saved as 'stoic_quotes_full.csv'.")

scrape_all_stoic_quotes()