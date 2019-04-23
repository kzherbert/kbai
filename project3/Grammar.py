VOCABULARY = ['project', 'the', 'ai', 'piazza', 'yaroslav', 'monday', 'projects', 'will', 'during', 'due', 'mandatory',
              'tuesday', 'assignment', 'belong', 'slack', 'python', 'wednesday', 'assignments', 'in', 'and', 'ashok',
              'canvas', 'thursday', 'midterm', 'is', 'pdf', 'goel', 'learning', 'friday', 'final', 'of', 'doing',
              'start', 'everyday', 'saturday', 'course', 'has', 'need', 'litvak', 'finish', 'sunday', 'announcements',
              'to', 'into', 'posted', 'complete', 'procedure', 'instructor', 'are', 'turn', 'class', 'check',
              'reading-list', 'report', 'a', 'week', 'many', 'contribute', 'reports', 'this', 'java', 'weeks', 'submit',
              'class-grade', 'as', 'c++', 'videos', 'there', 'morning', 'by', 'close', 'hours', 'reading', 'midnight',
              'exams', 'for', 'list', 'video', 'human', 'classroom', 'strategies', 'on', 'book', 'late', 'occurs',
              'available', 'strategy', 'all', 'does', 'end', 'example', 'submitted', 'policy', 'occur', 'docx', 'files',
              'regularly', 'distributed', 'peer-feedback', 'must', 'text', 'after', 'should', 'attendance',
              "office-days", 'no', 'worth', 'write', 'method', 'knowledge-based', 'content', 'every', 'file', 'learn',
              'planning', 'self-reflection', 'communication', 'do', 'open', 'have', 'cognition', 'peer-to-peer',
              'submissions', 'can', 'turned', 'teach', 'released', 'decision-making', 'TA', 'get', 'credit',
              'preferred', 'collaboration', 'component', 'i', 'zip', 'grade', 'code', 'if', 'gz', 'work', 'policies',
              'my', 'bz2', 'begin', 'be']
NOUNS = ["assignment", "i", "week", "project", "start", "midterm", "final", "submissions", "end", "weeks", "code",
         "finish", "grade", "canvas", "pdf", "zip", "file", "report", "procedure", "class", "announcements", "piazza",
         "collaboration", "learning", "ai", "human", "cognition", "there", "projects", "assignments", "course",
         "instructor", "report", "exams", "strategies", "strategy", "policy", "peer-feedback", "office-days", "content",
         "communication", "TA", "component", "policies", "doing", "java", "c++", "list", "book", "text", "credit", "gz",
         "bz2", "slack", "ashok", "goel", "litvak", "videos", "hours", "video", "files", "work", "yaroslav", "python",
         "reading", "example", "method", "planning", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
         "sunday", "reading-list", "class-grade", "morning", "midnight", "classroom", "self-reflection",
         "decision-making", "reports", "attendance"]
VERBS = ["will", "do", "can", "begin", "start", "is", "distributed", "occurs", "does", "open", "need", "submitted",
         "turned", "submit", "should", "have", "turn", "close", "complete", "finish", "write", "code", "grade",
         "contribute", "get", "are", "must", "end", "released", 'close', "occur", "posted", "learn", "teach", "check",
         "preferred", "belong", "has", 'be', "due", "available"]
ADJS = ["available", "worth", "final", "open", "due", "learning", "many", "knowledge-based", "human", "a", "the", "my",
        "docx", "late", "mandatory", "everyday", "knowledge-based", "peer-to-peer", 'no']
ADVS = ["as", "regularly"]
PREPS = ["in", "on", "during", "of", "to", "by", "for", "into", "after"]
CONJS = ["and", "if"]
QWORDS = []
DETERMINERS = ["every", "all", "this"]
GREEN_WORDS = ["project", "projects", "assignment", "assignments", "midterm", "final", "course", "announcements",
            "instructor", "report", "reports", "exams", "strategies", "strategy", "policy", "peer-feedback",
            "office-days", "content", "communication", "submissions", "TA", "component", "code", "policies"]


def validate_sentence(list_of_words):
    if len(list_of_words) > 11:
        return 0

    if not any(gw in GREEN_WORDS for gw in list_of_words):
        return 1

    for w in list_of_words:
        if w.isnumeric() or "%" in w:
            continue
        if w not in VOCABULARY:
            return w

    if not any(gw in GREEN_WORDS for gw in list_of_words):
        return 1

    return True

def is_numeric(x):
    if (x.isnumeric()) or ("%" in x):
        return True
    else:
        return False


