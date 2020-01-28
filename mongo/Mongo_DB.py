import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
table_DISEASES = mydb["DISEASES"]
table_ADDITIONAL_INFOS = mydb["ADDITIONAL_INFO"]
table_ICD_10 = mydb["ICD_10"]
table_ICD_11 = mydb["ICD_11"]
table_WIKI = mydb["WIKI"]
table_DISEASES_REL = mydb["DISEASES_REL"]
###here download data from rdb 


##query result to array so  we can transform data to the json 
DISEASE_array=[] 
for row in result_DISEASE:
        DISEASE_array.append({'ID_DISEASE':row[0],'NAME':row[1]})

ADDITIONAL_INFO_array=[] 
for row in result_ADDITIONAL_INFO:
        ADDITIONAL_INFO_array.append({'ID_DISEASE':row[0],'ID_ADDITIONAL_INFO':row[1],'TYPE':row[2],'AUTHOR':row[3],'INFO':row[4]})

ICD_10_array=[] 
for row in result_ICD_10:
        ICD_10_array.append({'ID_DISEASE':row[0],'Code':row[1]})

ICD_11_array=[] 
for row in result_ICD_11:
        ICD_11_array.append({'ID_DISEASE':row[0],'Code':row[1]})
WIKI_array=[] 
for row in result_WIKI:
       WIKI_array.append({'ID_DISEASE':row[0],'LANGUAGE':row[1],'TITLE':row[2],'LINK':row[3]})

DISEASES_REL_array=[] 
for row in result_DISEASES_REL:
       DISEASES_REL_array.append({'ID_REL':row[0],'ID_DISEASE_1':row[1],'ID_DISEASE_2':row[2],'REL_TYPE':row[3]})

## arrayy to json
json_DISEASE=json.dumps(DISEASE_array)
json_ADDITIONAL_INFO=json.dumps(ADDITIONAL_INFO_array)
json_ICD_10=json.dumps(ICD_10_array)
json_ICD_11=json.dumps(ICD_11_array)
json_WIKI=json.dumps(WIKI_array)
json_DISEASES_REL=json.dumps(DISEASES_REL_array)

#insert to the db
table_DISEASES.insert_many(json_DISEASE)
table_ADDITIONAL_INFO.insert_many(json_ADDITIONAL_INFO)
table_ICD_10.insert_many(jsonICD_10)
table_ICD_11.insert_many(json_DICD_11)
table_WIKI.insert_many(json_WIKI)
table_DISEASES_REL.insert_many(json_DISEASES_REL)


