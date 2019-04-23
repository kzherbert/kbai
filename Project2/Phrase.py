
from Sentence import Sentence

# prepositional phrase


# main verb phrase
# main verb after question, next verb is auxillary
# see a verb
class MVPhrase:

    def __init__(self):
        self.start_idx = -1
        self.end_idx = -1
        self.verb = []
        self.modifiers = []

    def __str__(self):
        return str(self.verb) + "|" + str(self.modifiers)

    def contains(self, st):
        if st in self.verb:
            return True
        if st in self.modifiers:
            return True
        return False

    def build(self, sentence):
        word_list = sentence.sentence
        pos_list = sentence.pos
        verb_indexes = [i for i, x in enumerate(pos_list) if x == ['V']]
        main_verb_index = verb_indexes[0]
        self.verb = [word_list[main_verb_index]]
        self.start_idx = main_verb_index
        self.end_idx = main_verb_index
        if (self.verb == ['will']) and (pos_list[main_verb_index + 1] == ['V']):
            self.modifiers.append(word_list[main_verb_index + 1])
            self.end_idx += 1
        return self


class AVPhrase:

    def __init__(self):
        self.start_idx = -1
        self.end_idx= -1
        self.aux_verb = []
        self.modifiers = []

    def __str__(self):
        return str(self.aux_verb) + "|" + str(self.modifiers)

    def contains(self, st):
        if st in self.aux_verb:
            return True
        if st in self.modifiers:
            return True
        return False

    def build(self, sentence):
        word_list = sentence.sentence
        pos_list = sentence.pos
        verb_indexes = [i for i, x in enumerate(pos_list) if x == ['V']]
        if len(verb_indexes) < 2:
            raise Exception("No Auxilliary Verb in this sentence: " + str(word_list))
        aux_verb_index = verb_indexes[1]
        self.aux_verb = [word_list[aux_verb_index]]
        self.start_idx = aux_verb_index
        self.end_idx = aux_verb_index
        if word_list[aux_verb_index + 1] == 'the':
            return self
        if pos_list[aux_verb_index + 1] == ['V']:
            self.modifiers.append(word_list[aux_verb_index + 1])
            self.end_idx = aux_verb_index + 1
        if pos_list[aux_verb_index + 1] == ['ADJ']:
            self.modifiers.append(word_list[aux_verb_index + 1])
            self.end_idx = aux_verb_index + 1
        if (pos_list[aux_verb_index + 1] == ['P']) and (pos_list[aux_verb_index + 2] == ['V']):
            self.modifiers.append(word_list[aux_verb_index + 1])
            self.modifiers.append(word_list[aux_verb_index + 2])
            self.end_idx = aux_verb_index + 2
            if ((aux_verb_index + 3) < len(word_list)) and (pos_list[aux_verb_index + 3] == ['V']):
                self.modifiers.append(word_list[aux_verb_index + 3])
                self.end_idx = aux_verb_index + 3
            if ((aux_verb_index + 3) < len(word_list)) and (pos_list[aux_verb_index + 3] == ['P']):
                self.modifiers.append(word_list[aux_verb_index + 3])
                self.end_idx = aux_verb_index + 3
        if (pos_list[aux_verb_index + 1] == ['P']) and (pos_list[aux_verb_index + 2] == ['P']):
            self.modifiers.append(word_list[aux_verb_index + 1])
            self.modifiers.append(word_list[aux_verb_index + 2])
            self.end_idx = aux_verb_index + 2
            if ((aux_verb_index + 3) < len(word_list)) and (pos_list[aux_verb_index + 3] == ['N']):
                self.modifiers.append(word_list[aux_verb_index + 3])
                self.end_idx = aux_verb_index + 3
            if ((aux_verb_index + 4) < len(word_list)) and (pos_list[aux_verb_index + 4] == ['#']):
                self.modifiers.append(word_list[aux_verb_index + 4])
                self.end_idx = aux_verb_index + 4

        return self


class AAVPhrase:

    def __init__(self):
        self.start_idx = -1
        self.end_idx= -1
        self.aux_verb = []
        self.modifiers = []

    def __str__(self):
        return str(self.aux_verb) + "|" + str(self.modifiers)

    def contains(self, st):
        if st in self.aux_verb:
            return True
        if st in self.modifiers:
            return True
        return False

    def build(self, sentence):
        word_list = sentence.sentence
        pos_list = sentence.pos
        verb_indexes = [i for i, x in enumerate(pos_list) if x == ['V']]
        if len(verb_indexes) < 3:
            raise Exception("Not enough verbs to have another auxiliary verb phrase")
        aaux_verb_index = verb_indexes[2]
        self.aux_verb = [word_list[aaux_verb_index]]
        self.start_idx = aaux_verb_index
        self.end_idx = aaux_verb_index
        if (self.end_idx+1 < len(word_list)):
            self.modifiers.append(word_list[self.end_idx+1:])
            self.end_idx = len(word_list) - 1
        return self


