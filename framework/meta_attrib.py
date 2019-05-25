"""
The module that governs metadata attribute container
"""

class Tag:
    def __init__(self, name=None, courses=[]):
        self.name = name
        self.courses = courses

    def add_course(self, course):
        """
        Assign current tag to a course, works both way.

        Parameters
        ----------
        course: `Course`
            The course to be associated with

        Returns
        -------
        `Tag`
            The self `Tag` object
        """
        if course not in self.courses: self.courses.append(course)
        if self not in course.tags: course.tags.append(course)

    def find_common_with_other(self, other_tags=None):
        """
        Returns the courses that share the same tags between current tag
        and the given tag.

        This function will return the current tag's courses if no tags
        are passed.

        Parameters
        ----------
        other_tags: `list`
            A list that contains other `Tag` to find the courses that shares
            the same tags

        Returns
        -------
        `list`
            The list of the courses that share the same tags
        """
        if other_tags and len(other_tags)>0:
            return Tag.find_common(other_tags + [self])
        else: return self.courses

    @staticmethod
    def find_common(*tags):
        if len(tags)==1 and type(tags[0])==list: tags = tags[0]
        if len(tags)>0:
            if len(tags)==1: return tags[0].courses
            else:
                common = set(tags[0])
                for tag in tags[1:]: common = common & set(tag)
                return list(common)
        else: raise Exception('At least one tag is needed.')