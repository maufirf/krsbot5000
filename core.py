from framework.dbprocess import DBProcess
from framework.card import Study_Plan
#import numpy as np
from numpy import random as rd
from enum import Enum

class Core_C(Enum):
    # Credit quantification
    GENERAL_CREDITS = [18, 20, 22, 24]
    
    # Slotting behavior
    GREED = ('greed', 0.1) # Forcibly use all the credits
    NORMAL = ('normal', 0.8) # Take possible courses while allowing unsued credits
    SPARSE = ('sparse', 0.1) # Take just the essentials

class Core:
    def __init__(self, json_path='courses.json'):
        self.dbproc = DBProcess(json_path)
        self.wrap_instance = self.dbproc.wrap_as_object()

    def get_course_list_by_sem_credits(self, sem_credits, slot_behave=Core_C.NORMAL):
        if sem_credits <= 0: raise Exception('Semester Credits must be greater than zero!')
        courses_set = self.wrap_instance[3].copy()
        picks = []
        if slot_behave==Core_C.NORMAL:
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
        if random_type==0:
            if sem_credits <= 0 : sem_credits = rd.choice(Core_C.GENERAL_CREDITS.value)
            if not university: university = rd.choice(self.wrap_instance[0])
            if not faculty: faculty = rd.choice(self.wrap_instance[1])
            if not major: major = rd.choice(self.wrap_instance[2])
            if not semester: semester = rd.randint(1,9)
            courses = self.get_course_list_by_sem_credits(sem_credits)
            return Study_Plan(university, faculty, major, sem_credits, courses, semester)
            