from bs4 import BeautifulSoup
import requests
import re
from os import system, name
import os, sys
from tqdm import tqdm
from pathlib import Path

# Self-explanatory
def clear():
    if name == "nt": # For windows
        _ = system('cls')
    else: 
        _ = system('clear') # For Linux/MacOS

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

def downloader(link, fileName):
    print(f"Downloading book {fileName}")
    homePath = Path.home()
    subPath = "tmp"
    fileSize = int(requests.head(link).headers["Content-Length"])
    os.makedirs(os.path.join(homePath, subPath), exist_ok=True)
    dlPath = os.path.join(homePath, subPath, fileName)
    chunkSize = 1024
    with requests.get(link, stream=True) as r, open(dlPath, "wb") as f, tqdm(
        unit = "B",  # unit string to be displayed.
        unit_scale = True,  # let tqdm to determine the scale in kilo, mega..etc.
        unit_divisor = 1024,  # is used when unit_scale is true
        total = fileSize,  # the total iteration.
        file = sys.stdout,  # default goes to stderr, this is the display on console.
        desc = fileName  # prefix to be displayed on progress bar.
) as progress:
        for chunk in r.iter_content(chunk_size=chunkSize):
            dataSize = f.write(chunk)
            progress.update(dataSize)
    print(f"File downloaded at {dlPath}")

print("Enter the name of the book: ", end='')
book = input()
print("Searching...")

url = f'http://libgen.rs/search.php?req={book}&open=0&res=25&view=simple&phrase=1&column=def'
source = requests.get(url)

soup = BeautifulSoup(source.text, 'lxml')
table = soup.find("table", class_="c")
tableRow = table.find_all("tr")
pageList = []
downloadLinksRef = []
fileNameRef = []
del tableRow[0]
if (len(tableRow)>1):
    for tr in range(len(tableRow)):
        tableContent = tableRow[tr].find_all("td")
        bookId = tableContent[0].text
        title = tableContent[2].find("a", id=bookId).text
        title = titleFilter(title)
        fileNameRef.append(title)
        author = tableContent[1].text.strip()
        link = tableContent[9].find("a")["href"]
        downloadLinksRef.append(link)
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
            if opt in ["D", "d", "download"]:
                num = int(input("Enter book no.-> "))
                try:
                    linkGen = downloadLinksRef[num-1]
                except Exception as e:
                    print("Please enter a valid number!")
                else:
                    print("Please wait...")
                    linkGen = dlLinkGrabber(linkGen)
                    downloader(linkGen, fileNameRef[num-1])
                    exit()
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