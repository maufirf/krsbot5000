"""
This module handles the process of the main function, which is
the study plan generation using the previously made frameworks
that packs the data into usable objects in wrappers.
"""

# Built-in libraries
from enum import Enum

# Third-party libraries
#import numpy as np
from numpy import random as rd

# Premade frameworks
from framework.dbprocess import DBProcess
from framework.card import Study_Plan

class Core_C(Enum):
    """
    Enum for class `Core`

    So far, it tells about the average amount of credits
    the student usually have and the quantification of
    the student behavior on choosing study plans
    """
    # Credit quantification
    GENERAL_CREDITS = [18, 20, 22, 24]
    SPARSE_MULTIPLER = [0.5, 0.75]
    
    # Slotting behavior
    # Tuple contains the name and the probability
    GREED = ('greed', 0.1) # Forcibly use all the credits
    NORMAL = ('normal', 0.8) # Take possible courses while allowing unsued credits
    SPARSE = ('sparse', 0.1) # Take just the essentials

class Core:
    """
    Governs the study plan card generation

    Uses the Database Processor from `DBProcess`
    """
    def __init__(self, json_path='courses.json'):
        self.dbproc = DBProcess(json_path)
        self.wrap_instance = self.dbproc.wrap_as_object()

    def get_course_list_by_sem_credits(self, sem_credits, slot_behave=Core_C.NORMAL):
        """
        Returns a list of random courses (as `Course` object) with given
        semester credit and other settings.

        Parameters
        ----------
        sem_credits : `int`
            The amount of available credits
        slot_behave : `Core_C` (`Enum`)
            The student behavior while choosing the study plan, affects
            on how many final used credits will be.

        Returns
        -------
        `list`
            A list of `Courses` objects randomly selected.
        """
        if sem_credits <= 0: raise Exception('Semester Credits must be greater than zero!')
        courses_set = self.wrap_instance[3].copy()
        picks = []
        if slot_behave in [Core_C.NORMAL, Core_C.SPARSE]:
            if slot_behave==Core_C.SPARSE:
                sem_credits = int(sem_credits * rd.choice(Core_C.SPARSE_MULTIPLER.value)) + 1
            while(1):
                if (sem_credits <= 0 or len(courses_set)==0) or sem_credits < min(courses_set, key=lambda x: x.credit).credit: break
                if sem_credits < max(courses_set, key=lambda x: x.credit).credit: courses_set = list(filter(lambda x: x.credit < sem_credits, courses_set))
                #print(len(courses_set),end=' ')
                if (sem_credits <= 0 or len(courses_set)==0) or sem_credits < min(courses_set, key=lambda x: x.credit).credit: break
                picks.append(courses_set[rd.randint(0,len(courses_set))])
                sem_credits -= picks[-1].credit
                courses_set.remove(picks[-1])
        return picks

    def get_random_study_plan(self, sem_credits=-1, university=None, faculty=None, major=None, semester=None, random_type=0):
        """
        Returns an `Study_Plan` card. If the items are not given, the `Core`
        will select it randomly through the data obtained from its `DBProcess`.

        Parameters
        ----------
        sem_credits : `int`
            The amount of available credits\n
        university : `University` or `str`
            The `University` to be displayed on card. Will find the appropriate
            university in database if the argument is passed as `str`. In other
            cases, it assigns a random available university in the database.\n
        faculty : `Faculty` or `str`
            The `Faculty` to be displayed on card. Behaves the same like university
            argument\n
        major : `Major` or `str`
            The `Major` to be displayed on card. behaves the same like university
            argument\n
        semester : `int`
            What semester is this? If not given, it will pick between 1..8 inclusive.\n
        random_type : `int`
            Chooses the randomizer behavior explained in the module docs. possible
            values: `0`, `1`, and `2`.

        Returns
        -------
        `Study_Plan`
            The study plan card.
        """
        if random_type==0:
            if sem_credits <= 0 : sem_credits = rd.choice(Core_C.GENERAL_CREDITS.value)
            if not university: university = rd.choice(self.wrap_instance[0])
            if not faculty: faculty = rd.choice(self.wrap_instance[1])
            if not major: major = rd.choice(self.wrap_instance[2])
            if not semester: semester = rd.randint(1,9)
            courses = self.get_course_list_by_sem_credits(sem_credits)
            return Study_Plan(university, faculty, major, sem_credits, courses, semester)
            