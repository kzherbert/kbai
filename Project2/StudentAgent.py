"""
Project 2

ADD YOUR CODE HERE

Please read project directions before importing anything
"""
import json
from Sentence import Sentence
from Phrase import QPhrase, MVPhrase, AVPhrase, AAVPhrase, QPhrase, SubjPhrase, ObjPhrase
import operator

INTENT_MAP = {0: ('uk', 'uk'),
              1: ('ass1', 'RELEASEDATE'),
              2: ('proj1', 'RELEASEDATE'),
              3: ('ass2', 'RELEASEDATE'),
              4: ('midterm', 'RELEASEDATE'),
              5: ('proj2', 'RELEASEDATE'),
              6: ('ass3', 'RELEASEDATE'),
              7: ('proj3', 'RELEASEDATE'),
              8: ('final', 'RELEASEDATE'),
              9: ('ass1', 'DUEDATE'),
              10: ('proj1', 'DUEDATE'),
              11: ('ass2', 'DUEDATE'),
              12: ('midterm', 'DUEDATE'),
              13: ('proj2', 'DUEDATE'),
              14: ('ass3', 'DUEDATE'),
              15: ('proj3', 'DUEDATE'),
              16: ('final', 'DUEDATE'),
              17: ('ass1', 'DURATION'),
              18: ('proj1', 'DURATION'),
              19: ('ass2', 'DURATION'),
              20: ('midterm', 'DURATION'),
              21: ('proj2', 'DURATION'),
              22: ('ass3', 'DURATION'),
              23: ('proj3', 'DURATION'),
              24: ('final', 'DURATION'),
              25: ('ass1', 'WEIGHT'),
              26: ('proj1', 'WEIGHT'),
              27: ('ass2', 'WEIGHT'),
              28: ('midterm', 'WEIGHT'),
              29: ('proj2', 'WEIGHT'),
              30: ('ass3', 'WEIGHT'),
              31: ('proj3', 'WEIGHT'),
              32: ('final', 'WEIGHT'),
              33: ('ass1', 'PROCESS'),
              34: ('proj1', 'PROCESS'),
              35: ('ass2', 'PROCESS'),
              36: ('midterm', 'PROCESS'),
              37: ('proj2', 'PROCESS'),
              38: ('ass3', 'PROCESS'),
              39: ('proj3', 'PROCESS'),
              40: ('final', 'PROCESS'),
              41: ('piazza', 'GENERAL'),
              42: ('goals', 'GENERAL')
              }

DUEDATE_KEYWORDS = ['when', 'due', 'date', 'turn', 'submit', 'submitted']
PROCESS_KEYWORDS = ['how', 'where', 'procedure', 'do', 'process']
RELEASEDATE_KEYWORDS = ['when', 'release', 'date', 'begin', 'start', 'available', 'open']
WEIGHT_KEYWORDS = ['how', 'much', 'worth', 'percentage', 'grade', 'weight']
DURATION_KEYWORDS = ['how', 'long', 'time', 'between']
GENERAL_KEYWORDS = ['piazza', 'goals', 'learning', 'announcements']

DUEDATE_TUPLES = [('due', 'date'), ('turn', 'in'), ('turned', 'in'), ('turning', 'in'), ('submit', 'by'),
                  ('submitted', 'by'), ('submissions', 'close'), ('completed', 'by')]
PROCESS_TUPLES = [('how', 'do'), ('where', 'do')]
RELEASEDATE_TUPLES = [('open', 'by'), ('available', 'by')]
WEIGHT_TUPLES = [('how', 'much'), ('weight', 'of')]
DURATION_TUPLES = [('how', 'long'), ('much', 'time'), ('how', 'much')]
GENERAL_TUPLES = [('learning', 'goals')]

