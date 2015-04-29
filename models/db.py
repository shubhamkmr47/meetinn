db = DAL("sqlite://storage.sqlite")

a=[]
for i in range(3,5):
    for j in range(10):
        a.append(str(i)+'0'+str(j))
def fun():
    return db.meet.time_in<db.meet.time_out
    
import datetime
db.define_table('meet',
		Field('agenda',unique=True),
		Field('room',requires=IS_IN_SET(a)),
		Field('date_in','date',requires=IS_DATE()),
		Field('time_in','time',requires=IS_TIME()),
		Field('time_out','time',requires=IS_TIME()),
		Field('file','upload'),
	       )
db.meet.requires=fun()>0

    
from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
