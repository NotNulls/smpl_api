from db import db

class StoreModel(db.Model):
    __tablename__= 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    #lazy refers to initiation of the item objects maching that store. later, it is referred to the self.items.all() which makes a list of all items in that store.
    items = db.relationship('ItemModel',lazy='dynamic')

    def __init__(self,name, price, store_id) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'items': [item.json for item in self.items.all()]}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        
    #it does the job to both inserting and updating    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete()
        db.session.commit()

        