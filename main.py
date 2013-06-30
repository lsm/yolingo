import webapp2
import jinja2
import urllib2
import json
import hashlib
import uuid
import os
import cgi

from google.appengine.ext import db
from microsofttranslator import Translator

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class User(db.Model):
    word_list = db.StringListProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class Reader(webapp2.RequestHandler):
    def get(self):
        url = "http://www.readability.com/api/content/v1/parser?url=" + self.request.get('url') + "&token=3df59e199a9dd1ffcd0794419776004b1cf97407"
        data = urllib2.urlopen(url).read()
        parsed = json.loads(data)
        template = jinja_environment.get_template('reader.html')
        template_values = {
            'title' : parsed['title'],
            'article' : parsed['content']
        }
        self.response.out.write(template.render(template_values))

class AJAXTranslate(webapp2.RequestHandler):
    def get(self):
        text = self.request.get('text')
        translator = Translator('YoLingoApp', 'ArNe8ZslXG7fKZmKf22lUGCFhEDp22sSxuKZ1d64H84=')
        self.response.out.write(translator.translate(text, "en"))

class AJAXQuiz(webapp2.RequestHandler):
    def get(self):
        pass

class AJAXAnswer(webapp2.RequestHandler):
    def get(self):
        pass

class CreateUser:
    user = User(word_list=[])
    user.put()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/reader', Reader),
    ('/ajax/translate', AJAXTranslate),
    ('/ajax/quiz', AJAXQuiz),
    ('/ajax/answer', AJAXAnswer),
    ('/admin/createuser', CreateUser)
], debug=True)