# Project Health Check Script
# Simulates CI/CD checks to find corrupted files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PROJECT HEALTH CHECK - CI/CD SIMULATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0
$WarningCount = 0
$CorruptedFiles = @()

# 1. Check Python Files
Write-Host "[1/6] Checking Python files for syntax errors..." -ForegroundColor Yellow
$PythonFiles = Get-ChildItem -Path "." -Include "*.py" -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "\\env\\" -and $_.FullName -notmatch "\\venv\\" -and $_.FullName -notmatch "\\__pycache__\\" }

foreach ($file in $PythonFiles) {
    try {
        $null = python -m py_compile $file.FullName 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  ❌ SYNTAX ERROR: $($file.Name)" -ForegroundColor Red
            $ErrorCount++
            $CorruptedFiles += @{
                File  = $file.FullName
                Type  = "Python"
                Error = "Syntax Error"
            }
        }
    }
    catch {
        Write-Host "  ⚠️  WARNING: Could not check $($file.Name)" -ForegroundColor Yellow
        $WarningCount++
    }
}
Write-Host "  ✅ Python syntax check complete" -ForegroundColor Green
Write-Host ""

# 2. Check TypeScript/TSX Files
Write-Host "[2/6] Checking TypeScript/React files..." -ForegroundColor Yellow
if (Test-Path "frontend") {
    Push-Location "frontend"
    
    # Check if node_modules exists
    if (-not (Test-Path "node_modules")) {
        Write-Host "  ⚠️  node_modules not found. Run 'npm install' first." -ForegroundColor Yellow
        $WarningCount++
    }
    else {
        # Run TypeScript compiler check
        Write-Host "  Running TypeScript compiler check..." -ForegroundColor Gray
        $tsOutput = npx tsc --noEmit 2>&1 | Out-String
        
        if ($tsOutput -match "error TS") {
            Write-Host "  ❌ TypeScript errors found!" -ForegroundColor Red
            
            # Parse errors and find corrupted files
            $tsErrors = $tsOutput -split "`n" | Where-Object { $_ -match "\.tsx?\(" }
            $uniqueFiles = @{}
            
            foreach ($errorLine in $tsErrors) {
                if ($errorLine -match "(.+\.tsx?)\((\d+),(\d+)\): error (TS\d+): (.+)") {
                    $errorFile = $matches[1]
                    $errorCode = $matches[4]
                    $errorMsg = $matches[5]
                    
                    if (-not $uniqueFiles.ContainsKey($errorFile)) {
                        $uniqueFiles[$errorFile] = @()
                    }
                    $uniqueFiles[$errorFile] += "$errorCode - $errorMsg"
                }
            }
            
            foreach ($file in $uniqueFiles.Keys) {
                Write-Host "  ❌ CORRUPTED: $file" -ForegroundColor Red
                Write-Host "     Errors: $($uniqueFiles[$file].Count)" -ForegroundColor Red
                $ErrorCount++
                $CorruptedFiles += @{
                    File    = Join-Path (Get-Location) $file
                    Type    = "TypeScript"
                    Error   = "TypeScript Errors: $($uniqueFiles[$file].Count)"
                    Details = $uniqueFiles[$file] -join "; "
                }
            }
        }
        else {
            Write-Host "  ✅ No TypeScript errors found" -ForegroundColor Green
        }
    }
    
    Pop-Location
}
else {
    Write-Host "  ⚠️  frontend folder not found" -ForegroundColor Yellow
    $WarningCount++
}
Write-Host ""

# 3. Check for Duplicate Content (Common corruption sign)
Write-Host "[3/6] Checking for duplicate content (corruption signature)..." -ForegroundColor Yellow
$FilesToCheck = Get-ChildItem -Path "." -Include "*.py", "*.tsx", "*.ts", "*.jsx", "*.js" -Recurse -ErrorAction SilentlyContinue | 
Where-Object { $_.FullName -notmatch "\\env\\" -and $_.FullName -notmatch "\\venv\\" -and $_.FullName -notmatch "\\node_modules\\" -and $_.FullName -notmatch "\\__pycache__\\" }

