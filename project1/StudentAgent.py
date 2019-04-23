"""
ADD YOUR CODE HERE

Please read project directions before importing anything
"""


import common

DUEDATE_KEYWORDS = ['when', 'due', 'date', 'turn', 'submit', 'submitted']
PROCESS_KEYWORDS = ['how', 'where', 'procedure', 'do']
RELEASEDATE_KEYWORDS = ['when', 'release', 'date', 'begin', 'start', 'available']
WEIGHT_KEYWORDS = ['how', 'much', 'worth', 'percentage', 'grade']
DURATION_KEYWORDS = ['how', 'long', 'time', 'between']

DUEDATE_TUPLES = [('due', 'date'), ('turn', 'in'), ('turned', 'in'), ('turning', 'in')]
PROCESS_TUPLES = [('how', 'do'), ('where', 'do')]
RELEASEDATE_TUPLES = [('submit', 'by'), ('submitted', 'by')]
WEIGHT_TUPLES = [('how', 'much')]
DURATION_TUPLES = [('how', 'long'), ('much', 'time'), ('how', 'much')]

CONJUNCTIONS = ['for', 'and', 'nor', 'but', 'but', 'or', 'yet', 'so']
QUESTIONS = ['who', 'what', 'where', 'when', 'why', 'how']
VERBS = ['is', 'are', 'do', 'will', 'can', 'does', 'be', 'must', 'release', 'released', 'going']
DETERMINERS = ['the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their']
PREPOSITIONS = ['for', 'by', 'of', 'with', 'on']
ADJECTIVES = ['worth', 'located']
BAD_WORDS = ['i', 'you', 'he', 'she', 'it', 'we']

class Candidate_Object:

    def __init__(self, word, index):
        self.data = word
        self.index = index
        self.preposition_proximity = 1000
        self.determiner_proximity = 1000

class Lexicon:

    def __init__(self):
        self.QP = []
        self.AVP = []
        self.SP = []
        self.MVP = []
        self.AV_index = -1
        self.MV_index = -1

    def locate_auxillary_verb(self, word_list):
        av = ''
        index = -1
        for idx, word in enumerate(word_list):
            if word in VERBS:
                av = word
                index = idx
                self.AV_index = idx
                self.AVP.append(word)
                break
        return av, index

    def locate_main_verb(self, word_list):
        mv = ''
        index = -1
        for idx, word in enumerate(word_list):
            if idx > self.AV_index:
                if word in VERBS:
                    self.MV_index = idx
                    for w in word_list[idx:]:
                        self.MVP.append(w)
                    mv = word
                    index = idx
                    break
        return mv, index

    def build(self, word_list):

        av, av_idx = self.locate_auxillary_verb(word_list)
        mv, mv_idx = self.locate_main_verb(word_list)

        if self.MV_index != -1:
            for idx, word in enumerate(word_list):
                if idx < av_idx:
                    self.QP.append(word)
                if (idx > av_idx) & (idx < mv_idx):
                    self.SP.append(word)
        else:
            for idx, word in enumerate(word_list):
                if idx < av_idx:
                    self.QP.append(word)
                if idx > av_idx:
                    self.SP.append(word)

        if self.SP[-1] == 'due':
            self.SP.remove('due')
            self.MVP.append('due')

    def is_number(self, n):
        try:
            float(n)  # Type-casting the string to `float`.
            # If string is not a valid `float`,
            # it'll raise `ValueError` exception
        except ValueError:
            return False
        return True

    def get_object(self, word_list):

        candidates =[]
        for idx, word in enumerate(word_list):
            if (word not in DETERMINERS) & (word not in VERBS) & (word not in CONJUNCTIONS) & (word not in ADJECTIVES):
                candidates.append(Candidate_Object(word, idx))
            if (self.is_number(word) == True):
                candidates.append(Candidate_Object(word, idx))

        for c in candidates:
            for i, w in enumerate(word_list[:c.index]):
                if w in DETERMINERS:
                    c.determiner_proximity = min(c.determiner_proximity, c.index - i)
                if w in PREPOSITIONS:
                    c.preposition_proximity = min(c.preposition_proximity, c.index - i)

        if len(candidates) == 1:
            return candidates[0].data

        for i, c in enumerate(candidates):
            if (c.preposition_proximity == 1000) & (c.determiner_proximity == 1000) & (c.data not in BAD_WORDS) & \
                    (i == 0):
                # print(type(c.data))
                if (self.is_number(' '.join(candidates[i+1].data)) == True):
                    c.data = word_list[c.index:c.index+2]
                if type(c.data) == list:
                    return ' '.join(c.data)
                else:
                    return c.data
            if (c.preposition_proximity == 1000) & (c.determiner_proximity != 1000) & (c.determiner_proximity > 1):
                c.data = word_list[c.index - c.determiner_proximity + 1:c.index + 1]
            if (c.determiner_proximity == 1000) & (c.preposition_proximity != 1000) & (c.preposition_proximity > 1):
                c.data = word_list[c.index - c.preposition_proximity + 1:c.index + 1]
            if self.is_number(' '.join(c.data)):
                c.data = word_list[c.index-1:c.index+1]

        # print(c.index)
        # print(len(word_list) - 1)
        if c.index < len(word_list) - 1:
            # print(c.index)
            # print(len(word_list))
            # print(word_list)
            if self.is_number(word_list[c.index]):
                return ' '.join([word_list[c.index - 1], c.data])

        if type(c.data) == list:
            return ' '.join(c.data)
        else:
            return c.data

    def get_object_candidates(self):
        if len(self.SP) == 0:
            return self.get_object(self.QP)
        else:
            return self.get_object(self.SP)



