





#from pickle import FALSE
#from pydoc import doc
from contextlib import nullcontext
from flask import Flask, request_started, session, render_template, redirect, request, url_for
from flaskext.mysql import MySQL
from pymysql import NULL
from werkzeug.utils import secure_filename
import os
 
mysql = MySQL()


app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0000'
app.config['MYSQL_DATABASE_DB'] = 'user_info'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.secret_key = "ABCDEFG"
mysql.init_app(app)
# STEP 2: MySQL Connection 연결
#con = pymysql.connect(host='localhost', user='root', password='0000',
#                       db='user_info', charset='utf8') # 한글처리 (charset = 'utf8')


class CommonUser:
    myid = 0
    myfollow = 0
    loginuser = NULL
    def __init__(self):
        self.flag = False
        #pass
    def getstatebyid(self,id):
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
       
        
        sql = "SELECT * FROM items where document_id = %s "
        #sql = "select * from users"
        value = (id)
        cursor.execute("set names utf8")
        cursor.execute(sql,value)
        #cursor.execute(sql)
       
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        retval = int(rows[0][8] ) 
        
        return retval
    def getdoucumentid(self,id):
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
       
        
        sql = "SELECT * FROM items where document_id = %s "
        #sql = "select * from users"
        value = (id)
        cursor.execute("set names utf8")
        cursor.execute(sql,value)
        #cursor.execute(sql)
       
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        retval = int(rows[0][4] ) 
        
        return retval
    def getdocumentbyid(self,id):
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
       
        
        sql = "SELECT wrtid, title,content, DATE_FORMAT(wrtdate, '%%Y-%%m-%%d') as wrtdate, document_id, image_path, tag ,state FROM items where document_id = %s "
        #sql = "select * from users"
        value = (id)
        cursor.execute("set names utf8")
        cursor.execute(sql,value)
        #cursor.execute(sql)
       
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        retval = rows 
        
        return retval
    def getlist_search(self,ptext):
        ret = []
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
        #20220516 제목 필터링 title에서 tag 로 
       
       
        sql = "SELECT * FROM items where tag =  %s"
        
        
        #ptext = "%" + ptext + "%"
        #sql = "select * from users"
        value = (ptext)
        cursor.execute("set names utf8")
        cursor.execute(sql,value)
        #cursor.execute(sql)
        #e[7]추가
       
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for e in rows:
            temp = {'wrtid':e[0],'title':e[1],'content':e[2],'wrtdate':e[3], 'document_id':e[4], 'tag':e[7] , 'state':e[8]}
            ret.append(temp)
        
       
        return ret
            
    
    def getlist(self):
        ret = []
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
       
        
        sql = "SELECT * FROM items "
        #sql = "select * from users"
        #value = (id, pw)
        cursor.execute("set names utf8")
        cursor.execute(sql)
        #cursor.execute(sql)
       
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        #e[7]추가
        for e in rows:
            temp = {'wrtid':e[0],'title':e[1],'content':e[2],'wrtdate':e[3], 'document_id':e[4], 'tag':e[7], 'state':e[8] }
            ret.append(temp)
        
       
        return ret
    def getfollowlist(self, id):
        
        ret = []
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
       
        
        sql = "select * from items as i, followers as f where f.id =  %s and i.wrtid = f.follow "
        #sql2 = "select * from items as i, followers as where i.wrtid = f.follow and f.id = " + " '" + id
        #sql = "select * from users
        #session['login_user'] = id
        #id = (session['login_user'])
        
        value = (id)
        cursor.execute("set names utf8")
        cursor.execute(sql,value)
        #cursor.execute(sql)
        #e[7]추가, 8도  
       
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for e in rows:
            temp = {'wrtid':e[0],'title':e[1],'content':e[2],'wrtdate':e[3], 'document_id':e[4],'tag':e[7], 'state':e[8] }
            ret.append(temp)
        
        CommonUser.myfollow = 1
        return ret
        

followobj = CommonUser()

@app.route("/",methods=['GET','POST'])

def dongguk():
    
    '''if request.method == "POST":
        id = request.form['username']
        pw = request.form['password']
        if id!= 'admin' or pw!= 'admin':
            return render_template("login.html")
            
            
        else:
            session['logged_in'] = True
            return render_template("about.html")
            
    return render_template("login.html")#/'''
    error = None
    
 
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        
 
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
       
        
        sql = "SELECT id FROM users WHERE id = %s AND pw = %s"
        #sql = "select * from users"
        value = (id, pw)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
        #cursor.execute(sql)
        
        data = cursor.fetchall()
        cursor.close()
        conn.close()
 
        for row in data:
            data = row[0]
 
        if data:
            session['login_user'] = id
            
            return redirect(url_for('about'))
            #return redirect(url_for('about'))
        else:
            error = 'invalid input data detected !'
    return render_template('login.html', error = error)
