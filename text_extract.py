import pandas as pd
from bs4 import BeautifulSoup
import requests


text_extraction_path ="Input.xlsx"   # use to extract text from articles
text_analysis_path = "Output Data Structure.xlsx" # text extraction for analysis
df = pd.read_excel (text_analysis_path)
text_extraction_folder_path ="text_extracted_folder"  # extracted text folder path
text_analysis_folder_path = "text_analysis_folder"  # extracted text folder path for text analysis

def extract(url_id,url_text):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
    page = requests.get(url_text, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraph = soup.find_all('p')
    with open('{}/{}.txt'.format(text_analysis_folder_path,url_id), 'w') as f:
        for row in paragraph:
            f.write(row.text+'\n')

    

for ind in df.index:
   extract(int(df['URL_ID'][ind]),df['URL'][ind])
    


