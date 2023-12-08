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


def get_book_price(soup):
    book_price_main = soup.find("div", class_="product_main")
    
    # Checking to see if there is any product_main div present
    if book_price_main:
        # Grabbing the paragraph where the price is located
        sub_book_price = book_price_main.find("p", class_="price_color")
        
        # Checking if the sub_book_price element is found
        if sub_book_price:
            # Extract and return the text content of the price element
            return sub_book_price.text.strip()
    
    # Return None if price element is not found
    return None


# ... (your existing code)

def get_book_details(soup):
    details = {}
    details_table = soup.find('table', class_='table table-striped')
    
    if details_table:
        rows = details_table.find_all('tr')
        
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            
            if header and data:
                # Extract text content, strip extra spaces, and replace unwanted characters
                row_key = header.text.strip()
                row_value = data.text.strip().replace('\u200e', '')
                details[row_key] = row_value
        
        return details
    
    # Return None if the details table is not found
    return None



def extract_book_info(url):
    book_info={}
    print(f"Scraping URL: {url}")
    html = get_page_html(url)
    
    # We will have to set up our soup inside of our main executable 
    soup = bs4.BeautifulSoup(html, "lxml")
    book_info["title"] = get_book_title(soup)
    print("Book Title:", book_info["title"])
    
    # I want to scrap the price 
    book_info["price"] = get_book_price(soup)
    print("Book Price:", book_info["price"])
    
    # I want to scrap the details
    book_info["details"] = get_book_details(soup)
    print("Book Details:", book_info["details"])

    return book_info 

# ... (your existing code)






if __name__ == "__main__":
    books_data = []
    with open("bookstore_products.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            books_data.append(extract_book_info(url))

    output_file_name = "output-{}.csv".format(
        datetime.today().strftime("%m-%d-%Y"))
    
    # Extracting the keys from the first book's details as column headings
    column_headings = list(books_data[0]["details"].keys())
    column_headings.insert(0, "Title")  # Adding the Title column
    column_headings.insert(1, "Price")  # Adding the Price column

    with open(output_file_name, 'w', newline='') as outputfile:
        writer = csv.writer(outputfile)
        
        # Writing the column headings to the CSV file
        writer.writerow(column_headings)
        
        for book in books_data:
            # Creating a list with values in the same order as column_headings
            row_values = [book["title"], book["price"]] + [book["details"].get(key, "") for key in column_headings[2:]]
            
            # Writing the row to the CSV file
            writer.writerow(row_values)
            
