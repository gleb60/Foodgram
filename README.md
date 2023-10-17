# Foodgram
 С помощью этого приложения можно делиться рецептами по всему земному шару!)<br/>
### Технологии
#### Python
#### Django
#### PostgreSQL
#### API DRF
#### Docker
#### GitHub

Сайт

```
https://foodgramapp.ddnsking.com/
```

### Запуск проекта:
1. Клонируйте проект:
```commandline
git@github.com:gleb60/foodgram-project-react.git
```
2. Скопируйте файлы с локального компьютера на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```
3. Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```
4. Соберите контейнер, выполните миграции, создайте суперюзера и соберите статику:
```
sudo docker-compose up -d --build
sudo docker-compose migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
5. Скопируйте данные с перечнем ингредиентов:
```
sudo docker-compose exec backend python3 manage.py load_ingredients
```