import nltk
from glob import glob
import pandas as pd
import os

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
import nltk.data
import re
from nltk.util import ngrams
from nltk.corpus import PlaintextCorpusReader, stopwords
stops = stopwords.words('english') + ['thou','thy']
#get the list of directories
dirs = glob('*/')
punctuation = re.compile(r'[\W]')
punct = [',','.','&','{','}','?',"'",'-',';',':','|','(',')','[',']']
#for everything in the list
names=dict()
for d in dirs:
    #make each of the directories a temporary corpus
    #also make a list of all the n-grams for 2<=n<=5, for common phrasings
    name = d[:-1]
    words = [list() for i in range(2,5)]
    with cd(d):
        corpus = PlaintextCorpusReader('./','.*')
        tokens =[token for token in corpus.words() if not punctuation.match(token)]
        grams = list(ngrams(tokens,2))
        n=len(grams)
        gramscount= [(j,grams.count(j)/n) for j in [('your','self'),('our','selfe'),('him','self')]]
        stuff = corpus.words()
        morphemes = [l for l in stuff if l not in stops and l not in punct]
        #make a pseudo-dictionary for the single words
        n=len(morphemes)
        series = [(l,morphemes.count(l)/n) for l in ['have','haue','good','goode','never','neuer','come','cum','unto','vnto','which','whych','kyng','king','kynge','verbe','verb','whiche','hath','has','lorde','lord','yourself','ourself','himself']]
        series = dict(series+gramscount)
    names[name]=series
data = pd.DataFrame(names)
data.to_csv(path_or_buf='spellingData.csv')
