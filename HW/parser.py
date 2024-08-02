from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup




 # returns soup object
def retrieveURL(url):  
    html = urlopen(url)
    soup = BeautifulSoup(html.read(), 'html.parser')
    return soup


# <div class="col-md directory-listing"> indicates that the page lists faculty members
# <div class="fac-info">
def target_page(url,html,db):
    faculty = html.find('div',{'class':"fac-info"})   #this is the one!!!
    if faculty is not None:
        print("*****Target url******: ",url)
        storeFaculty(url,html,db)

        #print(faculty.get_text().strip("\n"))
        #return True
    #return False
    return faculty is not None

def storeFaculty(url,html,db):
    #<div class="col">
    doc_text = []
    left_column = html.find_all('div',{'class':'col'})
    right_column = html.find_all('div',{'class':'accolades'})
    for elem in left_column:
        doc_text.append(str(re.sub(r"[\xa0\n\t]", " ", elem.text)))
    for elem in right_column:
       doc_text.append(str(re.sub(r"[\xa0\n\t]", " ", elem.text)))
    doc = {"_id": url,
           "faculty_text": doc_text}
    
    db.delete_one({"_id":url})
    db.insert_one(doc)




# returns list of parsed urls 
def parse(html):
    possible_urls = html.find_all('a',href=True) 
    urls=[]
    for i in range(len(possible_urls)):
        possible_urls[i] = possible_urls[i].get('href')

    for url in possible_urls:
        if re.match(r'^ ?http',url):    #literally only one faculty website link starts with a whitespace char ugh 
            urls.append(url)   #should this be urljoin?
        elif re.match('^/',url):
            newURL = urljoin("https://www.cpp.edu",url)
            urls.append(newURL)
            #print("partial: ", url)
        else: 
            pass
    return urls    











