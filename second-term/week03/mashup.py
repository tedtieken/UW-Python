'''
A script to find products people are enthusiastic about merging data from multiple twitter APIs and amazon.com
- gets references to amazon.com on twitter from backtweet
- resolves who tweeted it from twitter
- checks tweeter's influence from backtweet to eliminate spammers
- Extracts the item's rating and number of reviews from amazon
'''

import urllib2
import json
from BeautifulSoup import BeautifulSoup

import keys
from getproduct import extract_item_from_url

from pprint import pprint

print "starting"
backtweet_url = 'http://backtweets.com/search.json?q=amazon.com&key=' + keys.backtweet_key + '&itemsperpage=10'
influencer_url = 'http://api.backtype.com/user/influencer_score.json?user_name=%s&key=' + keys.backtweet_key
twitter_url = 'http://api.twitter.com/1/statuses/show/%s.json'
amazon_url = 'http://www.amazon.com/dp/%s/'
supertweet_url = 'http://api.supertweet.net/%s' # gets 350 req per hour

# Setup Password for supertweet requests
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, supertweet_url % "", keys.supertweet_user, keys.supertweet_pass)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

# Get backtweet refs.
data = urllib2.urlopen(backtweet_url)
json_data = json.load(data)

def out_of_5(text):
    text = text.lower()
    if ('out of 5 stars' in text):
        return True


def customer_reviews(text):
    text = text.lower()
    if ('customer reviews' in text):
        return True


def be_the_first(text):
    text = text.lower()
    if ('be the first to review this item' in text):
        return True



remaining_hits = json.load(urllib2.urlopen('http://api.supertweet.net/1/account/rate_limit_status.json'))['remaining_hits']   
print remaining_hits
spammers = {}
for item in json_data['tweets']:
    rating = reviews = None
    
    #Get twitter stats
    if remaining_hits > 1:
        tweet_id = item['tweet_id']
        remaining_hits -= 1
        print remaining_hits
        try:
            query_part = '1/statuses/show/%s.json' % tweet_id
            item_data = urllib2.urlopen(supertweet_url % query_part)
            item_json_data = json.load(item_data)
            scalar = item_json_data['user']['followers_count']
            tweeter = item_json_data['user']['screen_name']
            magnitude = item_json_data['retweet_count']
            said = item_json_data['text']
            #print remaining_hits, product_code, rating, reviews, scalar, tweeter, said
        except urllib2.HTTPError:
            continue

    
    # Current influencer implementation using backtype has very low rate limit
    # Get influencer score
    if spammers.has_key(tweeter):
        continue
    else:
        in_score = json.load(urllib2.urlopen(influencer_url % tweeter))['influencer']['score']

    if in_score < 20:
        spammers[tweeter] = in_score
        continue
    remaining_hits = json.load(urllib2.urlopen('http://api.supertweet.net/1/account/rate_limit_status.json'))['remaining_hits']

    product_code = extract_item_from_url(item['resolved_urls'])
        
    #Get amazon popularity
    if product_code:
        print "going to try", amazon_url % product_code
        try:
            amzn_resp = urllib2.urlopen(amazon_url % product_code)    
        except urllib2.HTTPError:
            continue
        soup = BeautifulSoup(amzn_resp.read())
        raw_rating = soup.find(text=out_of_5)
        raw_reviews = soup.find(text=customer_reviews)
        if raw_rating and raw_reviews:
            rating = raw_rating.split(' out of')[0]
            reviews = raw_reviews.split(' customer reviews')[0]
            #print product_code, rating, reviews 
        else:
            be_first = soup.find(text=be_the_first)
            if be_first:
                print product_code, 0, 0
            else:
                print item['resolved_urls']
    
        print remaining_hits, scalar, tweeter, said, product_code, rating, reviews

        
    #print extract_item_from_url(item['resolved_urls'][0])
    #print item['tweet_id']
print spammers