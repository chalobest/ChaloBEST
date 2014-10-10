from utils import *
tweety = Tweetbot()
from twitter import *    
auth = OAuth("296097629-QdjEw3B2z4LoCWgA6yOBXzKuO2ukModQQyEiTm2i", "BofoeYVwm4pG3dTwf32kFsDgwnp9tvxnX7utH9BkKrcUz", "07n0QQY30ge2Pvz9WThPJAZzl", "adFFBOcDfQPu1DlGLLygsV83mnFOHmjyjQZKe11fWzGNkKAhQr")
f = open("twitterstream.log","w+")
f2 = open("twitterstream_everything.log","w+")
import sys
t = Twitter(auth=auth)
twitter_userstream = TwitterStream(auth=auth, domain='userstream.twitter.com')
for msg in twitter_userstream.user():
   f2.write(str(msg))
   f2.write("\n")
   f2.flush()
   if msg.has_key('entities'):
      try:
         if len(msg['entities']['user_mentions']) == 1 and str(msg['entities']['user_mentions'][0]['id']) == '296097629':
            print msg['text'], msg['id_str']   
            text = msg['text']
            usr = msg['user']['screen_name']
            txt = text.lower().replace("@chalobest","").strip(" ").strip("\n")
            resp = tweety.handler(txt)
            reply = "@" + usr + " " + resp
            if len(reply) > 140:
               reply = reply.rstrip("...")[0:137] + "..."
            t.statuses.update(status=reply)
         f.write(str(msg))
         f.write("\n")
         f.flush()
      except:
         print sys.exc_info()[1]

