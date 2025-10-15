# 🔧 Smart Offer Replacer - Troubleshooting Guide

Common issues and their solutions.

## Table of Contents

1. [Environment & Setup Issues](#environment--setup-issues)
2. [API & Authentication Issues](#api--authentication-issues)
3. [Offer Discovery Issues](#offer-discovery-issues)
4. [Campaign Update Issues](#campaign-update-issues)
5. [Performance Issues](#performance-issues)
6. [Data Issues](#data-issues)

---

## Environment & Setup Issues

### Issue: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'binom_api'
```

**Причина:** Неправильная рабочая директория или путь к модулям.

**Решение:**
```bash
# Убедитесь что вы в правильной директории
cd /path/to/binom-api-encyclopedia/scripts/automation

# Проверьте структуру
ls -la ../core/
# Должны быть: binom_api.py, transform_campaign_data.py, __init__.py

# Запустите скрипт
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/config.json
```

### Issue: API Key Not Found

**Error:**
```
Error: API ключ не найден в переменных окружения: binomPublic
```

**Причина:** Переменная окружения не установлена.

**Решение:**
```bash
# Установите переменную
export binomPublic="your_api_key_here"

# Проверьте
echo $binomPublic

# Для постоянного использования добавьте в ~/.bashrc
echo 'export binomPublic="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'replacement_results.json'
```

**Причина:** Нет прав на запись в директорию.

**Решение:**
```bash
# Проверьте права
ls -la

# Дайте права на запись
chmod +w .

# Или укажите другую директорию в конфиге
{
  "options": {
    "results_file": "/tmp/replacement_results.json"
  }
}
```

---

## API & Authentication Issues

### Issue: 401 Unauthorized

**Error:**
```
API Error 401: Unauthorized
```

**Причина:** Неверный API ключ или неправильный формат авторизации.

**Решение:**

1. Проверьте API ключ:
```bash
echo $binomPublic
```

2. Проверьте формат в Binom UI:
   - Откройте https://pierdun.com/panel/login
   - Settings → API Keys
   - Скопируйте правильный ключ

3. Убедитесь что используется правильный заголовок:
```python
# В binom_api.py должно быть:
headers = {
    "api-key": api_key,  # НЕ "Authorization: Bearer"
    "Content-Type": "application/json"
}
```

### Issue: 403 Forbidden

**Error:**
```
API Error 403: Forbidden
```

**Причина:** API ключ не имеет прав на операцию.

**Решение:**

1. Проверьте права API ключа в Binom UI
2. Создайте новый API ключ с полными правами
3. Обновите переменную окружения

### Issue: 429 Too Many Requests

**Error:**
```
API Error 429: Too Many Requests
```

**Причина:** Превышен лимит запросов к API.

**Решение:**

Увеличьте задержку между запросами:
```json
{
  "options": {
    "delay_between_updates": 1.0  // Было 0.5
  }
}
```

### Issue: Connection Timeout

**Error:**
```
requests.exceptions.ConnectionError: Connection timeout
```

**Причина:** Проблемы с сетью или сервер недоступен.

**Решение:**

1. Проверьте интернет соединение
2. Проверьте доступность сервера:
```bash
curl -I https://pierdun.com/public/api/v1/info/offer
```
3. Попробуйте позже

---

## Offer Discovery Issues

### Issue: No Old Offers Found

**Error:**
```
⚠️ Старые офферы не найдены с паттерном: Memorra
```

**Причина:** Паттерн не совпадает с названиями офферов.

**Решение:**

1. Проверьте названия офферов в Binom UI
2. Попробуйте частичное совпадение:
```json
{
  "replacement": {
    "old_offer_pattern": "Memor"  // Вместо "Memorra"
  }
}
```

3. Проверьте регистр (script case-sensitive)

### Issue: No New Offers Found

**Error:**
```
⚠️ Новые офферы не найдены с паттерном: Cleanserra
```

**Причина:** Новые офферы не созданы или паттерн неверный.

**Решение:**

1. Создайте новые офферы в Binom UI
2. Убедитесь что названия содержат паттерн
3. Проверьте что офферы активны

### Issue: Offer Count Mismatch

**Error:**
```
❌ Количество старых (3) и новых (2) офферов не совпадает
```

**Причина:** Разное количество старых и новых офферов.

**Решение:**

1. Создайте недостающие офферы
2. Или отключите офферы которые не нужны
3. Убедитесь что все офферы имеют номера (#1, #2, #3)

### Issue: Number Extraction Failed

**Error:**
```
⚠️ Не удалось извлечь номер из названия: Memorra Cleaner
```

**Причина:** Название оффера не содержит номер (#1, #2, #3).

**Решение:**

Переименуйте офферы в Binom UI:
```
Memorra Cleaner → Memorra Cleaner #1
Memorra Cleaner 2 → Memorra Cleaner #2
Memorra Cleaner Three → Memorra Cleaner #3
```

---

## Campaign Update Issues

### Issue: 400 Bad Request

**Error:**
```
API Error 400: Bad Request
```

**Причина:** Неверный формат данных для обновления кампании.

**Решение:**

1. Проверьте что используется `transform_campaign_for_update()`:
```python
campaign_data = transform_campaign_for_update(campaign)
```

2. Проверьте логи DEBUG:
```json
{
  "options": {
    "log_level": "DEBUG"
  }
}
```

3. Сравните payload с документацией API

### Issue: Campaign Not Updated

**Error:**
```
✅ Успешно обновлено (но изменения не видны в UI)
```

**Причина:** Кэширование в Binom UI.

**Решение:**

1. Обновите страницу в браузере (Ctrl+F5)
2. Очистите кэш браузера
3. Проверьте через API:
```bash
curl -H "api-key: $binomPublic" \
  "https://pierdun.com/public/api/v1/campaign/{campaign_id}"
```

### Issue: Weights Not Recalculated

**Error:**
```
Веса остались прежними: 50/25/25
```

**Причина:** Функция пересчета весов не вызвана.

**Решение:**

Проверьте что в скрипте есть:
```python
new_weights = recalculate_weights(len(offers))
for i, offer in enumerate(offers):
    offer['weight'] = new_weights[i]
```

---

## Performance Issues

### Issue: Script Too Slow

**Problem:** Обработка 100 кампаний занимает >30 минут.

**Причина:** Большая задержка между запросами.

**Решение:**

1. Уменьшите задержку (если API позволяет):
```json
{
  "options": {
    "delay_between_updates": 0.2  // Было 0.5
  }
}
```

2. Отключите DEBUG логи:
```json
{
  "options": {
    "log_level": "INFO"  // Вместо DEBUG
  }
}
```

3. Обрабатывайте один трекер за раз

### Issue: High Memory Usage

**Problem:** Скрипт использует много памяти.

**Причина:** Загрузка всех кампаний в память.

**Решение:**

Обрабатывайте кампании порциями (требует модификации скрипта):
```python
# Вместо загрузки всех кампаний сразу
for campaign_id in campaign_ids:
    campaign = api.get_campaign(campaign_id)
    process_campaign(campaign)
```

---

## Data Issues

### Issue: Duplicate Offers in Path

**Problem:** В path несколько одинаковых офферов.

**Причина:** Ошибка в данных кампании.

**Решение:**

1. Проверьте кампанию в Binom UI
2. Удалите дубликаты вручную
3. Запустите скрипт снова

### Issue: Missing Paths

**Problem:** Скрипт не находит paths в кампании.

**Причина:** Структура кампании отличается от ожидаемой.

**Решение:**

1. Проверьте структуру через API:
```bash
curl -H "api-key: $binomPublic" \
  "https://pierdun.com/public/api/v1/campaign/{id}" | python -m json.tool
```

2. Адаптируйте скрипт под вашу структуру

### Issue: Incorrect Weight Sum

**Problem:** Сумма весов != 100.

**Причина:** Ошибка в функции пересчета.

**Решение:**

Проверьте функцию `recalculate_weights()`:
```python
def recalculate_weights(count):
    if count == 0:
        return []
    base_weight = 100 // count
    remainder = 100 % count
    weights = [base_weight] * count
    weights[-1] += remainder  # Остаток последнему
    return weights

# Тест
assert sum(recalculate_weights(3)) == 100  # [33, 33, 34]
assert sum(recalculate_weights(4)) == 100  # [25, 25, 25, 25]
```

---

## Debug Mode

Для детальной диагностики включите DEBUG режим:

```json
{
  "options": {
    "log_level": "DEBUG"
  }
}
```

**Вывод будет содержать:**
- Все API запросы и ответы
- Детальную информацию о каждой операции
- Полные данные кампаний
- Трассировку ошибок

---

## Getting More Help

If none of these solutions work:

1. **Check logs** - Enable DEBUG mode
2. **Check API documentation** - https://docs.binom.org/api-v2.php
3. **Review GitHub issues** - https://github.com/pavelraiden/binom-api-encyclopedia/issues
4. **Create new issue** - With logs and config (remove API keys!)

---

## Prevention Tips

✅ **Always use DRY RUN first**  
✅ **Test on one campaign manually**  
✅ **Backup your data**  
✅ **Monitor API rate limits**  
✅ **Keep API keys secure**  
✅ **Review results file before production**  

---

**Most issues can be prevented by careful testing in DRY RUN mode!** 🛡️

