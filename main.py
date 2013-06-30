import webapp2
import jinja2
import urllib2
import json
import hashlib
import random
import uuid
import os
import cgi

from google.appengine.ext import db
from microsofttranslator import Translator

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def translate(text):
    translator = Translator('YoLingoApp2', '4D6+ku6Be8JmzmfD26mJj4yp+xHvxu1I782n9IA3tLI=')
    return translator.translate(text, "en").lower()

class User(db.Model): #needs fields for authentication
    word_list = db.StringListProperty()
    points = db.IntegerProperty()

class Quiz(db.Model): #timestamp all database models
    word = db.StringProperty()
    translation = db.StringProperty()
    choices = db.StringListProperty()
    answer = db.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class Reader(webapp2.RequestHandler):
    def get(self):
        url = "http://www.readability.com/api/content/v1/parser?url=" + self.request.get('url') + "&token=3df59e199a9dd1ffcd0794419776004b1cf97407"
        data = urllib2.urlopen(url).read()
        parsed = json.loads(data) #decode JSON from readability
        template = jinja_environment.get_template('reader.html')
        template_values = {
            'title' : parsed['title'],
            'article' : parsed['content']
        }
        self.response.out.write(template.render(template_values))

class AJAXTranslate(webapp2.RequestHandler):
    def get(self):
        text = self.request.get('text')
        #self.response.out.write("{Success: true, Translation: '" + translate(text)+ "'}")
        self.response.out.write(translate(text).lower())
        user = db.get("agpzfnlvLWxpbmdvcgoLEgRVc2VyGAEM")
        if text not in user.word_list:
            user.word_list.append(text.lower()) #transparently add word to word list
            user.put()

class AJAXQuiz(webapp2.RequestHandler):
    def get(self):
        random_list = ['redistribute', 'sample', 'fresh', 'slowly', 'feature',
            'exemplify', 'click', 'happen', 'laugh', 'creation',
            'challenging', 'compete', 'technology', 'drenched', 'scale',
            'twine', 'destination', 'broad', 'worth', 'questionable',
            'maroon', 'stylish', 'port', 'nested', 'martyr', 'validate',
            'balloon', 'born', 'offend', 'stable', 'label', 'connect',
            'people', 'attraction', 'severely', 'gigantic', 'establishment',
            'mental', 'evaluate', 'grand', 'yell', 'posing', 'rounded',
            'design', 'fail', 'milk', 'golden', 'celestial', 'test',
            'contact', 'return', 'above', 'exist', 'adjoining', 'grew',
            'stepped', 'entering', 'bright', 'competitive', 'environment',
            'government', 'rested'] #read from file in future
        user = db.get("agpzfnlvLWxpbmdvcgoLEgRVc2VyGAEM") #this should get the user's login
        text = self.request.get('text')
        if text not in user.word_list:
            self.error('416') #out of range error
            self.response.out.write("{Success: false, Error: 'This word is not in the word list'}")
        else:
            translation = translate(text).lower()
            answer_list = random.sample(random_list, 4)
            answer_list.append(translation)
            random.shuffle(answer_list)
            response = {
                'Success' : True,
                'Text' : text,
                #'translation' : translation,
                'Choices' : answer_list
                #'answer' : answer_list.index(translation)
            }
            self.response.out.write(json.dumps(response))
            quiz = Quiz(choices=answer_list, answer=translation, word=text, translation=translation)
            quiz.put()

class AJAXAnswer(webapp2.RequestHandler):
    def get(self):
        text = self.request.get('text')
        answer = self.request.get('ans')
        results = db.GqlQuery("SELECT * FROM Quiz WHERE word = :1", text)
        exists = False
        for result in results:
            quiz = result
            exists = True
        if not exists:
            self.response.out.write("{Success: false, Error: 'There is no active quiz for that word'}")
            return
        if answer == quiz.answer:
            response = {
                'Success' : True,
                'Correct' : True,
            }
        else:
            response = {
                'Success' : True,
                'Correct' : False,
                'Answer' : quiz.answer
            }
        self.response.out.write(json.dumps(response))
        quiz.delete()

class CreateUser(webapp2.RequestHandler): #for debug purposes
    def get(self):
        user = User(word_list=[], points=0)
        user.put()
        self.response.out.write("User created")

app = webapp2.WSGIApplication([ #use the webapp2 Route API to cut down on this
    ('/', MainHandler),
    ('/reader', Reader),
    ('/ajax/translate', AJAXTranslate),
    ('/ajax/quiz', AJAXQuiz),
    ('/ajax/answer', AJAXAnswer),
    ('/ajax/translate', AJAXTranslate),
    ('/admin/createuser', CreateUser)
], debug=True)
