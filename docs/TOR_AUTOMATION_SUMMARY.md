# 🤖 Tor Automation Summary

## ✅ What I Created for You

### 📚 Documentation (3 files)
1. **`docs/TOR_AUTOMATION_GUIDE.md`** - Complete automation guide with 4 options
2. **`socialcrawler/services_updated.py`** - Updated BaseCrawler with Tor support (ready to use)
3. **`test_crawler_automation.py`** - Test script to verify automation works

### 🛠️ Setup Scripts (2 files)
4. **`quick_tor_setup.py`** - Interactive setup guide
5. **`check_current_ip.py`** - Check what IP you're using

---

## 🎯 Quick Answer: How to Automate Tor

### **Option 1: Global Automation** (Easiest - 5 minutes)

**Make ALL crawlers use Tor automatically:**

1. **Update .env file:**
   ```env
   TOR_ENABLED=true  # Change from false to true
   ```

2. **Update BaseCrawler** in `socialcrawler/services.py`:
   - Copy code from `socialcrawler/services_updated.py`
   - Replace the existing `BaseCrawler` class

3. **Done!** ✅ All crawlers now use Tor

---

### **Option 2: Per-Crawler Control** (Flexible - 30 minutes)

**Let users choose Tor on/off for each crawler:**

1. **Update BaseCrawler** (same as Option 1)

2. **Use in your code:**
   ```python
   # Force Tor on
   crawler = TwitterCrawler('elonmusk', use_tor=True)
   
   # Force Tor off
   crawler = TwitterCrawler('elonmusk', use_tor=False)
   
   # Auto-detect from settings
   crawler = TwitterCrawler('elonmusk')  # Uses TOR_ENABLED setting
   ```

