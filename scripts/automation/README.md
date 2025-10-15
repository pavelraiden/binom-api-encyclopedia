# 🤖 Automation Scripts

Production-ready automation scripts for Binom API.

## Available Scripts

### 🔄 Smart Offer Replacer

**File:** `smart_offer_replacer.py`

Intelligent tool for replacing offers in Binom campaigns with automatic weight recalculation and smart mapping by offer numbers.

**Features:**
- ✅ Smart mapping (#1→#1, #2→#2, #3→#3)
- ✅ Automatic weight recalculation
- ✅ Multiple tracker support
- ✅ DRY RUN mode
- ✅ Comprehensive logging

**Quick Start:**
```bash
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/config.example.json
```

**Documentation:**
- [Full Documentation](../../docs/scripts/automation/smart-offer-replacer.md)
- [Quick Start Guide](../../docs/scripts/automation/quick-start.md)
- [Troubleshooting](../../docs/scripts/automation/troubleshooting.md)

---

## Usage

### Prerequisites

1. Python 3.11+
2. Binom API access
3. API keys in environment variables

### Basic Workflow

```bash
# 1. Set up environment
export binomPublic="your_api_key"

# 2. Create configuration
cd ../../configs/smart_offer_replacer
cp config.example.json my_config.json
nano my_config.json

# 3. Run in DRY RUN mode
cd ../../scripts/automation
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_config.json

# 4. Review results
cat replacement_results.json | python -m json.tool

# 5. Run in production (if OK)
# Edit config: "dry_run": false
python smart_offer_replacer.py --config ../../configs/smart_offer_replacer/my_config.json
```

---

## Core Dependencies

All automation scripts use shared core modules from `../core/`:

- `binom_api.py` - Binom API client
- `transform_campaign_data.py` - Data transformation utilities

---

## Adding New Scripts

When adding new automation scripts:

1. **Use core modules:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from binom_api import BinomAPI
from transform_campaign_data import transform_campaign_for_update
```

2. **Follow naming convention:**
   - Use snake_case: `my_automation_script.py`
   - Be descriptive: `replace_offers.py` not `script1.py`

3. **Add documentation:**
   - Create `docs/scripts/automation/my-script.md`
   - Update this README

4. **Add configuration:**
   - Create `configs/my_script/config.example.json`
   - Document all options

5. **Add tests:**
   - Create `tests/unit/test_my_script.py`
   - Ensure >80% coverage

---

## Best Practices

✅ **Always include DRY RUN mode**  
✅ **Use configuration files (not hardcoded values)**  
✅ **Comprehensive logging**  
✅ **Error handling**  
✅ **Results file output**  
✅ **Type hints**  
✅ **Docstrings**  

---

## Safety Guidelines

⚠️ **IMPORTANT:** All automation scripts must:

1. **Preserve data integrity** - Never modify unrelated settings
2. **Support DRY RUN** - Allow preview before changes
3. **Log all operations** - For audit trail
4. **Handle errors gracefully** - Don't crash on single failure
5. **Respect rate limits** - Include delays between requests

---

## Support

- **Documentation:** [docs/scripts/automation/](../../docs/scripts/automation/)
- **Configuration:** [configs/](../../configs/)
- **Core Modules:** [scripts/core/](../core/)
- **API Docs:** https://docs.binom.org/api-v2.php

---

## Scripts Roadmap

Future automation scripts:

- [ ] Campaign cloner with bulk operations
- [ ] Traffic distribution optimizer
- [ ] Automated A/B testing setup
- [ ] Performance analytics exporter
- [ ] Bulk campaign settings updater

**Contributions welcome!** See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**⚠️ CRITICAL:** Never delete files from this directory without reviewing dependencies!  
These are production-tested scripts used in live environments.

