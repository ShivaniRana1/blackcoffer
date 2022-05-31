from matplotlib.pyplot import text
from nltk.tokenize import word_tokenize,sent_tokenize
import pandas as pd
from openpyxl import load_workbook
from textstat.textstat import textstatistics
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
from string import punctuation
import re

stopwords = stopwords.words('english')
punctuation = list(punctuation)
pronounRegex = r"(\b(I|we|We|my|My|ours|us)\b)"

a_file = open("all_stop_word.txt", "r", encoding='latin-1')
a_file = a_file.readlines()
string_without_stopword = []
for line in a_file:
  string_without_stopword.append(line.strip())

score_dict = {"URL_ID": [],"URL" :[],"POSITIVE SCORE":[],"NEGATIVE SCORE":[],"POLARITY SCORE":[],"SUBJECTIVITY SCORE":[],"AVG SENTENCE LENGTH":[],"PERCENTAGE OF COMPLEX WORDS":[],"FOG INDEX":[],
              "AVG NUMBER OF WORDS PER SENTENCE":[],"COMPLEX WORD COUNT":[],"WORD COUNT":[],"SYLLABLE PER WORD":[],
              "PERSONAL PRONOUNS":[],"AVG WORD LENGTH":[]}



def syllables_count(word):
    return textstatistics().syllable_count(word)

def score_value(text,url_id,url_text):
    
    
    #Sentimental Analysis
    
    # remove given stopwords from text
    text_temp = [para for para in text.split() if para not in string_without_stopword ]
    text_temp = " ".join(text_temp)
     
    # to find variables 
    negetive_words =  open("MasterDictionary/negative-words.txt", "r",encoding="ISO-8859-1")
    positive_words =  open("MasterDictionary/positive-words.txt", "r",encoding="ISO-8859-1")
    negetive_words_tokenize = word_tokenize(negetive_words.read())
    positive_words_tokenize = word_tokenize(positive_words.read())
    positive_score = [int(1) for word in text_temp.split() if word.lower()  in positive_words_tokenize ]
    negetive_score = [int(-1) for word in text_temp.split() if word.lower()  in negetive_words_tokenize]
    positive_score = sum(positive_score)
    negetive_score = sum(negetive_score) * int(-1)
    polarity_score = (positive_score - negetive_score)/ ((positive_score + negetive_score) + 0.000001)
    subjectivity_score = (positive_score + negetive_score)/ (len(text) + 0.000001)
    subjectivity_score  = "{:.6f}".format(subjectivity_score )

    #Analysis of Readability
    # to find complex word
    
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    cleaned_tokens = [token for token in words if token not in stopwords and token not in punctuation]
    word_count = len(cleaned_tokens)
      
    total = 0
    count = 0
    for word in words:
        length = len(word)
        total = total + length
        count = count +1
        
    avg_word = total/count  
    diff_words_set = set() 
    syllable_length =[]  
    for word in words:
        syllable_count = syllables_count(word)
        syllable_length.append(syllable_count)
        if syllable_count >= 2:
            diff_words_set.add(word)
    average_sentence_length = len(words)/len(sentences)
    percentage_of_complex_word = (len(diff_words_set)/len(words))*100
    fog_index =  0.4 * (average_sentence_length + percentage_of_complex_word)
    average_no_of_words_sentence  = total /len(sentences)
    complex_word_count = len(diff_words_set)
    
    # to find pronouns

    pronouns = re.findall(pronounRegex, text)
    pronouns_len = len(pronouns)

    # append in dictionary
    score_dict["URL_ID"].append(url_id)
    score_dict["URL"].append(url_text)
    score_dict["POSITIVE SCORE"].append(positive_score)
    score_dict["NEGATIVE SCORE"].append(negetive_score)
    score_dict["POLARITY SCORE"].append(polarity_score)
    score_dict["SUBJECTIVITY SCORE"].append(subjectivity_score)
    score_dict["AVG SENTENCE LENGTH"].append(average_sentence_length)
    score_dict["PERCENTAGE OF COMPLEX WORDS"].append(percentage_of_complex_word)
    score_dict["FOG INDEX"].append(fog_index)
    score_dict["AVG NUMBER OF WORDS PER SENTENCE"].append(average_no_of_words_sentence)
    score_dict["COMPLEX WORD COUNT"].append(complex_word_count)
    score_dict["WORD COUNT"].append(word_count)
    score_dict["SYLLABLE PER WORD"].append(len(syllable_length))
    score_dict["PERSONAL PRONOUNS"].append(pronouns_len)
    score_dict["AVG WORD LENGTH"].append(avg_word)
   
    return score_dict

   
# extracting text from articles in Output Data Structure.xlsx
text_analysis_path = "Output Data Structure.xlsx" # text extraction for analysis
df = pd.read_excel("Output Data Structure.xlsx", engine='openpyxl')

def extract(url_id,url_text):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
    page = requests.get(url_text, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraph = soup.find_all('p')
    text_list = []
    for row in paragraph:
        text_list.append(row.text)
    paraph = " ".join(text_list)
    text = score_value(paraph,url_id,url_text)
    return text


# calling for text extraction
for ind in df.index:
    score_value_dict = extract(int(df['URL_ID'][ind]),df['URL'][ind])


#changing dictionary 
df = pd.DataFrame(score_value_dict)   
  
writer = pd.ExcelWriter('Output_analysis_info.xlsx', engine='xlsxwriter')
# # Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1', index=False)
# # Close the Pandas Excel writer and output the Excel file.
writer.save()
