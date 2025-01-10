### Запуск без контейнеров
1. Настроить виртуальное окружение 
2. Клонировать проект
3. Установить нужные библиотеки
4. Настроить переменное окружение
5. Запустить скрипт models.py для создания БД и заливки тестовых данных
6. Запустить скрипт site_code.py
7. Проверить результат.  


### 1. Установите виртуальную среду и активируйте ее:
```
python3 -m venv venv
source venv/bin/activate
```
### 2. Клонируйте репозиторий:
```Bash
git clone git@github.com:Alonsole/Aiohttp_test_one.git
```
### 3. Установите библиотеки:
```
pip install requirements.txt
```
### 4.Настройка переменное окружение
Необходимо переименовать пример.env в .env и заполнить:
```
POSTGRES_DBNAME='db_site'
POSTGRES_PASSWORD='Пароль Подключения к PostgreSQL'
POSTGRES_USER='Имя Пользователя для Подключения к PostgreSQL'
POSTGRES_PORT='5431' или 5432 (без Docker)
```
### 5. Запустить скрипт models.py
```
python models.py
```
### 6. Запустить скрипт site_code.py
```
python site_code.py
```
### 7. Проверить результат.  
```
http://127.0.0.1:5000
```
### Результат:

Ссылки для моего проекта на ~~Flask~~ aiohttp  
1️⃣Главная страница✅  
2️⃣Все объявления✅  

или
```
Выполнить запрос GET {{baseUrl}} из REST client файл requests-examples.http
```
### Результат:
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 358
Date: Thu, 09 Jan 2025 20:42:20 GMT
Server: Python/3.12 aiohttp/3.11.11
Connection: close

<meta charset="UTF-8">
<h3 style="color: #3f7320;">Ссылки для моего проекта на <s>Flask</s> aiohttp</h3>
<p><a rel="nofollow noopener" href="http://127.0.0.1:5000">1️⃣Главная страница✅</a></p>
<p><a rel="nofollow noopener" href="http://127.0.0.1:5000/announcements">2️⃣Все объявления✅</a></p>
```
### Запуск проекта с контейнером для ДБ
1. Настроить виртуальное окружение 
2. Клонировать проект
3. Установить нужные библиотеки
4. Настроить переменное окружение
5. Собрать контейнер с ДБ
6. Запустить скрипт models.py для создания БД и заливки тестовых данных  
6.1. Проверка контейнера
7. Запустить скрипт site_code.py
8. Проверить результат.  

### 5. Описание процесса запуска контейнера 
```
docker-compose up -d
```
### 6.1. Проверка результата создания ДБ и заливки тестовых данных
```
docker exec -it "Контейнер ID" sh
```
```
psql -U postgres
``` 
``` 
\c db_site
```
```
SELECT * FROM announcement;
```
Пример результата: 
```
id |   title    |   description    |     author      |         created_at
----+------------+------------------+-----------------+----------------------------
  1 | Test Title | Test Description | Maksim Velichko | 2025-01-09 23:57:33.696061
(1 row)
```

### Описание Models
Скрипт содержит описание моделей для БД, асинхронное создание ДБ, Таблиц. Предусмотрена заливка тест данных
### Описание db_settings
- Загрузка переменных окружений
- Настройки подключения к базе данных
- Подключение к базе данных PostgreSQL
- Асинхронный движок базы для создания ДБ
- Асинхронный движок базы для создания Таблиц
- Управление соединениями с базой данных и выполнение запросов
### Описание db_code
- async def get_announcements() - функция получения всех объявлений из ДБ
- async def send_new_announcement(new_announcement) - функция создания нового объявления
- async def delete_announcement_id(id) - функция удаления объявления по id
- async def update_announcement_id(id, data) - функция обновления конкретного объявления

### Docker-Compose
- Уже настроен на postgres:17.0-alpine

### Тестирование предусмотрено через REST Client
```
requests-examples.http
```



