import json
def cor(a):
    words=a.split()
    string=str()
    with open('new.json','r') as file:
        string=json.load(file)
    string=string['corrections']
    for i in range(len(words)):
        for j in string:
            if words[i] in j['synonyms']:
                words[i]=j['value']
                break
            else:
                pass
    a=(' '.join(words))
    return a