@app.route("/guest" ,methods = ['GET', 'POST'])
def guest():
    ccommon2 = CommonUser()
    data = ccommon2.getlist()
    
    error = None
    id = 'guest'
    if request.method == 'POST':
        #팔로우리스트 에서 검색할시. flag 1일시 0 으로 바꾸고 다시 접속 
        #20220516 tag 로 변경 text에서 
        
        if request.form["tag"] != 'none':
            
            data = ccommon2.getlist_search(request.form["tag"])
            error = None
            #id = session['login_user']
            #return redirect(url_for('about'))
            return render_template('guest.html', error = error, name = id, rows = data)
        else:
            
            #data = ccomon.getlist()
            #return redirect(url_for('about'))
            error = None
            data = ccommon2.getlist()
            #id = session['login_user']
            return render_template('guest.html', error = error, name = id, rows = data)
            
    return render_template('guest.html', error = error, name = 'guest', rows = data)
@app.route("/about", methods=['GET', 'POST'])
def about():
    #return render_template("login.html")
    ccomon = CommonUser()
    data = ccomon.getlist()
    #ccomon.flag = True
    
    #if(ccomon.flag):  
    #    data = ccomon.getlist()
    #elif(ccomon.flag is False):
    #    data = ccomon.getlist_search(request.form["text"])
        
    
    # 트루: 전체 펄스: 비전체 
    #retval = ccomon.getdoucumentid(1) 
    if followobj.myfollow == 1:
            error = None
            followobj.myfollow = 0
            data2 = followobj.getfollowlist(session['login_user'])
            return render_template('about.html', error = error, name = session['login_user'], rows = data2)
    if request.method == 'POST':
        #팔로우리스트 에서 검색할시. flag 1일시 0 으로 바꾸고 다시 접속 
        #20220516 tag 로 변경 text에서 
        
        if request.form["tag"] != 'none':
            ccomon.flag = False
            data = ccomon.getlist_search(request.form["tag"])
            error = None
            id = session['login_user']
            #return redirect(url_for('about'))
            return render_template('about.html', error = error, name = id, rows = data)
        else:
            ccomon.flag = True
            #data = ccomon.getlist()
            #return redirect(url_for('about'))
            error = None
            data = ccomon.getlist()
            id = session['login_user']
            return render_template('about.html', error = error, name = id, rows = data)
            
            
        
        
        
    
    
    
    #if request.method == 'POST':
        
        #if request.form["cls"] == "logout":
            #cls 에서바꿈
        
        #    session.pop('login_user',None)
        #    return render_template("login.html")
        #elif request.form["cls"] == "add":
           #return redirect(url_for(seedocument, document_id = retval)) 이건 그냥 주석침 
        #elif request.form["cls"] == "search":
        #    ccomon.flag = False#이거도 search로 바꿈 
        #    return redirect(url_for('about'))
            
            
            
            
        
      
    error = None
    id = session['login_user']
    return render_template('about.html', error = error, name = id, rows = data)
#20220516추가  - 주석 

@app.route("/state",methods = ["GET","POST"]) 
def updstate():
    if request.method == 'POST':
        
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
        para1 = "SOLD"
        sql = "update items set state = %s where document_id = %s "
        if(request.form["state"] == "SOLD"):
            para1 = "SOLD"
        elif(request.form["state"] == "SELLING"):
            para1 = "SELLING"
        else:
            para1 = "SOLD"
            
        #para1 = "SOLD"
        #if(CommonUser.getstatebyid(CommonUser.myid) == "SOLD"):
        #    para1 = "SELLING"
        #elif(CommonUser.getstatebyid(CommonUser.myid) == "SELLING"):
        #    para1 = "SOLD"
        #else:
        #    para1 = "SOLD"
        para2 = CommonUser.myid    
        value = (para1, para2)
        cursor.execute("set names utf8")
        
        cursor.execute(sql, value)
        #cursor.execute(sql)
        
        data = cursor.fetchall()
        if not data:
            conn.commit()
        else:
            conn.rollback()
            return "update failed"    
        cursor.close()
        conn.close()
        #return render_template("about.html")
        return redirect(url_for('about')   )
   
        #para1 = "SOLD"
        #if(CommonUser.getstatebyid(CommonUser.myid) == "SOLD"):
        #    para1 = "SELLING"
        #elif(CommonUser.getstatebyid(CommonUser.myid) == "SELLING"):
        #    para1 = "SOLD"
        #else:
        #    para1 = "SOLD"
    return render_template("statechange.html")           
        
       
            
        #체크체크
    
@app.route("/update", methods = ['GET', 'POST'])
def updateqry():
    if request.method == 'POST':
        
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
        wrtid = session['login_user']
        title = request.form['title']
        content = request.form['content']
        tag = request.form['tag']
        
        #파일업로드 추가부분 
        f = request.files['file']
        f.save('static/uploads/' + secure_filename(f.filename))
        files = os.listdir("static/uploads")
        
        #파일업로드        
        
        #20220516 태그 추가
        
        sql = "update  items set wrtid = %s , title = %s , content = %s , image_path = %s,tag = %s   where document_id = %s;"
        #insert into items (wrtid, title, content) values (%s, %s, %s);
        #tmppath = 'uploads/'+secure_filename(f.filename)
        tmppath = 'static/uploads/'+secure_filename(f.filename)
        value = (wrtid,title,content,tmppath,tag,CommonUser.myid)
        cursor.execute("set names utf8")
        
        cursor.execute(sql, value)
        #cursor.execute(sql)
        
        data = cursor.fetchall()
        if not data:
            conn.commit()
        else:
            conn.rollback()
            return "update failed"    
        cursor.close()
        conn.close()
        return redirect(url_for('about'))
    
    
    
    return render_template('update.html',documentid_forupdate = '<document_id>')
