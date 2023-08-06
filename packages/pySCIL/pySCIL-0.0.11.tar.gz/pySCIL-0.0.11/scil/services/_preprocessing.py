# This file is for general preprocessing to be done on dialogues such as
# Part of Speech extraction or any high-cost processing that we want
# to perform only once.

#Import Json elements to encode Python data structures
import json
#Import functions to deal with text
import re, string, unicodedata
#Import nartural language processing functions
import nltk
from nltk import word_tokenize, sent_tokenize, ngrams
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
#Import stanford PoS tagger
from nltk.tag import StanfordPOSTagger
#Import file manipulation function
import codecs
#Import pickle
import pickle
#Import pathlib
from pathlib import Path

#Function that Break texts into words
#Input: string
#ouput: list
def tokenize(text):
    return nltk.word_tokenize(text.lower())

#Function that removes non-ASCII characters from list of tokenized words
#Input: list
#ouput: list
def removeNonAscii(words):
    return [unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore') for word in words]

#Remove empty elements after some preprocessing
#Input: list
#ouput: list
def removeEmptyElements(words):
    return [word.replace('\n', '') for word in words if word != ""]

#Remove punctuation from list of tokenized words
#Input: list
#output: list
def removePunctuation(words):
    return [word.translate(str.maketrans(' ',' ',string.punctuation)) for word in words if word != ""]

#Clean text using other functions
#Input: string
#output: list
def normalize(text):
    words=tokenize(text)
    words=removeNonAscii(words)
    words=removePunctuation(words)
    words=removeEmptyElements(words)
    return words

#Concatenate dialogue utterances  
def concatenateUtterances(dialogueTurns):
    return [normalize(turn["text"]) for turn in dialogueTurns]

#expand NLTK stopwords
swnltk = set(stopwords.words('english'))
swnltk.update([elem for sublist in [tokenize(word) for word in swnltk] for elem in sublist])
swnltk = set(removeEmptyElements(removePunctuation(swnltk)))

#get anew
path = str(Path(__file__).parent.parent)
with open(path + '/anew.pickle', 'rb') as handle:
    anew = pickle.load(handle)

# returns all words with noun tags in each turn
def getNouns(posTags):
    tags=['NN','NNS','NNP','NNPS']
    return [[word[0] for word in elements if word[1] in tags] for elements in posTags]
    
#Extract the wordnet PoS from a word
#Input: string
#output: wordnet PoS
def get_wordnet_pos(word):
    #Map POS tag to first character
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, None)

#Lemmatizes a word using its PoS
#Input: (word, pos), lemmatizer
#output: word
def lemmatizeWord(word, lemmatizer):
    pos = get_wordnet_pos(word[1])
    if not pos:
        return word[0]
    return lemmatizer.lemmatize(word[0], pos)

#Takes one bigram and determines it is a valid topic
#Input: ((word,pos),(word,pos))
#output: boolean
def isValidBigram(bigram):
    a = bigram[0]
    b = bigram[1]

    # stopwords can't be topics
    # words must be at least length 2
    if (a[0] in swnltk or b[0] in swnltk) or (len(a[0]) < 2 or len(b[0]) < 2):
        return False

    # refuse adjectives with extreme sentiments
    # here we define extreme sentiment to be more than
    # two points away from the average of '5' #! investigate what the actual average is in the dataset, the median, stdv
    #! does this actually work, maybe removes too many cases?
    #! average 5.48 median 5.78
    if a[1] == 'JJ':
        # get sentiment, if word is unknown assume it to be neutral
        sentiment = anew.get(a[0],5.0)
        if (sentiment < 3 or sentiment > 7):
            return False

    # [[Allowed for A], [Allowed for B], [Not allowed for C]]
    patterns = [
        [['NN','NNS'],['NN','NNS']],
        [['JJ'],['NN','NNS']]
    ]

    # accept cases of ADJ NOUN or NOUN NOUN
    if (
        (a[1] in patterns[0][0] and b[1] in patterns[0][1]) or
        (a[1] in patterns[1][0] and b[1] in patterns[1][1])
    ):
        return True
    return False

#Takes a unigram and decides if it is valid
#Input: (word,pos)
#output: boolean
def isValidUnigram(gram):
    tags = ['NN','NNS','NNP','NNPS']
    # words must be at least length 2
    if gram[0] in swnltk or len(gram[0]) < 2:
        return False
    if gram[1] in tags:
        return True
    return False

def getBigramTopics(posTags,n,mesoTopicThreshold):
    bigramBase = {}
    # i = turn counter
    # j = index counter
    i,j = 0,0
    for turn in posTags:
        #append empty list for every turn 
        # allTopics.append([])
        
        bigrams = ngrams(turn,2)
        for gram in bigrams:
            if isValidBigram(gram):
                joined = gram[0][0] + " " + gram[1][0]
                if joined in bigramBase:
                    bigramBase[joined]['occ'] += 1
                    bigramBase[joined]['loc'].extend([(i,j),(i,j+1)])
                else:
                    # loc stored in format of (line,index)
                    bigramBase[joined] = {'occ': 1, 'loc': [(i,j),(i,j+1)]}
            j += 1
        i += 1
        j = 0
    bigramTopics = {key:{'occ': bigramBase[key]['occ'], 'loc': bigramBase[key]['loc']}  
        for key, val in bigramBase.items() if bigramBase[key]['occ'] >= n}  
    bigramMesoTopics = {key:{'occ': bigramBase[key]['occ'], 'loc': bigramBase[key]['loc']}  
        for key, val in bigramBase.items() if bigramBase[key]['occ'] >= mesoTopicThreshold}
    return (bigramTopics, bigramMesoTopics)

