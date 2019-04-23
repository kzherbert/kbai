from project3.Sentence import Sentence

CONCEPTS = ["project", "projects", "assignment", "assignments", "midterm", "final", "course", "announcements",
            "instructor", "report", "reports", "exams", "strategies", "strategy", "policy", "peer-feedback",
            "office-days", "content", "communication", "submissions", "TA", "component", "code", "policies"]


class Concept:

    # the concept contained in the object
    concept = None
    # below attributes relevant to submission style concepts
    number = None
    due_date = []
    process = []
    release_date = []
    weight = []
    # below attributes relevant for concepts with a span of time
    duration = []
    # below attributes relevant for instructor concepts
    name = []

    # list of other modifiers that do not fit the above categories
    modifiers = []

    def __init__(self, concept, number=None, due_date=None, process=None, release_date=None, weight=None,
                 modifiers=None, duration=None, name=None):
        self.concept = concept
        if number is not None:
            self.number = number
        elif due_date is not None:
            self.due_date.append(due_date)
        elif process is not None:
            self.process.append(process)
        elif release_date is not None:
            self.release_date.append(release_date)
        elif weight is not None:
            self.weight.append(weight)
        elif modifiers is not None:
            self.modifiers.append(modifiers)
        elif duration is not None:
            self.duration.append(duration)
        elif name is not None:
            self.name.append(name)
        else:
            self.number = None
            self.due_date = []
            self.process = []
            self.release_date = []
            self.weight = []
            self.modifiers = []
            self.duration = []


    def __str__(self):
        return ("Concept: " + str(self.concept) + "\n" + "Number: " + str(self.number) + "\n" +
                "Due Date: " + str(self.due_date) + "\n" + "Process: " + str(self.process) + "\n" +
                "Release Date: " + str(self.release_date) + "\n" + "Weight: " + str(self.weight) + "\n" +
                "Duration: " + str(self.duration) + "\n" + "Modifiers: " + str(self.modifiers) + "\n")

    def find_number(self, statement):
        sentence = statement.sentence
        if len(sentence.subject) > 1:
            for w in sentence.subject[1:]:
                if w.isnumeric():
                    self.number = int(w)
        return


class Statement:

    concept = None
    category = None
    sentence = None
    words = []

    def __init__(self, list_of_words):
        self.words = list_of_words
        self.sentence = Sentence(list_of_words)
        c = Concept(self.sentence.object)
        self.concept = self.get_concept(c)

    def __str__(self):
        # print("Sentence:\n")
        # print(str(self.sentence))
        return "Concept: " + str(self.concept) + "\n" + "Words: " + str(self.words) + "\n" + \
               "POS: " + str(self.sentence.parts_of_speech)

    def get_concept(self, concept):
        object = self.sentence.object
        # obj_index = self.sentence.list_of_words.index(object)

        scores = self.sentence.get_category_scores()
        # print(scores)

        category = max(scores, key=scores.get)
        self.category = (category, scores)
        # print(scores)
        # print(category)

        # some code for recording noun modifiers to the main concept
        # if object in self.sentence.subject:
        #     subject_pre_object = self.sentence.subject[:self.sentence.subject.index(object)]
        #     subject_post_object = self.sentence.subject[self.sentence.subject.index(object)+1:]
        #     if len(subject_pre_object) > 0:
        #         concept.modifiers.append(subject_pre_object)
        #     if len(subject_post_object) > 0:
        #         concept.modifiers.append(subject_post_object)


        # some code for submission type concepts
        if object in ["project", "assignment", "report", "code", "component"]:
            concept.find_number(statement=self)

        if category == 'RELEASEDATE':
            predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
            idxs = [i for i, x in enumerate(predicate_pos) if x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
            concept.release_date.append([self.sentence.predicate[i] for i in idxs])
        elif category == 'DUEDATE':
            predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
            idxs = [i for i, x in enumerate(predicate_pos) if x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
            concept.due_date.append([self.sentence.predicate[i] for i in idxs])
        elif category == 'DURATION':
            predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
            idxs = [i for i, x in enumerate(predicate_pos) if x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
            concept.duration.append([self.sentence.predicate[i] for i in idxs])
        elif category == 'WEIGHT':
            predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
            idxs = [i for i, x in enumerate(predicate_pos) if x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
            concept.weight.append([self.sentence.predicate[i] for i in idxs])
        elif category == 'PROCESS':
            if concept.concept in ['projects', 'assignments', 'reports', 'exams', 'submissions']:
                if 'late' in self.words \
                        and ('projects' in self.words or 'assignments' in self.words or
                             'reports' in self.words or 'exams' in self.words or
                             'submissions' in self.words) \
                        and 'credit' in self.words:
                    mod = ['late', 'gets', self.words[self.words.index('credit') - 1], 'credit']
                    concept.process.append(mod)
            if concept.concept == 'course':
                if 'attendance' in self.words and 'is' in self.words and 'mandatory' in self.words:
                    if 'not' in self.words:
                        mod = ['attendance', 'is', 'not', 'mandatory']
                    else:
                        mod = ['attendance', 'is', 'mandatory']
                    concept.process.append(mod)
            predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
            idxs = [i for i, x in enumerate(predicate_pos) if x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
            concept.process.append([self.sentence.predicate[i] for i in idxs])
        elif category == 'GENERAL':
            if concept.concept in ['instructor', 'TA']:
                if self.sentence.mvp == ['is'] and \
                        (self.sentence.predicate == ['the', 'instructor'] or self.sentence.predicate == ['the', 'TA']):
                    concept.modifiers.append(self.sentence.subject)
                else:
                    predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
                    idxs = [i for i, x in enumerate(predicate_pos) if
                            x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
                    concept.modifiers.append([self.sentence.predicate[i] for i in idxs])
            elif concept.concept == 'course':
                if self.sentence.mvp == ['is'] and self.sentence.predicate == ['in', 'the', 'course']:
                    concept.modifiers.append(self.sentence.subject)
                else:
                    predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
                    idxs = [i for i, x in enumerate(predicate_pos) if
                            x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
                    concept.modifiers.append([self.sentence.predicate[i] for i in idxs])
            else:
                predicate_pos = self.sentence.parts_of_speech[self.sentence.pred_index:]
                idxs = [i for i, x in enumerate(predicate_pos) if
                        x == ['N'] or x == ['P'] or x == ['#'] or x == ['ADJ']]
                concept.modifiers.append([self.sentence.predicate[i] for i in idxs])

        # print(str(concept))
        return concept
