
class Branch():

    def __init__(self):
        self.title = "Branch Title"
        self.description = "Branch Description"
        self.image = "lock.png"
        self.button_text = "Go"
        self.next = 0

branch1 = Branch()
branch1.description = "Go to another storylet."
branch1.next = 2
branch2 = Branch()

class Storylet():

    def __init__(self):
        self.title = "Test Title"
        self.description = "This is a test description!"
        self.image = "lock.png"
        self.branches = [branch1, branch2]
        self.escapable = True