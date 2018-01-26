from nltk.stem import WordNetLemmatizer


wordnet_lemmatizer = WordNetLemmatizer()

l = ['algorithms', 'flowers', 'auto-encoders', 'machines', 'encoders']

for words in l:
    print(wordnet_lemmatizer.lemmatize(words))

