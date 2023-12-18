import os
import pywebio
from pywebio.output import *
import pywebio.input as inp

from handlers.menu import TaskHandler


@pywebio.config(theme='dark')
async def main():
    clear()


    task = TaskHandler()
    logo_path = os.path.join('data/img', 'cover.jpg')
    put_image(open(logo_path, 'rb').read())

    action = await inp.select(
        'Выберите нужный вариант',
        [
            'Добавить задачу',
            'Список задач'
        ])


    if 'Добавить задачу' == action:
        await task.add_task_in_list()
    elif 'Список задач' == action:
        task.get_task_list()


if __name__ == '__main__':
    pywebio.start_server(main, host='0.0.0.0', port=4444)
