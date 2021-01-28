import re
import time
import requests
from bs4 import BeautifulSoup as b
#import numpy as np
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
#import pickle

#try to avoid copyright infringement
copyright=re.compile('[pP]rohibit(ed|s)')
full_text=re.compile('View entire text')
#start off at the beginning browse by title
base_url = 'https://quod.lib.umich.edu/e/eebo?cginame=text-idx;id=navbarbrowselink;key=title;page=browse'
base_soup = b(requests.get(base_url).text,'html.parser')
#navigate to the row of letters
first_hierarchy = base_soup.find_all(href=True,class_='browsenav_r1')
for i in first_hierarchy[:26]:
    #navigate to the row of subletters
    next_page = b(requests.get(i.attrs['href']).text,'html.parser')
    titlestart=next_page.find_all(href=True,class_='browsenav_r2')
    for j,k in enumerate(titlestart):
        if j>10:
            break
        time.sleep(1)
        current_page=b(requests.get(k.attrs['href']).text,'html.parser')
        #grab the list of browselistitem
        
        titles = current_page.find_all(class_='browsecell')
        for ii,jj in enumerate(titles):
            if ii > 20:
                break
            if ii%2==0:
                #alternates between year and link to book
                author_year = jj.text
            else:
                book = b(requests.get(jj.contents[0].attrs['href']).text,'html.parser')
                text = []
                if book.find(name='p',string=copyright) is not None:  #check the copyright area.
                    pass
                contents = book.find_all(class_='buttonlink')[-1].contents[0]
                time.sleep(1)
                page = b(requests.get(contents.attrs['href']).text,'html.parser')
                accept = page.find(name='a')
                actual = b(requests.get(accept.attrs['href']).text,'html.parser')
                for ss in actual.find_all(name='p',limit=4000):
                    text.append(ss.string)
                #write the text to a file
                with open(author_year.replace('.','').replace('/','')+'.txt','a+') as outfile:
                    for aa in text:
                        if aa is not None:
                            outfile.write(aa)
                            outfile.write('\n')
