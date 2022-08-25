from kanban.database import db


class CardsLists(db.Model):
    __tablename__ = 'cards_lists'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
    list_id = db.Column('list_id', db.Integer, db.ForeignKey('list.id'))
