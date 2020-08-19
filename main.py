#Version 84.0.4147.125 (Official Build) (64-bit) chrome 
#ctrl k c / ctrl k u
import cfscrape
from bs4 import BeautifulSoup
import pandas as pd

def ether():
    try:
        scraper = cfscrape.create_scraper()
        fullDataScraped = scraper.get('https://etherscan.io/address/0xded17acd827814ab885bf993aa25e84f9ca62cab?fbclid=IwAR2jOXgMemNif20ynFgfxW9f_yvqB5RHLmY2Dk_JIcJjRFd_RD1sK_99fMY.com').content
        soup = BeautifulSoup(fullDataScraped,'html.parser')

        txn_hash_table = soup.table
        table_rows = txn_hash_table.find_all('tr')
        
         for tr in table_rows:
             td = tr.find_all('td') 
             row= [i.text for i in td]
             print(row)
        
        #pt=pd.DataFrame(table_rows,index=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
        #print(table_rows)

    except Exception as Err:
        print('Error: ',Err)



if __name__ == '__main__':
    ether()