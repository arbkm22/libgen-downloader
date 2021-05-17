from bs4 import BeautifulSoup
import requests
import re

def titleFilter(title):
    title = title.split()
    while (len(title)>1):
        rf = re.findall(r"^[0-9,-]+[a-z]*$", string=title[-1], flags=re.IGNORECASE)
        if (len(rf) != 0):
            title.pop()
        else:
            break
    return " ".join(title)

print("Enter the name of the book: ", end='')
book = input()
print("Searching...")

url = f'http://libgen.rs/search.php?req={book}&open=0&res=25&view=simple&phrase=1&column=def'
source = requests.get(url)

soup = BeautifulSoup(source.text, 'lxml')
table = soup.find("table", class_="c")
tableRow = table.find_all("tr")
del tableRow[0]
if (len(tableRow)>1):
    for tr in range(len(tableRow)):
        tableContent = tableRow[tr].find_all("td")
        bookId = tableContent[0].text
        title = tableContent[2].find("a", id=bookId).text
        #title = ''.join([i for i in title if not i.isdigit()])
        title = titleFilter(title)
        author = tableContent[1].text.strip()
        link = tableContent[9].find("a")["href"]
        size = tableContent[7].text.strip()
        fileType = tableContent[8].text.strip()
        lang = tableContent[6].text.strip()

        print(title)

        """ print(f
            [{tr}]
            Title:      {title}
            Author:     {author}
            Language:   {lang}      Size:   {size}      Extension:   {fileType}
            Link:       {link}
            ) """
else:
    print("No Book Found")