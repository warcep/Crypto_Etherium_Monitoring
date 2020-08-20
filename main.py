#Version 84.0.4147.125 (Official Build) (64-bit) chrome 
#download the data of etherium and save the into csv file
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
        table_rows  = txn_hash_table.find_all('tr')

        webHeader =['Txn Hash','Block','Date Time (UTC)','DIFF','FROM','SELL','TO','VALUE','[TXN Fee]']
        allData=[]
        for tr in table_rows:
            td = tr.find_all('td')
            if len(td)!=0:
                allData.append([i.text for i in td])
        df = pd.DataFrame(allData)
        df.to_csv('filename.csv', index=False,header=webHeader,sep='\t')




    except Exception as Err:
        print('Error: ',Err)


if __name__ == '__main__':
    ether()