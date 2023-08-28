import datetime
import gc
#import matplotlib
#matplotlib.use('Agg')
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
#import Family
#from Family import *
#import networkx as nx
#from Tree import hierarchy_pos
#import matplotlib.image as mpimg
#import io
#from flask import Response
#import matplotlib.pyplot as plt
#import base64
from functools import wraps
from wtforms import Form, StringField, EmailField, PasswordField, validators
import os
import uuid
from werkzeug.utils import secure_filename
from dbhandler import connection
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.secret_key = 'welcome'
'''
familyList = []
global uname
ax = plt.gca()
fig = plt.gcf()
trans = ax.transData.transform
trans2 = fig.transFigure.inverted().transform
imsize = 0.1
label_pos = 0.5

def displayImage(name,image,pos):
    img = mpimg.imread('C:/Users/prems/OneDrive/Documents/FamilyTree/static/users/'+image)
    (x1,y1) = pos[name]
    (x2,y2) = pos[image]
    (x,y) = (x1 * label_pos  * (1.0 - label_pos),
             y1 * label_pos + y2 * (1.0 - label_pos))
    xx,yy = trans((x,y)) # figure coordinates
    xa,ya = trans2((xx,yy)) # axes coordinates
    #imsize = G[n1][n2]['size']
    a = plt.axes([xa-imsize/2.0,ya-imsize/2.0, imsize, imsize ])
    a.imshow(img)
    a.set_aspect('equal')
    a.axis('off')
    
'''
def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("you need to log in first")
            return redirect(url_for('login'))
    return wrap


@app.route("/logout/")

@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html')

