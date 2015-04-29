# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def time_greater(a0,a1,b0,b1):
    if a0 > b0:
        return True
    elif a0 == b0 and a1 > b1:
        return True
    else:
        return False
    
def overlapping(st1,sd1,ct1,cd1,st2,sd2,ct2,cd2):
    if time_greater(sd2,st2,sd1,st1) and time_greater(sd2,st2,cd1,ct1):
        return False
    elif time_greater(sd1,st1,cd1,ct1) and time_greater(sd1,st1,cd2,ct2):
        return False
    else:
        return True
    
import datetime
from time import gmtime, strftime

def index():
    return dict()
def Sheduling():
    
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    
    session.wrong=0
    row=db().select(db.meet.ALL,orderby=~db.meet.id)
    if session.newField is 1:
        session.newField=0
        last=row[0]
        if last.time_in < last.time_out and  ((last.date_in > datetime.date.today()) or (last.date_in == datetime.date.today() and (str(last.time_in)>strftime("%H:%M:%S",)))):
            pass
        else:
            db(db.meet.id==last.id).delete()
            session.wrong=1
            redirect(URL('Meeting_sheduling'))
        query=((db.meet.room==last.room)&(~(db.meet.agenda == last.agenda))&(db.meet.date_in==last.date_in)&(~(((db.meet.time_in > last.time_in)&(db.meet.time_in>last.time_out))|((db.meet.time_in<last.time_in)&(db.meet.time_out<last.time_in)))))
        row=db(query).select()
        if row:
            db(db.meet.id==last.id).delete()
            session.wrong=2
            redirect(URL('Meeting_sheduling'))
    
    meets=db(db.meet.date_in <datetime.date.today).select(db.meet.ALL,orderby=db.meet.date_in|db.meet.time_in)
    listeprev=[]
    for i in meets:
        listeprev.append(i)
    listetoday=[]
    meets=db(db.meet.date_in == datetime.date.today).select(db.meet.ALL,orderby=db.meet.date_in|db.meet.time_in)
    for i in meets:
        listetoday.append(i)
    listeupcoming=[]  
    meets=db(db.meet.date_in > datetime.date.today).select(db.meet.ALL,orderby=db.meet.date_in|db.meet.time_in)
    for i in meets:
        listeupcoming.append(i)
    session.wrong=0           
    return dict(meetsprev=listeprev,meetstoday=listetoday,meetsupcoming=listeupcoming)

@auth.requires_login()
def Meeting_sheduling():
    session.newField=1
    form=SQLFORM(db.meet).process(
    next = URL('Sheduling',args=request.args))
    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