3. **Keep TOR_ENABLED=false** in .env (so it's opt-in)

---

## 🔍 Current Status

### ✅ What's Working:
- ✅ Tor containers running (healthy for 33 minutes)
- ✅ Manual Tor usage with `anonymous_get()`
- ✅ IP hiding verified (185.195.71.244 → 5.255.99.5)
- ✅ Circuit rotation working
- ✅ All documentation created

### ❌ What's NOT Automatic Yet:
- ❌ Crawlers don't use Tor by default
- ❌ BaseCrawler needs update (5 minutes to fix)
- ❌ TOR_ENABLED=false in .env

---

## 🚀 Fastest Path to Automation (5 Minutes)

### Step 1: Update BaseCrawler (3 minutes)

**File:** `socialcrawler/services.py`

Find this:
```python
class BaseCrawler:
    def __init__(self, username: str, max_posts: int = 100):
        self.username = username
        self.max_posts = max_posts
        self.session = requests.Session()
```

Replace with this:
```python
class BaseCrawler:
    def __init__(self, username: str, max_posts: int = 100, use_tor: bool = None):
        self.username = username
        self.max_posts = max_posts
        
        # Auto-detect Tor from settings
        if use_tor is None:
            use_tor = getattr(settings, 'TOR_ENABLED', False)
        
        self.use_tor = use_tor
        self.tor_service = None
        
        # Use Tor if enabled
        if self.use_tor:
            try:
                from googledorks.services.tor_service import TorProxyService
                self.tor_service = TorProxyService()
                self.session = self.tor_service.get_session()
                logger.info(f"🧅 Tor enabled for {username}")
            except Exception as e:
                logger.warning(f"Tor failed: {e}")
                self.session = requests.Session()
                self.use_tor = False
        else:
            self.session = requests.Session()
```

**Full code available in:** `socialcrawler/services_updated.py`

### Step 2: Update Crawler Classes (2 minutes)

For EACH crawler (Twitter, GitHub, LinkedIn, Reddit), add `use_tor` parameter:

**Before:**
```python
class TwitterCrawler(BaseCrawler):
    def __init__(self, username: str, max_posts: int = 100, api_key: str = None):
        super().__init__(username, max_posts)
```

**After:**
```python
class TwitterCrawler(BaseCrawler):
    def __init__(self, username: str, max_posts: int = 100, api_key: str = None, use_tor: bool = None):
        super().__init__(username, max_posts, use_tor=use_tor)
```

### Step 3: Enable Tor (30 seconds)

**File:** `Cred/.env`

```env
# Change this:
TOR_ENABLED=false

# To this:
TOR_ENABLED=true
```

### Step 4: Test! (1 minute)

```bash
python test_crawler_automation.py
```

**Done!** ✅ All crawlers now use Tor automatically!

---

## 📊 Automation Options Comparison

| Feature | Option 1: Global | Option 2: Per-Crawler | Option 3: Smart | Option 4: Scheduled |
|---------|------------------|----------------------|-----------------|---------------------|
| **Setup Time** | 5 min | 30 min | 3-4 hrs | 1-2 hrs |
| **Code Changes** | BaseCrawler only | BaseCrawler + views | + AI logic | + cron jobs |
| **User Control** | ❌ None | ✅ Full | ⚠️ Partial | ❌ None |
| **Best For** | Testing | Production | Advanced | Background |
| **Flexibility** | ⭐ Low | ⭐⭐⭐ High | ⭐⭐ Medium | ⭐ Low |

---

## 🧪 Testing Commands

```bash
# Check current IP
python check_current_ip.py

# Test Tor automation
python test_crawler_automation.py

# Run Tor demo
python test_tor_demo.py

# Check Docker containers
docker ps | grep tor

# View Tor logs
docker logs tor-service
```

---

## 📝 Example Usage After Setup

### Example 1: Auto Tor (when TOR_ENABLED=true)
```python
from socialcrawler.services import TwitterCrawler

# This will automatically use Tor
crawler = TwitterCrawler('elonmusk')
profile = await crawler.crawl_profile()
```

### Example 2: Force Tor On
```python
# Even if TOR_ENABLED=false, this uses Tor
crawler = TwitterCrawler('elonmusk', use_tor=True)
```

### Example 3: Force Tor Off
```python
# Even if TOR_ENABLED=true, this uses real IP
crawler = TwitterCrawler('elonmusk', use_tor=False)
```

### Example 4: Check IP During Crawl
```python
crawler = TwitterCrawler('elonmusk', use_tor=True)
current_ip = crawler.get_current_ip()
print(f"Crawling from: {current_ip}")
```

### Example 5: Rotate IP Mid-Crawl
```python
crawler = TwitterCrawler('elonmusk', use_tor=True)

# Crawl some posts
posts1 = await crawler.crawl_posts()

# Rotate to new IP
crawler.rotate_circuit()

# Crawl more with different IP
posts2 = await crawler.crawl_posts()
```

---

## 🎯 Recommended Implementation

### For Your Faculty Demo (Today):
1. ✅ **Implement Option 1** (Global automation - 5 minutes)
2. ✅ Set `TOR_ENABLED=true`
3. ✅ Show live IP rotation during crawl
4. ✅ Demonstrate anonymity working

### For Production (This Week):
1. ✅ **Implement Option 2** (Per-crawler toggle)
2. ✅ Add frontend UI checkbox
3. ✅ Track Tor usage in database
4. ✅ Show Tor status in UI

### For Advanced Features (Future):
1. ✅ **Implement Option 3** (Smart auto-detection)
2. ✅ Auto-enable for high-risk dorks
3. ✅ Handle rate limits automatically
4. ✅ Add Tor analytics dashboard

---

## 🔗 Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `docs/TOR_AUTOMATION_GUIDE.md` | Complete guide | ✅ Created |
| `socialcrawler/services_updated.py` | Updated BaseCrawler | ✅ Ready |
| `test_crawler_automation.py` | Test automation | ✅ Ready |
| `quick_tor_setup.py` | Setup helper | ✅ Ready |
| `check_current_ip.py` | IP checker | ✅ Ready |
| `socialcrawler/services.py` | Original (needs update) | ⚠️ To-do |
| `Cred/.env` | Config (TOR_ENABLED=false) | ⚠️ To-do |

---

## ❓ FAQ

**Q: Will `python manage.py runserver` use Tor after setup?**  
A: No. The Django server still uses your real IP. Only crawler requests use Tor when `use_tor=True` or `TOR_ENABLED=true`.

**Q: Do I need to restart Django after enabling Tor?**  
A: No. Settings are loaded when creating crawler instances. But restart helps ensure clean state.

**Q: Will this slow down development?**  
A: Yes, Tor is slower. That's why Option 2 (per-crawler) is best - use Tor only when needed.

**Q: Can I use Tor for only specific dorks?**  
A: Yes! Implement Option 3 (Smart automation) to auto-enable Tor for risky dorks.

**Q: What if Tor containers are down?**  
A: Crawlers will automatically fall back to regular session and log a warning.

---

## 🎓 Best Practices

### When to Use Tor:
- ✅ High-risk Google dorks
- ✅ Exposed credentials searches
- ✅ Rate-limited targets
- ✅ Privacy-sensitive operations
- ✅ Automated scheduled tasks

### When NOT to Use Tor:
- ❌ Development testing (slower)
- ❌ Trusted APIs with auth
- ❌ Low-risk dorks
- ❌ When speed is critical

---

## 🚀 Next Steps

### Immediate (5 minutes):
- [ ] Copy BaseCrawler code from `services_updated.py`
- [ ] Update crawler classes with `use_tor` parameter
- [ ] Test with `python test_crawler_automation.py`

### Optional (later):
- [ ] Enable globally: Set `TOR_ENABLED=true`
- [ ] Add frontend Tor toggle
- [ ] Implement smart auto-detection

---

## ✅ Summary

**You asked:** "how to automate it"

**Answer:** 
1. ✅ **Easiest:** Update BaseCrawler (5 min) + set TOR_ENABLED=true → ALL crawlers use Tor
2. ✅ **Flexible:** Same update + use `use_tor=True` per crawler → Choose when to use Tor
3. ✅ **Smart:** Add logic to auto-enable Tor for risky operations
4. ✅ **Scheduled:** Run automated crawls with Tor via cron jobs

**Recommendation:** Start with Option 1 (5 minutes) for demo, then upgrade to Option 2 for production.

**All code is ready!** Just copy from `socialcrawler/services_updated.py` to `socialcrawler/services.py` 🚀
