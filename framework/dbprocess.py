"""
The module that governs about transforming the raw json database for the courses.json
into usable, wrapped, objects.
"""

import json
from framework.instance import University, Faculty, Major, Course

class DBProcess:
    """
    Database Processor for courses.json, designed specifically to wrap the database
    into study card items.
    """
    def __init__(self, path='courses.json'):
        self.fetch_json(path)

    def fetch_json(self, path='courses.json'):
        """
        Refreshes the database, manually called when the json is updated.

        It takes a default path to `courses.json` that contains all the
        preset study card items. It also take other json files as long
        as the format follows.

        Parameters
        ----------
        path : `str`
            The path to the json database. Default is `courses.json`
        
        Returns
        -------
        `DBProcess`
            the self `DBProcess` object
        """
        auth_file = open(path)
        auth_str = auth_file.read()
        self.courses_path = path
        self.db = json.loads(auth_str)
        return self

    def wrap_as_object(self, prune_defaults=True):
        """
        Converts the raw dictionary-array database into item objects

        Parameters
        ----------
        prune_defaults : `bool`
            States whether you want to remove the default placeholders
            or not. The default value is `True`

        Return
        ------
        `tuple`
            A tuple of four lists for every type of objects. Sorted, from
            universities, faculties, majors, and then courses.
        """
        luni = []; lfac = []; lmaj = []; lcou = []

        for gra_key in self.db:
            tunis = self.db[gra_key]
            for uni_key in tunis:
                if prune_defaults and uni_key.startswith('defuni'): continue
                uni = University(uni_key, aliases=tunis[uni_key]['aliases'])
                luni.append(uni)

                tfacs = tunis[uni_key]['faculties']
                for fac_key in tfacs:
                    if prune_defaults and fac_key.startswith('deffaculty'): continue
                    fac = Faculty(fac_key, aliases=tfacs[fac_key]['aliases']).set_university(uni)
                    lfac.append(fac)

                    tmajs = tfacs[fac_key]['majors']
                    for maj_key in tmajs:
                        if prune_defaults and maj_key.startswith('defmajor'): continue
                        maj = Major(maj_key, aliases=tmajs[maj_key]['aliases']).set_faculty(fac)
                        lmaj.append(maj)

                        tcous = tmajs[maj_key]['courses']
                        for cou_arr in tcous:
                            if prune_defaults and cou_arr[0].startswith('defcourse'): continue
                            cou = Course(cou_arr[0],cou_arr[1]).set_major(maj)
                            lcou.append(cou)

        return luni, lfac, lmaj, lcou

# Below are the deprecated functions

    #'''
    def courses_from(self, grade, university, faculty, major, unique=True, prune_defaults=True):
        majorcourselist =  self.db[grade][university]['faculties'][faculty]['majors'][major]['courses']
        if unique:
            majorcourselist = list(set(majorcourselist))
        if prune_defaults:
            majorcourselist = list(filter(('course1').__ne__, majorcourselist))
    #'''

    #'''
    def all_courses(self, unique=True, prune_defaults=True):
        allist = [course\
            for grade_key in self.db\
                for uni_key in self.db[grade_key]\
                    for faculty_key in self.db[grade_key][uni_key]['faculties']\
                        for major_key in self.db[grade_key][uni_key]['faculties'][faculty_key]['majors']\
                            for course in self.db[grade_key][uni_key]['faculties'][faculty_key]['majors'][major_key]['courses']]
        if unique:
            allist = list(set(allist))
        if prune_defaults:
            allist = list(filter(('course1').__ne__, allist))
        return allist
    #'''

    #'''
    def all_majors(self, unique=True, prune_defaults=True):
        allist = [major\
            for grade_key in self.db\
                for uni_key in self.db[grade_key]\
                    for faculty_key in self.db[grade_key][uni_key]['faculties']\
                        for major in self.db[grade_key][uni_key]['faculties'][faculty_key]['majors']]
        if unique:
            allist = list(set(allist))
        if prune_defaults:
            allist = list(filter(('major1').__ne__, allist))
        return allist
    #'''

    #'''
    def all_universities(self, unique=True, prune_defaults=True):
        allist = ['{}'.format(self.db[grade_key][uni]['aliases'][0])\
            for grade_key in self.db\
                for uni in self.db[grade_key]]
        if unique:
            allist = list(set(allist))
        if prune_defaults:
            allist = list(filter(('major1').__ne__, allist))
        return allist
    #'''