from utils.twitter import *
import runpy


if __name__ == '__main__':

	#list of key competitrs
	# users = ['DataScienceDojo', 'coursera','getsmarter','HypDev',
	# 	'simplilearn','udacity','NYCDataSci','I_T_Academy',
	# 	'edXOnline', 'udemy', 'AfriDataSch', 
	# 	'DataCamp', 'Springboard', 'wethinkcode' , 'UmuziOrg']

			
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
		output = runpy.run_path(path_name='utils/twitter_loader.py')
		return output
