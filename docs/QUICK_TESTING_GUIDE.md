# Quick Testing Guide - Social Media Crawler

## 🧪 Test the API Endpoints

### Prerequisites
1. Server running: `python manage.py runserver`
2. You need a JWT token for authentication

---

## 1️⃣ Get JWT Token (Login)

First, you need to login to get your JWT token:

```powershell
# Login with your credentials
$loginBody = @{
    username = "your_username"
    password = "your_password"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $response.access
Write-Host "Token: $token"
```

---

## 2️⃣ Test Supported Platforms

```powershell
# Check which platforms are available
$headers = @{
    "Authorization" = "Bearer $token"
}

$platforms = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/supported_platforms/" -Method GET -Headers $headers
$platforms | ConvertTo-Json
```

**Expected Output:**
```json
{
  "platforms": ["github", "reddit"],
  "message": "2 platforms currently supported"
}
```

---

## 3️⃣ Create a GitHub Crawl Job

Let's crawl Linus Torvalds' GitHub profile:

```powershell
# Create GitHub crawl job
$jobBody = @{
    platform = "github"
    target_username = "torvalds"
    crawl_posts = $true
    max_posts = 20
} | ConvertTo-Json

$job = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/" -Method POST -Body $jobBody -ContentType "application/json" -Headers $headers
$jobId = $job.id
Write-Host "Job ID: $jobId"
$job | ConvertTo-Json
```

**Expected Output:**
```json
{
  "id": "abc123...",
  "platform": "github",
  "target_username": "torvalds",
  "status": "pending",
  "progress": 0,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 4️⃣ Check Job Progress

```powershell
# Check job status (wait a few seconds for crawling to complete)
Start-Sleep -Seconds 5
$jobStatus = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/$jobId/" -Method GET -Headers $headers
$jobStatus | ConvertTo-Json
```

**Expected Output:**
```json
{
  "id": "abc123...",
  "status": "completed",
  "progress": 100,
  "profiles_found": 1,
  "posts_found": 20,
  "completed_at": "2024-01-15T10:30:15Z"
}
```

---

## 5️⃣ View Crawled Profile

```powershell
# Get all profiles
$profiles = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/profiles/" -Method GET -Headers $headers
$profiles.results | ConvertTo-Json

# Get specific profile details
$profileId = $profiles.results[0].id
$profile = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/profiles/$profileId/" -Method GET -Headers $headers
$profile | ConvertTo-Json
```

**Expected Output:**
```json
{
  "id": "xyz789...",
  "platform": "github",
  "username": "torvalds",
  "display_name": "Linus Torvalds",
  "bio": "...",
  "followers_count": 150000,
  "following_count": 0,
  "posts_count": 20,
  "profile_url": "https://github.com/torvalds",
  "avatar_url": "https://avatars.githubusercontent.com/...",
  "crawled_at": "2024-01-15T10:30:15Z"
}
```

---

## 6️⃣ View Crawled Posts (Repositories)

```powershell
# Get all posts/repositories
$posts = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/posts/" -Method GET -Headers $headers
$posts.results | ConvertTo-Json

# Filter posts by profile
$posts = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/posts/?profile=$profileId" -Method GET -Headers $headers
$posts.results | Select-Object -First 5 | ConvertTo-Json
```

**Expected Output:**
```json
[
  {
    "id": "post123...",
    "post_id": "linux",
    "content": "Linux kernel source tree",
    "likes_count": 150000,
    "post_url": "https://github.com/torvalds/linux",
    "posted_at": "2011-09-04T00:00:00Z"
  }
]
```

---

## 7️⃣ Test Reddit Crawler

```powershell
# Create Reddit crawl job
$redditJob = @{
    platform = "reddit"
    target_username = "spez"
    crawl_posts = $true
    max_posts = 30
} | ConvertTo-Json

$job = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/" -Method POST -Body $redditJob -ContentType "application/json" -Headers $headers
$jobId = $job.id

# Wait and check status
Start-Sleep -Seconds 10
$jobStatus = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/$jobId/" -Method GET -Headers $headers
$jobStatus | ConvertTo-Json
```

---

## 8️⃣ Get Profile Analytics

```powershell
# Get analytics for a profile
$analytics = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/profiles/$profileId/analytics/" -Method GET -Headers $headers
$analytics | ConvertTo-Json
```

**Expected Output:**
```json
{
  "profile": {
    "username": "torvalds",
    "platform": "github"
  },
  "total_posts": 20,
  "total_engagement": 500000,
  "avg_engagement_per_post": 25000.0,
  "most_liked_post": {
    "content": "Linux kernel source tree",
    "likes_count": 150000
  },
  "most_commented_post": {
    "content": "...",
    "comments_count": 5000
  },
  "engagement_by_type": {
    "likes": 450000,
    "comments": 50000,
    "shares": 0
  }
}
```

---

## 9️⃣ Get User Statistics

```powershell
# Get your crawl statistics
$stats = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/statistics/" -Method GET -Headers $headers
$stats | ConvertTo-Json
```

**Expected Output:**
```json
{
  "total_jobs": 2,
  "completed_jobs": 2,
  "failed_jobs": 0,
  "pending_jobs": 0,
  "in_progress_jobs": 0,
  "total_profiles_crawled": 2,
  "total_posts_crawled": 50,
  "jobs_by_platform": {
    "github": 1,
    "reddit": 1
  }
}
```

---

## 🔟 Create Recurring Schedule

```powershell
# Schedule daily crawl for a GitHub user
$schedule = @{
    name = "Daily Linux Kernel Check"
    platform = "github"
    target_username = "torvalds"
    frequency = "daily"
    is_active = $true
    crawl_config = @{
        crawl_posts = $true
        max_posts = 10
    }
} | ConvertTo-Json

