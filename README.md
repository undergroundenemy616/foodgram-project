# foodgram-project

## Что умеет проект

Ооооо, если вы любите вкусно покушать, этот проект для вас!
Здесь вы можете:
- Добавить рецепт;
- Удалить рецепт;
- Изменить рецепт;
- Добавить рецепт в список своих любимых рецептов;
- Подписаться на автора что бы следить за тем какие рецепты он пишет;
- Добавить рецепт в список покупок, чтобы в любой удобный момент скачать его;
- Просматривать рецеты, выбирая с помощью тегов когда вы хотите вкусно покушать;


## Как это сделано

Стек:
- Python3
- Django;
- PostgreSQL;

## Как запустить проект

## Вариант для тех кто ненавидит докер:

1. Скопировать код проекта к себе на компьютер.

2. Установить виртуальное окружение командой:
    
    ```python -m venv venv```

3. Активировать виртуальное окружение командой:
    
    ```source venv/bin/activate```

4. Установить необходимые зависимости командой:
    
    ```pip install -r requirements.txt```

5. Сделать миграции для формирования базы данных:
    
    ```python manage.py migrate```

6. При необходимости создать суперпользователя:
    
    ```python manage.py createsuperuser```
    (и следовать подсказкам в консоли)

7. Запустить проект командой:
    
    ```python manage.py runserver```

8. Перейти в браузере по адресу http://127.0.0.1:8000/


