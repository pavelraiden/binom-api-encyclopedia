# 🚀 Smart Offer Replacer - Quick Start Guide

Get started with Smart Offer Replacer in 5 minutes!

## Prerequisites

- Python 3.11+
- Access to Binom API
- API keys for your trackers

## Step-by-Step Guide

### Step 1: Clone Repository (if not done)

```bash
git clone https://github.com/pavelraiden/binom-api-encyclopedia.git
cd binom-api-encyclopedia
```

### Step 2: Set Up Environment Variables

```bash
# Add to your ~/.bashrc or ~/.zshrc
export binomPublic="your_pierdun_api_key"
export Binom_Newareay="your_newareay_api_key"
export WARPHELSING_KEY="your_warphelsing_api_key"

# Reload shell
source ~/.bashrc
```

**Verify:**
```bash
echo $binomPublic
```

### Step 3: Create Your Configuration

```bash
cd configs/smart_offer_replacer
cp config.example.json my_first_replacement.json
```

**Edit the file:**
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
    "old_offer_pattern": "Memorra",
    "new_offer_pattern": "Cleanserra",
    "min_clicks": 5000,
    "date_preset": "last_30_days"
  },
  "options": {
    "dry_run": true,
    "delay_between_updates": 0.5,
    "log_level": "INFO"
  }
}
```

### Step 4: Run in DRY RUN Mode

```bash
cd ../../scripts/automation
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_first_replacement.json
```

**Expected output:**
```
================================================================================
УМНАЯ ЗАМЕНА ОФФЕРОВ ВО ВСЕХ ТРЕКЕРАХ
================================================================================
Старые офферы: Memorra
Новые офферы: Cleanserra
Режим: DRY RUN
================================================================================
```

### Step 5: Review Results

Check the output and `replacement_results.json`:

```bash
cat replacement_results.json | python -m json.tool
```

**Look for:**
- Number of campaigns found
- Number of offers to be replaced
- Any errors or warnings

### Step 6: Run in Production

If everything looks good:

1. Edit config: `"dry_run": false`
2. Run again:

```bash
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_first_replacement.json
```

3. Verify in Binom UI

### Step 7: Verify Changes

1. Open Binom panel
2. Check one of the updated campaigns
3. Verify:
   - Offers are replaced correctly
   - Weights are recalculated
   - All other settings preserved

## Common First-Time Issues

### Issue 1: API Key Not Found

**Error:**
```
Error: API ключ не найден в переменных окружения: binomPublic
```

**Solution:**
```bash
export binomPublic="your_api_key"
# Verify
echo $binomPublic
```

### Issue 2: No Offers Found

**Error:**
```
⚠️ Старые офферы не найдены с паттерном: Memorra
```

**Solution:**
- Check offer names in Binom UI
- Adjust `old_offer_pattern` in config
- Try partial match (e.g., "Memor" instead of "Memorra")

### Issue 3: Import Error

**Error:**
```
ModuleNotFoundError: No module named 'binom_api'
```

**Solution:**
```bash
# Make sure you're in scripts/automation directory
cd scripts/automation
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_first_replacement.json
```

## Next Steps

✅ **Read full documentation:** [smart-offer-replacer.md](./smart-offer-replacer.md)  
✅ **Learn about configuration:** [Configuration Guide](../../../configs/smart_offer_replacer/README.md)  
✅ **Troubleshooting:** [troubleshooting.md](./troubleshooting.md)  

## Tips for Success

1. **Always start with DRY RUN** - Never skip this step!
2. **Test on one tracker first** - Before enabling all trackers
3. **Start with high min_clicks** - To limit number of campaigns
4. **Check results file** - Before running in production
5. **Backup your data** - Just in case

## Example Workflow

```bash
# 1. Set up environment
export binomPublic="your_key"

# 2. Create config
cd configs/smart_offer_replacer
cp config.example.json test_run.json
nano test_run.json  # Edit settings

# 3. DRY RUN
cd ../../scripts/automation
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/test_run.json

# 4. Review
cat replacement_results.json | python -m json.tool

# 5. Production (if OK)
nano ../../configs/smart_offer_replacer/test_run.json  # Set dry_run: false
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/test_run.json

# 6. Verify in Binom UI
```

## Getting Help

- **Documentation:** [smart-offer-replacer.md](./smart-offer-replacer.md)
- **Troubleshooting:** [troubleshooting.md](./troubleshooting.md)
- **Configuration:** [Config Guide](../../../configs/smart_offer_replacer/README.md)
- **API Docs:** https://docs.binom.org/api-v2.php

---

**Ready to replace offers like a pro!** 🚀

