import snscrape.modules.twitter as scraper
import pandas as pd
from datetime import datetime as dt
import re
import numpy as np
import preprocessor as p
import boto3
from io import StringIO



def load_twitter_data(usernames):
	'''
    	Func scrape data using snscraper & load dataset 
        usernames:list of competitors
        return:list of collected competitors data
    	'''
	tweets = []
	for n, k in enumerate(usernames):
		for index , tweet in enumerate(scraper.TwitterSearchScraper('from:{} since 2021-01-01'.format(usernames[n])).get_items()):
			if index > 50000:
				break
			else:
				tweets.append([tweet.user.username, tweet.content,tweet.media,tweet.date, 
                               tweet.likeCount,tweet.replyCount,tweet.retweetCount,
                               tweet.quoteCount, tweet.hashtags , tweet.user.followersCount])

	# Creating a dataframe from the tweets list above
	data = pd.DataFrame(tweets, columns = ['Username' , 'Text' ,'Media', 'Datetime' ,'Likes' , 'Replies','Retweets', 'Quotes','Hashtags', 'Followers'])
		                                   

	data['Datetime'] = pd.to_datetime(data['Datetime'])
	data['Date'] = pd.to_datetime(data['Datetime']).dt.date
	data['Hour'] = pd.to_datetime(data['Datetime']).dt.hour

	data['Time'] = data['Datetime'].dt.time
	data['Weekday'] = data['Datetime'].apply(lambda x: dt.strftime(x, '%A'))
	data.drop(['Datetime'],axis=1, inplace=True)
	return data


def tweet_preprocessor(data):
	'''
	Func clean tweet using tweet-preprocessor
		data: Pandas Dataframe
		return:Dataframe of cleaned tweets
	'''
	tweets = data['Text']
	tweets= p.clean(tweets)
	return tweets


def preprocess_dataset(data):
	data['Media'] = data['Media'].astype('string')
	data.loc[data['Media'].str.contains('Photo'), 'Media'] = 'Photo'
	data.loc[ data['Media'].str.contains('Vid'), 'Media'] = 'Video'
	data.loc[ data['Media'].str.contains('Git'), 'Media'] = 'Link' #links or Githubs
	data.loc[ data['Media'].str.contains('Gif'), 'Media'] = 'Gif'
	data['Media'].fillna('Tweet', inplace=True)
	
	# Removing Digits and lower the text (makes it easy to deal with)
	data['Text'] = data['Text'].astype(str).str.replace('\d+', '')
	# lower_text = data['Text'] .str.lower()

	# Remove extra white spaces, punctuation and apply lower casing
	data['Text'] = data['Text'].str.lower().str.replace('[^\w\s]',' ').str.replace('\s\s+', ' ')
	data.fillna(value=np.nan, axis=1 , inplace=True)
	data.Media.replace(pd.NA , np.nan)
	data['Hashtags'] = data['Hashtags'].str.join('')
	return data
	
def store_dataset(data):
	'''
	 Func convert pandas dataframe to csv file & push file to S3 Bucket
		data: Pandas Dataframe
		return: Dict indicating metadata
	'''
	client = boto3.client('s3')
	IObuffer = StringIO()

	data.to_csv(IObuffer , header=True , index=False)
	IObuffer.seek(0)
	#connect to S3Bucket and update the bucket
	#If Bucket is empty push a new csv file
	output = client.put_object(Bucket='competitor-data-store', Body=IObuffer.getvalue() , Key='twitter/twitter.csv')
	return output
