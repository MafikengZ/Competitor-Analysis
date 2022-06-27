from utils.twitter import *


if __name__ == '__main__':
	
	#list of key competitrs
	users = ['DataScienceDojo', 'coursera','getsmarter','HypDev',
		    'simplilearn','udacity','NYCDataSci','I_T_Academy',
		    'edXOnline', 'udemy', 'AfriDataSch', 
		    'DataCamp', 'Springboard', 'wethinkcode' , 'UmuziOrg']

	def lambda_handler(event, context):
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
		
		data = load_twitter_data(users)
		data['Text'] = data.apply(tweet_preprocessor , axis=1)
		data = data.apply( preprocess_dataset , axis=1)
		output = data.apply(store_dataset)
		return {
		"statusCode": 200,
		"headers": {
			"Content-Type": "application/json"},
			"body": json.dumps({"output ": output})
			}
	
	#function call
	#lambda_handler(users)
