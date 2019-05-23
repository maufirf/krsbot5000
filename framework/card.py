"""
This module contains the container class for Student Study Plan kind of Cards
"""

from framework.instance import University, Faculty, Major, Course

class Study_Plan:
    """
    Container class for Study Plan card
    """
    def __init__(self, university=None, faculty=None, major=None, sem_credits=None, courses=None, semester=1):
        self.university = university
        self.faculty = faculty
        self.major = major
        self.sem_credits = sem_credits
        self.courses = courses
        self.semester = semester

    def as_list(self, as_str=False):
        """
        Returns the `list` representation of current object

        Parameters
        ----------
        as_str : `bool`
            Whether you want it as objects or as raw string.

        Returns
        -------
        `list`
            a list of wrapper objects, ordered from university, faculty
            major, semester, semester credits, and courses
        """
        if as_str:
            return [
                self.university.name,
                self.faculty.name,
                self.major.name,
                self.semester,
                self.sem_credits,
                [
                    (i.name, i.credit) for i in self.courses
                ] if self.courses else None
            ]
        else:
            return [
                self.university,
                self.faculty,
                self.major,
                self.semester,
                self.sem_credits,
                self.courses
            ]
    
    def __str__(self):
        out = f'{self.university.aliases[0].upper()}\n{self.faculty.aliases[0]} - {self.major.aliases[0]}\nSemester {self.semester}\n\n'
        i = 1; tot_cred=0
        if self.courses:
            for course in self.courses:
                out += '{: 2}. ({}) {}\n'.format(i,course.credit,course.name)
                i+=1; tot_cred+=course.credit
        out += f'\nAvailable credits = {self.sem_credits} credits\nUsed credits = {tot_cred} credits'
        return out