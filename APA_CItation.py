import requests
from bs4 import BeautifulSoup
import datetime

#Use of headers to simulate actual browser
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

#List of webpages to be crawled
webpages = []

for webpage in webpages:
    source = requests.get(webpage, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    
    #get Content section from Meta Tag
    def get_content(string, limiter):
        index = string.find("content") + 9
        delta = 0
        for letter in string[index:]:
            if letter == limiter:
                break
            delta += 1
        return string[index:index+delta]
        
    #Name
    try:
        name = soup.find("meta", attrs = {"name" : "author"}) #cant use name as keyword argument as BeautifulSoup already assigned name argument
    except Exception:
        name = soup.find("meta", property = "article:author")
    
    try:
        name = get_content(str(name), '"')
        *first_middle, last = name.split()
        name = f"{last},"
        for fm in first_middle:
            name += f" {fm[0].upper()}."
    #In case if there is no author, retrieve name from webpage instead
    except Exception:
        index = 0
        for letter in webpage[12:]:
            if letter == ".":
                break
            index += 1
            name = webpage[12:12+index].upper()
    #Date
    #Returns date in RFC 3399
    dates = soup.find("meta", property = "article:published_time")
    
    if dates == None:
        dates = "n.d."
    else:
        dates = get_content(str(dates), 'T')
        dates = datetime.datetime.strptime(dates, "%Y-%m-%d")
        dates = dates.strftime("%Y, %B %d")
    #Article Name
    try:
        title = soup.title.text
    except Exception:
        title = "Please retrieve the title yourself!"
    
    print(f"""{name} ({dates}). {title}. Retrieved from
    {webpage}""")
    print()
