# Проект «Продуктовый помощник» (API Foodgram)

Проект размещен по адресу:
[на сервере Yandex.Cloud](http://158.160.21.112/)
```
Логин администратора: admin85@yandex.ru

Пароль администратора: Team8558banda
```

## Описание проекта foodgram-project-react\*\*
![foodgram_workflow](https://github.com/ArtemBalandin81/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


Проект разворачивается в Docker контейнерах: 
- api backend-приложение foodgram;
- frontend-контейнер (используется для сборки файлов и после запуска останавливается).
- база данных Postgres;
- cервер Nginx.


**Используемые технологии**

- Python 3.7
- Django 3.2
- djoser
- Rest API
- PostgreSQL
- Nginx
- gunicorn
- Docker
- DockerHub
- JS
- GitHub Actions (CI/CD)
- Yandex.Cloud

## Установка проекта\
1. Необходима учетная запись на https://hub.docker.com (LOGIN).
2. Необходима учетная запись на Yandex.Cloud (username).

3. Форкните и клонируйте репозиторий проекта foodgram-project-react.

```
git clone https://github.com/ArtemBalandin81/foodgram-project-react
```
4. Подготовьте и разместите образ frontend на https://hub.docker.com (LOGIN - ваш логин на hub.docker.co):

```
cd frontend
docker image build -t LOGIN/foodgram_frontend:latest .
```

5. Подготовьте и разместите образ backend на https://hub.docker.com (LOGIN - ваш логин на hub.docker.co):

```
cd backend/Foodgram
docker image build -t LOGIN/foodgram_backend:latest .
```

6. Подготовьте Yandex.Cloud к работе:

```
- Запустить ВМ, в качестве образа выберите Ubuntu 20.04 lts.
- Установите на ВМ docker-compose (v. 2.0) 
https://docs.docker.com/engine/install/ubuntu/
- Создайте в домашней директории ВМ каталог docs (для файлов схемы api)
```

7. Измените файл docker-compose.yml под настройки ваших логинов:

```
1. cd infra
2. frontend: образ frontend из п.4
3. backend: образ backend из п.5

```

8. Заполните с помощью .env и собственных настроек secret actions прокета на https://github.com:

```
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
PASSPHRASE
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY
TELEGRAM_TO
TELEGRAM_TOKEN
USER

```

9. Перенесите установочные файлы на ВМ Yandex.Cloud:

```
1. cd infra
2. scp docker-compose.yml username@pub.lic.i.p:/home/username/ 
3. scp nginx.conf username@pub.lic.i.p:/home/username/
4. cd docs
5. scp openapi-schema.yml username@pub.lic.i.p:/home/username/docs
6. scp redoc.html username@pub.lic.i.p:/home/username/docs
```

10. Запустите CI и CD проекта, выполнив push на https://github.com. При пуше изменений в основную ветку проект автоматически тестируется на соотвествие требованиям PEP8. После успешного прохождения тестов, на git-платформе собирается образ backend-контейнера Docker и автоматически размешается в облачном хранилище DockerHub. Далее образы фронтэнд и бэкэнда автоматически разворачивается на виртуальной машине в Яндекс облаке вместе с контейнерами веб-сервера Nginx и базой данных Postgres.


11. В случае успешного прохождения всех этапов workflow actions:
```
1. Проверьте работоспособность контейнеров: sudo docker container ls -a
2. Проведите миграции: sudo docker compose exec backend python manage.py migrate
```

12. Создайте суперпользователя

```
sudo docker compose exec backend python manage.py createsuperuser
```

13. Осуществите сбор статики

```
sudo docker compose exec backend python manage.py collectstatic
```

14. Зазрузите данные в models для тестирования

```
sudo docker compose exec backend python manage.py loaddatatobase
```

15. Проект размещен по адресу:
[на сервере Yandex.Cloud](http://158.160.21.112/)
```
Логин администратора: admin85@yandex.ru

Пароль администратора: Team8558banda
```
Ссылки на документацию к проекту: [redoc/](http://158.160.21.112/api/docs/)


## Автор проекта\*\*
Артем Баландин https://github.com/ArtemBalandin81