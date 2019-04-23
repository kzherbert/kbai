# This file contains grammar rules and for determining parts of speech in a sentence
NOUNS = ["assignment", "i", "week", "we", "project", "you", "download", "second", "start", "midterm", "final",
         "submissions", "time", "beginning", "end", "weeks", "code", "finish", "days", "percentage", "grade", "weight",
         "total", "process", "canvas", "pdf", "zip", "file", "report", "specification", "procedure", "class",
         "announcements", "question", "piazza", "forum", "discussions", "collaboration", "it", "log", "times",
         "learning", "goals", "this", "concepts", "methods", "issues", "intelligence", "skills", "abilities", "design",
         "ai", "agents", "third", "relationship", "study", "human", "cognition", "4%", "15%", "20%", "there", "day",
         "use"]
VERBS = ["will", "be", "do", "know", "can", "begin", "working", "download", "start", "is", "distributed", "occurs",
         "does", "starts", "open", "need", "submitted", "turned", "submit", "completed", "should", "have", "turn",
         "close", "submitting", "complete", "finish", "write", "code", "grade", "contribute", "contributing", "process",
         "getting", "report", "go", "get", "question", "answering", "are", "organized", "teaches", "needed", "apply",
         "design", "must", "end", "learning", "released", 'use', 'close', "log"]
ADJS = ["available", "second", "worth", "final", "open", "due", "long", "learning", "many", "important",
        "first", "possible", "least", "primary", "knowledge-based", "artificial", "specific", "third", "human", "that",
        "this", "a", "an", "the", "my", "our", "those", "prominent", "much"]
ADVS = ["not", "as", "regularly", "frequently", "least", "daily", "around"]
PREPS = ["in", "on", "during", "at", "of", "to", "by", "for", "into", "between", "around"]
CONJS = ["and", "or", "if"]
QWORDS = ['when', 'what', 'where', 'how']
NUMERICS = ['two', 'three']

# ties:
#     N/V: download, start(s), end, code, finish, grade, process, report, question, learning, design, use
#     N/ADJ: this, human, final
#     V/ADJ: open, close, complete


class Sentence:

    def __init__(self, word_list):
        self.sentence = word_list
        self.pos = self.assign_pos()
        self.phrase_list = []

    def __str__(self):
        ret_str = str(self.sentence) + '\n' + str(self.pos) + '\n'
        for i in self.phrase_list:
            ret_str = ret_str + str(i) + "****"
        return ret_str

    # def join_numerics(self):
    #     numeric_index = [i for i,x in enumerate(self.pos) if x == ['#']]
    #     for i in numeric_index:
    #         if (self.sentence[i-1] != 'the'):
    #             self.phrase_list[i-1] = self.phrase_list[i-1] + ' ' + self.phrase_list[i]
    #             del self.phrase_list[i]
    #     return self.phrase_list

    def break_pos_ties(self):
        for i, word in enumerate(self.sentence):
            if self.pos[i] == ['N', 'V']:
                if (i+1) >= len(self.pos):
                    self.pos[i] = ['N']
                    if self.pos[i - 1] == ['ADJ']:
                        self.pos[i] = ['N']
                    continue
                if self.pos[i-1] == ['ADJ']:
                    self.pos[i] = ['N']
                    continue
                if self.pos[i-1] == ['#']:
                    self.pos[i] = ['N']
                    continue
                if (self.sentence[i - 1] in ['i', 'we', 'you', 'class']):
                    self.pos[i] = ['V']
                    continue
                if self.pos[i+1] == ['V']:
                    self.pos[i] = ['N']
                    continue
                else:
                    self.pos[i] = ['V']
                    continue
            if self.pos[i] == ['N', 'ADJ']:
                if (i+1) >= len(self.pos):
                    self.pos[i] = ['N']
                    continue
                if (self.pos[i-1] == ['ADJ']) and (self.pos[i+1] == ['N']):
                    self.pos[i] = ['ADJ']
                    continue
                if (self.pos[i-1] == ['ADJ']) and (self.pos[i+1] == ['N', 'V']):
                    self.pos[i] = ['ADJ']
                    continue
                if (self.pos[i-1] == ['ADJ']) and (self.pos[i+1] != ['N']):
                    self.pos[i] = ['N']
                    continue
                if (self.pos[i-1] == ['P']) and (self.pos[i+1] == ['N']):
                    self.pos[i] = ['ADJ']
                    continue
            if self.pos[i] == ['V', 'ADJ']:
                if (self.pos[i-1] == ['N']) and (self.sentence[i-1] not in ['i', 'we', 'you', 'class']):
                    self.pos[i] = ['ADJ']
                    continue
                if (self.pos[i-1] == ['N']) and (self.sentence[i-1] in ['i', 'we', 'you', 'class']):
                    self.pos[i] = ['V']
                    continue
            if self.pos[i] == ['N', 'V', 'ADJ']:
                if (self.pos[i-1] == ['ADJ']) and (self.pos[i+1] == ['N']):
                    self.pos[i] = ['ADJ']
                if (self.pos[i-1] == ['#']) and (self.pos[i+1] == ['N']):
                    self.pos[i] = ['ADJ']


            # if len(self.pos[i]) > 1:
            #     if word == 'download':
            #         if ((i+1) >= len(self.pos)):
            #             self.pos[i] = ['N']
            #             continue
            #         if (self.sentence[i-1] in ['i', 'we', 'you', 'class']):
            #             self.pos[i] = ['V']
            #             continue
            #         if (self.pos[i-1] == ['#']):
            #             self.pos[i] = ['N']
            #             continue
        return self.pos

    def assign_pos(self):

        pos = []

        for w in self.sentence:
            possible_pos = []
            if ((w not in QWORDS) and (w not in NOUNS) and (w not in VERBS) and (w not in ADJS) and (w not in ADVS)
                    and (w not in PREPS) and (w not in CONJS) and (not w.isnumeric()) and (w not in NUMERICS)):
                raise Exception("A word in this sentence is not in the vocabulary:" + '\n' + str(self.sentence) +
                                '\n' + w)
            if w in QWORDS:
                possible_pos.append('Q')
            if w in NOUNS:
                possible_pos.append('N')
            if w in VERBS:
                possible_pos.append('V')
            if w in ADJS:
                possible_pos.append('ADJ')
            if w in ADVS:
                possible_pos.append('ADV')
            if w in PREPS:
                possible_pos.append('P')
            if w in CONJS:
                possible_pos.append('C')
            if (w.isnumeric()) or (w in NUMERICS):
                possible_pos.append('#')
            pos.append(possible_pos)

        self.pos = pos
        return self.break_pos_ties()
