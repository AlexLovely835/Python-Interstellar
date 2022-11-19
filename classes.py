storylets = []
branches = []
results = []

class Results():
    
    def __init__(self, id, parent_id = 0, title = 'Result Title', description = 'Result Description', type = 'General', next = 0):
        self.id = id
        self.parent_id = parent_id
        self.title = title
        self.description = description
        self.type = type
        self.next = next
        results.append(self)

class Branch():

    def __init__(self, id, parent_id = 0, title = 'Branch Title', image = 'rapier.png', description = 'Branch Description', button_text = 'Go'):
        self.id = id
        self.parent_id = parent_id
        self.title = title
        self.image = image
        self.description = description
        self.button_text = button_text
        self.results = {}
        branches.append(self)

    def populate(self):
        for result in results:
            if result.parent_id == self.id:
                self.results[result.type] = result

class Storylet():

    def __init__(self, id, title = 'Test', image = 'rapier_gradient.png', description = 'Test description', requirements = None, available = 'Always', escapable = True):
        self.id = id
        self.title = title
        self.image = image
        self.description = description
        self.requirements = requirements
        self.branches = []
        self.available = available
        self.escapable = escapable
        storylets.append(self)

    def populate(self):
        for branch in branches:
            if branch.parent_id == self.id:
                self.branches.append(branch)





















# Temp Testing Objects
storylet1 = Storylet(id=1, title="First Storylet", description="I am the first Storylet ever!")
branch1 = Branch(id=1, parent_id=1, title="Return Home", description="Go back to the main screen.")
branch2 = Branch(id=2, parent_id=1, title="Visit Storylet 2", description="See another Storylet!")
storylet1.populate()
result1 = Results(id=1, parent_id=1, title="Returning you home!", description="Thanks for visiting!")
branch1.populate()
result2 = Results(id=2, parent_id=2, title="Visiting Storylet 2!", description="Thanks for visiting!", next=2)
branch2.populate()
storylet2 = Storylet(id=2, title="Second Storylet", description="I am the second storylet!", available="Never", escapable=False)
branch3 = Branch(id=3, parent_id=2, title="Return home", description="Return home")
storylet2.populate()
result3 = Results(id=3, parent_id=3, title="Returning you home!", description="Thanks for visiting!")
branch3.populate()
storylet3 = Storylet(id=3)
storylet4 = Storylet(id=4)
storylet5 = Storylet(id=5, available="Sometimes", title="Deck1")
storylet6 = Storylet(id=6, available="Sometimes", title="Deck2")
storylet7 = Storylet(id=7, available="Sometimes", title="Deck3")
storylet8 = Storylet(id=8, available="Sometimes", title="Deck4")