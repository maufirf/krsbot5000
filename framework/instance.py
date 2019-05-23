class University:
    def __init__(self, name=None, faculties=[], aliases=[]):
        self.name = name
        self.aliases = aliases
        self.faculties = faculties

    def add_faculty(self, faculty):
        if faculty not in self.faculties: self.faculties.append(faculty)
        faculty.university = self
        return self

class Faculty:
    def __init__(self, name=None, university=None, majors=[], aliases=[]):
        self.name = name
        self.aliases = aliases
        self.univerisity = university
        self.majors = majors

    def set_university(self, university):
        if self not in university.faculties: university.faculties.append(self)
        self.university = university
        return self

    def add_major(self, major):
        if major not in self.majors: self.majors.append(major)
        major.faculty = self
        return self

class Major:
    def __init__(self, name=None, faculty=None, courses=[], aliases=[]):
        self.name = name
        self.aliases = aliases
        self.faculty = faculty
        self.courses = courses
    
    def set_faculty(self, faculty):
        if self not in faculty.majors: faculty.majors.append(self)
        self.faculty = faculty
        return self

    def add_course(self, course):
        if course not in self.courses: self.courses.append(course)
        course.major = self
        return self

class Course:
    def __init__(self, name=None, credit=1, major=None, aliases=[]):
        self.name = name
        self.major = major
        self.credit = credit
        self.aliases = aliases

    def set_major(self, major):
        if self not in major.courses: major.courses.append(self)
        self.major = major
        return self
