import json
text=list()
while True:
    value=input('enter the word : ')
    if value is '' or value is '.':
        break
    synonyms=input('enter synonyms : ').split()
    text.append({'value':value,'synonyms':synonyms})
try:
    with open('new.json','r') as file:
        temp=json.load(file)
        temp['corrections'].extend(text)
        with open('new.json','w') as wfile:
            json.dump(temp,wfile,indent=4)
except: #FileNotFoundError:
    with open('new.json','w') as file:
        temp={}
        temp['corrections']=list()
        temp['corrections'].append(text)
        json.dump(temp,file,indent=4)
