"""
Project 3

ADD YOUR CODE HERE

Please read project directions before importing anything
"""
from project3.Statement import *
from project3.Question import Question
from project3 import Grammar


class StudentAgent:
    """ADD YOUR CODE HERE"""

    def __init__(self, verbose):
        self._verbose = verbose
        self.statements = []        # array of interpreted statements from Syllabus.json
        self.knowledge = []         # array of concepts, condensed from the series of statements
        # TODO: Add your init code here

    def build_knowledge(self):

        for i, s in enumerate(self.statements):
            for stmnt in self.knowledge:
                # if concept is submission type, it will also need to match the number
                if s.concept.number is None:
                    if s.concept.concept == stmnt.concept.concept:
                        if s.concept.due_date is None and stmnt.concept.due_date is not None:
                            s.concept.due_date = stmnt.concept.due_date
                        if s.concept.process is None and stmnt.concept.process is not None:
                            s.concept.process = stmnt.concept.process
                        if s.concept.release_date is None and stmnt.concept.release_date is not None:
                            s.concept.release_date = stmnt.concept.release_date
                        if s.concept.weight is None and stmnt.concept.weight is not None:
                            s.concept.weight = stmnt.concept.weight
                        if s.concept.duration is None and stmnt.concept.duration is not None:
                            s.concept.duration = stmnt.concept.duration
                        if s.concept.modifiers != stmnt.concept.modifiers:
                                s.concept.modifiers.append(stmnt.concept.modifiers)
                        if s.concept.due_date is not None and stmnt.concept.due_date is not None:
                            for e in stmnt.concept.due_date:
                                s.concept.due_date.append(e)
                        if s.concept.process is not None and stmnt.concept.process is not None:
                            for e in stmnt.concept.process:
                                s.concept.process.append(e)
                        if s.concept.release_date is not None and stmnt.concept.release_date is not None:
                            for e in stmnt.concept.release_date:
                                s.concept.release_date.append(e)
                        if s.concept.weight is not None and stmnt.concept.weight is not None:
                            for e in stmnt.concept.weight:
                                s.concept.weight.append(e)
                        if s.concept.duration is not None and stmnt.concept.duration is not None:
                            for e in stmnt.concept.duration:
                                s.concept.duration.append(e)
                        self.knowledge.remove(stmnt)
                elif s.concept.number is not None:
                    if s.concept.concept == stmnt.concept.concept and s.concept.number == stmnt.concept.number:
                        if s.concept.due_date is None and stmnt.concept.due_date is not None:
                            s.concept.due_date = stmnt.concept.due_date
                        if s.concept.process is None and stmnt.concept.process is not None:
                            s.concept.process = stmnt.concept.process
                        if s.concept.release_date is None and stmnt.concept.release_date is not None:
                            s.concept.release_date = stmnt.concept.release_date
                        if s.concept.weight is None and stmnt.concept.weight is not None:
                            s.concept.weight = stmnt.concept.weight
                        if s.concept.duration is None and stmnt.concept.duration is not None:
                            s.concept.duration = stmnt.concept.duration
                        if s.concept.modifiers != stmnt.concept.modifiers:
                            s.concept.modifiers.append(stmnt.concept.modifiers)
                        if s.concept.due_date is not None and stmnt.concept.due_date is not None:
                            for e in stmnt.concept.due_date:
                                s.concept.due_date.append(e)
                        if s.concept.process is not None and stmnt.concept.process is not None:
                            for e in stmnt.concept.process:
                                s.concept.process.append(e)
                        if s.concept.release_date is not None and stmnt.concept.release_date is not None:
                            for e in stmnt.concept.release_date:
                                s.concept.release_date.append(e)
                        if s.concept.weight is not None and stmnt.concept.weight is not None:
                            for e in stmnt.concept.weight:
                                s.concept.weight.append(e)
                        if s.concept.duration is not None and stmnt.concept.duration is not None:
                            for e in stmnt.concept.duration:
                                s.concept.duration.append(e)
                        if s.concept.number is None:
                            s.concept.number = stmnt.concept.number
                        self.knowledge.remove(stmnt)
            self.knowledge.append(s)

    def load_syllabus(self, list_of_list_of_statement_words):
        """Train agents from statements"""

        for i, _statement in enumerate(list_of_list_of_statement_words):
            list_of_words = _statement.lower().split(' ')

            # for debugging one at a time
            # if i in [1, 2, 22]:
            #     continue

            # check if list of words is valid
            valid = Grammar.validate_sentence(list_of_words)
            if valid is not True:
                if valid == 0:
                    print(list_of_words)
                    print("This statement is not valid. It is too long.")
                    print("Length: " + str(len(list_of_words)))
                    continue
                elif valid == 1:
                    print(list_of_words)
                    print("This statement is not valid. It has no green word.")
                    continue
                else:
                    print(list_of_words)
                    print("This statement is not valid. It contains words not in the Vocabulary")
                    print("Bad Word:" + str(Grammar.validate_sentence(list_of_words)))
                    continue

            s = Statement(list_of_words)

            # if concept is already in knowledge-base, update
            # else append
            self.statements.append(s)

            # print('------------------START-------------------------------------')
            # print(list_of_words)
            # print('------------------------------------------------------------')
            # print(s.sentence)
            # print(s.category)
            # print(_statement)   # for debugging
            # print("Statement:\n" + str(i) + "\n" + str(s))
            # print('------------------END---------------------------------------')
            # print('############################################################')

        self.build_knowledge()

    def input_output(self, word_list):
        """takes in list of words, returns question_object and data_requested"""

        try:
            _answer = "idk"

            list_of_words = word_list
            print(word_list) # for debugging only

            valid = Grammar.validate_sentence(list_of_words)
            if valid is not True and valid != 1:
                if valid == 0:
                    print(list_of_words)
                    print("This statement is not valid. It is too long.")
                    print("Length: " + str(len(list_of_words)))
                    return "IDK"
                else:
                    print(list_of_words)
                    print("This statement is not valid. It contains words not in the Vocabulary")
                    print("Bad Word:" + str(Grammar.validate_sentence(list_of_words)))
                    return "IDK"

            question = Question(list_of_words)

            q_object = question.object
            q_subject = question.subject
            q_category = question.category[0]
            q_mods = question.modifiers[0]
            q_modis = question.modifiers[1]
            q_number = None
            q_pos = question.parts_of_speech

            if q_object == 'IDK':
                return 'idk'

            for w in q_subject:
                if w.isnumeric():
                    q_number = int(w)
                if q_number is None:
                    words = question.list_of_words
                    try:
                        qoi = words.index(q_object)
                        if qoi + 1 < len(words):
                            if words[qoi+1].isnumeric():
                                q_number = int(words[qoi+1])
                    except:
                        if q_object == 'projects':
                            qot = 'project'
                        elif q_object == 'assignments':
                            qot = 'assignment'
                        elif q_object == 'reports':
                            qot = 'report'
                        elif q_object == 'course':
                            qot = 'class'
                        else:
                            qot = q_object
                        qoti = words.index(qot)
                        if qoti + 1 < len(words):
                            if words[qoti+1].isnumeric():
                                q_number = int(words[qoti+1])

            # print(q_object)
            #
            # print("--------------------------------------------")
            # print(question)
            # print("--------------------------------------------")
            # print(q_object)
            # print(q_subject)
            # print(q_category)
            # print(q_mods)
            # print(q_modis)
            # print(q_number)
            # print("--------------------------------------------")
            for k in self.knowledge:
                concept = k.concept
                match_score = -1

                if q_object is concept.concept:
                    match_score = 0

                    if q_object not in question.list_of_words and q_object == 'projects':
                        q_object = 'project'
                    if q_object not in question.list_of_words and q_object == 'assignments':
                        q_object = 'assigment'
                    if q_object not in question.list_of_words and q_object == 'reports':
                        q_object = 'report'

                    if q_object in ['projects', 'assignments', 'reports']:
                        qoi = question.list_of_words.index(q_object)
                        if question.list_of_words[:qoi - 1] == ['are', 'there'] and question.list_of_words[qoi-1].isnumeric():
                            num = int(question.list_of_words[qoi-1])
                            cntr = 0
                            for k in self.knowledge:
                                if k.concept.concept == 'project' and q_object == 'projects':
                                    cntr += 1
                                if k.concept.concept == 'assignment' and q_object == 'assignments':
                                    cntr += 1
                                if k.concept.concept == 'report' and q_object == 'reports':
                                    cntr += 1

                            if cntr == num:
                                _answer = "yes"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer
                            else:
                                _answer = "no"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer
                        if question.list_of_words[:qoi] == ['are', 'there', 'many']:
                            cntr = 0
                            for k in self.knowledge:
                                if k.concept.concept == 'project' and q_object == 'projects':
                                    cntr += 1
                                if k.concept.concept == 'assignment' and q_object == 'assignments':
                                    cntr += 1
                                if k.concept.concept == 'report' and q_object == 'reports':
                                    cntr += 1

                            if cntr > 1:
                                _answer = "yes"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer
                            else:
                                _answer = "no"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer

                    if q_object not in question.list_of_words and q_object == 'course':
                        g = question.list_of_words[:question.list_of_words.index('class')]
                    else:
                        g = question.list_of_words[:question.list_of_words.index(q_object)]

                    if g == ['is', 'there', 'a'] or g == ['are', 'there', 'any'] or g == ['is', 'there', 'an']:
                        _answer = "yes"
                        # print("---")
                        # print(_answer)
                        # print("---")
                        return _answer

                    if q_number is None:

                        # print(concept.concept)
                        # if concept.number is not None:
                        #     print("Num: " + str(concept.number))
                        # if len(concept.due_date) > 0:
                        #     print("DueDate: " + str(concept.due_date))
                        # if len(concept.process) > 0:
                        #     print("Proc: " + str(concept.process))
                        # if len(concept.release_date) > 0:
                        #     print("RelDate: " + str(concept.release_date))
                        # if len(concept.weight) > 0:
                        #     print("Weight: " + str(concept.weight))
                        # if len(concept.duration) > 0:
                        #     print("Duration: " + str(concept.duration))
                        # if len(concept.modifiers) > 0:
                        #     print("Mods: " + str(concept.modifiers))

                        if q_category is "DUEDATE":
                            if len(concept.due_date) == 0:
                                _answer = "idk"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer

                            for (i, m) in zip(q_modis, q_mods):
                                # print(i)
                                # print(m)
                                for phrase in concept.due_date:
                                    phrase_l = len(phrase)
                                    if q_pos[i] == ['#'] and m in phrase:
                                        match_score += 5
                                    if q_pos[i] == ['N'] and m in phrase:
                                        match_score += 5

                        elif q_category is "RELEASEDATE":
                            if len(concept.release_date) == 0:
                                _answer = "idk"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer

                            for (i, m) in zip(q_modis, q_mods):
                                # print(i)
                                # print(m)
                                for phrase in concept.release_date:
                                    phrase_l = len(phrase)
                                    if q_pos[i] == ['#'] and m in phrase:
                                        match_score += 5
                                    if q_pos[i] == ['N'] and m in phrase:
                                        match_score += 5

                        elif q_category is "DURATION":
                            if len(concept.duration) == 0:

                                if len(concept.due_date) == 1 and len(concept.release_date) == 1:
                                    num_due = int([n for n in concept.due_date[0] if n.isnumeric()][0])
                                    num_rel = int([n for n in concept.release_date[0] if n.isnumeric()][0])
                                    num_ask = 0
                                    # print(num_rel, num_due)
                                    # print('###')
                                    for m in q_mods:
                                        if "week" in m:
                                            if m[m.index("week")-1].isnumeric():
                                                num_ask = int(m[m.index("week")-1])
                                        else:
                                            for w in m:
                                                if w.isnumeric():
                                                    num_ask = int(w)

                                    if num_ask == (num_due - num_rel):
                                        _answer = "yes"
                                        # print("---")
                                        # print(_answer)
                                        # print("---")
                                        return _answer
                                    else:
                                        _answer = "no"
                                        # print("---")
                                        # print(_answer)
                                        # print("---")
                                        return _answer

                                _answer = "idk"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer
                            for (i, m) in zip(q_modis, q_mods):
                                # print(i)
                                # print(m)
                                for phrase in concept.duration:
                                    phrase_l = len(phrase)
                                    if q_pos[i] == ['#'] and m in phrase:
                                        match_score += 5
                                    if q_pos[i] == ['N'] and m in phrase:
                                        match_score += 5

                        elif q_category is "WEIGHT":
                            if len(concept.weight) == 0:
                                _answer = "idk"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer
                            for (i, m) in zip(q_modis, q_mods):
                                # print(i)
                                # print(m)
                                for phrase in concept.weight:
                                    phrase_l = len(phrase)
                                    if q_pos[i] == ['#'] and m in phrase:
                                        match_score += 5
                                    if q_pos[i] == ['N'] and m in phrase:
                                        match_score += 5

                        elif q_category is "PROCESS":
                            if len(concept.process) == 0:
                                _answer = "idk"
                                # print("---")
                                # print(_answer)
                                # print("---")
                                return _answer
                            for (i, m) in zip(q_modis, q_mods):
                                # print(i)
                                # print(m)
                                for phrase in concept.process:
                                    phrase_l = len(phrase)
                                    if q_pos[i] == ['#'] and m in phrase:
                                        match_score += 5
                                    if q_pos[i] == ['N'] and m in phrase:
                                        match_score += 5

                        else:

                            for (i, m) in zip(q_modis, q_mods):
                                # print(i)
                                # print(m)
                                for phrase in concept.modifiers:
                                    phrase_l = len(phrase)
                                    if q_pos[i] == ['#'] and m in phrase:
                                        match_score += 5
                                    if q_pos[i] == ['N'] and m in phrase:
                                        match_score += 5

                                    if m in phrase:
                                        match_score += 1

                    else:

                        if q_number is concept.number:

                            # print(concept.concept)
                            # if concept.number is not None:
                            #     print("Num: " + str(concept.number))
                            # if len(concept.due_date) > 0:
                            #     print("DueDate: " + str(concept.due_date))
                            # if len(concept.process) > 0:
                            #     print("Proc: " + str(concept.process))
                            # if len(concept.release_date) > 0:
                            #     print("RelDate: " + str(concept.release_date))
                            # if len(concept.weight) > 0:
                            #     print("Weight: " + str(concept.weight))
                            # if len(concept.duration) > 0:
                            #     print("Duration: " + str(concept.duration))
                            # if len(concept.modifiers) > 0:
                            #     print("Mods: " + str(concept.modifiers))

                            if q_category is "DUEDATE":
                                if len(concept.due_date) == 0:
                                    _answer = "idk"
                                    # print("---")
                                    # print(_answer)
                                    # print("---")
                                    return _answer
                                for (i, m) in zip(q_modis, q_mods):
                                    # print(i)
                                    # print(m)
                                    for phrase in concept.due_date:
                                        phrase_l = len(phrase)
                                        if q_pos[i] == ['#'] and m in phrase:
                                            match_score += 5
                                        if q_pos[i] == ['N'] and m in phrase:
                                            match_score += 5

                            elif q_category is "RELEASEDATE":
                                if len(concept.release_date) == 0:
                                    _answer = "idk"
                                    # print("---")
                                    # print(_answer)
                                    # print("---")
                                    return _answer
                                for (i, m) in zip(q_modis, q_mods):
                                    # print(i)
                                    # print(m)
                                    for phrase in concept.release_date:
                                        phrase_l = len(phrase)
                                        if q_pos[i] == ['#'] and m in phrase:
                                            match_score += 5
                                        if q_pos[i] == ['N'] and m in phrase:
                                            match_score += 5

                            elif q_category is "DURATION":
                                if len(concept.duration) == 0:

                                    if len(concept.due_date) == 1 and len(concept.release_date) == 1:
                                        num_due = int([n for n in concept.due_date[0] if n.isnumeric()][0])
                                        num_rel = int([n for n in concept.release_date[0] if n.isnumeric()][0])
                                        num_ask = 0

                                        if "week" in q_mods:
                                            num_ask = int(q_mods[q_mods.index("week") - 1])
                                        elif "weeks" in q_mods:
                                            num_ask = int(q_mods[q_mods.index("weeks") - 1])

                                        print(num_ask, num_due, num_rel)
                                        if num_ask == (num_due - num_rel):
                                            _answer = "yes"
                                            # print("---")
                                            # print(_answer)
                                            # print("---")
                                            return _answer
                                        else:
                                            _answer = "no"
                                            # print("---")
                                            # print(_answer)
                                            # print("---")
                                            return _answer

                                    _answer = "idk"
                                    # print("---")
                                    # print(_answer)
                                    # print("---")
                                    return _answer
                                for (i, m) in zip(q_modis, q_mods):
                                    # print(i)
                                    # print(m)
                                    for phrase in concept.duration:
                                        phrase_l = len(phrase)
                                        if q_pos[i] == ['#'] and m in phrase:
                                            match_score += 5
                                        if q_pos[i] == ['N'] and m in phrase:
                                            match_score += 5

                            elif q_category is "WEIGHT":
                                if len(concept.weight) == 0:
                                    _answer = "idk"
                                    # print("---")
                                    # print(_answer)
                                    # print("---")
                                    return _answer
                                for (i, m) in zip(q_modis, q_mods):
                                    # print(i)
                                    # print(m)
                                    for phrase in concept.weight:
                                        phrase_l = len(phrase)
                                        if q_pos[i] == ['#'] and m in phrase:
                                            match_score += 5
                                        if q_pos[i] == ['N'] and m in phrase:
                                            match_score += 5

                            elif q_category is "PROCESS":
                                if len(concept.process) == 0:
                                    _answer = "idk"
                                    # print("---")
                                    # print(_answer)
                                    # print("---")
                                    return _answer
                                for (i, m) in zip(q_modis, q_mods):
                                    # print(i)
                                    # print(m)
                                    for phrase in concept.process:
                                        phrase_l = len(phrase)
                                        if q_pos[i] == ['#'] and m in phrase:
                                            match_score += 5
                                        if q_pos[i] == ['N'] and m in phrase:
                                            match_score += 5

                            else:

                                for (i, m) in zip(q_modis, q_mods):
                                    # print(i)
                                    # print(m)
                                    for phrase in concept.modifiers:
                                        phrase_l = len(phrase)
                                        if q_pos[i] == ['#'] and m in phrase:
                                            match_score += 5
                                        if q_pos[i] == ['N'] and m in phrase:
                                            match_score += 5

                                        if m in phrase:
                                            match_score += 1

                # print(match_score)
                if match_score >= 7:
                    _answer = "yes"
                    # print("---")
                    # print(_answer)
                    # print("---")
                    return _answer
                elif match_score == -1:
                    _answer = "idk"
                else:
                    _answer = "no"
                    # print("---")
                    # print(_answer)
                    # print("---")
                    return _answer
                # print(_answer)

            # print("---")
            # print(_answer)
            # print("---")
            return _answer
        except:
            return "idk"

