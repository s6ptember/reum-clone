# Отчет по аудиту безопасности

В этом документе описаны уязвимости безопасности и проблемы конфигурации, найденные в проекте `raum-clone`.

## 1. Небезопасная прямая ссылка на объект (IDOR) в деталях заказа
**Критичность:** Высокая
**Расположение:** `apps/orders/views.py:80`

**Описание:**
Представление `order_detail` получает заказ исключительно на основе `order_id`, переданного в URL. Нет проверки того, что текущий пользователь является владельцем заказа. Это позволяет любому пользователю просматривать детали заказа любого другого пользователя, просто угадав ID.

**Исправление:**
Убедитесь, что заказ принадлежит текущему пользователю (если используется аутентификация) или сверьте с значением, сохраненным в сессии (если оформление заказа гостевое).

```python
# apps/orders/views.py

def order_detail(request, order_id):
    # Если используются аутентифицированные пользователи:
    # order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Если используется гостевое оформление с сессией:
    session_order_id = request.session.get('order_id')
    if str(session_order_id) != str(order_id):
         # Возвращаем 403 Forbidden или 404 Not Found
         from django.core.exceptions import PermissionDenied
         raise PermissionDenied
         
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/detail.html', {'order': order})
```

## 2. Манипуляция ценами в корзине / Устаревшие цены
**Критичность:** Средняя
**Расположение:** `apps/cart/cart.py:60`

**Описание:**
Корзина хранит цены товаров в сессии пользователя (`self.cart[product_id]['price']`). При расчете итогов или итерации используется эта сохраненная цена вместо текущей цены из базы данных. Это позволяет:
1.  Пользователям платить по старой цене, если администратор обновил её.
2.  Злоумышленникам потенциально модифицировать сессию (если хранилище сессий небезопасно), чтобы заплатить меньшую цену.

**Исправление:**
Всегда используйте цену из объекта товара в базе данных при итерации или расчете итогов.

```python
# apps/cart/cart.py

def __iter__(self):
    # ...
    for product in products:
        cart[str(product.id)]['product'] = product
        # ОБНОВЛЕНИЕ ЦЕНЫ ИЗ БД
        cart[str(product.id)]['price'] = product.price 
    
    for item in cart.values():
        item['price'] = Decimal(item['price'])
        # ...
```

## 3. Отсутствуют заголовки безопасности для продакшена
**Критичность:** Средняя
**Расположение:** `config/settings.py`

**Описание:**
В проекте отсутствуют стандартные заголовки безопасности, необходимые для продакшен-среды для защиты от XSS, кликджекинга и SSL stripping.

**Исправление:**
Добавьте следующие настройки в `config/settings.py`, убедившись, что они включены только в продакшене (например, когда `DEBUG = False`).

```python
# config/settings.py

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
```
