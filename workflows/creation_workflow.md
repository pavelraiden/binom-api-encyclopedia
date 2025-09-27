# Workflow: Full Campaign Creation (with Fallbacks)

**Goal:** Создать новую рекламную кампанию с нуля, включая все необходимые сущности.

**AI Pattern:** `Create with Verification & Fallback`

> Этот workflow пытается создать сущности через API, но включает шаги для ручного вмешательства и верификации из-за нестабильности CREATE-эндпоинтов.

## Steps

### Step 1: MANUAL_CREATION_AND_VERIFICATION
API для создания Traffic Source нестабилен. Создайте его вручную в UI Binom, затем получите его ID через GET /info/traffic_source.

### Step 2: MANUAL_CREATION_AND_VERIFICATION
API для создания Landing Page нестабилен. Создайте его вручную в UI Binom, затем получите его ID через GET /info/landing.

### Step 3: MANUAL_CREATION_AND_VERIFICATION
API для создания Offer нестабилен. Создайте его вручную в UI Binom, затем получите его ID через GET /info/offer.

### Step 4: MANUAL_CREATION_AND_VERIFICATION
API для создания кампаний нестабилен. Рекомендуется создавать кампанию вручную в UI, используя ID созданных ранее сущностей.