foreach ($file in $FilesToCheck) {
    try {
        $content = Get-Content $file.FullName -Raw
        $lines = Get-Content $file.FullName
        
        # Check for duplicate imports (common corruption sign)
        $imports = $lines | Where-Object { $_ -match "^import " }
        $uniqueImports = $imports | Select-Object -Unique
        
        if ($imports.Count -gt $uniqueImports.Count -and $imports.Count -gt 5) {
            $duplicateRatio = [math]::Round((($imports.Count - $uniqueImports.Count) / $imports.Count) * 100, 2)
            if ($duplicateRatio -gt 30) {
                Write-Host "  ❌ DUPLICATE IMPORTS: $($file.Name) ($duplicateRatio% duplicated)" -ForegroundColor Red
                $ErrorCount++
                $CorruptedFiles += @{
                    File  = $file.FullName
                    Type  = $file.Extension
                    Error = "Duplicate Imports ($duplicateRatio%)"
                }
            }
        }
        
        # Check for repeated lines (corruption signature)
        $lineGroups = $lines | Group-Object | Where-Object { $_.Count -gt 5 -and $_.Name.Trim().Length -gt 10 }
        if ($lineGroups) {
            Write-Host "  ⚠️  REPEATED LINES: $($file.Name) (suspicious pattern)" -ForegroundColor Yellow
            $WarningCount++
        }
    }
    catch {
        # Ignore errors for this check
    }
}
Write-Host "  ✅ Duplicate content check complete" -ForegroundColor Green
Write-Host ""

# 4. Check JSON Files
Write-Host "[4/6] Checking JSON files..." -ForegroundColor Yellow
$JsonFiles = Get-ChildItem -Path "." -Include "*.json" -Recurse -ErrorAction SilentlyContinue | 
Where-Object { $_.FullName -notmatch "\\node_modules\\" -and $_.FullName -notmatch "\\env\\" }

foreach ($file in $JsonFiles) {
    try {
        # Use -AsHashtable to handle package-lock.json with empty string keys (valid npm format)
        $null = Get-Content $file.FullName -Raw | ConvertFrom-Json -AsHashtable
    }
    catch {
        Write-Host "  ❌ INVALID JSON: $($file.Name)" -ForegroundColor Red
        $ErrorCount++
        $CorruptedFiles += @{
            File  = $file.FullName
            Type  = "JSON"
            Error = "Invalid JSON"
        }
    }
}
Write-Host "  ✅ JSON validation complete" -ForegroundColor Green
Write-Host ""

# 5. Check File Sizes (Abnormally large files might be corrupted)
Write-Host "[5/6] Checking for abnormally large files..." -ForegroundColor Yellow
$SourceFiles = Get-ChildItem -Path "." -Include "*.py", "*.tsx", "*.ts", "*.jsx", "*.js" -Recurse -ErrorAction SilentlyContinue | 
Where-Object { $_.FullName -notmatch "\\env\\" -and $_.FullName -notmatch "\\venv\\" -and $_.FullName -notmatch "\\node_modules\\" }

foreach ($file in $SourceFiles) {
    $sizeKB = [math]::Round($file.Length / 1KB, 2)
    if ($sizeKB -gt 50) {
        # Files over 50KB might be corrupted
        Write-Host "  ⚠️  LARGE FILE: $($file.Name) ($sizeKB KB)" -ForegroundColor Yellow
        $WarningCount++
        
        # Check if it's actually corrupted (duplicate content)
        $content = Get-Content $file.FullName -Raw
        if ($content -match "(.{100,})\1{2,}") {
            # Pattern repeats 3+ times
            Write-Host "  ❌ CORRUPTED (Duplicate Content): $($file.Name)" -ForegroundColor Red
            $ErrorCount++
            $CorruptedFiles += @{
                File  = $file.FullName
                Type  = $file.Extension
                Error = "Large file with duplicate content ($sizeKB KB)"
            }
        }
    }
}
Write-Host "  ✅ File size check complete" -ForegroundColor Green
Write-Host ""

