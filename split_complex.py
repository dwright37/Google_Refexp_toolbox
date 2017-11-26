import json
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import mapping
from nltk.stem.porter import PorterStemmer
import operator
import enchant
import string
import sys

refexp_dataset_path = sys.argv[1]
complex_refexp_dataset_path = sys.argv[2]
refexp_key = 'refexps'
tokenized_key = 'tokens'
raw_key = 'raw'

num_nouns = []
num_nouns_distinct = []
num_verbs = []
complex_refs = []
annotations = []
porter_stemmer = PorterStemmer()

with open(refexp_dataset_path) as refexp_file:
    refexp_json = json.load(refexp_file)
    for refexp in refexp_json[refexp_key]:
        tokens = refexp[tokenized_key]
        tagged = nltk.pos_tag(tokens)
        distinct = set([porter_stemmer.stem(w) for w in tokens])
        tagged_distinct = nltk.pos_tag(distinct)
        
        utags = np.array([mapping.map_tag('en-ptb', 'universal', tag[1]) for tag in tagged])
        utags_distinct = np.array([mapping.map_tag('en-ptb', 'universal', tag[1]) for tag in tagged_distinct])
        
        nouns = utags == 'NOUN'
        nouns_distinct = utags_distinct == 'NOUN'
        
        total_nn = np.sum(nouns)
        num_nouns.append(total_nn)
        
        total_nn_distinct = np.sum(nouns_distinct)
        num_nouns_distinct.append(total_nn_distinct)
        if total_nn_distinct > 2:
            #Separate more complex ref exp from dataset
            complex_refs.append(refexp)
    #Get all the IDs of complex refs
    ids = [item['refexp_id'] for item in complex_refs]
    for ann in refexp_json['annotations']:
        _ids = []
        for _id in ann['refexp_ids']:
            if _id in ids:
                _ids.append(_id)
        if _ids:
            new_ann = ann
            new_ann['refexp_ids'] = _ids
            annotations.append(new_ann)

print('Mean nouns per sentence without stemming: ', np.mean(num_nouns))
print('Mean nouns per sentence with stemming: ', np.mean(num_nouns_distinct))
print('Number of referring expressions with > 2 distinct nouns: ', len(complex_refs))
complex_json = {'annotations': annotations, refexp_key: complex_refs}

with open(complex_refexp_dataset_path, 'w') as f:
    json.dump(complex_json, f)
