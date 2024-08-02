from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import parser

import datetime
import re


def storePage(url,html,db):
    # checks for duplicate urls
    page_exists = db.find_one({'_id': url})
    if not page_exists:
        doc = {"_id": url,
           "html": str(html)}
        db.insert_one(doc)

    


# crawl thread procedure from template 
def crawl(db,frontier,num_targets):
    targets_found = 0
    while not frontier.done():
        try:
            url = frontier.nextURL()
            #print("current: ",url)
            html = parser.retrieveURL(url)
            storePage(url,html,db)
            if parser.target_page(url,html,db):
                targets_found +=1
                #storeFaculty(url,html)  #maybe this should be in the parser so the crawl thread is exactly like the template
            if targets_found == num_targets:
                print("All targets found for department.")
                frontier.clear()
            else:
                urls = parser.parse(html)
                for url in urls:
                    if url not in frontier.getQueue():
                        frontier.addURL(url)

        except HTTPError as e:
            print({e})
        except Exception as e:
            print({e})
              
        


