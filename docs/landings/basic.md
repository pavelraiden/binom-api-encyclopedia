# Базовые операции с лендингами

## 🔑 Авторизация

**ВАЖНО:** Используйте только `api-key` header. Bearer token НЕ РАБОТАЕТ!

```bash
# ✅ ПРАВИЛЬНО
curl -H "api-key: YOUR_API_KEY" https://pierdun.com/public/api/v1/info/landing

# ❌ НЕ РАБОТАЕТ
curl -H "Authorization: Bearer YOUR_API_KEY" https://pierdun.com/public/api/v1/info/landing
```

## 📋 Получение списка лендингов

### GET /info/landing

**Обязательные параметры:**
- `datePreset` - период данных
- `timezone` - временная зона

```bash
curl -H "api-key: YOUR_API_KEY" \
     "https://pierdun.com/public/api/v1/info/landing?datePreset=last_7_days&timezone=UTC"
```

**Доступные значения datePreset:**
- `today`, `yesterday`
- `last_7_days`, `last_30_days`
- `this_month`, `last_month`

## 🆕 Создание лендинга

### POST /landing (integrated)

**Статус:** ⚠️ Нестабильный (часто возвращает 502)

```bash
curl -H "api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -X POST https://pierdun.com/public/api/v1/landing \
     -d '{
       "name": "Test Landing",
       "path": "/test-landing",
       "language": "en"
     }'
```

### POST /landing (not integrated)

```bash
curl -H "api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -X POST https://pierdun.com/public/api/v1/landing \
     -d '{
       "name": "External Landing",
       "url": "https://example.com/landing",
       "language": "en"
     }'
```

## 📊 Получение статистики лендинга

### GET /stats/landing

```bash
curl -H "api-key: YOUR_API_KEY" \
     "https://pierdun.com/public/api/v1/stats/landing?datePreset=today&timezone=UTC&limit=10"
```

## 🔍 Получение конкретного лендинга

### GET /landing/{id}

```bash
curl -H "api-key: YOUR_API_KEY" \
     https://pierdun.com/public/api/v1/landing/123
```

## ✏️ Обновление лендинга

### PUT /landing/{id}

```bash
curl -H "api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -X PUT https://pierdun.com/public/api/v1/landing/123 \
     -d '{
       "name": "Updated Landing Name",
       "language": "ru"
     }'
```

## 🗑️ Удаление лендинга

### DELETE /landing/{id}

```bash
curl -H "api-key: YOUR_API_KEY" \
     -X DELETE https://pierdun.com/public/api/v1/landing/123
```

## ⚠️ Типичные ошибки

### 502 Bad Gateway
**Причина:** Серверная ошибка при создании лендинга  
**Решение:** Повторить запрос через 5-10 секунд

### 400 Bad Request
**Причина:** Отсутствуют обязательные параметры  
**Решение:** Проверить наличие `datePreset` и `timezone`

### 401 Unauthorized
**Причина:** Неправильная авторизация  
**Решение:** Использовать `api-key` header вместо Bearer token

## 🔄 Retry логика

```python
import time
import requests

def create_landing_with_retry(data, max_retries=3):
    headers = {"api-key": "YOUR_API_KEY", "Content-Type": "application/json"}
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://pierdun.com/public/api/v1/landing",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 502:
                print(f"502 error, retrying in {2**attempt} seconds...")
                time.sleep(2**attempt)
                continue
            else:
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2**attempt)
    
    raise Exception("Max retries exceeded")
```

## 📚 Связанные разделы

- [Продвинутые операции](advanced.md)
- [Отчеты по лендингам](reporting.md)
- [Troubleshooting](../troubleshooting/common_errors.md)
