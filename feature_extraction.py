import csv
import re
import string
import nltk


result_file = open("sample_obama_sentiment.csv", 'w')
input_writer= csv.writer(result_file, delimiter='\t', quotechar= '\"', lineterminator= '\n', quoting=csv.QUOTE_MINIMAL)



stopWords =[]
stopwords_file1 = open("stopwords.csv", 'rU')
stopwords_reader1 =csv.reader(stopwords_file1, delimiter='\t', quotechar ='\"')

for row, content in enumerate(stopwords_reader1):
	stopWords.append(content[0])

# print len(stopWords)

def unicode_to_ascii(tweet):
	tweet = filter(lambda x: x in string.printable, tweet)
    # s = s.replace("'", " ")
	return tweet

def ProcessTweet(tweet): 
	tweet= tweet.lower()
	tweet= unicode_to_ascii(tweet)
	tweet= re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
	# tweet = re.sub('@[^\s]+','',tweet)
	tweet = re.sub('[\s]+', ' ', tweet)
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	tweet = tweet.strip('\'"')
	return tweet 

def getFeatureVector(tweet):
	featureVector =[]
	words = tweet.split()
	for w in words:
		w= w.strip('\'"?,.:-')
		if w in stopWords:
			continue
			# print " yes stopwords"
		else:
			featureVector.append(w.lower())
	return featureVector

input_file1= open("obama_senti_handcoding.csv", 'rU')
input_reader1= csv.reader(input_file1, delimiter='\t', quotechar= '\"')

tweets =[]
featureList=[]

count =0 
for row, content in enumerate(input_reader1):
	if row==0:
		continue
	sentiment =content[1]
	processedTweet =ProcessTweet(content[0])
	vectorizedTweet =getFeatureVector(processedTweet)
	featureList.extend(vectorizedTweet)
	tweets.append((vectorizedTweet, sentiment))

featureList=list(set(featureList))
#print featureList
# print tweets
	# print vectorizedTweet
	# print processedTweet
	# print vectorizedTweet

def extract_features (tweet):
	tweet_words =set(tweet)
	features ={}
	for word in featureList:
		features['contains(%s)' % word] =(word in tweet_words)
	return features 

training_set=nltk.classify.util.apply_features(extract_features, tweets)

NBClassifier= nltk.NaiveBayesClassifier.train(training_set)

# print NBClassifier.show_most_informative_features(10)

input_file2= open("sample_obama_tweets.csv", 'rU')
input_reader2= csv.reader(input_file2, delimiter='\t', quotechar= '\"')


for row, content in enumerate(input_reader2):
	if row==0:
		continue
	output_list =[]
	line = content[2]
# testTweet= "It's true: I have chosen to endorse Obama because I'm proud to have someone of the *human* race as President. So there" 
	processedLine =ProcessTweet(line)
	# content.insert(3, NBClassifier.classify(extract_features(getFeatureVector(processedLine)))
	# print NBClassifier.classify(extract_features(getFeatureVector(processedLine)))
	sentiment=NBClassifier.classify(extract_features(getFeatureVector(processedLine)))
	content.insert(3, sentiment)

	input_writer.writerow(content)
	# output_list.append(line)
	# output_list.append(sentiment)
	

# processedTestTweet =ProcessTweet(testTweet)
# print processedTestTweet
# print NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
