from typing import Callable


class MenuItem:
    func = None
    text = None

    def __init__(self, func: Callable, text: str) -> None:
        self.func = func
        self.text = text
    
    def run(self):
        self.func()
    
    def __str__(self):
        return self.text

class Menu:
    def __init__(self, menu_items_list: list[MenuItem]) -> None:
        self.menu_items_list = menu_items_list
    
    def __str__(self):

        return '\n'.join([
            f'{str(index + 1)}. {text}' 
            for index, text in enumerate(self.menu_items_list)
            ]) + f'\n0. Выход\n'
    
    def start(self):
        while True:
            print(self)

            try:
                ans = int(input('Выберите пункт меню: '))
                if ans == 0:
                    input(
                        f'Программа завершила работу.\n'
                        f'Нажмите любую клавишу для выхода...'
                        )
                    break
                elif 0 < ans <= len(self.menu_items_list):
                    self.menu_items_list[ans-1].run()
                    print()
                else:
                    print('Такой пункт меню отсутсвует. Повторите попытку.\n')
            except ValueError:
                print('Вы ввели не число попробуйте еще раз.\n')
            except Exception as ex:
                print(f'Что-то пошло не так. Попробуйте еще раз. {ex}\n')

