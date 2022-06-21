# #import Facebook_scraper class from facebook_page_scraper
# from facebook_page_scraper import Facebook_scraper
# import StringIO
# import boto3

# import pandas as pd
# import numpy as np


# def _load_facebook_data(usernames):
#     '''
#     Func scrape data using Facebook scraper & load dataset 
#         usernames:list of competitors
#         return:list of collected competitors data from facebook
#     '''
#     for username in usernames:
#         page_name = username
#         posts_count = 1000000
#         browser = "chrome"
#         proxy = "IP:PORT" #if proxy requires authentication then user:password@IP:PORT
#         timeout = 6000 #6000 seconds
#         competitor = Facebook_scraper(page_name,posts_count,browser,proxy=proxy,timeout=timeout)
#     return competitor

# def _preprocess_data(data):
#     pass

# def _store_dataset(data):
#     '''
#     Func convert pandas dataframe to csv file & push file to S3 Bucket
#     data: Pandas Dataframe
#     return: Dict indicating metadata
#     '''
# 	client = boto3.client('s3')
# 	IObuffer = StringIO()

# 	data.to_csv(IObuffer , header=True , index=False)
# 	IObuffer.seek(0)
# 	output = client.put_object(Bucket='competitor-data-store', Body=IObuffer.getvalue() , Key='facebook/facebook.csv')
# 	return output