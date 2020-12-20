import logging

class Node:

    def __init__(self, text, level=5, is_title=False):
        self.text = text
        self.is_title = is_title

        if is_title:
            self.level = 0
        else:
            self.level = level

        self.children = []
        self.parent = None

    def beget(self, *children):
        for child in children:
            self.children.append(child)
            logging.debug(f"{self} begets {child}")

        child.parent = self

    """Returns a list with self, parent of self, parent of parent of self and so on"""
    def get_ancestry(self):
        ancestry = []

        new_ancestor = self
        while new_ancestor:
            ancestry.append(new_ancestor)
            new_ancestor = new_ancestor.parent

        return ancestry

    def __str__(self):
        return self.text