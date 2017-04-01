import itertools
import re
import pandas as pd
import sys
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
import json
from pymongo import MongoClient

def create_vocab(filename):
    data = pd.read_csv(filename)
    fields = ['question1', 'question2']
    data_q = data[fields]
    data_q_array = np.array(data_q).flatten()
    data_q_splitted = map(lambda x: re.split(r'\W*', x) if isinstance(x,str) else '',data_q_array)
    vocab_all = []
    for i in data_q_splitted: 
        try:
	    vocab_all+=i 
	except Exception as e: print e,i
    vocab_all = map(lambda x: x.lower(), list(set(vocab_all)))
    
    return vocab_all

def create_trainable_for_vector(filenames):
    data_all = []
    for filename in filenames:
        data = pd.read_csv(filename)
        fields = ['question1', 'question2']
        data_q = data[fields]
	data_q_array = np.array(data_q).flatten()
	data_q_array = map(lambda x: re.sub(r'\W+',' ',x) if isinstance(x, str) else '', data_q_array)
	data_all += data_q_array
    data = ' '.join(data_all).lower()
    return data

def write_vectors(binary_file_path, vocab_file_path, client):
    word_vectors = KeyedVectors.load_word2vec_format(binary_file_path, binary=True)  # C binary format
    vocab = json.load(open(vocab_file_path))
    for i in vocab:
        try:
	    client.data.wordvec.insert({'vec': word_vectors[i].tolist(), 'word':i})
	except Exception as e:
	    print e
def index_training_data():
    print 'create trainable data'
    #x1 = map(lambda x: map(lambda xx: coll_vec.find_one({'word':xx})['vec'] if coll_vec.find_one({'word':xx})!=None else np.zeros(wordvec_dim), x), x1)
    #x2 = map(lambda x: map(lambda xx: coll_vec.find_one({'word':xx})['vec'] if coll_vec.find_one({'word':xx})!=None else np.zeros(wordvec_dim), x), x2)
    x1_train = []
    for i in xrange(len(x2)):
        #print 'hello111111111',i
        x1_sents = []
        for j in xrange(max_sent_len):
            try:
                if j>=len(x1[i]):
                    x1_sents.append(np.zeros(wordvec_dim))
                else:
                        #print 'hello1222222222222', j
                    x1_sents.append(coll_vec.find_one({'word':x1[i][j]})['vec'])
            except:
                #if j>=len(x1[i]):
                x1_sents.append(np.zeros(wordvec_dim))
               # else:
               #     x1[i][j] = np.zeros(wordvec_dim)
        question1_collection.insert_one({'_id':i, 'vec':np.array(x1_sents).tolist()})
        try: 1/(i%10000)
        except: print i

    for i in xrange(len(x2)):
        x2_sents = []
        for j in xrange(max_sent_len):
            try:
                if j>=len(x2[i]):
                    x2_sents.append(np.zeros(wordvec_dim))
                else:
                    x2_sents.append(coll_vec.find_one({'word':x2[i][j]})['vec'])
            except:
                if j>=len(x2[i]):
                    x2_sents.append(np.zeros(wordvec_dim))
                #else:
                #    x2[i][j] = np.zeros(wordvec_dim)
        question2_collection.insert_one({'_id':i, 'vec':np.array(x2_sents).tolist()})
        try: 1/(i%10000)
        except: print i


if __name__ == '__main__':
    client = MongoClient()
    if sys.argv[-1] == 'create_vocab':
        d1= create_vocab('../quora_data/train.csv')
        d2= create_vocab('../quora_data/test.csv')
        d = list(set(d1+d2))
        json.dump(d, open('../quora_data/vocab.json','w'))
    if sys.argv[-1] == 'index_vectors':
        write_vectors('../quora_data/quora-vector.bin', '../quora_data/vocab.json', client)

    if sys.argv[-1]=='index_train':
        import pandas as pd
        from pymongo import MongoClient
        import numpy as np
        import re
        
        c = MongoClient()
        coll_vec = c.data.wordvec
        question1_collection = c.data.question1
        question2_collection = c.data.question2
        wordvec_dim = 200
        data = pd.read_csv('../quora_data/train.csv')
        y = data['is_duplicate']
        x1 = data['question1']
        x2 = data['question2']
        
        x1 = map(lambda x: re.split(r'\W*', x.lower())[:-1] if isinstance(x, str) else '', x1)
        x2 = map(lambda x: re.split(r'\W*', x.lower())[:-1] if isinstance(x, str) else '', x2)
        
        
        max_sent_len = max([max(map(lambda x: len(x), x1)), max(map(lambda x: len(x), x2))])
        max_sent_len = 60

        index_training_data()
