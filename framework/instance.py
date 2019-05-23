"""
instance.py contains the basic classes of the items in a study plan card,
like university, faculty, major, and course. This was made to 'objectify' the
data fetched from the courses.json file
"""

class University:
    """Wrapper for University item"""
    def __init__(self, name=None, faculties=[], aliases=[]):
        self.name = name
        self.aliases = aliases
        self.faculties = faculties

    def add_faculty(self, faculty):
        """
        Associate a single faculty to current university, works both ways.
        
        It first checks if current university already have the given faculty
        associated. Otherwise, it adds to the `faculties` attributes. Then,
        it changes the `university` parent attribute on the faculty object
        to current university.

        Parameters
        ----------
        faculty : `Faculty`
            The faculty object that is going to be associated with

        Returns
        -------
        `University`
            The self university object
        """
        if faculty not in self.faculties: self.faculties.append(faculty)
        faculty.university = self
        return self

class Faculty:
    """Wrapper for faculty item"""
    def __init__(self, name=None, university=None, majors=[], aliases=[]):
        self.name = name
        self.aliases = aliases
        self.univerisity = university
        self.majors = majors

    def set_university(self, university):
        """
        Associate current faculty to a given university, works both ways.
        
        It first checks if the given university already have current faculty
        associated. Otherwise, it adds to the `faculties` attributes. Then,
        it changes the `university` parent attribute on current faculty object
        to the given university.

        Parameters
        ----------
        university : `University`
            The university object that is going to be associated with

        Returns
        -------
        `Faculty`
            The self faculty object
        """
        if self not in university.faculties: university.faculties.append(self)
        self.university = university
        return self

    def add_major(self, major):
        """
        Associate a single major to current faculty, works both ways.
        
        It first checks if current faculty already have the given major
        associated. Otherwise, it adds to the `majors` attributes. Then,
        it changes the `faculty` parent attribute on the major object
        to current faculty.

        Parameters
        ----------
        major : Major
            The major object that is going to be associated with

        Returns
        -------
        Faculty
            The self faculty object
        """
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
        """
        Associate current major to a given faculty, works both ways.
        
        It first checks if the given faculty already have current major
        associated. Otherwise, it adds to the `majors` attributes. Then,
        it changes the `faculty` parent attribute on current major object
        to the given faculty.

        Parameters
        ----------
        faculty : `Faculty`
            The faculyt object that is going to be associated with

        Returns
        -------
        `Major`
            The self major object
        """
        if self not in faculty.majors: faculty.majors.append(self)
        self.faculty = faculty
        return self

    def add_course(self, course):
        """
        Associate a single course to current major, works both ways.
        
        It first checks if current major already have the given course
        associated. Otherwise, it adds to the `courses` attributes. Then,
        it changes the `major` parent attribute on the course object
        to current major.

        Parameters
        ----------
        course : `Course`
            The course object that is going to be associated with

        Returns
        -------
        `Major`
            The self major object
        """
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
        """
        Associate current course to a given major, works both ways.
        
        It first checks if the given major already have current course
        associated. Otherwise, it adds to the `courses` attributes. Then,
        it changes the `major` parent attribute on current course object
        to the given major.

        Parameters
        ----------
        major : `Major`
            The major object that is going to be associated with

        Returns
        -------
        `Course`
            The self course object
        """
        if self not in major.courses: major.courses.append(self)
        self.major = major
        return self