def break_pos_ties(pos, list_of_words):
    for i, word in enumerate(list_of_words):
        if pos[i] == ['N', 'V']:
            if (i + 1) >= len(pos):
                pos[i] = ['N']
                if pos[i - 1] == ['ADJ']:
                    pos[i] = ['N']
                continue
            if pos[i - 1] == ['ADJ']:
                pos[i] = ['N']
                continue
            if pos[i - 1] == ['#']:
                pos[i] = ['N']
                continue
            if list_of_words[i - 1] in ['i', 'class']:
                pos[i] = ['V']
                continue
            if pos[i + 1] == ['V']:
                pos[i] = ['N']
                continue
            else:
                pos[i] = ['V']
                continue
        if pos[i] == ['N', 'ADJ']:
            if (i + 1) >= len(pos):
                pos[i] = ['N']
                continue
            if (pos[i - 1] == ['ADJ']) and (pos[i + 1] == ['N']):
                pos[i] = ['ADJ']
                continue
            if (pos[i - 1] == ['ADJ']) and (pos[i + 1] == ['N', 'V']):
                pos[i] = ['ADJ']
                continue
            if (pos[i - 1] == ['ADJ']) and (pos[i + 1] != ['N']):
                pos[i] = ['N']
                continue
            if (pos[i - 1] == ['P']) and (pos[i + 1] == ['N']):
                pos[i] = ['ADJ']
                continue
        if pos[i] == ['V', 'ADJ']:
            if (pos[i - 1] == ['N']) and (list_of_words[i - 1] not in ['i', 'class']):
                pos[i] = ['ADJ']
                continue
            if (pos[i - 1] == ['N']) and (list_of_words[i - 1] in ['i', 'class']):
                pos[i] = ['V']
                continue
            if (pos[i - 1] == ['N']) or (pos[i - 1] == ['#'] and pos[i - 2] == ['N']):
                pos[i] = ['V']
        if pos[i] == ['N', 'V', 'ADJ']:
            if (pos[i - 1] == ['ADJ']) and (pos[i + 1] == ['N']):
                pos[i] = ['ADJ']
            if (pos[i - 1] == ['#']) and (pos[i + 1] == ['N']):
                pos[i] = ['ADJ']

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

    return pos


def assign_pos(list_of_words):
    pos = []

    for w in list_of_words:
        possible_pos = []
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
        if (w.isnumeric()) or ("%" in w):
            possible_pos.append('#')
        if w in DETERMINERS:
            possible_pos.append('D')
        pos.append(possible_pos)

    return break_pos_ties(pos, list_of_words)


vocab = ['project', 'the', 'ai', 'piazza', 'yaroslav', 'monday', 'projects', 'will', 'during', 'due', 'mandatory',
         'tuesday', 'assignment', 'belong', 'slack', 'python', 'wednesday', 'assignments', 'in', 'and', 'ashok',
         'canvas', 'thursday', 'midterm', 'is', 'pdf', 'goel', 'learning', 'friday', 'final', 'of', 'doing', 'start',
         'everyday', 'saturday', 'course', 'has', 'need', 'litvak', 'finish', 'sunday', 'announcements', 'to', 'into',
         'posted', 'complete', 'procedure', 'instructor', 'are', 'turn', 'class', 'check', 'reading-list', 'report', 'a',
         'week', 'many', 'contribute', 'reports', 'this', 'java', 'weeks', 'submit', 'class-grade', 'as',
         'c++', 'videos', 'there', 'morning', 'by', 'close', 'hours', 'reading', 'midnight', 'exams',
         'for', 'list', 'video', 'human', 'classroom', 'strategies', 'on', 'book', 'late', 'occurs', 'available',
         'strategy', 'all', 'does', 'end', 'example', 'submitted', 'policy', 'occur', 'docx', 'files', 'regularly',
         'distributed', 'peer-feedback', 'must', 'text', 'after', 'should', 'attendance', "office-days", 'no', 'worth',
         'write', 'method', 'knowledge-based', 'content', 'every', 'file', 'learn', 'planning', 'self-reflection',
         'communication', 'do', 'open', 'have', 'cognition', 'peer-to-peer', 'submissions', 'can', 'turned', 'teach',
         'released', 'decision-making', 'TA', 'get', 'credit', 'preferred', 'collaboration', 'component', 'i', 'zip',
         'grade', 'code', 'if', 'gz', 'work', 'policies', 'my', 'bz2', 'begin']

# this code was for reducing from project 2 vocab to project 3 vocab

# forgotten = []
# twice = []
# old = []
# for w in vocab:
#     if w not in NOUNS and w not in VERBS and w not in ADJS and w not in ADVS and w not in PREPS and w not in CONJS and \
#             w not in QWORDS and w not in DETERMINERS:
#         forgotten.append(w)
#     cntr = 0
#     for l in [NOUNS, VERBS, ADJS, ADVS, PREPS, CONJS, QWORDS, DETERMINERS]:
#         if w in l:
#             cntr += 1
#     if cntr > 1:
#         twice.append(w)
#
#     for l in [NOUNS, VERBS, ADJS, ADVS, PREPS, CONJS, QWORDS, DETERMINERS]:
#         for y in l:
#             if y not in vocab:
#                 old.append(y)
#
# print(forgotten)
# print(twice)
# print(old)