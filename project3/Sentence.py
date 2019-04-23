from project3 import Grammar

CONCEPTS = ["project", "projects", "assignment", "assignments", "midterm", "final", "course", "announcements",
            "instructor", "report", "reports", "exams", "strategies", "strategy", "policy", "peer-feedback",
            "office-days", "content", "communication", "submissions", "TA", "component", "code", "policies"]

DUEDATE_KEYWORDS = ['when', 'due', 'date', 'turn', 'submit', 'submitted']
PROCESS_KEYWORDS = ['how', 'where', 'procedure', 'do', 'process', 'canvas', 'piazza', 'download', 'pdf', 'zip', 'bz2',
                    'gz', 'credit', 'component', 'attendance', 'mandatory']
RELEASEDATE_KEYWORDS = ['when', 'release', 'date', 'begin', 'start', 'available', 'open', 'released', 'get']
WEIGHT_KEYWORDS = ['how', 'much', 'worth', 'percentage', 'grade', 'weight']
DURATION_KEYWORDS = ['how', 'long', 'time', 'between', 'weeks']
GENERAL_KEYWORDS = ['goals', 'learning', 'announcements', 'knowledge-based', 'ashok', 'goel', 'yaroslav', 'litvak',
                    'class']

DUEDATE_TUPLES = [('due', 'date'), ('turn', 'in'), ('turned', 'in'), ('turning', 'in'), ('submit', 'by'),
                  ('submitted', 'by'), ('submissions', 'close'), ('completed', 'by'), ('occurs', 'on'),
                  ('exam', 'during'), ('final', 'during'), ('midterm', 'during')]
PROCESS_TUPLES = [('how', 'do'), ('where', 'do'), ('submitted', 'to'), ('submitted', 'as'), ('no', 'credit'),
                  ('video', 'hours'), ('on', 'piazza')]
RELEASEDATE_TUPLES = [('open', 'by'), ('available', 'by')]
WEIGHT_TUPLES = [('how', 'much'), ('weight', 'of')]
DURATION_TUPLES = [('how', 'long'), ('much', 'time'), ('how', 'much')]
GENERAL_TUPLES = [('learning', 'goals')]


class Sentence:

    def __init__(self, list_of_words):
        self.list_of_words = list_of_words
        self.parts_of_speech = Grammar.assign_pos(list_of_words)
        self.object = self.find_concept()
        self.subject= self.list_of_words[0:self.parts_of_speech.index(['V'])]
        (self.mvp, self.predicate, self.pred_index) = self.build_mvp_and_predicate()

    def __str__(self):
        return ("Words: " + str(self.list_of_words) + "\n" + "PoS:   " + str(self.parts_of_speech) + "\n" +
                "Object: " + self.object + "\n" + "Subject: " + str(self.subject) + "\n" +
                "MVP: " + str(self.mvp) + "\n" + "Pred: " + str(self.predicate) + "\n")

    def find_concept(self):
        for c in CONCEPTS:
            if c in self.list_of_words:
                return c
        return "IDK"

    def build_mvp_and_predicate(self):
        verb_indexes = [i for i, x in enumerate(self.parts_of_speech) if x == ['V']]
        # verbs = self.list_of_words[verb_indexes]
        mvp_indexes = []

        # loop to determine the first verb phrase indexes
        prev = -1
        for i, n in enumerate(verb_indexes):
            curr = n
            if i == 0:
                mvp_indexes.append(n)
                prev = n
                continue
            if curr == prev + 1:
                mvp_indexes.append(n)
                prev = curr
                continue
            if curr != prev + 1:
                break

        main_verb_phrase = [self.list_of_words[i] for i in mvp_indexes]
        predicate = self.list_of_words[mvp_indexes[-1]+1:]
        return main_verb_phrase, predicate, mvp_indexes[-1]+1

    def get_category_scores(self):

        s = self.list_of_words

        if self.object == 'IDK':
            return {'RELEASEDATE': 0, 'DUEDATE': 0, 'DURATION': 0, 'WEIGHT': 0, 'PROCESS': 0, 'GENERAL': 1}

        if self.object == 'piazza':
            return "GENERAL"

        if self.object == 'goals':
            return "GENERAL"

        if ('when' in s) and (s[s.index('when') + 1] == 'to') and (s[s.index('when') + 2] == 'submit'):
            return "DUEDATE"

        scores = {'RELEASEDATE': self.get_keyword_score(s, RELEASEDATE_KEYWORDS, RELEASEDATE_TUPLES),
                  'DUEDATE': self.get_keyword_score(s, DUEDATE_KEYWORDS, DUEDATE_TUPLES),
                  'DURATION': self.get_keyword_score(s, DURATION_KEYWORDS, DURATION_TUPLES),
                  'WEIGHT': self.get_keyword_score(s, WEIGHT_KEYWORDS, WEIGHT_TUPLES),
                  'PROCESS': self.get_keyword_score(s, PROCESS_KEYWORDS, PROCESS_TUPLES),
                  'GENERAL': self.get_keyword_score(s, GENERAL_KEYWORDS, GENERAL_TUPLES)}

        # print(scores)
        return scores

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




