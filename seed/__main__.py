"""
Заполняет базу данных информацией из .xlsx таблицы
"""

import openpyxl
from sqlalchemy.orm import Session

from database import schemas, crud, models
from database.session import SessionLocal

from definitions import RESOURCE_DIR

FILEPATH = RESOURCE_DIR + "/xlsx/houses.xlsx"


def main():
    wb = openpyxl.load_workbook(FILEPATH);
    ws = wb.active

    db = SessionLocal()

    for row in ws.iter_rows(values_only=True, min_col=3, min_row=2):
        # Адрес дома
        address: str = row[0]

        # Оптимизированный адрес дома. Заметим, что в таблице
        # Excel в конце каждого адреса пишется 'Москва'. Однако, поскольку мы знаем, что данный сервис будет
        # использоваться для субъектов Москвы, мы можем избавиться от этой строки
        moscow_part         = address.find(", Москва")
        address_optimized   = address[:moscow_part]

        # Проверим, нет ли уже в бд дома с таким адресом. Если да, то повторное его введение приведет к ошибке
        db_house_address = crud.get_house_address_by_address_str(db, address_optimized)
        already_present = (db_house_address is not None)

        # Число квартир, как строка
        apartments = row[5]

        if (not isinstance(apartments, int)):
            continue

        # Число квартир, как целочисленное
        apartments_number = int(apartments)

        # Добавление к сообщению, если в бд уже был дом с таким адресом
        ignored_message = " (Ignored)" if already_present else ""
        print("{0}: {1}{2}".format(address, apartments_number, ignored_message))

        if not already_present:
            create_house(db, address_optimized, apartments_number)


def create_house(db: Session, address: str, apartments_number: int):
    """
    Добавить новый дом в базу данных.
    Это функция добавляет по ряду в две таблицы: Таблицу с адресами домов и
    в таблицу с числом квартир на дом. Связаны эти два ряда будут
    через FOREIGN KEY.
    """

    # Сперва создадим `house_address`
    house_address: schemas.HouseAddressCreate = schemas.HouseAddressCreate(address=address)
    house_address_created = crud.create_house_address(db, house_address)

    # Теперь мы можем узнать id house_address...
    house_id = house_address_created.__dict__['id']

    # ... И с помощью него мы сможем создать house_apartments, которые ссылаются на house_address
    house_apartments: schemas.HouseApartmentsCreate = schemas.HouseApartmentsCreate(house_id=house_id, apartments=apartments_number)
    crud.create_house_apartments(db, house_apartments)


if __name__ == "__main__":
    main()
