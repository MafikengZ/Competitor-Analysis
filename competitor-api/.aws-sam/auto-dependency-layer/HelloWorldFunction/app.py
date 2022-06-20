import snscrape.modules.twitter as scraper
import pandas as pd
from datetime import datetime as dt
import re
import numpy as np
import preprocessor as p
import boto3
from io import StringIO



if __name__ == '__main__':
	
	usernames = ['DataScienceDojo', 'coursera','getsmarter','HypDev',
		    'simplilearn','udacity','NYCDataSci','I_T_Academy',
		    'edXOnline', 'udemy', 'AfriDataSch', 
		    'DataCamp', 'Springboard', 'wethinkcode' , 'UmuziOrg']

	tweets = []
	for n, k in enumerate(usernames):
		for index , tweet in enumerate(scraper.TwitterSearchScraper('from:{} since:2021-01-01'.format(usernames[n])).get_items()):
			if index > 50000:
				break
			else:
				tweets.append([tweet.date, tweet.content,tweet.user.username, 
				tweet.user.followersCount,tweet.replyCount,
				tweet.retweetCount, tweet.likeCount, tweet.quoteCount,
				tweet.links, tweet.media, tweet.retweetedTweet, 
				tweet.quotedTweet, tweet.hashtags])

	# Creating a dataframe from the tweets list above
	data = pd.DataFrame(tweets, columns = ['Username' , 'Text' ,'Media', 'Datetime' , 'Likes' , 
						'Replies','Retweets', 'Quotes','Hashtags', 'Followers'])
		                                   

	data['Datetime'] = pd.to_datetime(data['Datetime'])
	data['Date'] = pd.to_datetime(data['Datetime']).dt.date
	data['Hour'] = pd.to_datetime(data['Datetime']).dt.hour

	data['Time'] = data['Datetime'].dt.time
	data['Weekday'] = data['Datetime'].apply(lambda x: dt.strftime(x, '%A'))
	data.drop(['Datetime'],axis=1, inplace=True)


	def _tweet_preprocessor(row):
	    #Cleaning using tweet-preprocessor
	    data = row['Text']
	    data = p.clean(data)
	    return data


	data['Media'] = data['Media'].astype('string')
	data.loc[data['Media'].str.contains('Photo'), 'Media'] = 'Photo'
	data.loc[ data['Media'].str.contains('Vid'), 'Media'] = 'Video'
	data.loc[ data['Media'].str.contains('Git'), 'Media'] = 'GitHub'
	data.loc[ data['Media'].str.contains('Gif'), 'Media'] = 'Gif'
	data['Media'].fillna('Tweet', inplace=True)

	data['Text'] = data.apply(_tweet_preprocessor , axis=1)

	# Removing Digits and lower the text (makes it easy to deal with)
	data['Text'] = data['Text'].astype(str).str.replace('\d+', '')
	# lower_text = data['Text'] .str.lower()

	# Remove extra white spaces, punctuation and apply lower casing
	data['Text'] = data['Text'].str.lower().str.replace('[^\w\s]',' ').str.replace('\s\s+', ' ')
	data.fillna(value=np.nan, axis=1 , inplace=True)
	data.Media.replace(pd.NA , np.nan)
	data['Hashtags'] = data['Hashtags'].str.join('')


	client = boto3.client('s3')
	IObuffer = StringIO()

	data.to_csv(IObuffer , header=True , index=False)
	IObuffer.seek(0)
	client.put_object(Bucket='competitor-data-store', Body=IObuffer.getvalue() , Key='twitter/twitter.csv')



