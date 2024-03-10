# Habit Hive

Habit Hive - трекер привычек. Пользователь может создавать привычки, которые хочет привить.
Пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

Действие, время и место - 3 обязательных параметра для создания привычки. 
Чтобы привить привычку, пользователь может связать новое действие с уже выработанной привычкой.
Ещё один способ - установить вознаграждение за выполнение действия.
Необходимо помнить, что новое действие необходимо практиковать регулярно - не реже, чем раз в неделю. 
Также важно, чтобы действие можно было выполнить не более, чем за 2 минуты.

Пользователь может менять видимость привычек: оставлять их приватными или делиться с другими пользователями сервиса.
Указав в профиле свой Телеграм аккаунт, пользователь будет получать напоминание, о необходимости практиковать новую привычку.

### Технологии

- **Django**
- **Python**
- **PostgreSQL**
- **Django REST Framework**
- **Django REST Framework SimpleJWT**
- **Django CORS Headers**
- **drf-yasg**
- **Celery**
- **Redis**
- **django-celery-beat**

###  Установка и использование

+ Клонируйте репозиторий: git clone git@github.com:nataliadudina/habit_hive.git
+ Перейдите в каталог проекта: cd habit_hive
+ Создайте (python3 -m venv env) и активируйте  (.\env\Scripts\activate) виртуальное окружение
+ Активируйте виртуальное окружение: source env/bin/activate (Linux/Mac) или .\env\Scripts\activate (Windows)
+ Установите зависимости: poetry install (требуется предварительная установка poetry)
+ Настройте переменные окружения: создайте файл `.env` в корне проекта и добавьте необходимые переменные окружения
+ Примените миграции: python manage.py migrate
+ Создайте суперпользователя: python manage.py csu
+ Запустите сервер: python manage.py runserver
+ Запустите брокер Redis: sudo service redis-server start
+ Запустите Celery worker: celery -A your_project_name worker --loglevel=info
+ Запустите Celery beat для планирования периодических задач: celery -A your_project_name beat -l info

    Пример содержимого файла `.env` в файле `.env.sample`
---

### Структура проекта

    Проект "Habit Hive" состоит из двух приложений:
    1) habit: модели Habit
    2) users: модель User
---
