from utils import *


if __name__ == '__main__':
	
	#list of key competitrs
	users = ['DataScienceDojo', 'coursera','getsmarter','HypDev',
		    'simplilearn','udacity','NYCDataSci','I_T_Academy',
		    'edXOnline', 'udemy', 'AfriDataSch', 
		    'DataCamp', 'Springboard', 'wethinkcode' , 'UmuziOrg']

	def lambda_handler(usernames):
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
		twitter = _load_twitter_data(usernames)
		twitter['Text'] = twitter.apply(_tweet_preprocessor , axis=1)
		twitter = twitter.apply( _preprocess_dataset , axis=1)
		output2 = twitter.apply(_store_dataset)
	
	#function call
	lambda_handler(users)