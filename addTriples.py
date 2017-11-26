import json
import csv

refexp_dataset_path = './google_refexp_dataset_release/google_refexp_train_201511.json'
refexp_key = 'refexps'
tokenized_key = 'tokens'
ref_id_key = 'refexp_id'
raw_key = 'raw'

#Create empty placeholder for triples
with open(refexp_dataset_path) as refexp_file:
    refexp_json = json.load(refexp_file)
    for refexp in refexp_json[refexp_key]:
        refexp['clausie_triples'] = []

with open(refexp_dataset_path, 'w') as f:
    json.dump(refexp_json, f)


#Gather all triples in dictionary
save_file = './clausietriples_save.txt'
triples = {}
with open(save_file) as f:
    parsed = csv.reader(f, delimiter=",")
    for row in parsed:
        trip = {
            "subject": row[1],
            "predicate": row[2],
            "object": row[3]
        }
        if row[0] in triples:
            triples[row[0]].append(trip)
        else:
            triples[row[0]] = [trip]

#Write out triples
with open(refexp_dataset_path) as refexp_file:
    refexp_json = json.load(refexp_file)
    for refexp in refexp_json[refexp_key]:
        key = str(refexp[ref_id_key])
        if key in triples:
            print(triples[key])
            refexp['clausie_triples'] = triples[key]

with open(refexp_dataset_path, 'w') as f:
    json.dump(refexp_json, f)
