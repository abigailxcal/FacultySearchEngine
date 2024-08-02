from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import parser
from pymongo import MongoClient
import re
# should connecting to db be here or parser or main??????/
def connectDataBase():
    DB_NAME = "Project"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

#db = connectDataBase()
#documents = db.documents

def storePage(url,html):
    #print("Non-faculty: ", url)
    doc = {"_id": url,
           "html": html}
    #documents.insert_one(doc)

def storeFaculty(url,html):
    print("Faculty: ",url)
    name = html.find('h1').text
    print("Name: ",name)
    #<div class="col">
    #span3 fac rightcol
    left_column = html.find_all('div',{'class':'col'})
    right_column = html.find_all('div',{'class':'accolades'})
    doc_text = []
    for elem in left_column:
        #print(elem.text.strip('\n'))
        doc_text.append(re.sub(r"[\xa0\n\t]", " ", elem.text))

    for elem in right_column:
        #print(elem.text.strip('\n'))
       doc_text.append(re.sub(r"[\xa0\n\t]", " ", elem.text))
    for text in doc_text:
        print(text)
    headers = html.find_all('h2')
    print("*******find_all.h2: ",headers)

    doc = {"_id": url,
           "html": html}
    
    #documents.delete_one
    #documents.update_one(doc)
    #delete doc and add new doc



# crawl thread procedure from template 
def crawl(frontier,num_targets):
    links_visited = []
    targets_found = 0
    while not frontier.done():
        try:
            url = frontier.nextURL()
            links_visited.append(url)
            #print("current: ",url)
            html = parser.retrieveURL(url)
            storePage(url,html)

            # ----insert storePage() here----

            if parser.target_page(html):
                targets_found +=1
                storeFaculty(url,html)
                #store faculty method
            else: 
                
            if targets_found == num_targets:
                frontier.clear()
            else:
                urls = parser.parse(html)
                for url in urls:
                    if url not in links_visited and url not in frontier.getQueue():
                        frontier.addURL(url)

        except HTTPError as e:
            print({e})
        except Exception as e:
            print({e})
              
        