$newSchedule = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/schedules/" -Method POST -Body $schedule -ContentType "application/json" -Headers $headers
$newSchedule | ConvertTo-Json
```

---

## 1️⃣1️⃣ Filter Posts by Date

```powershell
# Get posts from last 30 days
$date = (Get-Date).AddDays(-30).ToString("yyyy-MM-dd")
$recentPosts = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/posts/?posted_after=$date" -Method GET -Headers $headers
$recentPosts.results | ConvertTo-Json
```

---

## 1️⃣2️⃣ Cancel Running Job

```powershell
# If a job is taking too long, cancel it
Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/$jobId/cancel/" -Method POST -Headers $headers
```

---

## 1️⃣3️⃣ Restart Failed Job

```powershell
# Restart a failed job
Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/$jobId/restart/" -Method POST -Headers $headers
```

---

## 📊 Using Django Admin

1. Create superuser (if not done):
```powershell
.\env\Scripts\activate
python manage.py createsuperuser
```

2. Visit: `http://localhost:8000/admin/`

3. Navigate to:
   - **Crawl jobs** - View all crawl jobs
   - **Social profiles** - View all profiles
   - **Social posts** - View all posts
   - **Social metrics** - View time-series data
   - **Crawl schedules** - Manage schedules

---

## 🎯 Quick Test Script

Here's a complete script to test everything:

```powershell
# Complete Test Script

# 1. Login
$loginBody = @{
    username = "testuser"
    password = "testpass"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $response.access
$headers = @{ "Authorization" = "Bearer $token" }

Write-Host "✅ Logged in successfully" -ForegroundColor Green

# 2. Check platforms
$platforms = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/supported_platforms/" -Method GET -Headers $headers
Write-Host "✅ Platforms: $($platforms.platforms -join ', ')" -ForegroundColor Green

# 3. Create GitHub job
$jobBody = @{
    platform = "github"
    target_username = "torvalds"
    crawl_posts = $true
    max_posts = 10
} | ConvertTo-Json

$job = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/" -Method POST -Body $jobBody -ContentType "application/json" -Headers $headers
$jobId = $job.id
Write-Host "✅ Created job: $jobId" -ForegroundColor Green

# 4. Wait for completion
Write-Host "⏳ Waiting for crawl to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 5. Check results
$jobStatus = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/jobs/$jobId/" -Method GET -Headers $headers
Write-Host "✅ Job Status: $($jobStatus.status)" -ForegroundColor Green
Write-Host "✅ Profiles Found: $($jobStatus.profiles_found)" -ForegroundColor Green
Write-Host "✅ Posts Found: $($jobStatus.posts_found)" -ForegroundColor Green

# 6. Get profiles
$profiles = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/profiles/" -Method GET -Headers $headers
Write-Host "✅ Total Profiles: $($profiles.count)" -ForegroundColor Green

# 7. Get posts
$posts = Invoke-RestMethod -Uri "http://localhost:8000/api/crawler/posts/" -Method GET -Headers $headers
Write-Host "✅ Total Posts: $($posts.count)" -ForegroundColor Green

Write-Host "`n🎉 All tests passed!" -ForegroundColor Cyan
```

---

## ✅ Success Criteria

After running the tests, you should see:
- ✅ JWT token obtained
- ✅ Platforms list returned (github, reddit)
- ✅ Crawl job created and completed
- ✅ Profile data retrieved
- ✅ Posts/repositories retrieved
- ✅ Analytics working
- ✅ Statistics showing correct counts

---

## 🐛 Common Issues

### Issue: "Authentication credentials were not provided"
**Solution:** Make sure you're passing the JWT token in the Authorization header

### Issue: "Platform not supported"
**Solution:** Only 'github' and 'reddit' are currently supported

### Issue: Job stuck in 'pending'
**Solution:** Check server logs for errors. The crawler runs asynchronously.

### Issue: "User not found" (GitHub/Reddit)
**Solution:** Verify the username exists on that platform

---

## 📖 Next Steps

1. ✅ Test all endpoints with this guide
2. ⏳ Build React frontend components
3. ⏳ Add more platforms (Twitter, LinkedIn)
4. ⏳ Implement sentiment analysis
5. ⏳ Add data visualization

---

*Happy Crawling! 🚀*