# question phrase
class QPhrase:

    def __init__(self):
        self.start_idx = -1
        self.end_idx = -1
        self.q_word = []
        self.modifiers = []

    def __str__(self):
        return str(self.q_word) + "|" + str(self.modifiers)

    def contains(self, st):
        if st in self.q_word:
            return True
        if st in self.modifiers:
            return True
        return False

    def build(self, sentence):
        word_list = sentence.sentence
        pos_list = sentence.pos
        qword_index = 0
        main_verb_index = pos_list.index(['V'])
        self.q_word = [word_list[0]]
        self.start_idx = 0
        self.modifiers = word_list[qword_index+1: main_verb_index]
        self.end_idx = main_verb_index - 1
        return self


# noun phrases
class SubjPhrase:

    def __init__(self):
        self.start_idx = -1
        self.end_idx = -1
        self.noun = []
        self.pre_modifiers = []
        self.post_modifiers = []

    def __str__(self):
        return str(self.pre_modifiers) + "|" + str(self.noun) + "|" + str(self.post_modifiers)

    def contains(self, st):
        if st in self.noun:
            return True
        if st in self.pre_modifiers:
            return True
        if st in self.post_modifiers:
            return True
        return False



    def build(self, sentence):
        word_list = sentence.sentence
        pos_list = sentence.pos
        verb_indexes = [i for i, x in enumerate(pos_list) if x == ['V']]
        main_verb_index = sentence.phrase_list[-1].end_idx
        aux_verb_index = -1
        if len(verb_indexes) > 1:
            aux_verb_index = verb_indexes[1]
        if word_list[main_verb_index + 1] == 'the':
            if (pos_list[main_verb_index + 2] != ['ADJ']) and (pos_list[main_verb_index + 2] != ['#']):
                self.pre_modifiers.append(word_list[main_verb_index + 1])
                self.noun = [word_list[main_verb_index + 2]]
                self.start_idx = main_verb_index + 1
                self.end_idx = main_verb_index + 2
                if self.end_idx < (len(word_list) - 1):
                    if ['V'] not in pos_list[self.end_idx:]:
                        self.post_modifiers.append(word_list[self.end_idx+1:])
                        self.end_idx += len(word_list[self.end_idx+1:])
                        return self
                    else:
                        return self
            else:
                self.start_idx = main_verb_index + 1
                self.end_idx = main_verb_index + 1
                for i, x in enumerate(pos_list):
                    if i > main_verb_index:
                        if x == ['ADJ']:
                            self.pre_modifiers.append(word_list[i])
                            self.end_idx += 1
                        if x == ['N']:
                            self.noun.append(word_list[i])
                            self.end_idx += 1
                            break
                if (self.end_idx + 1 < len(word_list)) and pos_list[self.end_idx] == ['P']:
                    self.post_modifiers.append(word_list[self.end_idx:])
                    self.end_idx += len(word_list[self.end_idx:])
                return self
        if (pos_list[main_verb_index + 1] == ['N']):
            self.noun = [word_list[main_verb_index + 1]]
            self.start_idx = main_verb_index + 1
            self.end_idx = main_verb_index + 1
        if (pos_list[main_verb_index + 2] == ['#']):
            self.post_modifiers.append(word_list[main_verb_index + 2])
            self.end_idx = main_verb_index + 2
        if (pos_list[main_verb_index + 2] == ['N']):
            self.post_modifiers.append(word_list[main_verb_index + 2])
            self.end_idx = main_verb_index + 2
        if main_verb_index + 3 < len(pos_list):
            if ((pos_list[main_verb_index + 3] == ['N']) or (pos_list[main_verb_index + 3] == ['ADJ'])) and \
                    (word_list[main_verb_index + 3] in ['open', 'close', 'start', 'due', 'worth']):
                self.post_modifiers.append(word_list[main_verb_index + 3])
                self.end_idx = main_verb_index + 3
        if (self.end_idx+1) < aux_verb_index:
            self.post_modifiers.append(word_list[self.end_idx+1:aux_verb_index])
            self.end_idx = aux_verb_index - 1
        if (self.end_idx+1 < len(word_list)) and pos_list[self.end_idx] == ['P']:
            self.post_modifiers.append(word_list[self.end_idx:])
            self.end_idx += len(word_list[self.end_idx:])

        return self


