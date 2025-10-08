# 🤖 How to Automate Tor Usage - Complete Guide

## Current Status
- ✅ Tor integration working
- ✅ Manual usage via `anonymous_get()` ready
- ❌ Automatic usage NOT enabled yet
- ❌ Crawlers still use real IP by default

---

## 🎯 4 Ways to Automate Tor

### **Option 1: Quick Global Automation** ⚡ (Recommended for testing)
**What:** All crawlers automatically use Tor when enabled  
**Time:** 30 minutes  
**Difficulty:** Easy ⭐

#### Steps:
1. **Update BaseCrawler** to use Tor automatically
2. **Enable in .env**: `TOR_ENABLED=true`
3. **Done!** All requests use Tor

#### Pros:
- ✅ Fastest implementation
- ✅ No database changes
- ✅ Works immediately

#### Cons:
- ❌ All-or-nothing (can't choose per request)
- ❌ May slow down development

---

### **Option 2: Per-Job Tor Toggle** 🎚️ (Recommended for production)
**What:** Users can choose Tor on/off for each crawl job  
**Time:** 2-3 hours  
**Difficulty:** Medium ⭐⭐

#### Steps:
1. **Add `use_tor` field to CrawlJob model**
2. **Update crawlers to accept use_tor parameter**
3. **Add Tor toggle checkbox in frontend**
4. **Create migration and update API**

#### Pros:
- ✅ User control per job
- ✅ Flexible and transparent
- ✅ Can track which jobs used Tor

#### Cons:
- ❌ Requires database migration
- ❌ Frontend changes needed

---

### **Option 3: Smart Auto-Detection** 🧠 (Recommended for advanced)
**What:** System automatically enables Tor for risky operations  
**Time:** 3-4 hours  
**Difficulty:** Advanced ⭐⭐⭐

#### Steps:
1. **Add `tor_recommended` field to GoogleDork**
2. **Auto-enable Tor when:**
   - Dork risk_level = 'high' or 'critical'
   - Rate limit detected (429 response)
   - Specific categories (e.g., 'exposed-credentials')
3. **Log Tor usage for audit**

#### Pros:
- ✅ Intelligent automation
- ✅ Reduces detection risk
- ✅ Automatic rate limit handling

#### Cons:
- ❌ Complex logic
- ❌ Requires testing

---

### **Option 4: Scheduled Automation** ⏰ (Recommended for background jobs)
**What:** Run automated dorks with Tor on schedule  
**Time:** 1-2 hours  
**Difficulty:** Medium ⭐⭐

#### Steps:
1. **Create management command** `tor_crawl_scheduled.py`
2. **Set up cron job or Celery task**
3. **Run periodically** (e.g., daily at midnight)

#### Pros:
- ✅ Background execution
- ✅ No user interaction
- ✅ Scheduled operations

#### Cons:
- ❌ Requires task scheduler
- ❌ Setup complexity

---

## 🚀 Quick Start: Option 1 Implementation

### Step 1: Update BaseCrawler (30 minutes)

**File:** `socialcrawler/services.py`

```python
# Add at top
from django.conf import settings
from googledorks.services.tor_service import TorProxyService

class BaseCrawler:
    """Base class for social media crawlers"""
    
    def __init__(self, username: str, max_posts: int = 100, use_tor: bool = None):
        self.username = username
        self.max_posts = max_posts
        
        # Auto-detect Tor usage
        if use_tor is None:
            use_tor = getattr(settings, 'TOR_ENABLED', False)
        
        self.use_tor = use_tor
        
        # Use Tor session if enabled
        if self.use_tor:
            try:
                self.tor_service = TorProxyService()
                self.session = self.tor_service.get_session()
                logger.info(f"🧅 Tor enabled for {self.username}")
            except Exception as e:
                logger.warning(f"Failed to enable Tor: {e}. Using regular session.")
                self.session = requests.Session()
        else:
            self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with optional Tor support"""
        try:
            if self.use_tor and hasattr(self, 'tor_service'):
                # Use Tor with retry
                response = self.tor_service.request_with_retry(url, method=method, **kwargs)
                logger.debug(f"🧅 Tor request to {url}")
            else:
                # Regular request
                response = self.session.request(method, url, **kwargs)
                logger.debug(f"🌐 Regular request to {url}")
            
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
```

### Step 2: Enable Tor in .env

**File:** `Cred/.env`

```env
# Change this line:
TOR_ENABLED=true  # Change from 'false' to 'true'
```

### Step 3: Start Tor containers

```bash
docker-compose -f docker-compose.tor.yml up -d
```

### Step 4: Test!

```bash
# Run your crawler
python manage.py runserver

# Or test directly
python test_tor_demo.py
```

**Done!** ✅ All crawlers now use Tor automatically!

---

## 📊 Comparison Table

| Feature | Option 1: Global | Option 2: Toggle | Option 3: Smart | Option 4: Scheduled |
|---------|-----------------|------------------|-----------------|---------------------|
| **Setup Time** | 30 min | 2-3 hrs | 3-4 hrs | 1-2 hrs |
| **User Control** | ❌ None | ✅ Per-job | ⚠️ Partial | ❌ None |
| **Flexibility** | ⭐ Low | ⭐⭐⭐ High | ⭐⭐ Medium | ⭐ Low |
| **Best For** | Testing | Production | Advanced | Background |
| **DB Changes** | ❌ None | ✅ Required | ✅ Required | ❌ None |
| **Frontend Changes** | ❌ None | ✅ Required | ⚠️ Optional | ❌ None |

---

## 🎯 Recommended Path

### For Quick Testing (Today):
1. ✅ **Implement Option 1** (30 minutes)
2. ✅ Test with Google Dorks
3. ✅ Verify IP rotation works

### For Production (This Week):
1. ✅ Implement Option 2 (Per-job toggle)
2. ✅ Add Tor status indicator in UI
3. ✅ Track Tor usage statistics

### For Advanced Features (Future):
1. ✅ Add Option 3 (Smart auto-detection)
2. ✅ Implement rate limit handling
3. ✅ Add Tor usage analytics

---

## 🔧 Example: Complete Implementation

### 1. Update BaseCrawler (services.py)

```python
class BaseCrawler:
    def __init__(self, username: str, max_posts: int = 100, use_tor: bool = None):
        self.username = username
        self.max_posts = max_posts
        
        # Auto-detect Tor
        if use_tor is None:
            use_tor = getattr(settings, 'TOR_ENABLED', False)
        
        self.use_tor = use_tor
        self.tor_service = None
        
        # Setup session
        if self.use_tor:
            try:
                from googledorks.services.tor_service import TorProxyService
                self.tor_service = TorProxyService()
                self.session = self.tor_service.get_session()
                logger.info(f"🧅 Tor enabled for @{username}")
            except Exception as e:
                logger.warning(f"Tor failed, using regular: {e}")
                self.session = requests.Session()
                self.use_tor = False
        else:
            self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
```

### 2. Update TwitterCrawler

```python
class TwitterCrawler(BaseCrawler):
    def __init__(self, username: str, max_posts: int = 100, api_key: str = None, use_tor: bool = None):
        super().__init__(username, max_posts, use_tor=use_tor)
        self.api_key = api_key
        self.base_url = "https://twitter.com"
```

### 3. Update views.py to pass use_tor

```python
def create_crawl_job(request):
    if request.method == 'POST':
        use_tor = request.POST.get('use_tor', 'false') == 'true'
        
        # Create crawler with Tor
        if platform == 'twitter':
            crawler = TwitterCrawler(username, max_posts=max_posts, use_tor=use_tor)
```

---

## 🧪 Testing Automation

### Test Script: test_crawler_automation.py

```python
#!/usr/bin/env python
"""
Test Crawler Tor Automation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from socialcrawler.services import TwitterCrawler, GitHubCrawler
import requests

def test_crawler_tor():
    print("=" * 70)
    print("🧪 Testing Crawler Tor Automation")
    print("=" * 70)
    
    # Test 1: Check real IP
    print("\n1️⃣ Real IP (without Tor):")
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        real_ip = response.json().get('ip')
        print(f"   🌐 Real IP: {real_ip}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Crawler with Tor disabled
    print("\n2️⃣ Crawler with Tor DISABLED:")
    try:
        crawler = TwitterCrawler('elonmusk', use_tor=False)
        print(f"   use_tor: {crawler.use_tor}")
        print(f"   tor_service: {crawler.tor_service}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Crawler with Tor enabled
    print("\n3️⃣ Crawler with Tor ENABLED:")
    try:
        crawler = TwitterCrawler('elonmusk', use_tor=True)
        print(f"   ✅ use_tor: {crawler.use_tor}")
        print(f"   🧅 tor_service: {crawler.tor_service}")
        
        # Verify Tor IP
        if crawler.tor_service:
            result = crawler.tor_service.verify_tor_connection()
            if result['success']:
                print(f"   🎯 Tor IP: {result['exit_ip']}")
                if result['exit_ip'] != real_ip:
                    print(f"   ✅ SUCCESS! Using different IP through Tor!")
                else:
                    print(f"   ⚠️  WARNING: Same IP detected")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    test_crawler_tor()
```

---

## 📝 Next Steps

### Immediate (Today - 30 minutes):
- [ ] Copy BaseCrawler update code to `socialcrawler/services.py`
- [ ] Test with `python test_crawler_automation.py`
- [ ] Verify Tor works with crawlers

### Short-term (This Week - 2-3 hours):
- [ ] Add `use_tor` field to CrawlJob model
- [ ] Update frontend with Tor toggle
- [ ] Add Tor status indicators

### Long-term (Future):
- [ ] Smart auto-detection for risky dorks
- [ ] Scheduled Tor crawls
- [ ] Tor usage analytics dashboard

---

## 🎓 Best Practices

### When to Use Tor Automatically:
- ✅ High-risk Google dorks
- ✅ Critical security research
- ✅ Rate-limited targets
- ✅ Privacy-sensitive operations
- ✅ Automated scheduled tasks

### When NOT to Use Tor:
- ❌ Development/testing (slower)
- ❌ Trusted APIs with authentication
- ❌ Internal network requests
- ❌ When speed is critical

### Security Tips:
- 🔒 Always verify Tor connection before sensitive operations
- 🔄 Rotate circuits regularly (every 10-20 requests)
- 📝 Log Tor usage for audit trails
- ⚠️ Monitor for Tor exit node blocks
- 🛡️ Use HTTPS even with Tor

---

## 📞 Quick Commands

```bash
# Start Tor containers
docker-compose -f docker-compose.tor.yml up -d

# Check Tor status
docker-compose -f docker-compose.tor.yml ps

# View Tor logs
docker logs tor-service

# Test Tor connection
python test_tor_demo.py

# Check current IP
python check_current_ip.py

# Restart Tor (rotate IP)
docker-compose -f docker-compose.tor.yml restart tor-proxy
```

---

## ✅ Status Checklist

- [x] Tor integration working
- [x] Docker containers running
- [x] Manual Tor usage ready
- [ ] Automatic Tor in crawlers
- [ ] Per-job Tor toggle
- [ ] Smart auto-detection
- [ ] Scheduled automation

---

**Ready to implement? Start with Option 1 (30 minutes)!** 🚀