def getUnigramTopics(posTags,n,mesoTopicThreshold,bigramTopics,bigramMesoTopics):
    # so that we don't double count topics, store used locations
    usedLocations = {elem for sublist in [bigramTopics[key]['loc'] for key in bigramTopics] for elem in sublist}
    usedLocationsMeso = {elem for sublist in [bigramMesoTopics[key]['loc'] for key in bigramMesoTopics] for elem in sublist}

    # calculate unigram topics
    unigramTopics = {}
    # i = turn counter
    # j = index counter
    i,j = 0,0
    for turn in posTags:
        for word in turn:
            # if this word was used in a bigram, skip it
            #! should we still count it towards topic counts though?
            if (i,j) in usedLocations:
                continue
            if isValidUnigram(word):
                if word[0] in unigramTopics:
                    unigramTopics[word[0]]['occ'] += 1
                    unigramTopics[word[0]]['loc'].append((i,j))
                else:
                    unigramTopics[word[0]] = {'occ': 1, 'loc': [(i,j)]}
            j += 1
        i += 1
        j = 0

    # calculate unigram meso topics
    unigramMesoTopics = {}
    # i = turn counter
    # j = index counter
    i,j = 0,0
    for turn in posTags:
        for word in turn:
            # if this word was used in a bigram, skip it
            #! should we still count it towards topic counts though?
            if (i,j) in usedLocationsMeso:
                continue
            if isValidUnigram(word):
                if word[0] in unigramMesoTopics:
                    unigramMesoTopics[word[0]]['occ'] += 1
                    unigramMesoTopics[word[0]]['loc'].append((i,j))
                else:
                    unigramMesoTopics[word[0]] = {'occ': 1, 'loc': [(i,j)]}
            j += 1
        i += 1
        j = 0

    unigramTopics = {key:{'occ': unigramTopics[key]['occ'], 'loc': unigramTopics[key]['loc']}  
        for key, val in unigramTopics.items() if unigramTopics[key]['occ'] >= n}
    unigramMesoTopics = {key:{'occ': unigramMesoTopics[key]['occ'], 'loc': unigramMesoTopics[key]['loc']}  
        for key, val in unigramMesoTopics.items() if unigramMesoTopics[key]['occ'] >= mesoTopicThreshold}
    return(unigramTopics, unigramMesoTopics)

def getTopics(posTags,bigramTopics,unigramTopics):
    allTopics = [[] for x in posTags]
    for topic in bigramTopics:
        for i in range(0,len(bigramTopics[topic]['loc']),2):
            allTopics[bigramTopics[topic]['loc'][i][0]].append(topic)
    for topic in unigramTopics:
        for i in range(len(unigramTopics[topic]['loc'])):
            allTopics[unigramTopics[topic]['loc'][i][0]].append(topic)
    return allTopics

def getMesoTopics(posTags,bigramMesoTopics,unigramMesoTopics):
    allMesoTopics = {}
    for topic in bigramMesoTopics:
        for i in range(0,len(bigramMesoTopics[topic]['loc']),2):
            if topic not in allMesoTopics:
                allMesoTopics[topic] = []
            allMesoTopics[topic].append(bigramMesoTopics[topic]['loc'][i][0])
    for topic in unigramMesoTopics:
        for i in range(len(unigramMesoTopics[topic]['loc'])):
            if topic not in allMesoTopics:
                allMesoTopics[topic] = []
            allMesoTopics[topic].append(unigramMesoTopics[topic]['loc'][i][0])
    return allMesoTopics

class Preprocessing(object):
    #Tag words using Stanford PoS Tagger
    def stanfordPosTagger(self):
        try:
            #setup lemmatizer
            lemmatizer = WordNetLemmatizer()

            #Concatenate all utterances into a single list
            wordList=concatenateUtterances(self.jsonData["turns"])

            #get path
            path = str(Path(__file__).parent.parent)

            #Add jar and model via their path (instead of setting environment)
            jar=path+"/stanford-postagger-full-2015-04-20/stanford-postagger.jar"
            model=path+"/stanford-postagger-full-2015-04-20/models/english-left3words-distsim.tagger"
            #Set up PoS tagger
            posTagger = StanfordPOSTagger(model, jar, encoding='utf8')
            self.posTags=posTagger.tag_sents(wordList)
            self.posTags=[[(lemmatizeWord(word,lemmatizer),word[1]) for word in words] for words in self.posTags]
        except Exception as e:
            print("EXCEPTION:", e)

    #Tag words using NLTK PoS Tagger
    def NLTKPosTagger(self):
        try:
            #setup lemmatizer
            lemmatizer = WordNetLemmatizer()

            #concatenate all utterances into a single list
            wordList=concatenateUtterances(self.jsonData["turns"])

            self.posTags=[nltk.pos_tag(word) for word in [words for words in wordList]]
            self.posTags=[[(lemmatizeWord(word,lemmatizer),word[1]) for word in words] for words in self.posTags]
        except Exception as e:
            print("EXCEPTION:", e)

    #Get topics and mesotopics
    def nounPosTopics(self, n, mesoTopicThreshold):
        try:
            if (self.posTags):
                # get bigram topics and mesoTopics
                bigramTopics, bigramMesoTopics = getBigramTopics(self.posTags,n,mesoTopicThreshold)
                # get unigram topics and mesoTopics
                unigramTopics, unigramMesoTopics = getUnigramTopics(self.posTags,n,mesoTopicThreshold,bigramTopics,bigramMesoTopics)
            
                # get nouns
                self.nouns = getNouns(self.posTags)
                # get topics
                self.topics = getTopics(self.posTags,bigramTopics,unigramTopics)
                # get mesoTopics
                self.mesoTopics = getMesoTopics(self.posTags,bigramMesoTopics,unigramMesoTopics)
                
        except Exception as e:
            print("EXCEPTION:", e)

