# Smart Offer Replacer - Configuration Guide

## Configuration Files

### `config.example.json`
Example configuration file with all available options. Copy this file to create your own configuration.

### Configuration Structure

#### Trackers Section
```json
"trackers": {
  "tracker_name": {
    "api_key_env": "ENVIRONMENT_VARIABLE_NAME",
    "base_url": "https://tracker.com/public/api/v1",
    "enabled": true
  }
}
```

**Parameters:**
- `api_key_env` - Name of environment variable containing API key
- `base_url` - Base URL for Binom API
- `enabled` - Whether to process this tracker (true/false)

#### Replacement Section
```json
"replacement": {
  "old_offer_pattern": "Memorra",
  "new_offer_pattern": "Cleanserra",
  "min_clicks": 5000,
  "date_preset": "last_30_days"
}
```

**Parameters:**
- `old_offer_pattern` - Pattern to search in old offer names
- `new_offer_pattern` - Pattern to search in new offer names
- `min_clicks` - Minimum clicks threshold for campaigns
- `date_preset` - Time period for click counting

**Available date presets:**
- `today`, `yesterday`
- `last_7_days`, `last_14_days`, `last_30_days`
- `this_week`, `last_week`
- `this_month`, `last_month`
- `all_time`

#### Options Section
```json
"options": {
  "dry_run": true,
  "delay_between_updates": 0.5,
  "log_level": "INFO",
  "save_results": true,
  "results_file": "replacement_results.json"
}
```

**Parameters:**
- `dry_run` - If true, only shows what would be changed (no actual updates)
- `delay_between_updates` - Delay in seconds between API requests
- `log_level` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `save_results` - Save results to JSON file
- `results_file` - Path to results file

## Usage

1. Copy example config:
```bash
cp config.example.json my_config.json
```

2. Edit your config:
```bash
nano my_config.json
```

3. Set environment variables:
```bash
export binomPublic="your_api_key_here"
export Binom_Newareay="your_api_key_here"
export WARPHELSING_KEY="your_api_key_here"
```

4. Run script:
```bash
cd ../../scripts/automation
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_config.json
```

## Safety Tips

✅ **Always start with `dry_run: true`** to preview changes  
✅ **Test on one tracker first** before enabling all  
✅ **Backup your data** before running in production  
✅ **Check results file** after dry run  
✅ **Monitor API rate limits** with appropriate delay  

## Examples

### Example 1: Replace offers in all trackers (DRY RUN)
```json
{
  "trackers": { ... all enabled ... },
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

### Example 2: Production run for single tracker
```json
{
  "trackers": {
    "pierdun": { "enabled": true },
    "newareay": { "enabled": false },
    "warphelsing": { "enabled": false }
  },
  "options": {
    "dry_run": false,
    "delay_between_updates": 1.0
  }
}
```

### Example 3: High-traffic campaigns only
```json
{
  "replacement": {
    "min_clicks": 10000,
    "date_preset": "last_7_days"
  }
}
```

