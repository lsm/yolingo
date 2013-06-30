#Quiz
import json
import random



randomList = ['Redistribute', 'Sample', 'Fresh', 'Slowly', 'Feature',
              'Exemplify', 'Click', 'Happen', 'Laugh', 'Creation',
              'Challenging', 'Compete', 'Technology', 'Drenched', 'Scale',
              'Twine', 'Destination', 'Broad', 'Worth', 'Questionable',
              'Maroon', 'Stylish', 'Port', 'Nested', 'Martyr', 'Validate',
              'Balloon', 'Born', 'Offend', 'Stable', 'Label', 'Connect',
              'People', 'Attraction', 'Severely', 'Gigantic', 'Establishment',
              'Mental', 'Evaluate', 'Grand', 'Yell', 'Posing', 'Rounded',
              'Design', 'Fail', 'Milk', 'Golden', 'Celestial', 'Test',
              'Contact', 'Return', 'Above', 'Exist', 'Adjoining', 'Grew',
              'Stepped', 'Entering', 'Bright', 'Competitive', 'Environment',
              'Government', 'Rested']

class Quiz():
    def __init__(self, wordlist, randomlist):
        self.list = wordlist
        self.rand = randomlist
        

    def genRandom(self, word):
        if word in self.list:
            list2 = random.sample(self.rand, 5)
            return list2

            
        else:
            return json.dumps({'Error': 'Word not in user word list'})