# with open('Syllabus.json', encoding='utf-8') as json_data:
#     ground_truth_dicts = json.load(json_data)
#
# _questions = (ground_truth_dicts['questions'])
#
# agent = StudentAgent(False)
# flag = 0
#
# with open('out.txt', 'w') as f:
#     print('Filename:', 'out.txt', file=f)
#     agent.load_syllabus(ground_truth_dicts['statements'])
#     if flag == 1:
#         for s in agent.statements:
#             print(str(s))
#             print('#########')
#     for i, x in enumerate(agent.knowledge):
#         print(str(x.concept), file=f)
#
#     cntr = 0
#     for z, _ground_truth_dict in enumerate(_questions):
#
#         # if z in [13]:
#         #     continue
#
#
#         _ground_truth_question = _ground_truth_dict['question']
#         _ground_truth_intent = _ground_truth_dict['answer']
#
#         response = agent.input_output(_ground_truth_question)
#         if _ground_truth_intent == response:
#             cntr += 1
#             # print(z, file=f)
#             # print("question: " + str(_ground_truth_question), file=f)
#             # print("agent_q: " + str(Question(_ground_truth_question.lower().split(' '))), file=f)
#             # print("true_answer: " + str(_ground_truth_intent), file=f)
#             # print('response: ' + str(response), file=f)
#         else:
#             print(z, file=f)
#             print("question: " + str(_ground_truth_question), file=f)
#             print("agent_q: " + str(Question(_ground_truth_question.lower().split(' '))), file=f)
#             print("true_answer: " + str(_ground_truth_intent), file=f)
#             print('response: ' + str(response), file=f)
#         print("----------------------------------", file=f)
#     print(str(cntr) + '/' + str(len(_questions)), file=f)




