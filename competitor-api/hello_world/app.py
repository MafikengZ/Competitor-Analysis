from utils.twitter import *



if __name__ == '__main__':

	#list of key competitrs
	users = ['DataScienceDojo', 'coursera','getsmarter','HypDev',
		'simplilearn','udacity','NYCDataSci','I_T_Academy',
		'edXOnline', 'udemy', 'AfriDataSch', 
		'DataCamp', 'Springboard', 'wethinkcode' , 'UmuziOrg']

			
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
<<<<<<< HEAD
		twitter = load_twitter_data(usernames)
		twitter['Text'] = twitter.apply(tweet_preprocessor , axis=1)
		twitter = twitter.apply( preprocess_dataset , axis=1)
		output2 = twitter.apply(store_dataset)
		return output
=======
		print("Start..")
		twitter = load_twitter_data(users)
		twitter['Text'] = twitter.apply(tweet_preprocessor , axis=1)
		twitter = twitter.apply( preprocess_dataset , axis=1)
		output = twitter.apply(store_dataset, axis=1)
		print('End..')
		return output
	
	#function call
	lambda_handler(data)

>>>>>>> 1ae25c6d82a0cfbfe5f6eeeaa0b89e93f6e79346