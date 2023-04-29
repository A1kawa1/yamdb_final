# yamdb_final
YaMDb сервия для сбора отзывов о фильмах, книгах или музыке. Так же настроены CI/CD.  

![example workflow](https://github.com/A1kawa1/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)  

### Стек технологий:
- Python
- Django
- Django Rest Framework
- PostreSQL
- Nginx
- Docker

### Как запустить проект:

```
git clone https://github.com/A1kawa1/yamdb_final.git
cd api_yamdb
```


```
python3 -m venv venv
source /venv/bin/activate (source /venv/Scripts/activate - для Windows)
python -m pip install --upgrade pip
```


```
pip install -r requirements.txt
```


```
cd infra
```

Собираем необходимые контейнеры  
```
docker-compose up -d --build
```

Выполняем миграции  
```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя  
```
docker-compose exec web python manage.py createsuperuser
```

Cобираем статику  
```
docker-compose exec web python manage.py collectstatic --no-input
```


### Шаблон наполнения .env расположенный по пути infra/.env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Документация API YaMDb:
Документация доступна по эндпойнту: http://localhost/redoc/


### Работа с API:
1. Получить код подтверждения на переданный email. Права доступа: Доступно без токена. Использовать имя 'me' в качестве username запрещено. Поля email и username должны быть уникальными.  
Запрос: POST `/auth/signup/` 
{
  "email": "user@example.com",
  "username": "u6bM@_0aOkR-+.HnT9r6iiR@wGavUeqUuvNcC6ki27_V8gUdlRty9MM7KcjubykdPNShTr1-cl_+8RPeXKRmsfGN9S3HGlz"
}  
Ответ:  
{
  "email": "string",
  "username": "string"
}  

2. Создать категорию. Права доступа: Администратор. Поле slug каждой категории должно быть уникальным.  
Запрос: POST `/categories/` 
{
  "name": "string",
  "slug": "_r2dCbTfj8mS5rx8QL1ZaomjqdR8i1gvVx_Z0cBWpGW50PJGK8"
}
Ответ:  
{
  "name": "string",
  "slug": "string"
}  

3. Получить отзыв по id для указанного произведения. Права доступа: Доступно без токена.  
Запрос: GET `/titles/{title_id}/reviews/{review_id}/` 
Ответ:  
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 10,
  "pub_date": "2023-04-26T18:40:37.443Z"
}