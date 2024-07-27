from book_library import Book, BookLibrary
from menu import Menu, MenuItem

PATH = '/home/pinigun/Documents/git-repos/effective_mobile_junior/books_library.json'

class BookLibraryMenu(Menu):
    def find_book(self):
        finding_key = input(
            f'Выберите параметр по которому будет произведени поиск:\n'
            f'\t1. Название\n'
            f'\t2. Автор\n'
            f'\t3. Год издания\n'
            f'\t0. Выйти\n'
            f'Введите номер: '
            )

        # выясняем по какому ключу делаем поиск
        if finding_key == '0':
            return
        if finding_key == '1':
            finding_key = 'title'
        elif finding_key == '2':
            finding_key = 'author'
        elif finding_key == '3':
            finding_key = 'year'
        else:
            print('Введен неверный номер. Повторите попытку.')
            return
        
        value = input('Введите значение параметра: ')
        # проверяем типы данных для переменной поиска
        if finding_key in ('title', 'author'):
            if not isinstance(value, str):
                return
        elif finding_key == 'year':
            try:
                value = int(value)
            except ValueError:
                print('Введено не число.')
        else:
            print('Введен некорректные данные.')
            return
        
        BookLibrary(path=PATH).find_book(value=value, finding_key=finding_key)

    def add_book(self):
        try:
            book = Book(
                id=BookLibrary(path=PATH).get_new_id(), 
                title=input('Введите название книги: '),
                author=input('Введти имя автора: '),
                year=int(input('Введите год издания книги: '))
                )
            BookLibrary(path=PATH).add_book(book)
        except ValueError as ex:
            print('Ошибка введен неверно год.')
            return
        
        


    def del_book(self):
        id = input('Введите id книги, которую необходимо удалить: ')
        BookLibrary(path=PATH).del_book(id)

    
    def edit_status(self):
        id = input('Введите id книги, у которой необходимо изменить статус: ')
        BookLibrary(path=PATH).edit_status(id)

    def show_all_books(self):
        BookLibrary(path=PATH).show_all_books()


    def __init__(self):
        self.menu_items_list = [
            MenuItem(self.find_book, 'Поиск книги по Названию/Автору/Году издания.'),
            MenuItem(self.add_book, 'Добавить книгу.'),
            MenuItem(self.del_book, 'Удалить книгу.'),
            MenuItem(self.edit_status, 'Изменить статус книги.'),
            MenuItem(self.show_all_books, 'Посмотреть все книги')
        ]


if __name__ == '__main__':
    menu = BookLibraryMenu()
    menu.start()