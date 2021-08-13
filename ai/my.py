import sys
para=sys.argv
key=str()
for i in range(1,len(para)):
    if para[i]=='%':
        break
    else:
        key=key+para[i]
d2=int(key)
num=len(para)-1
table=para[num]

import mysql.connector

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='minor_project'
    )

mycursor=mydb.cursor()
'''
table= input('Enter table name:').lower()
d2=str()
if table in ['card','cards','card details','card detail']:
    table='cards';d2=input('Enter Card no:')
elif table in ['account','account Aetails']:
    table='accounts';d2= input('Enter Account no:')
elif table in ['personal details','my details','details','customers','customer detail']:
    table='customers';d2= input('Enter Username:')
'''

def show(table,idd):
    details=str()
    if table=='cards':
        details=['card_no','card_id','holder_name','till_month','till_year','card_type']
    elif table=='accounts':
        details=['acc_no','acc_name','acc_type','balance','status']
    elif table=='customers':
        details=['username', 'fname', 'lname', 'email', 'contact', 'postal_add', 'perm_add', 'city', 'state', 'country', 'pincode', 'dob', 'gender', 'hasAcc']
    querry="select "+','.join(details)+" from "+table+" where "+details[0]+" = %s;"
    mycursor.execute(querry,(idd,))
    d=mycursor.fetchall()
    for i in d:
        print(i)

show(table,d2)


#mycursor.execute('select * from cards;')
#a=mycursor.fetchall()
#print(a)

