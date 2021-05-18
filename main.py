from bs4 import BeautifulSoup
import requests
import re
from os import system, name

def clear():
    if name == "nt":
        _ = system('cls')
    else:
        _ = system('clear')

# Title filter, removes the ISBN no. from title
def titleFilter(title):
    title = title.split()
    while (len(title)>1):
        rf = re.findall(r"^[0-9,-]+[a-z]*$", string=title[-1], flags=re.IGNORECASE)
        if (len(rf) != 0):
            title.pop()
        else:
            break
    return " ".join(title)

# Download link grabber
def dlLinkGrabber(link):
    dlSource = requests.get(link)
    dlSoup = BeautifulSoup(dlSource.text, "lxml")
    dlSource = dlSoup.find("div", id="download")
    dlLink = dlSource.find("a")["href"]
    return dlLink

print("Enter the name of the book: ", end='')
book = input()
print("Searching...")

url = f'http://libgen.rs/search.php?req={book}&open=0&res=25&view=simple&phrase=1&column=def'
source = requests.get(url)

soup = BeautifulSoup(source.text, 'lxml')
table = soup.find("table", class_="c")
tableRow = table.find_all("tr")
pageList = []
del tableRow[0]
if (len(tableRow)>1):
    for tr in range(len(tableRow)):
        tableContent = tableRow[tr].find_all("td")
        bookId = tableContent[0].text
        title = tableContent[2].find("a", id=bookId).text
        title = titleFilter(title)
        author = tableContent[1].text.strip()
        link = tableContent[9].find("a")["href"]
        #link = dlLinkGrabber(link)
        size = tableContent[7].text.strip()
        fileType = tableContent[8].text.strip()
        lang = tableContent[6].text.strip()
        data = {"title": title,
                "author": author,
                "lang": lang,
                "size": size,
                "ext": fileType,
                "link": link}
        pageList.append(data)

    page = 0
    flag = False
    while (page < len(pageList)):
        data = pageList[page]
        if (page%5==0) and flag:
            print("Choose an option to perform")
            print("d - download")
            print("p - previous")
            print("n - next")
            print("q - quit")
            opt = input("--> ")
            if opt in ["N", "n", "next"]:
                clear()
                page += 1
            elif opt in ["P", "p", "previous"]:
                clear()
                page -= 9
            elif opt in ["Q", "q", "quit"]:
                print("Quiting...")
                exit()
        else:
            page += 1
            flag = True
        print(f""" 
[{page}] {data["title"]}
Author:   {data["author"]}  
Language: {data["lang"]} Size: {data["size"]} Extension: {data["ext"]}        
""")
        page = abs(page % len(pageList))

else:
    print("No Book Found")