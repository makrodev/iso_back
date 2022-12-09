<h1>Документация iso_back.</h1>


<h2>О проекте:</h2>
- iso_back это backend (серверная) часть проекта исо.
- Она создана для:
	1) отображения данных из бд в админке
	2) отдачи данных из бд через апи


<h2>Технологии используемые в этом проекте:</h2>
- Python 3.10
- Django + Django RestFramework
- Mysql
- Docker, Docker-compose
- Python libraries (requirements.txt)
- Telegram API
- Cron


<h2>Запуск проекта:</h2>
- Убедитесь, что запущен Docker, включена база данных от docker контейнера mysql.
	- Если база данных не включена найдите mysql_container и pma_container в github makrodev.
	- Зайдите в каждый проект и запустите их командой ```docker-compose up```.
- Откройте проект iso_back в терминале и пропишите команду ```docker-compose up```.
	- Если вы в первый раз запускаете проект и база пуста, то:
		1) пропишите команду ```docker exec -it iso_back_container /bin/bash```, вы попадете в docker terminal
		2) затем напишите ```python manage.py createsuperuser``` создайте суперюзера
		3) затем напишите ```python manage.py shell``` вы в docker terminal попадете в shell проекта django
		4) напишите ```from main.views import *``` а затем ```dbSeed()```. Этим действием вы запустите парсер дефолтных данных


<h2>Структура программы:</h2>

<pre>
iso_back
├───api
│   ├───migrations
│   │   └───...
│   ├───init.py
│   ├───admin.py
│   ├───apps.py
│   ├───helpers.py
│   ├───models.py
│   ├───serializers.py
│   ├───tests.py
│   ├───urls.py
│   ├───urls_app.py
│   ├───utils.py
│   ├───views.py
├───main
│   ├───init.py
│   ├───asgi.py
│   ├───settings.py
│   ├───urls.py
│   ├───views.py
│   ├───wsgi.py
├───media
│   ├───csv
│   │   └───...
│   ├───excel
│   │   └───...
│   ├───uploads
│   │   └───...
├──────.gitignore
├──────commands.txt
├──────docker-compose.yml
├──────Dockerfile
├──────manage.py
└──────requirements.txt
</pre>

<h2>Техническая часть проекта:</h2>

- URLS. От этого бекенда есть 2 приложения:
	- Бот. Все роуты апи для бота написаны в папке проекта (api/urls.py)
	- Мобайл. Все роуты апи для мобайла написаны в папке проекта (api/urls_app.py)
- Settings:
	- settings расположен в (main/settings.py)
	- В settings.py важные константы
		- DEBUG (стоит True, так как это корпоративная программа)
		- ALLOWED_HOSTS (разрешенные хосты)
		- CSRF_TRUSTED_ORIGINS (Разрешенные CSRF домены и айпи адреса)
		- DATABASES (подключение к базе данных)
		- LANGUAGE_CODE
		- TIME_ZONE
		- MEDIA_ROOT
		- MEDIA_URL
		- AUTH_USER_MODEL (Модель кастомного Юзера)
		- TELEGRAM_DOMAIN
		- BOT_KEY
- Libraries:
    - Все библиотеки лежат в файле requirements.txt
- PARSE DEFAULT DATA:
	- ДЕФОЛТНЫЕ данные лежат в папке проекта (main/views.py)
