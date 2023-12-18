import json
import asyncio
import os
from functools import partial

from pywebio.output import *
import pywebio.input as inp
from pywebio.session import run_js


class TaskHandler:
    def __init__(self):
        self.__task_types = ['Работа', 'Здоровье', 'Спорт']

    @staticmethod
    def read_task_file():
        with open('tasks.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def add_task_to_file(data: dict):
        last_changes = TaskHandler.read_task_file()
        last_changes[data['name']] = data['type'], data['date']
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(last_changes, file, indent=4)

    @staticmethod
    def delete_task_in_file(task_name, update=True):
        last_changes = TaskHandler.read_task_file()
        try:
            del last_changes[task_name]

            with open('tasks.json', 'w', encoding='utf-8') as file:
                json.dump(last_changes, file, indent=4)
        except KeyError:
            print('Ключ отсутствует в списке задач')
        if update:
            run_js('location.reload()')

    @staticmethod
    def get_task_list():
        result = []
        tasks = TaskHandler.read_task_file()

        for name in tasks.items():
            result.append([
                name[1][0],
                name[0],
                name[1][1],
                put_button(f'Удалить {name[0]}', onclick=partial(TaskHandler.delete_task_in_file, name[0]))
            ])

        put_table(
            result,
            header=['Тип задачи', 'Название задачи', 'Дата для выполнения', 'Удалить?']
        )
        put_button('Назад', onclick=lambda: run_js('location.reload()'))

    # Валидация форм для отправки
    @staticmethod
    def add_task_validate(data):
        if not data:
            return 'name_task', 'Необходимо заполнить поле'

    async def add_task_in_list(self):
        task_type = await inp.select('Выберите тип задачи', self.__task_types, multiple=False)
        name_task = await inp.input('Введите название задачи', validate=TaskHandler.add_task_validate)
        date_task = await inp.input('Введите дату окончания задачи. Пример: 17.12.2023', validate=TaskHandler.add_task_validate)

        if all([task_type, name_task, date_task]):
            toast('Задача успешна добавлена')
            await asyncio.sleep(1)
            run_js('location.reload()')
            TaskHandler.add_task_to_file({
                'type': task_type.lower(),
                'name': name_task.lower(),
                'date': date_task
            })