class StudentAgent:

    def __init__(self, verbose):
        self._verbose = verbose
        # TODO: Add your init code here
        return

    def get_keyword_score(self, word_list, response_keywords, response_tuples):
        score = 0
        for word in word_list:
            if word in response_keywords:
                score += 1
        adjacent_words = zip(word_list, word_list[1:])
        # print(list(adjacent_words))
        for pair in adjacent_words:
            if pair in response_tuples:
                score += 5
        return score

    def get_data_requested(self, word_list):

        data = ""
        duedate_score = self.get_keyword_score(word_list, DUEDATE_KEYWORDS, DUEDATE_TUPLES)
        process_score = self.get_keyword_score(word_list, PROCESS_KEYWORDS, PROCESS_TUPLES)
        releasedate_score = self.get_keyword_score(word_list, RELEASEDATE_KEYWORDS, RELEASEDATE_TUPLES)
        weight_score = self.get_keyword_score(word_list, WEIGHT_KEYWORDS, WEIGHT_TUPLES)
        duration_score = self.get_keyword_score(word_list, DURATION_KEYWORDS, DURATION_TUPLES)

        print(duedate_score, process_score, releasedate_score, weight_score, duration_score)

        if max(duedate_score, process_score, releasedate_score, weight_score, duration_score) == duedate_score:
            data = "DUEDATE"
        if max(duedate_score, process_score, releasedate_score, weight_score, duration_score) == process_score:
            data = "PROCESS"
        if max(duedate_score, process_score, releasedate_score, weight_score, duration_score) == releasedate_score:
            data = "RELEASEDATE"
        if max(duedate_score, process_score, releasedate_score, weight_score, duration_score) == duration_score:
            data = "DURATION"
        if max(duedate_score, process_score, releasedate_score, weight_score, duration_score) == weight_score:
            data = "WEIGHT"

        return data

    def get_question_object(self, word_list):

        lex = Lexicon()
        lex.build(word_list)
        print(lex.QP, lex.AVP, lex.AV_index, lex.SP, lex.MVP, lex.MV_index)
        return lex.get_object_candidates()


    # takes in list of words, returns question_object and data_requested
    def input_output(self, word_list):
        print(word_list) # for debugging only

        _data_requested = self.get_data_requested(word_list)
        _question_object = self.get_question_object(word_list)

        return _question_object, _data_requested


# agent = StudentAgent(verbose=True)
# words = common.ParseQuestion("what is the due date for project 1")
# print(agent.input_output(words))

