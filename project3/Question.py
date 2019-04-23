from project3 import Grammar

CONCEPTS = ["project", "projects", "assignment", "assignments", "midterm", "final", "course", "announcements",
            "instructor", "report", "reports", "exams", "strategies", "strategy", "policy", "peer-feedback",
            "office-days", "content", "communication", "submissions", "TA", "component", "code", "policies"]

DUEDATE_KEYWORDS = ['when', 'due', 'date', 'turn', 'submit', 'submitted']
PROCESS_KEYWORDS = ['how', 'where', 'procedure', 'do', 'process', 'canvas', 'piazza', 'download', 'pdf', 'zip', 'bz2',
                    'gz', 'credit', 'component', 'attendance', 'mandatory']
RELEASEDATE_KEYWORDS = ['when', 'release', 'date', 'begin', 'start', 'available', 'open', 'released']
WEIGHT_KEYWORDS = ['how', 'much', 'worth', 'percentage', 'grade', 'weight']
DURATION_KEYWORDS = ['how', 'long', 'time', 'between', 'weeks', 'have', 'week']
GENERAL_KEYWORDS = ['goals', 'learning', 'announcements', 'knowledge-based', 'ashok', 'goel', 'yaroslav', 'litvak']

DUEDATE_TUPLES = [('due', 'date'), ('turned', 'in'), ('turning', 'in'), ('submit', 'by'),
                  ('submitted', 'by'), ('submissions', 'close'), ('completed', 'by'), ('occurs', 'on'),
                  ('exam', 'during'), ('final', 'during'), ('midterm', 'during')]
PROCESS_TUPLES = [('how', 'do'), ('where', 'do'), ('submitted', 'to'), ('submitted', 'as'), ('no', 'credit'),
                  ('video', 'hours'), ('on', 'piazza')]
RELEASEDATE_TUPLES = [('open', 'by'), ('available', 'by')]
WEIGHT_TUPLES = [('how', 'much'), ('weight', 'of')]
DURATION_TUPLES = [('how', 'long'), ('much', 'time'), ('how', 'much'), ('to', 'complete'), ('to', 'finish')]
GENERAL_TUPLES = [('learning', 'goals')]


class Question:

    def __init__(self, list_of_words):

        self.list_of_words = list_of_words
        self.parts_of_speech = Grammar.assign_pos(list_of_words)
        self.object = self.find_concept()

        category_scores = self.get_category_scores()
        self.category = (max(category_scores, key=category_scores.get), category_scores)

        verb_idxs = [i for i, x in enumerate(self.parts_of_speech) if x == ['V']]
        if len(verb_idxs) > 1:
            self.subject = self.list_of_words[verb_idxs[0]+1:verb_idxs[1]]
        elif len(verb_idxs) == 1:
            self.subject = self.list_of_words[verb_idxs[0] + 1]
        else:
            self.subject = self.list_of_words[verb_idxs[0] + 1]

        (self.first_verb_phrase, self.second_verb_phrase, self.verb_indexes) = self.build_verb_phrases()

        self.modifiers = self.find_modifiers()

    def __str__(self):
        return ("Words: " + str(self.list_of_words) + "\n" + "PoS:   " + str(self.parts_of_speech) + "\n" +
                "Object: " + self.object + "\n" + "Subject: " + str(self.subject) + "\n" +
                "FVP: " + str(self.first_verb_phrase) + "\n" + "SVP: " + str(self.second_verb_phrase) + "\n" +
                "VIX: " + str(self.verb_indexes) + "\n" + "Category: " + str(self.category) + "\n" +
                "Mods: " + str(self.modifiers))

    def find_concept(self):
        for c in CONCEPTS:
            if c in self.list_of_words:
                c_i = self.list_of_words.index(c)
                if c in ["project", "assignment", "report"] and not self.list_of_words[c_i + 1] .isnumeric():
                    if c == "project":
                        return "projects"
                    if c == "assignment":
                        return "assignments"
                    if c == "report":
                        return "reports"
                return c

        if 'class' in self.list_of_words:
            return "course"



        return "IDK"

    def build_verb_phrases(self):
        verb_indexes = [i for i, x in enumerate(self.parts_of_speech) if x == ['V']]
        # verbs = self.list_of_words[verb_indexes]
        mvp_indexes = []

        # loop to determine the first verb phrase indexes
        # prev = -1
        # for i, n in enumerate(verb_indexes):
        #     curr = n
        #     if i == 0:
        #         mvp_indexes.append(n)
        #         prev = n
        #         continue
        #     if curr == prev + 1:
        #         mvp_indexes.append(n)
        #         prev = curr
        #         continue
        #     if curr != prev + 1:
        #         break

        first_verb_phrase = [self.list_of_words[verb_indexes[0]]]
        if len(verb_indexes) > 1:
            second_verb_phrase = [self.list_of_words[verb_indexes[1]]]
        else:
            second_verb_phrase = []
        return first_verb_phrase, second_verb_phrase, verb_indexes

    def find_modifiers(self):
        possible_mods = []
        pm_idxs = []
        for i, w in enumerate(self.list_of_words):
            if len(self.verb_indexes) > 1:
                if i <= self.verb_indexes[1]:
                    continue
                else:
                    possible_mods.append(w)
                    pm_idxs.append(i)
            else:
                if i <= self.verb_indexes[0]:
                    continue
                possible_mods.append(w)
                pm_idxs.append(i)
        return possible_mods, pm_idxs

    def get_category_scores(self):

        s = self.list_of_words

        if self.object == 'IDK':
            return {'RELEASEDATE': 0, 'DUEDATE': 0, 'DURATION': 0, 'WEIGHT': 0, 'PROCESS': 0, 'GENERAL': 1}

        if self.object in ["project", "assignment", "report", "code", "component"] and ('can' in s and 'i' in s and
                                                                                        'get' in s):
            return {'RELEASEDATE': 1, 'DUEDATE': 0, 'DURATION': 0, 'WEIGHT': 0, 'PROCESS': 0, 'GENERAL': 0}

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