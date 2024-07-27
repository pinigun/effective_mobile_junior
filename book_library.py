import json
import os.path
from dataclasses import dataclass


@dataclass
class Book:
    '''Класс книга.'''

    id: int # (уникальный идентификатор, генерируется автоматически)
    title: str # (название книги)
    status: bool = True  # (статус книги: “в наличии” 1 (true), “выдана” 0 (false))
    author: str = None # (автор книги)
    year: int = None # (год издания)

    def __str__(self):
        return (
            f'| {self.id:^5} ' 
            f'| {self.title:^20} '
            f'| {'в наличии' if self.status == 1 else 'выдана':^3} '
            f'| {self.author if self.author else 'Неизвестен':^20} '
            f'| {self.year if self.year else 'Неизвестен':^11} |'
            )

    @staticmethod
    def dict2book(dict_: dict):
        '''Функция для создания объекта класса Book, из словаря Python'''

        return Book(
            id = dict_['id'],
            title = dict_['title'],
            status = dict_['status'],
            author = dict_['author'],
            year = dict_['year']
        )


class BookLibrary:
    '''
    Интерфейс для работы с библиотекой книг.
    Необходим для корректного взаимодействия с библиотекой.

    '''

    path = None

    def __init__(self, path):
        self.path = path
        
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write('{\n}')


    ''' Доп. функции и декораторы '''


    def book_exist(func):
        '''Декоратор для проверки существования книги в библиотеке по id.'''

        def wrapper(*args, **kwargs):
            try:
                _ex = None
                return func(*args, **kwargs)
            except KeyError as ex:
                _ex = ex
                print('Книги с таким id не существует.')
            except Exception as ex:
                _ex = ex
                print('Неизвестная ошибка')
            finally:
                if _ex is None:
                    print('Успешно!')       
        return wrapper


    def get_new_id(self) -> int:
        '''Функция для инкрементирования ID.'''
        with open(self.path, "r") as json_r:
            current_book_list = json.load(json_r)

        # Увеличиваем последний id на 1
        if len(current_book_list) > 0:
            return int(list(current_book_list)[-1]) + 1
        else:
            return 1
    

    @staticmethod
    def print_table_header():
        '''Функция вывода шапки таблицы'''
        print(
                f'| {'ID':^5} | {'Название':^20} | {'Статус':^9} | {'Автор':^20} | {'Год издания':^11} |'
                )
        

    ''' Основные функции. '''


    def add_book(self, book: Book):
        '''Функция для добавления книги в библиотеку.'''
        with open(self.path, "r") as json_r:
            current_book_list = json.load(json_r)

        with open(self.path, "w") as json_w:
            id = int(book.id)
            new_book = book.__dict__
            del new_book['id']
            current_book_list[id] = new_book
            json.dump(current_book_list, json_w, indent= 2, ensure_ascii=False)


    @book_exist
    def del_book(self, id: str):
        '''Функция для удаления книги из библиотеки.'''

        with open(self.path, 'r') as f:
            data = json.load(f)
            del data[id]
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    def find_book(
            self,
            value: str | int,
            finding_key: str
    ):
        '''
        Функция поиска книги по ОДНОМУ из трех параметров.
        value (str | int): переменная для поиска в поле с выбранным параметром;
        finding_key (str): title/author/year

        '''     

        with open(self.path, 'r') as f:
            data = json.load(f)
            flag = False # флаг для определения нашлась ли хоть одна книга
            BookLibrary.print_table_header()

            for item in data:
                if data[item][finding_key] == value: # Можно усовершенствовать поиск
                    flag = True
                    print(Book.dict2book({'id': item, **data[item]}))
            print('Поиск завершен...')

            if not flag:
                print('Книги с таким параметром не найдено')


    def show_all_books(self):
        '''Функция для вывода всех книг на печать.'''

        with open(self.path, 'r') as f:
            books = json.load(f)

            if len(books) == 0:
                print('Библиотека пуста.')
            else:
                BookLibrary.print_table_header()
                for book_id in books:
                    print(Book.dict2book({'id': book_id, **books[book_id]}))


    @book_exist
    def edit_status(self, id: int):
        '''Функция для изменения статуса наличия книги.'''

        with open(self.path, 'r') as f:
            data = json.load(f)
            data[id] = not data[id]
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

