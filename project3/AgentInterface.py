"""
StudentAgent - Project 3 Updated 11/03/2018

DO NOT CHANGE THIS FILE
"""

from project3 import StudentAgent


class AgentInterface:
    """Interface between autograder and student agent"""

    def __init__(self, verbose):
        self._student_agent = StudentAgent.StudentAgent(verbose)

    def _parse_question(self, question):
        """Parse question into words"""

        return question.lower().split(' ')

    def load_syllabus(self, list_of_statements):
        """Load the statements into the agent"""

        self._student_agent.load_syllabus(list_of_statements)

    def input_output(self, question):
        """input_output(question : string) :        response : int"""

        _word_list = self._parse_question(question)
        _answer = self._student_agent.input_output(_word_list)
        return _answer