# 6. Check for Encoding Issues
Write-Host "[6/6] Checking for encoding issues..." -ForegroundColor Yellow
$SourceFiles = Get-ChildItem -Path "." -Include "*.py", "*.tsx", "*.ts", "*.jsx", "*.js" -Recurse -ErrorAction SilentlyContinue | 
Where-Object { $_.FullName -notmatch "\\env\\" -and $_.FullName -notmatch "\\venv\\" -and $_.FullName -notmatch "\\node_modules\\" } | 
Select-Object -First 50  # Limit to first 50 files for speed

foreach ($file in $SourceFiles) {
    try {
        $content = Get-Content $file.FullName -Raw
        # Check for NULL bytes (corruption signature)
        if ($content -match "\x00") {
            Write-Host "  ❌ NULL BYTES: $($file.Name)" -ForegroundColor Red
            $ErrorCount++
            $CorruptedFiles += @{
                File  = $file.FullName
                Type  = $file.Extension
                Error = "Contains NULL bytes"
            }
        }
    }
    catch {
        Write-Host "  ⚠️  ENCODING ISSUE: $($file.Name)" -ForegroundColor Yellow
        $WarningCount++
    }
}
Write-Host "  ✅ Encoding check complete" -ForegroundColor Green
Write-Host ""

# Summary Report
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SUMMARY REPORT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($CorruptedFiles.Count -eq 0 -and $ErrorCount -eq 0) {
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "   No corrupted files found." -ForegroundColor Green
}
else {
    Write-Host "❌ ISSUES FOUND" -ForegroundColor Red
    Write-Host ""
    Write-Host "Total Errors: $ErrorCount" -ForegroundColor Red
    Write-Host "Total Warnings: $WarningCount" -ForegroundColor Yellow
    Write-Host ""
    
    if ($CorruptedFiles.Count -gt 0) {
        Write-Host "CORRUPTED FILES:" -ForegroundColor Red
        Write-Host "================" -ForegroundColor Red
        foreach ($corrupt in $CorruptedFiles) {
            Write-Host ""
            Write-Host "File: $($corrupt.File)" -ForegroundColor Yellow
            Write-Host "Type: $($corrupt.Type)" -ForegroundColor Gray
            Write-Host "Error: $($corrupt.Error)" -ForegroundColor Red
            if ($corrupt.Details) {
                Write-Host "Details: $($corrupt.Details.Substring(0, [Math]::Min(200, $corrupt.Details.Length)))..." -ForegroundColor Gray
            }
        }
        
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "RECOMMENDATIONS:" -ForegroundColor Yellow
        Write-Host "1. Review the corrupted files listed above" -ForegroundColor White
        Write-Host "2. Restore from git history: git checkout HEAD~1 -- <file>" -ForegroundColor White
        Write-Host "3. Or manually fix the syntax errors" -ForegroundColor White
        Write-Host "4. Run this script again to verify" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Scan completed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan

# Export report to file
$reportFile = "health-check-report.txt"
@"
PROJECT HEALTH CHECK REPORT
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
========================================

Total Errors: $ErrorCount
Total Warnings: $WarningCount

CORRUPTED FILES:
"@ | Out-File $reportFile

foreach ($corrupt in $CorruptedFiles) {
    @"

File: $($corrupt.File)
Type: $($corrupt.Type)
Error: $($corrupt.Error)
"@ | Out-File $reportFile -Append
}

Write-Host ""
Write-Host "📄 Report saved to: $reportFile" -ForegroundColor Cyan
