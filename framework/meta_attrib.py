"""
The module that governs metadata attribute container
"""

class Tag:
    """
    The metadata object that connects relevancy between courses
    """
    def __init__(self, name=None, courses=[], collection_parent=None):
        self.name = name
        self.courses = courses
        if not collection_parent: self.assoc_coll_parent(collection_parent)

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

    def assoc_coll_parent(self, collection_parent):
        """
        Adds a `Tag` object to the collection and associates the `Tag`
        to the current collection object.

        Parameters
        ----------
        collection_parent : `Tags`
            The parent `Tags` that you want to associate with

        Returns
        -------
        `Tag`
            The self `Tag` object
        """
        collection_parent.add_tag(self)
        return self

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

class Tags:
    """
    The metadata object that collects the `Tag` object for an
    easier and centralized `Tag` management.
    """
    def __init__(self):
        self.tags = {}

    def add_tag(self, tag):
        """
        Adds a `Tag` object to the collection and associates the `Tag`
        to the current collection object.

        Parameters
        ----------
        tag : `Tag`
            The `Tag` that you want to associate with

        Returns
        -------
        `Tags`
            The self `Tags` object
        """
        if type(tag)==Tag:
            if not self.tags.get(tag.name): self.tags[tag.name] = tag
            tag.collection_parent = self
        else:
            raise TypeError('A tag argument must be a Tag object!')
        return self