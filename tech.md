# Техническое задание: E-Shop для стильных оправ очков

## 1. Общее описание проекта

**Название:** EyeFrame Shop  
**Назначение:** Интернет-магазин для продажи стильных оправ для очков  
**Язык интерфейса:** Английский

---

## 2. Технологический стек

|Компонент|Технология|
|---|---|
|Backend|Django (Python)|
|База данных|PostgreSQL|
|CSS Framework|Tailwind CSS|
|Интерактивность|HTMX + Alpine.js|
|Контейнеризация|Docker + Docker Compose|
|Web-сервер|Nginx|
|Платежная система|NOWPayments API|

---

## 3. Функциональные требования

### 3.1 Каталог продукции

- Отображение списка товаров с пагинацией
- Фильтрация по категориям (мужские, женские, унисекс, детские и т.д.)
- Фильтрация по дополнительным параметрам (материал, форма, цвет, бренд, цена)
- Сортировка (по цене, новизне, популярности)
- Динамическая загрузка результатов без перезагрузки страницы (HTMX)

### 3.2 Детальная страница товара

- Галерея изображений товара
- Полное описание товара
- Характеристики (материал, размеры, цвет)
- Цена
- Кнопка "Add to Cart"
- Связанные товары (рекомендации)

### 3.3 Корзина товаров

- Модальное окно корзины (Alpine.js)
- Добавление/удаление товаров
- Изменение количества
- Подсчет итоговой суммы
- Сохранение корзины в сессии
- Переход к оформлению заказа

### 3.4 Оформление заказа

- Форма с данными покупателя (имя, email, телефон, адрес доставки)
- Выбор способа доставки
- Просмотр состава заказа перед оплатой
- Валидация данных на клиенте и сервере

### 3.5 Оплата через NOWPayments

- Интеграция с NOWPayments API
- Поддержка криптовалютных платежей
- Создание платежной сессии
- Обработка callback/webhook от NOWPayments
- Обновление статуса заказа после оплаты
- Страница успешной оплаты и страница ошибки

### 3.6 SPA-подобное поведение

- Все переходы и обновления контента через HTMX
- Минимальные полные перезагрузки страницы
- Плавные переходы между разделами
- Обновление URL через hx-push-url

---

## 4. Нефункциональные требования

### 4.1 Безопасность

- CSRF-защита для всех форм
- Защита от SQL-инъекций (ORM Django)
- XSS-защита (экранирование вывода)
- Валидация всех входных данных
- Безопасное хранение секретов (environment variables)
- HTTPS в production
- Rate limiting для API endpoints
- Secure cookies configuration

### 4.2 Качество кода

- Соблюдение принципов ООП
- DRY (Don't Repeat Yourself)
- Использование паттернов проектирования где уместно
- Data Transfer Objects (DTO) / маппинг между слоями
- Service Layer для бизнес-логики
- Repository Pattern для работы с данными
- Чистая архитектура с разделением ответственности
- Type hints в Python коде
- Без комментариев в коде

### 4.3 Производительность

- Оптимизация запросов к БД (select_related, prefetch_related)
- Кэширование где необходимо
- Оптимизация изображений
- Lazy loading для изображений

---

## 5. Структура базы данных

### Основные сущности:

- **Category** — категории товаров
- **Product** — товары (оправы)
- **ProductImage** — изображения товаров
- **Cart / CartItem** — корзина (сессионная)
- **Order** — заказы
- **OrderItem** — позиции заказа
- **Payment** — информация о платежах

---

## 6. Структура проекта

```
eyeframe-shop/
├── docker-compose.yml
├── Dockerfile
├── nginx/
│   └── nginx.conf
├── manage.py
├── config/               # Django settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── catalog/          # Products, Categories
│   ├── cart/             # Shopping cart
│   ├── orders/           # Order management
│   └── payments/         # NOWPayments integration
├── core/                 # Base classes, mixins, utils
├── services/             # Business logic layer
├── templates/
│   ├── base.html
│   ├── components/       # Reusable HTMX components
│   ├── catalog/
│   ├── cart/
│   └── orders/
├── static/
│   ├── css/
│   └── js/
├── media/                # User uploaded files
├── requirements.txt
├── .env.example
└── README.md
```

---

## 7. API Endpoints (внутренние для HTMX)

|Метод|URL|Описание|
|---|---|---|
|GET|/catalog/|Список товаров|
|GET|/catalog/filter/|Фильтрация (HTMX partial)|
|GET|/catalog/{slug}/|Детальная страница товара|
|POST|/cart/add/|Добавить в корзину|
|POST|/cart/update/|Обновить количество|
|POST|/cart/remove/|Удалить из корзины|
|GET|/cart/modal/|Содержимое корзины (partial)|
|GET|/checkout/|Страница оформления заказа|
|POST|/checkout/create/|Создание заказа|
|POST|/payments/create/|Создание платежа NOWPayments|
|POST|/payments/webhook/|Webhook от NOWPayments|
|GET|/payments/success/|Успешная оплата|
|GET|/payments/failed/|Ошибка оплаты|

---

## 8. Docker конфигурация

- **web** — Django application (Gunicorn)
- **db** — PostgreSQL
- **nginx** — Reverse proxy, static files
- Volume для PostgreSQL data
- Volume для static/media files
- Network для связи контейнеров

---

## 9. Deliverables

1. Полностью рабочее приложение
2. Docker Compose для локального запуска
3. Файл .env.example с описанием переменных
4. README.md с инструкцией по запуску

---

## 10. Критерии приёмки

- Все функциональные требования реализованы
- SPA-подобная навигация работает без полных перезагрузок
- Корзина работает в модальном окне
- Интеграция с NOWPayments функционирует
- Код соответствует best practices
- Приложение запускается через docker-compose up

---

Приступить к реализации?