from flask import url_for
from app import db
from app.models import Storylet

class PageResult():
    def __init__(self, data, page=1, number=20):
        self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
        self.full_listing = [self.data[i:i+number] for i in range(0, len(self.data), number)]

    def __iter__(self):
        for i in self.full_listing[self.page-1]:
            yield i

    def __repr__(self):
        return url_for('admin.users', pagenum=self.page+1)

class Tag():
    def __init__(self, name):
        if name == None:
            self.name = "Unorganized"
        else:
            self.name = name
        self.q_list = db.session.query(Storylet).filter(Storylet.tag == name).all()

def defaultStorylet():
    return Storylet(
        title="Untitled",
        image="black.png",
        description=None,
        deck="Always",
        area="All",
        urgency="Normal",
        order=0,
        notes=None,
        escapable=True,
        tag=None
    )
        


