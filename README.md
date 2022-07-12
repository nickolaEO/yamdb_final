![YaMDb deploy](https://github.com/nickolaeo/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# **YaMDb Project**

### _СI и CD проекта API YaMDb_

# Описание

Проект **YaMDb** собирает **отзывы (Review)** пользователей на **произведения (Titles)**. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список **категорий (Category)** может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).  

Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.  

В каждой категории есть **произведения**: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.  

Произведению может быть присвоен **жанр (Genre)** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.  

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы (Review)** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.  

# Технологии

- [Python 3.8.8](https://www.python.org/downloads/release/python-388/)
- [Django 2.2.16](https://www.djangoproject.com/download/)
- [Django Rest Framework 3.12.4](https://www.django-rest-framework.org/)
- [PostgreSQL 13.0](https://www.postgresql.org/download/)
- [gunicorn 20.0.4](https://pypi.org/project/gunicorn/)
- [nginx 1.21.3](https://nginx.org/ru/download.html)

# Контейнер
- [Docker 20.10.14](https://www.docker.com/)
- [Docker Compose 2.4.1](https://docs.docker.com/compose/)

# URL's
- http://84.252.137.228/api/v1
- http://84.252.137.228/admin
- http://84.252.137.228/redoc

# Установка

Клонируйте репозиторий и перейдите в него в командной строке:
```sh
git clone https://github.com/nickolaEO/yamdb_final.git && cd yamdb_final
```
Перейдите в директорию с файлом _docker-compose.yaml_ и запустите контейнеры:
```sh
cd infra && docker-compose up -d --build
```
После успешного запуска контейнеров выполните миграции в проекте:
```sh
docker-compose exec web python manage.py makemigrations reviews
```
```sh
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```sh
docker-compose exec web python manage.py createsuperuser
```
Соберите статику:
```sh
docker-compose exec web python manage.py collectstatic --no-input
```
Создайте дамп (резервную копию) базы данных:
```sh
docker-compose exec web python manage.py dumpdata > fixtures.json
```
Для остановки контейнеров и удаления всех зависимостей воспользуйтесь командой:
```sh
docker-compose down -v
```

# Документация

Для просмотра документации к API перейдите по адресу:
http://84.252.137.228/redoc/

# Примеры запросов

**GET**: http://84.252.137.228/api/v1/categories/  
Пример ответа:
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

**POST**: http://84.252.137.228/api/v1/categories/  
Тело запроса:
```json
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```json
{
  "name": "string",
  "slug": "string"
}
```

**GET**: http://84.252.137.228/api/v1/users/  
Пример ответа:
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

## License

MIT

**Free Software**
