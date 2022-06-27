from utils.twitter import *
import snscrape.modules.twitter as scraper



#list of key competitrs
users = ['DataScienceDojo', 'coursera','getsmarter','HypDev',
	'simplilearn','udacity','NYCDataSci','I_T_Academy',
	'edXOnline', 'udemy', 'AfriDataSch', 
	'DataCamp', 'Springboard', 'wethinkcode' , 'UmuziOrg']
	
tweets = []
for n, k in enumerate(users):
	for index , tweet in enumerate(scraper.TwitterSearchScraper('from:{} since 2021-01-01'.format(users[n])).get_items()):
		if index > 60000:
			break
			
		tweets.append([tweet.user.username, tweet.content,tweet.media,tweet.date, 
              	tweet.likeCount,tweet.replyCount,tweet.retweetCount,
             	tweet.quoteCount, tweet.hashtags , tweet.user.followersCount])
        	

if __name__ == '__main__':
	
	# Creating a dataframe from the tweets list above
	data = pd.DataFrame(tweets, columns = ['Username' , 'Text' ,'Media', 
					'Datetime' ,'Likes' , 'Replies','Retweets',
					 'Quotes','Hashtags', 'Followers'])
			
			
	def lambda_handler(twitter):
		'''
		Func calls utility functions from utils, 
		this func is referenced by template.yaml (cloudformation)
		
		usernames:list of competitors
		
		'''
		#facebook
		# facebook = _load_facebook_data(usernames)
		# facebook = facebook.apply(_preprocess_dataset)
		# output1 = facebook.apply(_store_dataset)
		#twitter
		print("Start..")
		#twitter = load_twitter_data(users)
		twitter['Text'] = twitter.apply(tweet_preprocessor , axis=1)
		twitter = twitter.apply( preprocess_dataset , axis=1)
		output = twitter.apply(store_dataset, axis=1)
		print('End..')
		return output
	
	#function call
	lambda_handler(data)
