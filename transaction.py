import sys
para=sys.argv
key=str()
for i in range(1,len(para)):
    if para[i]=='%':
        break
    else:
        key=key+para[i]
d2=str(key)
num=len(para)-1
command=para[num]


import mysql.connector
import datetime
#mydb=str()
try:
	mydb=mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='',
		database='minor_project',
		)
except mysql.connector.errors.ProgrammingError as e:
	print(e)
except mysql.connector.errors.InterfaceError as e:
	print(e)
mycursor=mydb.cursor()
def perform_transaction():
	frm='007046167267'
	to=d2
	amount='100'
	time=datetime.datetime.now()
	sql='INSERT INTO transactions (from_acc,to_acc,amount,created_time) VALUES (%s,%s,%s,%s)'
	val=(frm,to,amount,time)
	mycursor.execute(sql,val)
	mydb.commit()
	print('transaction successfull')
def transaction_history():
        details=['from_acc','to_acc','amount','created_time']
        mycursor.execute('SELECT '+','.join(details)+' FROM transactions;')
        values=mycursor.fetchall()
        temp=str()
        for i in range(len(values)-6,len(values)):#print(values[i])
                for j in range(len(details)):
                        temp+=details[j]+' : '+str(values[i][j])+'<br>'
                temp+='<br>'
        print(temp)
if command == 'trans':
	perform_transaction()
elif command == 'list':
	transaction_history()
