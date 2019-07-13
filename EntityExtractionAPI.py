# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 10:27:33 2019

@author: skatiyar
"""
# Import relevant libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import pandas as pd

#Create Datarame to store Results
company_names=pd.DataFrame(columns=['URL','Company Name','Relevance'])
#Import Relevant librarire for IBM Watson API
import json 
from watson_developer_cloud import NaturalLanguageUnderstandingV1 
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions

#Initialize API connection
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='{apikey}',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-19')
# List of URLs from which Entities have to be extracted
urls=['https://www.cnbc.com/2019/03/22/reuters-america-update-4-german-bund-yield-crashes-below-zero-for-first-time-since-2016-as-bleak-data-rattles-markets.html']
# Run loop over list of URLs and append reuslts in a Dataframe
for url in urls:
    response = natural_language_understanding.analyze(url=url,features=Features(entities=EntitiesOptions(sentiment=True,limit=50))).get_result()
    entities=response['entities']    
    company_list=[]
    for i in entities:
        if i['type']=='Company':
            company_list.append(i)
    relevance_score=max([i['relevance'] for i in company_list])
    for i in company_list:
        if i['relevance']==relevance_score:
            company_name=i['text']
    company_names['URL']=pd.Series(url)
    company_names['Relevance']=pd.Series(relevance_score)
    company_names['Company Name']=pd.Series(company_name)
#Check API results in a dictionary format
print(repsonse)    
#Extract Entity information from API repsonse
entity_df=pd.DataFrame.from_dict(response['entities'],orient='columns')
# Extract outptut in a csv format
entity_df.to_csv('test3.csv')
