"""
============================================
Autograder - Version Project 3 student110318


usage: -s <json containing syllabus (statements/questions)>
       -l <path/filename to log file>
       -v verbose output to console
       -h this message to console
============================================
"""


# standard library
import sys
import getopt
import json
import traceback
from contextlib import redirect_stdout

# local libraries
from project3.AgentInterface import AgentInterface


def format_string(list_of_words, start=False):
    """Format list of words into a CSV string"""

    deli = ','
    retstr = ""
    if start:
        retstr += deli
    for word in list_of_words:
        retstr += (word + deli)
    return retstr


class Grader:
    """Compare the students result with the groundtruth"""

    def __init__(self):
        self._stats = {'answer': {'count': 0, 'match': 0}}

    def grade(self, groundtruth, student):
        """Compare and accumulate result"""

        self._stats['answer']['count'] += 1
        if groundtruth == student:
            self._stats['answer']['match'] += 1

    def header_string(self):
        """Generate a string to describe grader output"""

        retval = ["count", "match"]
        return retval

    def result_string(self):
        """Output grader result"""

        return [str(self._stats['answer']['count']), str(self._stats['answer']['match'])]


class Logger:
    """Log to a file"""

    def __init__(self, logname, verbose):
        self._verbose = verbose
        print("Logging to file: " + logname + ".log")
        self._log_file = open(logname + ".log", "w")
        self._result_file = open(logname + ".result", "w")

    def logmsg(self, msg):
        """Log msg to log file"""

        self._log_file.write(msg)
        if self._verbose:
            print(msg, end='')

    def resultmsg(self, msg):
        """Log msg to result file"""

        self._result_file.write(msg)
        if self._verbose:
            print(msg, end='')

    def logclose(self):
        """Close the log file"""

        self._log_file.write("\n\n")
        self._result_file.write("\n\n")
        self._log_file.close()


def agent_autograder(parameters):
    """Test student's agent"""

    retval = 0
    _syllabus_filename = parameters['syllabus']
    _verbose = parameters['verbose']
    print("Opening syllabus: " + _syllabus_filename)
    try:
        with open(_syllabus_filename, encoding='utf-8') as json_data:
            _ground_truth_dicts = json.load(json_data)
    except Exception as _err:
        print("Failure opening or reading syllabus: " + str(_err))
        return 1

    print("Redirecting to file: " + parameters['log'] + ".out")
    try:
        redirect = open(parameters['log'] + ".out", "w")
    except:
        print("Failed to open redirection file")
        return 1

    _logger = Logger(parameters['log'], _verbose)

    try:
        _statements = _ground_truth_dicts['statements']
    except IndexError as _err:
        print("Could not find statements in syllabus: "+str(_err))

    try:
        _questions = _ground_truth_dicts['questions']
    except IndexError as _err:
        print("Could not find questions in syllabus: "+str(_err))

    try:
        _grader = Grader()
        print("\n\nInstantiating student agent")
        _agent = AgentInterface(parameters['verbose'])

        print("\n\nTrain the student's agent")
        _agent.load_syllabus(_statements)

        print("\n\nStarting test")
        _head = ["question", "answer", "studentAnswer", "count", "# correct"]
        _logger.logmsg(format_string(_head, False))
        _logger.logmsg("\n")
        for _ground_truth_dict in _questions:
            _ground_truth_question = _ground_truth_dict['question']
            _ground_truth_intent = _ground_truth_dict['answer']

            with redirect_stdout(redirect):
                _student_agent_intent = _agent.input_output(_ground_truth_question)

            _grader.grade(_ground_truth_intent, _student_agent_intent)

            _result = [                                 \
                            _ground_truth_question,     \
                            str(_ground_truth_intent),  \
                            str(_student_agent_intent)  \
                      ]
            _logger.logmsg(format_string(_result, False))
            _logger.logmsg(format_string(_grader.result_string(), False))
            _logger.logmsg("\n")

        # log file
        _logger.logmsg("\n\n" + format_string(_grader.header_string(), False))
        _logger.logmsg("\n"+format_string(_grader.result_string(), False))

        # results file
        _logger.resultmsg("\n\n"+format_string(_grader.header_string(), False))
        _logger.resultmsg("\n"+format_string(_grader.result_string(), False))

    except Exception as _err:
        _logger.logmsg("Error during grading: " + str(_err))
        _logger.logmsg(traceback.print_exc(file=sys.stdout))
        retval = 1

    print("\nDone")
    _logger.logclose()
    return retval


def main(argv):
    """Command Line Interface"""

    parameters = {                                  \
                    'verbose': False,               \
                    'syllabus': "Syllabus.json",    \
                    'log': "results"                \
                 }

    print(__doc__)
    try:
        opts, args = getopt.getopt(argv, "vs:l:")
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        if opt in "-v":  # -v verbose
            parameters['verbose'] = True
        elif opt in "-s":  # -f <json containing dictionary frames>
            parameters['syllabus'] = arg
        elif opt in "-l":  # -l <path/filename to log file>
            parameters['log'] = arg

    return agent_autograder(parameters)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
