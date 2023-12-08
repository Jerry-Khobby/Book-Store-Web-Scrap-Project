from datetime import datetime
import requests
import csv 
import bs4


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
REQUEST_HEADER = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.5",
}

# defining the function for getting the html
def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

# I want to first scrap the name of the book 
def get_book_title(soup):
    book_title = soup.find("div", class_="product_main")
    
    if book_title:
        title_element = book_title.find("h1")
        
        try:
            book_name = title_element.text.strip()
            return book_name
        except AttributeError as e:
            print(f"Error extracting book name: {e}")
    
    return None

def get_book_price(soup):
    book_price_main = soup.find("div", class_="product_main")
    
    if book_price_main:
        sub_book_price = book_price_main.find("p", class_="price_color")
        
        if sub_book_price:
            return sub_book_price.text.strip()
    
    return None

def get_book_details(soup):
    details = {}
    details_table = soup.find('table', class_='table table-striped')
    
    if details_table:
        rows = details_table.find_all('tr')
        
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            
            if header and data:
                row_key = header.text.strip()
                row_value = data.text.strip().replace('\u200e', '')
                details[row_key] = row_value
        
        return details
    
    return None

def extract_book_info(url):
    book_info = {}
    print(f"Scraping URL: {url}")
    html = get_page_html(url)
    
    soup = bs4.BeautifulSoup(html, "lxml")
    book_info["title"] = get_book_title(soup)
    print("Book Title:", book_info["title"])
    
    book_info["price"] = get_book_price(soup)
    print("Book Price:", book_info["price"])
    
    book_info["details"] = get_book_details(soup)
    print("Book Details:", book_info["details"])

    return book_info 

if __name__ == "__main__":
    books_data = []
    with open("bookstore_products.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            books_data.append(extract_book_info(url))

    output_file_name = "output-{}.csv".format(
        datetime.today().strftime("%m-%d-%Y"))
    
    with open(output_file_name, 'w', newline='', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)

        # Writing the common columns (Title, Price, and all keys from details)
        common_columns = ["Title", "Price"] + list(books_data[0]["details"].keys())
        writer.writerow(common_columns)

        # Writing data for each book
        for book in books_data:
            # Writing common data (Title, Price)
            row_values = [book["title"], book["price"]]

            # Writing details data
            for key in common_columns[2:]:
                row_values.append(book["details"].get(key, ""))

            # Writing the row to the CSV file
            writer.writerow(row_values)