class StudentAgent:

    def __init__(self, verbose):
        self._verbose = verbose
        # TODO: Add your init code here
        return

    def parse_object(self, sentence):
        scores = {'ass1': 0,
                  'ass2': 0,
                  'ass3': 0,
                  'proj1': 0,
                  'proj2': 0,
                  'proj3': 0,
                  'midterm': 0,
                  'final': 0,
                  'piazza': 0,
                  'goals': 0,
                  'uk': 0}
        s = sentence.sentence
        for i, w in enumerate(s):
            if w == 'assignment':
                if 'code' in s:
                    scores['uk'] += 100
                if (i + 1) < len(s):
                    if s[i+1] == '1':
                        scores['ass1'] += 100
                    if s[i+1] == '2':
                        scores['ass2'] += 100
                    if s[i+1] == '3':
                        scores['ass3'] += 100
                    if s[i-1] == 'first':
                        scores['ass1'] += 100
                    if s[i-1] == 'second':
                        scores['ass2'] += 100
                    if s[i-1] == 'third':
                        scores['ass3'] += 100
                    else:
                        scores['uk'] += 10
            if w == 'project':
                if (i + 1) < len(s):
                    if s[i+1] == '1':
                        scores['proj1'] += 100
                    if s[i+1] == '2':
                        scores['proj2'] += 100
                    if s[i+1] == '3':
                        scores['proj3'] += 100
                    if s[i-1] == 'first':
                        scores['proj1'] += 100
                    if s[i-1] == 'second':
                        scores['proj2'] += 100
                    if s[i-1] == 'third':
                        scores['proj3'] += 100
                    else:
                        scores['uk'] += 10
            if w == 'midterm':
                if 'download' in s:
                    scores['uk'] += 100
                scores['midterm'] += 100
            if w == 'final':
                if 'code' in s:
                    scores['uk'] += 100
                scores['final'] += 100
            if w in ['piazza', 'announcements', 'forum']:
                scores['piazza'] += 100
            if w in ['goals']:
                scores['goals'] += 100
            else:
                scores['uk'] += 10
        print(scores)
        # print(max(scores, key=scores.get))
        return max(scores, key=scores.get)

    def get_keyword_score(self, sentence, response_keywords, response_tuples):
        score = 0
        for word in sentence:
            if word in response_keywords:
                score += 1
        adjacent_words = zip(sentence, sentence[1:])
        # print(list(adjacent_words))
        for pair in adjacent_words:
            if pair in response_tuples:
                score += 5
        return score

    def parse_category(self, sentence, sentence_object):

        s = sentence.sentence

        if sentence_object == 'uk':
            return 'uk'

        if sentence_object == 'piazza':
            return "GENERAL"

        if sentence_object == 'goals':
            return "GENERAL"

        if ('when' in s) and (s[s.index('when') + 1] == 'to') and (s[s.index('when') + 2] == 'submit'):
            return "DUEDATE"

        scores = {'RELEASEDATE': self.get_keyword_score(s, RELEASEDATE_KEYWORDS, RELEASEDATE_TUPLES),
                  'DUEDATE': self.get_keyword_score(s, DUEDATE_KEYWORDS, DUEDATE_TUPLES),
                  'DURATION': self.get_keyword_score(s, DURATION_KEYWORDS, DURATION_TUPLES),
                  'WEIGHT': self.get_keyword_score(s, WEIGHT_KEYWORDS, WEIGHT_TUPLES),
                  'PROCESS': self.get_keyword_score(s, PROCESS_KEYWORDS, PROCESS_TUPLES),
                  'GENERAL': self.get_keyword_score(s, GENERAL_KEYWORDS, GENERAL_TUPLES)}

        print(scores)

        return max(scores, key=scores.get)

    # takes in list of words, returns question_object and data_requested
    def input_output(self, word_list):
        try:

            print(word_list) # for debugging only
            s = Sentence(word_list)
            #print(s)

            a = QPhrase()
            a = QPhrase.build(a, s)
            s.phrase_list.append(a)
            b = MVPhrase()
            b = MVPhrase.build(b, s)
            s.phrase_list.append(b)
            d = SubjPhrase()
            d = SubjPhrase.build(d, s)
            s.phrase_list.append(d)
            if (len([i for i, x in enumerate(s.pos) if x == ['V']]) >= 2) and (
                    s.phrase_list[-1].end_idx < (len(s.pos) - 1)):
                c = AVPhrase()
                c = AVPhrase.build(c, s)
                s.phrase_list.append(c)
            if s.phrase_list[-1].end_idx < (len(s.pos) - 1):
                e = ObjPhrase()
                e = ObjPhrase.build(e, s)
                s.phrase_list.append(e)
            if s.phrase_list[-1].end_idx < (len(s.pos) - 1):
                f = AAVPhrase()
                f = AAVPhrase.build(f, s)
                s.phrase_list.append(f)


            sentence_object = self.parse_object(s)
            print(sentence_object)
            sentence_category = self.parse_category(s, sentence_object)
            print(sentence_category)

            result = (sentence_object, sentence_category)
            _intent = 0

            for key, value in INTENT_MAP.items():
                if value == result:
                    _intent = key

            return _intent

        except:
            return 0



# agent = StudentAgent(verbose=True)
#
# questions = []
# intents = []
#
# with open('ExampleQuestions.json', encoding='utf-8') as json_data:
#     ground_truth_dicts = json.load(json_data)
#     for gtd in ground_truth_dicts:
#         questions.append(gtd['question'])
#         intents.append(gtd['intent'])
#
# cntr = 0
# for i, q in enumerate(questions):
#      if intents[i] == agent.input_output(q):
#          cntr += 1
#      else:
#          print(i)
#          print("truth: " + str(intents[i]))
#          print('calc: ' + str(agent.input_output(q)))
#      print("----------------------------------")
# print(str(cntr) + '/' + '80')