class ObjPhrase:

    def __init__(self):
        self.start_idx = -1
        self.end_idx = -1
        self.noun = []
        self.pre_modifiers = []
        self.post_modifiers = []

    def __str__(self):
        return str(self.pre_modifiers) + "|" + str(self.noun) + "|" + str(self.post_modifiers)

    def contains(self, st):
        if st in self.noun:
            return True
        if st in self.pre_modifiers:
            return True
        if st in self.post_modifiers:
            return True
        return False

    def build(self, sentence):
        word_list = sentence.sentence
        pos_list = sentence.pos
        last_idx = sentence.phrase_list[-1].end_idx
        self.start_idx = last_idx + 1
        if (pos_list[last_idx + 1] == ['P']) and (last_idx + 1 <= len(pos_list)):
            self.pre_modifiers.append(word_list[last_idx + 1])
            self.end_idx = last_idx + 1
            if (pos_list[last_idx + 2] == ['N']):
                if (last_idx + 3 < len(pos_list)):
                    if (pos_list[last_idx + 3] == ['#']):
                        self.noun.append(word_list[last_idx + 2])
                        self.post_modifiers.append(word_list[last_idx + 3])
                        self.end_idx = last_idx + 3
                else:
                    self.noun.append((word_list[last_idx + 2]))
                    self.end_idx = last_idx + 2
            if (pos_list[last_idx + 2] == ['ADJ']) and (pos_list[last_idx + 3] == ['N']) and \
                    (last_idx + 3 <= len(pos_list)):
                self.pre_modifiers.append(word_list[last_idx + 2])
                self.noun.append(word_list[last_idx + 3])
                self.end_idx = last_idx + 3
            if (pos_list[last_idx + 2] == ['ADJ']) and (pos_list[last_idx + 3] == ['ADJ']) and \
                    (pos_list[last_idx + 4] == ['N']):
                self.pre_modifiers.append(word_list[last_idx + 2])
                self.pre_modifiers.append(word_list[last_idx + 3])
                self.noun.append(word_list[last_idx + 4])
                self.end_idx = last_idx + 4
        if (last_idx + 1) < (len(word_list) - 1):
            if (pos_list[last_idx + 1] == ['N']) and (pos_list[last_idx + 2] == ['#']) and \
                    (last_idx + 2 <= len(pos_list)):
                self.noun.append(word_list[last_idx + 1])
                self.post_modifiers.append(word_list[last_idx + 2])
                self.end_idx = last_idx + 2
            if (pos_list[last_idx + 1] == ['N']) and (pos_list[last_idx + 2] == ['N']) and \
                    (last_idx + 2 <= len(pos_list)):
                self.noun.append(word_list[last_idx + 1])
                self.post_modifiers.append(word_list[last_idx + 2])
                self.end_idx = last_idx + 2
            if (pos_list[last_idx + 1] == ['N']) and (pos_list[last_idx + 2] == ['P']) and \
                    (last_idx + 2 <= len(pos_list)):
                self.noun.append(word_list[last_idx + 1])
                self.post_modifiers.append(word_list[last_idx + 2])
                self.end_idx = last_idx + 2
            if (word_list[last_idx + 1] == 'the') and (pos_list[last_idx + 2] == ['N']) and \
                    (last_idx + 2 <= len(pos_list)):
                self.pre_modifiers.append(word_list[last_idx + 1])
                self.noun.append(word_list[last_idx + 2])
                self.end_idx = last_idx + 2
                if (self.end_idx + 1 < len(word_list)):
                    self.post_modifiers.append(word_list[self.end_idx+1:])
                    self.end_idx += len(word_list[self.end_idx:])

        return self




# questions = []
# intents = []
#
# with open('ExampleQuestions.json', encoding='utf-8') as json_data:
#     ground_truth_dicts = json.load(json_data)
#     for gtd in ground_truth_dicts:
#         questions.append(gtd['question'])
#         intents.append(gtd['intent'])
#
# for i, q in enumerate(questions):
#     print(i)
#     s = Sentence(q.lower())
#     print(s.sentence)
#     print(s.pos)
#     a = QPhrase()
#     a = QPhrase.build(a, s)
#     s.phrase_list.append(a)
#     print("QPhrase: " + str(a))
#     b = MVPhrase()
#     b = MVPhrase.build(b, s)
#     s.phrase_list.append(b)
#     print("MVPhrase: " + str(b))
#     d = SubjPhrase()
#     d = SubjPhrase.build(d, s)
#     s.phrase_list.append(d)
#     print("SubjPhrase: " + str(d))
#     if (len([i for i, x in enumerate(s.pos) if x == ['V']]) >= 2) and (s.phrase_list[-1].end_idx < (len(s.pos) - 1)):
#         c = AVPhrase()
#         c = AVPhrase.build(c, s)
#         s.phrase_list.append(c)
#         print("AVPhrase: " + str(c))
#     if s.phrase_list[-1].end_idx < (len(s.pos) - 1):
#         e = ObjPhrase()
#         e = ObjPhrase.build(e, s)
#         s.phrase_list.append(e)
#         print("ObjPhrase: " + str(e))
#     if s.phrase_list[-1].end_idx < (len(s.pos) - 1):
#         f = AAVPhrase()
#         f = AAVPhrase.build(f, s)
#         s.phrase_list.append(f)
#         print("AAVPhrase: " + str(f))
#     print("-------------------------------------------------------")
#     print(s)
#     print("-------------------------------------------------------")
#     print("-------------------------------------------------------")

#tricksters: 13, 15,