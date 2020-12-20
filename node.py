
class Node:

    def __init__(self, text, title=False):
        if title:
            self.data = {
                "title": text,
                "children": []
            }
        else:
            self.data = {"text": text}

    def beget(self, child):
        if "children" not in self.data:
            self.data["children"] = []

        self.data["children"].append(child)

    def __str__(self):
        return str(self.data)