# 🔄 Smart Offer Replacer

**Production-ready tool for intelligent offer replacement in Binom campaigns**

## Overview

Smart Offer Replacer is an automated tool that replaces offers in Binom campaigns while preserving all campaign settings and automatically recalculating traffic weights.

### Key Features

✅ **Smart Mapping** - Automatically matches offers by numbers (#1→#1, #2→#2, #3→#3)  
✅ **Automatic Weight Recalculation** - Distributes traffic evenly across new offers  
✅ **Multiple Tracker Support** - Process multiple Binom trackers in one run  
✅ **DRY RUN Mode** - Preview changes before applying them  
✅ **Comprehensive Logging** - Detailed logs of all operations  
✅ **Safety First** - All campaign settings preserved (cost, auto-cost, rules, etc.)  

## Quick Start

### 1. Prepare Configuration

```bash
cd configs/smart_offer_replacer
cp config.example.json my_config.json
nano my_config.json
```

### 2. Set Environment Variables

```bash
export binomPublic="your_api_key"
export Binom_Newareay="your_api_key"
export WARPHELSING_KEY="your_api_key"
```

### 3. Run in DRY RUN Mode

```bash
cd scripts/automation
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_config.json
```

### 4. Review Results

Check the output and `replacement_results.json` file.

### 5. Run in Production

Edit config: `"dry_run": false`, then run again.

## How It Works

### 1. Offer Discovery

The script searches for offers matching patterns in their names:

```
Old Pattern: "Memorra"
→ Finds: "Memorra Cleaner #1", "Memorra Cleaner #2", "Memorra Cleaner #3"

New Pattern: "Cleanserra"  
→ Finds: "Cleanserra Cleaner #1", "Cleanserra Cleaner #2", "Cleanserra Cleaner #3"
```

### 2. Smart Mapping

Offers are matched by their numbers:

| Old Offer | Number | New Offer | Number |
|-----------|--------|-----------|--------|
| Memorra Cleaner #1 | #1 | Cleanserra Cleaner #1 | #1 |
| Memorra Cleaner #2 | #2 | Cleanserra Cleaner #2 | #2 |
| Memorra Cleaner #3 | #3 | Cleanserra Cleaner #3 | #3 |

**Mapping:**
- ID 50 (#1) → ID 55 (#1) ✅
- ID 51 (#2) → ID 54 (#2) ✅
- ID 52 (#3) → ID 53 (#3) ✅

### 3. Campaign Processing

For each campaign with >5000 clicks (configurable):

1. **Get campaign data** via API
2. **Find paths** containing old offers
3. **Replace offer IDs** with new ones
4. **Recalculate weights** to equal distribution
5. **Update campaign** via API

### 4. Weight Recalculation

Weights are automatically distributed evenly:

| Before | After | Offers |
|--------|-------|--------|
| 54/13/46 | 33/33/34 | 3 |
| 50/25/25 | 33/33/34 | 3 |
| 50/50 | 50/50 | 2 |
| 25/25/25/25 | 25/25/25/25 | 4 |

**Rule:** Equal distribution, remainder goes to last offer.

## Configuration

See [Configuration Guide](../../../configs/smart_offer_replacer/README.md) for detailed documentation.

### Minimal Configuration

```json
{
  "trackers": {
    "pierdun": {
      "api_key_env": "binomPublic",
      "base_url": "https://pierdun.com/public/api/v1",
      "enabled": true
    }
  },
  "replacement": {
    "old_offer_pattern": "OldOffer",
    "new_offer_pattern": "NewOffer",
    "min_clicks": 5000,
    "date_preset": "last_30_days"
  },
  "options": {
    "dry_run": true
  }
}
```

## API Endpoints Used

The script uses the following Binom API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/info/offer` | GET | Get list of offers |
| `/stats/campaign` | GET | Get campaign statistics |
| `/campaign/{id}` | GET | Get campaign details |
| `/campaign/{id}` | PUT | Update campaign |

## Safety Features

### DRY RUN Mode

When `dry_run: true`:
- ✅ Shows what would be changed
- ✅ No actual API updates
- ✅ Saves preview to results file
- ❌ Does not modify campaigns

### Preserved Settings

The script preserves ALL campaign settings:

✅ Cost Model (CPA, CPC, CPM)  
✅ Amount and Currency  
✅ Auto-cost settings  
✅ Hide Referrer Type  
✅ Distribution Type  
✅ Rules and conditions  
✅ Landing pages  
✅ All other paths without target offers  

### What Changes

❌ **ONLY** offer IDs in paths containing old offers  
❌ **ONLY** weights in affected paths  

## Output

### Console Output

```
================================================================================
УМНАЯ ЗАМЕНА ОФФЕРОВ ВО ВСЕХ ТРЕКЕРАХ
================================================================================
Старые офферы: Memorra
Новые офферы: Cleanserra
Режим: DRY RUN
================================================================================
ОБРАБОТКА ТРЕКЕРА: PierDun
================================================================================
🔍 Поиск офферов...
   ✅ Маппинг #1: 50 → 55
   ✅ Маппинг #2: 51 → 54
   ✅ Маппинг #3: 52 → 53
📊 Получение кампаний...
   Найдено кампаний с >5000 кликов: 74
🔄 Обработка кампаний...
[1/74] Кампания ID 82: JOJ1 / PROPSSP / FR - Interstitial / CA
      Заменен оффер 50 → 55 в path 'Main Path'
      Заменен оффер 51 → 54 в path 'Main Path'
      Заменен оффер 52 → 53 в path 'Main Path'
      Веса пересчитаны: 50/25/25 → 33/33/34
  🔍 DRY RUN: Будет заменено 3 офферов
...
================================================================================
ИТОГОВАЯ СТАТИСТИКА ПО ВСЕМ ТРЕКЕРАМ
================================================================================
📊 PierDun:
   Обработано кампаний: 37
   Заменено офферов: 144
   Ошибок: 0
🎯 ВСЕГО:
   Кампаний обработано: 37
   Офферов заменено: 144
   Ошибок: 0
```

### Results File

```json
{
  "config": {
    "old_offer_pattern": "Memorra",
    "new_offer_pattern": "Cleanserra",
    "options": {
      "min_clicks": 5000,
      "date_preset": "last_30_days",
      "dry_run": true
    }
  },
  "trackers": [
    {
      "tracker": "PierDun",
      "campaigns_processed": 37,
      "offers_replaced": 144,
      "errors": [],
      "results": [
        {
          "id": 82,
          "name": "JOJ1 / PROPSSP / FR - Interstitial / CA",
          "replaced": 3
        }
      ]
    }
  ],
  "summary": {
    "total_campaigns": 37,
    "total_offers": 144,
    "total_errors": 0
  }
}
```

## Error Handling

### Common Errors

#### 1. API Key Not Found
```
Error: API ключ не найден
```
**Solution:** Set environment variable with API key

#### 2. No Offers Found
```
⚠️ Старые офферы не найдены
```
**Solution:** Check `old_offer_pattern` in config

#### 3. Mapping Mismatch
```
❌ Количество старых и новых офферов не совпадает
```
**Solution:** Ensure equal number of old and new offers with same numbers

#### 4. API Error
```
API Error 400: Bad Request
```
**Solution:** Check API endpoint documentation and payload format

## Performance

### Benchmarks

| Metric | Value |
|--------|-------|
| Average API response time | 0.3-0.5s |
| Campaigns processed per minute | ~100-120 |
| Recommended delay | 0.5s |
| Safe delay for rate limiting | 1.0s |

### Optimization Tips

- Use `delay_between_updates: 0.2` for faster processing (if API allows)
- Process one tracker at a time for better control
- Use `min_clicks` filter to reduce number of campaigns

## Examples

### Example 1: Replace Memorra with Cleanserra

```json
{
  "replacement": {
    "old_offer_pattern": "Memorra",
    "new_offer_pattern": "Cleanserra",
    "min_clicks": 5000,
    "date_preset": "last_30_days"
  }
}
```

### Example 2: High-traffic campaigns only

```json
{
  "replacement": {
    "old_offer_pattern": "OldOffer",
    "new_offer_pattern": "NewOffer",
    "min_clicks": 10000,
    "date_preset": "last_7_days"
  }
}
```

### Example 3: Single tracker

```json
{
  "trackers": {
    "pierdun": { "enabled": true },
    "newareay": { "enabled": false },
    "warphelsing": { "enabled": false }
  }
}
```

## Troubleshooting

See [Troubleshooting Guide](./troubleshooting.md) for common issues and solutions.

## Advanced Usage

### Custom Mapping

If you need custom mapping logic, modify `create_smart_mapping()` function in the script.

### Custom Weight Distribution

If you need custom weight distribution, modify `recalculate_weights()` function.

### Logging

Set `log_level` to `DEBUG` for detailed logging:

```json
{
  "options": {
    "log_level": "DEBUG"
  }
}
```

## Best Practices

✅ **Always test in DRY RUN first**  
✅ **Start with one tracker**  
✅ **Backup your data**  
✅ **Monitor results file**  
✅ **Check campaign in Binom UI after update**  
✅ **Use appropriate delay to avoid rate limiting**  
✅ **Keep API keys secure in environment variables**  

## Related Documentation

- [Quick Start Guide](./quick-start.md)
- [Troubleshooting Guide](./troubleshooting.md)
- [Configuration Guide](../../../configs/smart_offer_replacer/README.md)
- [Core API Documentation](../core/binom-api.md)

## Support

For issues and questions:
1. Check [Troubleshooting Guide](./troubleshooting.md)
2. Review [Configuration Guide](../../../configs/smart_offer_replacer/README.md)
3. Check API documentation at https://docs.binom.org/api-v2.php

## Version History

### v1.0.0 (2025-10-15)
- ✅ Initial release
- ✅ Smart mapping by offer numbers
- ✅ Automatic weight recalculation
- ✅ Multiple tracker support
- ✅ DRY RUN mode
- ✅ Comprehensive logging

