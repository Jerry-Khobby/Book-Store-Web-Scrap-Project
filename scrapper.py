from datetime import datetime
import requests
import csv 
import bs4


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
REQUEST_HEADER = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.5",
}

#defining the function for getting the html
def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content


#I want to first scrap the name of the book 
#  
def get_book_title(soup):
    # Find the first occurrence of the div with the class product_main 
    book_title = soup.find("div", class_="product_main")
    
    # Once it finds the first occurrence div, I will search again for the h1 tag and grab the title 
    if book_title:
        # Find the h1 tag within the book_title div 
        title_element = book_title.find("h1")
        
        try:
            # Try to extract and return the book name
            book_name = title_element.text.strip()
            return book_name
        except AttributeError as e:
            # Handle the case where title_element or its text attribute is None
            print(f"Error extracting book name: {e}")
    
    # Return None if book title is not found
    return None

def extract_book_info(url):
    book_info={}
    print(f"Scraping URL: {url}")
    html = get_page_html(url)
    
    # We will have to set up our soup inside of our main executable 
    soup = bs4.BeautifulSoup(html, "lxml")
    book_info["title"] = get_book_title(soup)
    print("Book Title:", book_info["title"])




if __name__ == "__main__":
    books_data = []
    with open("bookstore_products.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            books_data.append(extract_book_info(url))
            # I am breaking in order to stop on just the first URL 
            #break
