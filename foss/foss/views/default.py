from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc

from ..models import MyModel
from ..models import User
from ..models import Comment
from ..models import Count
from ..models import Total

import hashlib
import datetime
import time

uname = "admin"
@view_config(route_name='home', renderer='../templates/homepage.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'foss-blog'}

@view_config(route_name='log', renderer='../templates/login.jinja2')
def my_login(request):
    return {}

@view_config(route_name='user', renderer='../templates/userpage.jinja2')
def my_user(request):
    global uname
    uname = request.params['username']
    pwd = request.params['pswd']
    hash_obj = hashlib.md5(pwd.encode())
    m = hash_obj.hexdigest()
    query = request.dbsession.query(User)
    one = query.filter(User.username == uname, User.password == m).first()
    if one:
        return {'one': one}
    else:
        return Response("<h3>Check user name and password&nbsp;&nbsp;&nbsp;&nbsp;<a href='/login'>Login</a></h3>")

@view_config(route_name='post', renderer='../templates/post.jinja2')
def my_post(request):
    global uname
    query = request.dbsession.query(User)
    one=query.filter(User.username == uname).first()
    return {'one':one}

@view_config(route_name='view', renderer='../templates/view.jinja2')
def my_comment(request):
    global uname
    obj=request.dbsession.query(Comment).order_by(desc(Comment.datetime)).all()
    print(obj[0].email)
    return {'length':len(obj),'obj':obj}

@view_config(route_name='signup', renderer='../templates/signup.jinja2')
def my_signup(request):
    return {}

@view_config(route_name='adlogin', renderer='../templates/adlogin.jinja2')
def my_adlogin(request):
    return {}

@view_config(route_name='admin', renderer='../templates/admin.jinja2')
def my_admin(request):
    uname = request.params['username']
    pwd = request.params['pswd']
    if(uname == 'admin@gmail.com' and  pwd == 'admin'):
        obj=request.dbsession.query(Total).filter().order_by(desc(Total.tot)).first()
        ld=request.dbsession.query(Count).filter(Count.topic == 'Linux Distributions').order_by(desc(Count.count)).first()
        web=request.dbsession.query(Count).filter(Count.topic == 'Open Source Web Development Tools').order_by(desc(Count.count)).first()
        nw=request.dbsession.query(Count).filter(Count.topic == 'Open Source Networking Tools').order_by(desc(Count.count)).first()
        ml=request.dbsession.query(Count).filter(Count.topic == 'Open Source Machine Learning Tools').order_by(desc(Count.count)).first()
        mm=request.dbsession.query(Count).filter(Count.topic == 'Open Source Multimedia Tools').order_by(desc(Count.count)).first()
        return {'obj':obj , 'ld' : ld , 'web':web , 'nw': nw , 'ml': ml , 'mm' : mm}
    

    else:
        return render_to_response('../templates/adlogin.jinja2',{'message':'Access denied!!!Incorrect password'},request=request)

    


@view_config(route_name='account', renderer='../templates/userpage.jinja2')
def my_account(request):
    global uname
    query = request.dbsession.query(User)
    one=query.filter(User.username == uname).first()
    return {'one':one}



@view_config(route_name='register', renderer='../templates/login.jinja2')
def signup1(request):
    global uname
    uname = request.params['username']
    pwd = request.params['pswd']
    query = request.dbsession.query(User)
    one = query.filter(User.username == uname).all()
    hash_obj = hashlib.md5(pwd.encode())
    m = hash_obj.hexdigest()
    length=len(one)
    if one:
        return Response("<h3>'Username '+user+' already exists . Try another name.'&nbsp;&nbsp;&nbsp;&nbsp;<a href='/signup'>Signup</a></h3>")
    else:
        model = User(username = uname, password = m)
        request.dbsession.add(model)
        q = request.dbsession.query(Count)
        rec = Count(name = uname, count=0 ,topic = 'Linux Distributions')
        request.dbsession.add(rec)
        rec = Count(name = uname, count=0 ,topic = 'Open Source Web Development Tools')
        request.dbsession.add(rec)
        rec = Count(name = uname, count=0 ,topic = 'Open Source Networking Tools')
        request.dbsession.add(rec)
        rec = Count(name = uname, count=0 ,topic = 'Open Source Machine Learning Tools')
        request.dbsession.add(rec)
        rec = Count(name = uname, count=0 ,topic = 'Open Source Multimedia Tools')
        request.dbsession.add(rec)
        q1 = request.dbsession.query(Count)
        rec = Total(name = uname, tot=0)
        request.dbsession.add(rec)
        return {'one': one}

@view_config(route_name='postcomment')
def my_postcomment(request):
    global uname
    query = request.dbsession.query(Comment)
    mail = request.params['email']
    tp = request.params['topic']
    cmnt = request.params['comment']
    dt = datetime.datetime.now()
    model = Comment(email = mail, topic = tp,comment = cmnt,datetime = dt)
    request.dbsession.add(model)
    q = request.dbsession.query(Count)
    obj = q.filter(Count.name == mail , Count.topic == tp).first()
    obj.count=obj.count+1
    q1 = request.dbsession.query(Total)
    obj1 = q1.filter(Total.name == mail).first()
    obj1.tot=obj1.tot+1
    return Response("<h3>Thank you for posting Comment&nbsp;&nbsp;&nbsp;&nbsp;<a href='/post'>Back</a></h3>")

@view_config(route_name='request', renderer='../templates/requestcomment.jinja2')
def requestView(request):
    global uname
    query = request.dbsession.query(User)
    one=query.filter(User.username == uname).first()
    obj=request.dbsession.query(Comment).order_by(desc(Comment.datetime)).all()
    return {'one':one,'obj':obj}


@view_config(route_name='viewcomment', renderer='../templates/viewcomment.jinja2')
def viewcomment(request):
    query = request.dbsession.query(User)
    one=query.filter(User.username == uname).first()
    #items = request.dbsession.query(Comment).all()
    topic = request.params['topic']
    content=request.dbsession.query(Comment).filter(Comment.topic == topic)
    return {'content':content,'one':one}
    #return {'length':len(content),'content':content,'one':one}
    


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_foss_db" script
    to initialize your database tales.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
