#*shopapi*
# Инструкция по развёртыванию и запуску проекта (Django + MySQL)

## 1. Развёртывание базы данных (MySQL)

Перед запуском проекта необходимо создать базу данных и применить все необходимые таблицы, процедуры и функции.

1. Откройте консоль MySQL или любой клиент (например, DBeaver, MySQL Workbench, phpMyAdmin).
2. Создайте новую базу данных (если она ещё не создана):
   ```sql
   CREATE DATABASE shop_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Выберите созданную базу данных:
   ```sql
   USE shop_django;
   ```
4. Импортируйте SQL-скрипт с таблицами и структурами (выполните содержимое вашего SQL-файла с лабораторной/практической работы). Убедитесь, что в базу данных успешно добавлены:
   * Таблицы: `categories`, `products`, `customers`, `orders` и `order_items`.
   * Хранимые процедуры: `sp_product_add`, `sp_product_update_price`, `sp_order_create`, `sp_order_add_item`, `sp_customer_orders`, `sp_category_stats`.
   * Хранимые функции: `fn_customer_avg_check`, `fn_customer_discount`.

## 2. Установка зависимостей

Для работы проекта требуются Python 3.10+ и несколько библиотек для связи Django с MySQL и работы со средой.

1. Откройте терминал в корневой папке проекта.

2. Установите необходимые пакеты. В зависимости от используемого драйвера выполните:
   ```bash
   pip install django python-dotenv mysqlclient
   ```
   *Примечание: Если `mysqlclient` не устанавливается на Windows, используйте альтернативный коннектор `pip install pymysql` (и не забудьте инициализировать его в `__init__.py` вашего проекта).*

3. Создайте файл **`.env`** в корне проекта рядом с `manage.py` и укажите в нём настройки подключения к вашей локальной СУБД:
   ```env
   DB_NAME=shop_django
   DB_USER=root
   DB_PASSWORD=ваш_пароль_от_mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```


## 3. Запуск проекта

1. Убедитесь, что вы находитесь в корневой директории проекта (где лежит файл `manage.py`).

2. Запустите локальный сервер разработки:
   ```bash
   python manage.py runserver
   ```
4. Откройте браузер и перейдите по адресу: [http://127.0.0](http://127.0.0)

### Основные доступные страницы для проверки заданий:
* `/products/` — Список товаров (вызов `sp_products_list`).
* `/products/add/` — Форма добавления товара (вызов `sp_product_add` с получением `OUT p_new_id`).
* `/products/<id>/price/` — Изменение цены товара (вызов `sp_product_update_price`).
* `/orders/create/` — Страница создания заказа и добавления позиций (`sp_order_create` и интерактивная плашка добавления).
* `/customers/<id>/orders/` — Заказы клиента (вызов `sp_customer_orders` и расчет `fn_customer_avg_check`).
* `/stats/categories/` — Статистика по категориям (`sp_category_stats` с подсветкой топ-категории).
* `/discount/` — Форма расчёта скидки (вызов функции `fn_customer_discount`).
