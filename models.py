import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)

    def __str__(self):
        return f'Номер автора {self.id}, название {self.name}'
    
class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, nullable=False)
    id_publisher = sq.Column(
        sq.Integer,
        sq.ForeignKey('publisher.id'),
        nullable=False
    )

    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'Номер книги {self.id}, название {self.title}'
    
class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)

    def __str__(self):
        return f'Номер магазина {self.id}, название {self.name}'
    
class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f"""
        Номер продажи {self.id},
        цена {self.price},
        дата продажи {self.date_sale},
        номер склада {self.id_stock},
        количество {self.count}
        """
    
def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)