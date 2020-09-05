import cfscrape
from bs4 import BeautifulSoup
import pandas as pd
import base64
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import html_email_template
import SENDGRID_API_KEY

def check_ether():
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
        new_CSV_DATA = pd.DataFrame(allData)
        old_CSV_DATA = pd.read_csv('data/Etherium_Website_Data.csv',sep='\t')
        
        new_CSV_DATA_tuple = [tuple(x) for x in new_CSV_DATA.values]
        old_CSV_DATA_tuple = [tuple(x) for x in old_CSV_DATA.values]

        for i in range(0,len(new_CSV_DATA_tuple)):
            data_the_same=False
            for j in range(0,len(old_CSV_DATA_tuple)):
                if str(new_CSV_DATA_tuple[i][1]) == str(old_CSV_DATA_tuple[j][1]):   #1 its the column of Block number (like ID)
                    data_the_same=True
            if data_the_same==False: #for diff in database its mean that we want to save new DB & send notification via  about changes
                new_CSV_DATA.to_csv('data/Etherium_Website_Data.csv', index=False,header=webHeader,sep='\t')
                send_notification()
                print("discrepancy in data - notification will be send")
                break

    except Exception as e:
        print('Error to check: ',e)

def send_notification():
    try:
        message = Mail(
            from_email='warcep@gmail.com',
            to_emails='dawid.nieszporek1995@gmail.com',
            subject='Etherscan - DB updated, new position on website - please check',
            html_content=html_email_template.email_template)

        
        with open('data/Etherium_Website_Data.csv', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('Etherium_Website_Data.csv'),
            FileType('application/csv'),
            Disposition('attachment')
        )
        message.attachment = attachedFile
        
        sg = SendGridAPIClient(SENDGRID_API_KEY.sendgrid_key)
        sg.send(message)

    except Exception as e:
        print('Error to check: ',e)

if __name__ == '__main__':
    check_ether()
