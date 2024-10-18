import sqlalchemy
import json
import os
from sqlalchemy.orm import sessionmaker
from models import create_table, Publisher, Book, Shop, Stock, Sale

os.environ['name_sql'] = input('Название SQL: ')
os.environ['password_sql'] = input('Пароль от SQL: ')
os.environ['name_database'] = input('Название БД: ')
DSN = f'postgresql://{os.environ['name_sql']}:{os.environ['password_sql']}@localhost:5432/{os.environ['name_database']}'
engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('data.json', 'r', encoding='UTF=8') as d:
    data = json.load(d)

for element in data:
    check_class = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }[element.get('model')]
    session.add(check_class(id=element.get('pk'), **element.get('fields')))
session.commit()

def find_info(name_publisher):
    result = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
              .join(Book.publisher)
              .join(Stock)
              .join(Shop)
              .join(Sale)
              .filter(Publisher.name == name_publisher).all())
    if result == []:
        print(f'Продаж по данному автору не найдено')
        return
    else:
        for name_book, name_shop, price, date_sale in result:
            print(f'{name_book} | {name_shop} | {price} | {date_sale}')
session.close()

if __name__ == '__main__':
    publisher = input('Введите название автора: ')
    find_info(publisher)