@app.errorhandler(405)
def method_not_found(e):
    return render_template('405_error.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    
    if 'username' in session:
        uname = session['username']
        return render_template('index.html', msg='',uname=uname)
    else:
        return render_template('index.html', msg='',uname='')
        

@app.route('/shareTree', methods=['POST'])
@login_required
def shareTree():
    global uname
    c, conn = connection()
    uname = session['username']
    print(uname)
    c.execute(f"select uid from users where username='{uname}'")
    userid = c.fetchone()[0]
    print(userid)
    if request.method == 'POST':
        email = request.form['emailAddr']
        treeid = userid

        query = f"select * from tree_access where user_email='{email}' and tree_id = {treeid}"
        c.execute(query)
        init_rows = c.fetchone()
        if init_rows and len(init_rows) > 0:
            flash(f"Tree is already Shared with {email}")
            c.close()
            conn.close()
            return redirect(url_for('index'))
        query = f"select uid from users where email='{email}'"
        print(query)
        c.execute(query)
        rows = c.fetchone()
        newuser = True
        shareuserId = 0
        if rows and len(rows) > 0:
            shareuserId = rows[0]
            newuser = False
        if newuser:
            access_details = (treeid, email)
            query = "insert into tree_access(tree_id, user_email)" \
                " values (%s,%s)"
            id= c.execute(query,access_details)
        else:
            access_details = (treeid, email, shareuserId)
            query = "insert into tree_access(tree_id, user_email, user_id)" \
                " values (%s,%s,%s)"
            id= c.execute(query,access_details)
        flash(f"Tree Shared with {email}")
        conn.commit()
        c.close()
        conn.close()
        # sendmail(email)
        return redirect(url_for('index'))



@app.route('/SearchTree', methods=['GET', 'POST'])
@login_required
def SearchTree():
    uname = session['username']
    return render_template('SearchTree.html', msg='',uname=uname)


@app.route('/SearchTreeAction', methods=['GET', 'POST'])
@login_required
def SearchTreeAction():
    global familyList
    global uname
    c, conn = connection()
    uname = session['username']
    print(uname)
    c.execute(f"select uid from users where username='{uname}'")
    userid = c.fetchone()[0]
    print(userid)
    if request.method == 'POST':
        person = request.form['t1']
        query = f'''
        select  CONCAT_WS(' ', firstname,lastname) as name,imgPath,(select CONCAT_WS(' ', firstname,lastname) from persons where personID=p1.partnerID) as partnername,
        (select CONCAT_WS(' ', firstname,lastname) from persons where personID=p1.fatherID) as fatherName,(select CONCAT_WS(' ', firstname,lastname) from persons 
        where personID=p1.motherID) as motherName,if(gender='f','Female','Male') as gender,birth,if(death='1009-01-01','',death) death,personID,birthcountry,birthcity,
        birthaddress,marital_status from persons p1 where  userID = '{userid}' and (firstname like '%{person}%' or lastname like '%{person}%' 
        or Concat(firstname,' ',lastname) like '%{person}%' or birthcountry like '%{person}%' or birthcity like '%{person}%' 
        or birthaddress like '%{person}%' or marital_status like '%{person}%' )'''
        print(query)
        c.execute(query)
        pdata = c.fetchall()
        font = "<font size='3' color='black'>" 
        output = ""
        for value in pdata:
            output+=f"<tr><td><button class='btn' onclick='editUser({value[8]})' ><i class='fa fa-pencil'></i></button>"+"</td>"
            output+="<td>"+font+f"{value[0]}"+"</font></td>"
            output+="<td>"+font+f"{value[5]}"+"</font></td>"
            output+="<td>"+font+f"{value[2]}"+"</font></td>"
            output+="<td>"+font+f"{value[3]}"+"</font></td>"
            output+="<td>"+font+f"{value[4]}"+"</font></td>"
            output+="<td>"+font+f"{value[6]}"+"</font></td>"
            output+="<td>"+font+f"{value[7]}"+"</font></td>"
            output+="<td>"+font+f"{value[9]}"+"</font></td>"
            output+="<td>"+font+f"{value[10]}"+"</font></td>"
            output+="<td>"+font+f"{value[11]}"+"</font></td>"
            output+="<td>"+font+f"{value[12]}"+"</font></td>"
            output+="<td><img src="+f"{value[1]}"+" height='100' width='100'/></td><tr>"
        c.close()
        conn.close()
        return render_template('ViewSearch.html', msg=output,uname = uname)         

@app.route('/editRelation', methods=['GET'])
@login_required
def EditRelation():
    global uname
    c, conn = connection()
    uname = session['username']
    userid = request.args.get('id')
    c.execute(f"select firstname,lastname,birth, death from persons where personId='{userid}'")
    user = c.fetchone()
    if user is None:
        return render_template('SearchTree.html', msg='',uname=uname)
    firstname = user[0]
    lastname = user[1]
    birth = user[2]
    death = user[3]
    birth = birth.strftime("%d-%b-%Y")
    if death!= "-":
        death = death.strftime("%d-%b-%Y")
    return render_template('EditRelation.html', firstname=firstname,lastname=lastname,birth=birth,death=death,uname = uname,user=userid)  


@app.route('/EditAction', methods=['POST'])
def EditAction():
    global familyList
    global uname
    form = request.form
    if request.method == 'POST':
        personId =   request.form['t9']
        firstname_u = request.form['t1']
        lastname_u = request.form['t7']
        dob_u = request.form['t3']
        dod_u = request.form['t4']
        imgpath_u = request.files['t5']

        c, conn = connection()
        uname = session['username']
        c.execute(f"select firstname,lastname,birth,  death,imgPath from persons where personId='{personId}'")
        user = c.fetchone()
        firstname_o = user[0]
        lastname_o = user[1]
        dob_o = user[2]
        dod_o = user[3]
        imgpath_o = user[4]

        dob_u = datetime.datetime.strptime(dob_u,'%d-%b-%Y')
        if dod_u != '-':
            dod_u = datetime.datetime.strptime(dod_u,'%d-%b-%Y')
        else:
            dod_u = datetime.datetime.strptime("01-JAN-1009",'%d-%b-%Y')
        if imgpath_u:
            filename = uuid.uuid4().hex  + '.' + secure_filename(imgpath_u.filename).split('.')[-1]
            imgpath_u.save(os.path.join(app.root_path, 'static', 'relationImages', filename ))
            imgpath_u = F"/static/relationImages/{filename}"
        else:
            imgpath_u = imgpath_o
        person_details = (firstname_u,lastname_u, dob_u, dod_u, imgpath_u,personId)
        query = "update  persons set firstname=%s,lastname=%s,birth=%s,death=%s,imgPath=%s " \
                " where personID =%s"
        id= c.execute(query,person_details)
        conn.commit()
        flash("Person details Updated!")
        return redirect(url_for('SearchTree'))


@app.route('/DefineRelation', methods=['GET', 'POST'])
@login_required
def DefineRelation():
    global uname
    c, conn = connection()
    uname = session['username']
    print(uname)
    c.execute(f"select uid from users where username='{uname}'")
    userid = c.fetchone()[0]
    print(userid)
    c.execute(f"select * from persons where userID = '{userid}'")
    rows = c.fetchall()
    if len(rows) > 0:
        query = f"select personID, firstname,lastname from persons where gender='f' and userID = '{userid}'"
        c.execute(query)
        mdata = c.fetchall()
        mothers = mdata
        query = f"select personID, firstname, lastname from persons where gender='m' and userID = '{userid}'"
        c.execute(query)
        fdata = c.fetchall()
        fathers = fdata
        c.close()
        conn.close()
        return render_template('DefineRelation.html',mothers=mothers,fathers=fathers, hof = "False",uname=uname)
    else:
        c.close()
        conn.close()
        return render_template('DefineRelation.html',mothers=[],fathers=[],hof = "True",uname=uname)

@app.route('/ViewTree/<treeid>', methods=['GET', 'POST'])
@app.route('/ViewTree', methods=['GET', 'POST'])
@login_required
def DisplayMapping(treeid= None):
    global uname
    c, conn = connection()
    uname = session['username']
    c.execute(f"select uid from users where username='{uname}'")
    userid = c.fetchone()[0]
    print(userid)
    if treeid is None:
        treeid = userid
    query2 = f"select personID, firstname,lastname,fatherID,motherID,partnerID,imgPath from persons where userID={treeid}"
    c.execute(query2)
    reldata = c.fetchall()
    relations = []
    for x in reldata:
        ob = {
            "id" : x[0],
            "name": f"{x[1]} {x[2]}",
            "pids": [x[5]],
            "fid": x[3],
            "mid": x[4],
            "img": x[6]
        }

        if x[5] == 0:
            del ob['pids']
        if x[3] == 0:
            del ob['fid']
        if x[4] ==0:
            del ob['mid']
        relations.append(ob)
    r = relations
    for re in relations:
        r1 = re
        while True:
            if "fid" in r1.keys():
                iid = r1['id']
                fid = r1['fid']
                idx_f = find(r , "id" , fid)
                idx_c = find(r , "id" , iid)
                item = r[idx_f]
                if idx_f > idx_c:  
                    ne_i = idx_c - 1
                    if ne_i < 0 :
                        ne_i = 0
                    r.remove(item)
                    r.insert(ne_i, item)
                r1 = item
                if "fid" not in r1.keys():
                    break

            else:
                break
    print(r)
  
    trees = []
    query2 = f"select username,tree_id from tree_access t, users u where user_id={userid} and t.tree_id = u.uid;"
    c.execute(query2)
    trees = c.fetchall()
    trees.insert(0 , ('My',userid))
    c.close()
    conn.close()
    if treeid is None:
        treeid = userid
    trees2 = []
    for t in trees:
        t1 = list(t)
        if t1[1] == int(treeid):
            t1.append('True')
        else:
            t1.append('False')
        trees2.append(t1)
    print(trees2)
    return render_template('ViewTree.html',mothers=[],fathers=[],relations=r, trees=trees2, treeid=treeid,uname=uname)

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

@app.route('/getTree', methods=['POST'])
@login_required
def getTree():
    if request.method == 'POST':
        treeid = request.form['tree']
        return redirect(url_for('DisplayMapping',treeid=treeid))

@app.route('/getRelationData', methods=['GET'])
def getRelationData():
    global uname
    c, conn = connection()
    uname = session['username']

    c.execute(f"select uid from users where username='{uname}'")
    userid = c.fetchone()[0]
    print(userid)
    query2 = f"select personID, firstname,lastname,gender,birth,fatherID,motherID,partnerID,imgPath from persons where userID={userid}"
    c.execute(query2)
    reldata = c.fetchall()
    relations = []
    for x in reldata:
        ob = {
            "id" : x[0],
            "pid": x[7],
            "fid": x[5],
            "mid": x[6]
        }
        relations.append(ob)
    return jsonify(relations)
'''
@app.route('/checkRelations', methods=['POST'])
def validateRelation():
    print(request.form)
    gender = request.form['gender']
    relaion = request.form['relation']
    fid = request.form['fid']
    mid = request.form['mid']
    return({"message":"RELATION ERROR"},500)
'''



@app.route('/DefineAction', methods=['GET', 'POST'])
def DefineAction():
    global familyList
    global uname
    form = request.form
    if request.method == 'POST':
        person = request.form['t1']
        gender = request.form['t2']
        father = request.form['father']
        mother = request.form['mother']
        dob = request.form['t3']
        dod = request.form['t4']
        relation = request.form['t6']
        imgpath = request.files['t5']
        lastname = request.form['t7']
        filename = uuid.uuid4().hex  + '.' + secure_filename(imgpath.filename).split('.')[-1]
        imgpath.save(os.path.join(app.root_path, 'static', 'relationImages', filename ))
        imgPath = F"/static/relationImages/{filename}"
        binaryData = imgpath.read()

        birthcountry = request.form['bcountry']
        # birthstate = request.form['bstate']
        birthcity = request.form['bcity']
        birthaddress = request.form['baddress']

        marital_status = request.form['marital_status']

        c, conn = connection()
        uname = session['username']

        c.execute(f"select uid from users where username='{uname}'")
        userid = c.fetchone()[0]
        print("userid ",userid)
        if father !='none':
            fatherid = father
        else:
            fatherid = 0
        if mother !='none':
            motherid = mother
        else:
            motherid = 0

        if relation == 'p':
            if gender == 'm':
                partnerID = motherid
                motherid = 0
                fatherid = 0
            elif gender == 'f':
                partnerID = fatherid
                motherid = 0
                fatherid = 0
        else:
            partnerID = 0

        if relation == 'f':
            if fatherid != 0:
                childId = fatherid
                fatherid = 0
            if motherid != 0:
                childId = motherid
                motherid = 0

        if relation == 'p':
            pass
        elif relation == 'c':
            pass

        #print (person, gender, dob, dod, image, fatherid, motherid, userid)
        dob = datetime.datetime.strptime(dob,'%d-%b-%Y')
        if dod != '-':
            dod = datetime.datetime.strptime(dod,'%d-%b-%Y')
        else:
            dod = datetime.datetime.strptime("01-JAN-1009",'%d-%b-%Y')
        dob = datetime.datetime.strftime(dob,"%Y-%m-%d")
        dod = datetime.datetime.strftime(dod, "%Y-%m-%d")

        person_details = (person,lastname, gender, dob, dod,  fatherid, motherid, userid,partnerID,imgPath,
                          birthcountry,birthcity,birthaddress,marital_status)
        query = "insert into persons(firstname,lastname,gender,birth,death,fatherID,motherID,userID,partnerID,imgPath," \
                "birthcountry,birthcity,birthaddress,marital_status)" \
                " values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print("Before exec",query,person_details)
        c.execute(query,person_details)
        print("After exec")
        if relation == 'p':
            id = c.lastrowid
            q2 = f"update persons set partnerID={id} where personID={partnerID}"
            print(q2)
            c.close()
            conn.close()
            c, conn = connection()
            c.execute(q2)
            q3 = f"select personID from persons where fatherID={partnerID}"
            c.execute(q3)
            chid = c.fetchone()[0]
            if chid:
                q4 = f"update persons set motherID={id} where personID={chid}"
                c.execute(q4)
        if relation == 'f':
            id = c.lastrowid
            q2 = f"update persons set fatherID={id} where personID={childId}"
            c.execute(q2)
        conn.commit()
        print("Person details inserted!")
        flash("Family details added!")
        return redirect(url_for('DefineRelation'))

class RegisterationForm(Form):
    username = StringField('Username',[validators.Length(min=4,max=20)])
    email = EmailField('Email',[validators.InputRequired()])
    password = PasswordField('Password',[validators.InputRequired(),validators.EqualTo('confirm', message="Password must match")])
    confirm = PasswordField('Repeat Password')
        
@app.route('/login/', methods=['GET', 'POST'])
def login():
    error=None
    try:
        c, conn = connection()
        if request.method == 'POST':
            ip_username = request.form['username']
            c.execute(f"select * from users where username='{ip_username}'")
            passwd = c.fetchone()[2]

            if passwd:
                # decrypting the password
                if sha256_crypt.verify(request.form['password'],passwd):
                    session['logged_in'] = True
                    session['username'] = ip_username
                    session['message'] = "Welcome"+str(ip_username)
                    flash(f"You are Logged in {ip_username}")

                    return redirect(url_for('index'))
                else:
                    error = 'Invalid credentials Try Again !'
            else:
                error = "couldn't find username!!"
            return render_template('login.html', error=error)
        else:
            return render_template('login.html')

    except Exception as e:
        error = f'Bad data Try Again ! {e}'
        return render_template('login.html',error=error)

@app.route('/register/',methods=['GET','POST'])
def register_page():
    try:
        form = RegisterationForm(request.form)
        print("Before IF")
        if request.method == "POST" and form.validate():
            uname = form.username.data
            ipemail = form.email.data
            # for encrypting the password
            passwd = sha256_crypt.hash(form.password.data)

            c, conn = connection()
            query = "select * from users where username=%s"
            print(query)
            data = c.execute(query,(uname,))
            print(data)
            if data:
                flash("That username is already taken, please chose another one")
                c.close()
                conn.close()
                return render_template('register.html',form=form)
            else:
                c.execute("INSERT INTO users (username,password,email) values (%s,%s,%s)",(uname,passwd,ipemail))
                userid = c.lastrowid
                query = f"select id from tree_access where user_email='{ipemail}'"
                c.execute(query)
                rows = c.fetchall()
                if rows and len(rows) > 0:
                    for row in rows:
                        query = f"UPDATE tree_access set user_id = {userid} where id = {row[0]} "
                        c.execute(query)
                conn.commit()
                print("Thanks for the Sign Up !")
                flash("Thanks for the Sign Up !")
                c.close()
                conn.close()
                #session['logged_in'] = True
                session['username'] = uname
                return redirect(url_for('index'))
        else:
            return render_template('register.html',form=form)

    except Exception as e:
        return (str(e))


if __name__ == '__main__':
        app.run(debug=True)













