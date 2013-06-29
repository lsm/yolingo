import webapp2
import jinja2
import hashlib
import uuid
import os
import cgi

from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if login_check(self.request.cookies):
            template = jinja_environment.get_template('logged_in.html')
        else:
            template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class Auth(webapp2.RequestHandler):
    def post(self):
        username = cgi.escape(self.request.get('username'))
        password = self.request.get('password')
        if self.request.get('action') == 'login':
            auth_token = login(username, password)
            if type(auth_token) == int:
                self.redirect('/login?fail=' + auth_token)
                return
        elif self.request.get('action') == 'signup':
            error = create_user(username, password)
            if type(error) == int:
                self.redirect('/signup?fail=' + error)
                return
            auth_token = login(username, password)
        else:
            self.redirect('/')
            return
        self.response.headers.add_header('Set-Cookie', str('username=' + username + ";expires=Sun, 30-Dec-2017 23:59:59 GMT;"))
        self.response.headers.add_header('Set-Cookie', str('auth_token=' + auth_token + ";expires=Sun, 30-Dec-2017 23:59:59 GMT;"))
        template = jinja_environment.get_template('logged_in.html')
        self.response.out.write(template.render())

class Register(webapp2.RequestHandler):
    def get(self):
        errors = ("That username has already been taken")
        self.response.out.write(errors[self.request.get('fail')])

class Login(webapp2.RequestHandler):
    def get(self):
        errors = ("That username does not exist.", "That is the incorrect password for that account.")
        self.response.out.write(errors[self.request.get('fail')])

def login(username, password):
    results = db.GqlQuery("SELECT * FROM User WHERE username = :1", username)
    exists = False
    for result in results:
        user = result
        exists = True
    if not exists:
        return 0 #user does not exist
    secured_password = hashlib.sha512(password + user.salt).hexdigest()
    if secured_password != user.secured_password:
        return 1 #password is incorrect
    auth_token = str(uuid.uuid1())
    user.auth_tokens.append(auth_token)
    user.put()
    return auth_token

def create_user(username, password):
    results = db.GqlQuery("SELECT * FROM User WHERE username = :1", username)
    duplicate = False
    for result in results:
        duplicate = True
    if duplicate:
        return 0 #user already exists
    auth_token = str(uuid.uuid1())
    auth_tokens = [str(auth_token)]
    salt = str(uuid.uuid1())
    secured_password = hashlib.sha512(password + salt).hexdigest()
    user = User(username=username, secured_password=secured_password, salt=salt, auth_tokens=auth_tokens, word_list=[], word_confidence=[], points=0)
    user.put()
    return ""

def login_check(cookies):
    username = cookies.get('username')
    auth_token = cookies.get('auth_token')
    results = db.GqlQuery("SELECT * FROM User WHERE username = :1", username)
    exists = False
    for result in results:
        user = result
        exists = True
    if exists:    
        if auth_token in user.auth_tokens:
            return user
    else:
        return 0 #bad cookie

class User(db.Model):
    username = db.StringProperty()
    secured_password = db.StringProperty()
    salt = db.StringProperty()
    auth_tokens = db.StringListProperty()
    create_time = db.DateTimeProperty(auto_now_add=True)
    word_list = db.StringListProperty()
    word_confidence = db.ListProperty(long)
    points = db.IntegerProperty()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/auth', Auth),
    ('/register', Register),
    ('/login', Login)
], debug=True)