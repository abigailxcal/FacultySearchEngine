import crawler
import frontier
from pymongo import MongoClient

'''
What still needs to be done:
- scrape data from faculty websites and store/index into database
- allow for user queury 
- see if crawler works for business seed url

'''


def connectDataBase():
    DB_NAME = "Project_Test"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

def main():
    #SEED ='https://www.cpp.edu/sci/biological-sciences/index.shtml'
    #SEED = 'https://www.cpp.edu/engineering/ce/index.shtml'
    #SEED = 'https://www.cpp.edu/engineering/ce/faculty.shtml'
    #SEED = 'https://www.cpp.edu/cba/international-business-marketing/faculty-staff/index.shtml'
    faculty_index_links = ['https://www.cpp.edu/sci/biological-sciences/faculty/index.shtml',
                           'https://www.cpp.edu/cba/international-business-marketing/faculty-staff/index.shtml',
                           'https://www.cpp.edu/engineering/ce/faculty.shtml'
                           ]
    num_targets = 5
    request_queue = frontier.Frontier()
    db = connectDataBase()
    documents = db.documents
    for SEED in faculty_index_links:
        request_queue.addURL(SEED)
        crawler.crawl(documents,request_queue,num_targets)


if __name__ == '__main__':
    main()


