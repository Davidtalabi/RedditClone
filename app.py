from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from helper_functions import salt_password
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
#must add your engine here, i've omitted mine for secruity purposes
engine = create_engine('....')
database=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.secret_key = 'My key'

app.config.from_object(DevelopmentConfig)

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)

sql=text('SELECT title,post,postedby,date_created FROM post')
result=db.engine.execute(sql)
names = [row[0:4] for row in result]



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postedby= db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    post = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

titlez=Post.query.all()




    



@app.route('/login', methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        salted_pass = salt_password(password)
        hashed_pass = bcrypt.generate_password_hash(salted_pass)
        usernamedata=database.execute("SELECT username FROM user WHERE username=:username",{"username":username}).fetchone()
        if usernamedata is None:
             msg='NOT WORKING'
             return render_template('auth/login.html', msg='You have entered an Incorrect Username or Password')
        else:
            msg='WORKING'
            session['loggedin'] = True
            session['username'] = usernamedata['username']
            return render_template('index.html', usernames=names,loggedinaccount=session['username'])
            
    return render_template('auth/login.html', msg='')

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect('login')
    



@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        salted_pass = salt_password(_password)
        hashed_pass = bcrypt.generate_password_hash(salted_pass)

        try:
            new_user = User(username=_username,
                            email=_email,
                            password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
        except:
            print("An error occured creating your account.")
            return redirect('/')
        
        return redirect('login')
        
    return render_template('auth/reg.html')


'''@app.route('/search', methods=['GET','POST'])
def search():
    _search = request.form['search']
    sql=text("SELECT title,post,postedby,date_created FROM post where postedby='"+_search+"'")
    result=db.engine.execute(sql)
        #poster=database.execute("SELECT postedby,title,post FROM post WHERE postedby=:postedby",{"postedby":session['username']}).fetchone()
    posts = [row[0:4] for row in result]
        #userprofile=database.execute("SELECT username,email FROM user WHERE username=:username",{"username":session['username']}).fetchone()
    return redirect('index', usernames=posts,loggedinaccount=session['username'])    
    return render_template('search.html')'''

@app.route('/search', methods=['GET','POST'])
def search():
    msg=''
    if request.method == 'POST':
        search = request.form['search']
        searchh = '%'+search
        searchhh = searchh+'%'
        sql=text("SELECT title,post,postedby,date_created FROM post where post LIKE'"+searchhh+"' or title LIKE'"+searchhh+"'")
        result=db.engine.execute(sql)
        posts = [row[0:4] for row in result]
        if result is None:
             msg='NOT WORKING'
             return render_template('auth/search.html', msg='Search for something!')
        else:
            msg='WORKING'
            #session['loggedin'] = True
            #session['username'] = usernamedata['username']
            return render_template('index.html', usernames=posts,loggedinaccount=session['username'])
            
    return render_template('auth/search.html', msg='')









@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'POST' and 'loggedin' in session:
        _poster=session['username']
        _title = request.form['title']
        _post = request.form['post']

        try:
            new_post = Post(title=_title,
                            post=_post,
                            postedby=_poster)
            db.session.add(new_post)
            db.session.commit()
        except:
            print("An error occured creating your post.")
            return redirect('/')
        
        return redirect('/')
        
    return render_template('auth/newpost.html')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        currentuser=session['username']
        sql=text("SELECT postedby,title,post,date_created FROM post where postedby='"+currentuser+"'")
        result=db.engine.execute(sql)
        #poster=database.execute("SELECT postedby,title,post FROM post WHERE postedby=:postedby",{"postedby":session['username']}).fetchone()
        posts = [row[0:4] for row in result]
        #userprofile=database.execute("SELECT username,email FROM user WHERE username=:username",{"username":session['username']}).fetchone()
        return render_template('profile.html', postedbys=posts, usernames=names,loggedinaccount=session['username'],userprofile=database.execute("SELECT username,email,date_created FROM user WHERE username=:username",{"username":session['username']}).fetchone())
    else:
        return redirect('login')



@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('index.html', usernames=names,loggedinaccount=session['username'])
    else:
        return redirect('login')

if __name__ == '__main__':
    app.run(debug=True)
