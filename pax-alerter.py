# Penny Arcade Expo Alerter 
# github.com/codingbrent
from __future__ import absolute_import, print_function
import configparser
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from twilio.rest import TwilioRestClient
import configparser
import tweepy

config = configparser.ConfigParser()
config.read('paxalerter.cfg')
# twitter configuration
consumer_key = config.get('twitconfig','consumer_key')
consumer_secret = config.get('twitconfig','consumer_secret')
access_token = config.get('twitconfig','access_token')
access_token_secret = config.get('twitconfig','access_token_secret')
#debug (comment out below for github release)
#print(consumer_key, consumer_secret, access_token, access_token_secret)
# twillio configuration
account_sid = config.get('twilconfig','account_sid')
auth_token = config.get('twilconfig','auth_token')
twil_phone = config.get('twilconfig','twil_phone')
your_phone = config.get('twilconfig','your_phone')
# pax configuration
which_pax = config.get('pax','which_pax')
user_monitor = config.get('pax','user_monitor')
track_terms = ['pax east', 'pax east badge']


# text me 
def textme():
    message = client.messages.create(to=your_phone, from_=twil_phone,
                                         body="PAX EAST LIVE GO GO GO!")
# call me 
def callme():
        call = client.calls.create(to=your_phone,  # Any phone number
                               from_=twil_phone, # Must be a valid Twilio number
                               url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
        print(call.sid)
# session information
def printstatuses(user, api):
    print("Session Information")
    print("User Timeline: " + api.me().name)
    print("Monitoring Account: " + str(user_monitor))
    print("Monitoring Account ID: " +  str(user.id))
    print("==========================================")

# Stream Listener  
class StreamListener(tweepy.StreamListener): 
    # status checking/passing 
    def on_status(self, status):
        if which_pax in status.text.lower():
            # call function to twilio api
            textme()
            callme()
            print("Status DETECTED, Calling and Texting: " + status.text)
        # keep alive 
        return True 

    def on_error(self, status):
        print('Errored with: ' + status) 
        print('Errored with: '+  status) 
        # keep alive 
        return True 

    def on_timeout(self):     
    	print >> 'timeout...'
        # keep alive 
    	return True 

# main
if __name__ == '__main__':
    # OAuth Authentication
    l = StreamListener()
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.secure = True 
    auth.set_access_token(access_token,access_token_secret)	
    api = tweepy.API(auth)
    user = api.get_user(screen_name = str(user_monitor))
    printstatuses(user,api)
    # Twilio setup
    client = TwilioRestClient(account_sid, auth_token)
    # Stream Information
    stream = Stream(auth, l)
    stream.filter(follow=["39478528"])