@app.route("/delete", methods = ['GET', 'POST'])
def deleteqry():
    
    
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
     
        sql = "delete from  items where document_id = %s ;"
        #insert into items (wrtid, title, content) values (%s, %s, %s);
        #tmppath = 'uploads/'+secure_filename(f.filename)
        
        value = (CommonUser.myid)
        cursor.execute("set names utf8")
        
        cursor.execute(sql, value)
        #cursor.execute(sql)
        
        data = cursor.fetchall()
        if not data:
            conn.commit()
        else:
            conn.rollback()
            return "delete failed"    
        cursor.close()
        conn.close()
        return redirect(url_for('about'))    
    
        
@app.route("/about/<document_id>", methods=['GET', 'POST'])
def seedocument(document_id):
    
    CommonUser.myid = document_id #저장 
    ccomon2 = CommonUser()
    data2 = ccomon2.getdocumentbyid(document_id)
    path = str(data2[0][5])
    
    #retval2 = ccomon2.getdoucumentid(1)
    #breakpoint()
    #return render_template('content.html', document_id = retval2, row = data2)
    
    
    return render_template('content.html', row = data2, path = path , document_id = document_id)
    



#
@app.route('/about/add' , methods = ['GET','POST'])
def add():
    if request.method == 'POST':
    
        conn = mysql.connect()
        #conn =mysql.connection()
        cursor = conn.cursor()
        wrtid = session['login_user']
        title = request.form['title']
        content = request.form['content']
        #20220516추가
        tag = request.form['tag']
        state = "SELLING"
        #파일업로드 추가부분 
        f = request.files['file']
        f.save('static/uploads/' + secure_filename(f.filename))
        files = os.listdir("static/uploads")
        
        #파일업로드        
        #20220516 tag, 파라미터 추가 , value 에도 추가  state추가 
        sql = "insert into items (wrtid, title, content,  image_path,tag,state) values (%s, %s, %s,%s,%s,%s)"
        #insert into items (wrtid, title, content) values (%s, %s, %s);
        #tmppath = 'uploads/'+secure_filename(f.filename)
        tmppath = 'static/uploads/'+secure_filename(f.filename)
        value = (wrtid, title,content ,tmppath ,tag,state)
        cursor.execute("set names utf8")
        
        cursor.execute(sql, value)
        #cursor.execute(sql)
        
        data = cursor.fetchall()
        if not data:
            conn.commit()
        else:
            conn.rollback()
            return "add failed"    
        cursor.close()
        conn.close()
        return redirect(url_for('about')) 
        
    #return redirect(url_for('add'))
    return render_template('add.html')

    
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        id = request.form['regi_id']
        pw = request.form['regi_pw']
        follow = request.form['follow']
 
        conn = mysql.connect()
        cursor = conn.cursor()
 
        sql = "INSERT INTO users VALUES ('%s', '%s', '%s')" % (id, pw,follow)
        cursor.execute(sql)
 
        data = cursor.fetchall()
 
        if not data:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('dongguk'))
        else:
            conn.rollback()
            cursor.close()
            conn.close()
            
            
            return "register fail"      
 
 
        cursor.close()
        conn.close()
    return render_template('register.html', error=error)
@app.route('/followregister', methods=['GET', 'POST'])
def fregister():
    error = None
    if request.method == 'POST':
        # session['login_user']
        id = request.form['regi_id']
        
        follow = request.form['follow']
 
        conn = mysql.connect()
        cursor = conn.cursor()
 
        sql = "INSERT INTO followers VALUES ('%s',  '%s')" % (id, follow)
        cursor.execute(sql)
 
        data = cursor.fetchall()
 
        if not data:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('dongguk'))
        else:
            conn.rollback()
            cursor.close()
            conn.close()
            
            
            return "follow register fail"      
 
 
        cursor.close()
        conn.close()
    return render_template('followregister.html', error=error)
@app.route('/follow', methods=['GET', 'POST'])
def follow():
    followobj.myfollow = 1
    
    #id = session['login_user']
    #followobj = CommonUser()
    #data = followobj.getfollowlist(id)
    #error = None
    
    return redirect(url_for('about'))
    #return redirect("/about") 
    #return render_template('about.html', error = error, name = id, rows = data)

@app.route("/logout",methods = ['GET','POST'])
def logout():
    session.pop('login_user',None)
    return redirect('/')
    #return render_template("login.html")

if __name__ == '__main__':
    app.run( debug=True)
