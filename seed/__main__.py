"""
Заполняет базу данных информацией из .xlsx таблицы
"""

import openpyxl
from sqlalchemy.orm import Session

from database import schemas, crud, models

from definitions import RESOURCE_DIR

FILEPATH = RESOURCE_DIR + "/xlsx/houses.xlsx"

def main():
    wb = openpyxl.load_workbook(FILEPATH);
    ws = wb.active

    id = 0
    #                                                 V Don't include the 0 row, since it contains headers for the data
    for row in ws.iter_rows(values_only=True, min_col=3, min_row=2, max_row=140):
        # ИД элемента в БД
        current_id = ++id;

        # Адрес дома
        address: str = row[0]

        # Оптимизированный адрес дома. Заметим, что в таблице
        # Excel в конце каждого адреса пишется 'Москва'. Однако, поскольку мы знаем, что данный сервис будет
        # использоваться для субъектов Москвы, мы можем избавиться от этой строки
        moscow_part         = address.find(", Москва")
        address_optimized   = address[:moscow_part]

        # Число квартир, как строка
        apartments = row[5]
        if (apartments == "Не указано" or apartments == None):
            continue
        
        # Число квартир, как целочисленное
        apartments_number = int(apartments)

        print("{0}: {1}".format(address, apartments_number))



def create_house(db: Session, address: str, apartments_number: int):
    """
    Добавить новый дом в базу данных.
    Это функция добавляет по ряду в две таблицы: Таблицу с адресами домов и
    в таблицу с числом квартир на дом. Связаны эти два ряда будут
    через FOREIGN KEY.
    """

    # Сперва создадим `house_address`
    house_address: schemas.HouseAddressCreate = schemas.HouseAddressCreate(address=address)
    crud.create_house_address(db, house_address)

    # Теперь мы можем узнать id house_address...
    house_id = crud.get_house_id_by_address(db, house_address.address)

    # ... И с помощью него создадим `house_apartments`
    house_apartments: schemas.HouseApartments = schemas.HouseApartments(house_id=house_id, apartments=apartments_number)
    crud.create_house_apartments(**house_apartments.dict())


if __name__ == "__main__":
    main()
