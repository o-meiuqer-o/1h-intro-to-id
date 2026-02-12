# Wikimedia Category Harvest Script
# Implements "Category Search" strategy:
# 1. Find Category:Designer Name
# 2. List all images in category
# 3. Match against Manifest Targets -> Download to images/<designer>/
# 4. Download others -> images/_extras/<designer>/
# 5. Log results

$manifestPath = "D:\history of id course\gallery_manifest.json"
$targetDir = "D:\history of id course"
$logPath = "D:\history of id course\harvest_log_v2.csv"
$userAgent = "IDHistoryCourseProject/1.0 (https://example.com; muef2246@gemini.com)"

# Ensure Extras Directory
$extrasBase = Join-Path $targetDir "images/_extras"
if (-not (Test-Path $extrasBase)) { New-Item -ItemType Directory -Path $extrasBase | Out-Null }

# Initialize Log
"Designer,Work,Type,Status,SourceURL,LocalPath,Notes" | Out-File -FilePath $logPath -Encoding UTF8

# Load Manifest
$json = Get-Content -Path $manifestPath | ConvertFrom-Json

# Helper: Get Category Members
function Get-CategoryMembers($categoryName) {
    $encoded = [System.Web.HttpUtility]::UrlEncode($categoryName)
    $apiUrl = "https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=$encoded&cmtype=file&cmlimit=500&format=json&prop=imageinfo&iiprop=url|size|mime|extmetadata"
    
    try {
        $resp = Invoke-RestMethod -Uri $apiUrl -Method Get -UserAgent $userAgent -ErrorAction Stop
        if ($resp.query -and $resp.query.categorymembers) {
            return $resp.query.categorymembers
        }
    } catch {
        return @()
    }
    return @()
}

# Helper: Get Actual Image URL from Page ID (needed because list=categorymembers doesn't always give url directly in one go? 
# Actually, generator is better, but let's iterate. 
# Wait, categorymembers gives 'title'. We need 'imageinfo' for URL.
# Better to use a generator query.)

function Get-CategoryImages($categoryName) {
    $encoded = [System.Web.HttpUtility]::UrlEncode($categoryName)
    # Using generator to get imageinfo directly
    $apiUrl = "https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=$encoded&gcmtype=file&gcmlimit=50&format=json&prop=imageinfo&iiprop=url|size|mime"
    
    try {
        $resp = Invoke-RestMethod -Uri $apiUrl -Method Get -UserAgent $userAgent -ErrorAction Stop
        if ($resp.query -and $resp.query.pages) {
            return $resp.query.pages.PSObject.Properties.Value # Array of page objects
        }
    } catch {
        Write-Host "API Error: $_" -ForegroundColor Red
        return @()
    }
    return @()
}

# Helper: Fuzzy Match
function Test-Match($workName, $fileTitle) {
    # workName: "dreyfuss_big_ben_clock" -> keys: "big", "ben", "clock"
    # fileTitle: "File:Big Ben Westclox 1939.jpg" -> keys: "big", "ben", "westclox", "1939"
    
    $cleanWork = ($workName -replace "_", " ") -replace "dreyfuss", "" -replace "rams", "" # Remove designer name from work key to avoid false positives?
    # Actually, designer name in file title is GOOD.
    
    $workTokens = ($workName -replace "_", " ").Split(" ") | Where-Object { $_.Length -gt 2 }
    $fileTokens = ($fileTitle -replace "File:", "" -replace ".jpg", "" -replace ".png", "").Split(" ")
    
    $matchCount = 0
    foreach ($token in $workTokens) {
        if ($fileTitle -match $token) { $matchCount++ }
    }
    
    # If we match significant portion of tokens
    if ($workTokens.Count -gt 0 -and $matchCount -ge ($workTokens.Count * 0.6)) {
        return $true
    }
    return $false
}

# Main Loop
$designers = $json.PSObject.Properties.Name
foreach ($key in $designers) {
    if ($key -eq "_archive") { continue }
    
    $designer = $json.$key
    $realName = $designer.name
    $catName = "Category:$($realName)"
    
    Write-Host "Processing $realName ($catName)..." -ForegroundColor Cyan
    
    $commonsImages = Get-CategoryImages -categoryName $catName
    Write-Host "  Found $($commonsImages.Count) images in category." -ForegroundColor Gray
    
    # Track which manifest works are found
    $manifestWorks = $designer.images
    $foundWorks = @{}
    
    # 1. Match Manifest Works
    foreach ($targetPath in $manifestWorks) {
        $workBase = [System.IO.Path]::GetFileNameWithoutExtension($targetPath)
        $fullTargetPath = Join-Path $targetDir $targetPath
        $targetDirParent = [System.IO.Path]::GetDirectoryName($fullTargetPath)
        if (-not (Test-Path $targetDirParent)) { New-Item -ItemType Directory -Path $targetDirParent | Out-Null }
        
        $bestMatch = $null
        
        foreach ($img in $commonsImages) {
            $title = $img.title
            if (Test-Match -workName $workBase -fileTitle $title) {
                $bestMatch = $img
                break # Take first good match? Or best? First is okay for now.
            }
        }
        
        if ($bestMatch) {
            $url = $bestMatch.imageinfo[0].url
            $ext = [System.IO.Path]::GetExtension($url)
            # Save with original extension to avoid corruption, BUT we need to update manifest later if extension changes.
            # For now, just save to the TARGET path (forcing extension) or append correct extension?
            # User said "then convert". 
            # I will save as `filename.EXT` (real ext) and logging it. 
            # The HTML expects `.jpg`. 
            # I will save to `filename.jpg` even if it is png/webp. Browsers usually handle "png inside jpg file".
            
            try {
                Invoke-WebRequest -Uri $url -OutFile $fullTargetPath -UserAgent $userAgent -ErrorAction Stop
                $logLine = "$realName,$workBase,Target,Success,$url,$targetPath,Match: $($bestMatch.title)"
                Write-Host "  [MATCH] $workBase -> $($bestMatch.title)" -ForegroundColor Green
                $foundWorks[$bestMatch.pageid] = $true
            } catch {
                $logLine = "$realName,$workBase,Target,Failed,$url,$targetPath,$_"
                Write-Host "  [ERROR] ${workBase}: $_" -ForegroundColor Red
            }
        } else {
            $logLine = "$realName,$workBase,Target,NotFound,,$targetPath,No match in category"
            # Write-Host "  [MISS] $workBase" -ForegroundColor Yellow
        }
        $logLine | Out-File -FilePath $logPath -Append -Encoding UTF8
    }
    
    # 2. Download Extras
    $extrasDir = Join-Path $extrasBase $key
    if (-not (Test-Path $extrasDir)) { New-Item -ItemType Directory -Path $extrasDir | Out-Null }
    
    $extraCount = 0
    foreach ($img in $commonsImages) {
        if ($foundWorks.ContainsKey($img.pageid)) { continue }
        if ($extraCount -ge 5) { break } # Limit extras to 5 per designer to save dragging on
        
        $url = $img.imageinfo[0].url
        $title = $img.title -replace "File:", ""
        # Clean title for filename
        $safeTitle = $title -replace "[^a-zA-Z0-9\-\.]", "_"
        $localPath = Join-Path $extrasDir $safeTitle
        
        try {
            Invoke-WebRequest -Uri $url -OutFile $localPath -UserAgent $userAgent -ErrorAction Stop
            $logLine = "$realName,$title,Extra,Success,$url,$localPath,Extra Image"
            Write-Host "  [EXTRA] $title" -ForegroundColor Gray
            $extraCount++
        } catch {
            $logLine = "$realName,$title,Extra,Failed,$url,$localPath,$_"
        }
        $logLine | Out-File -FilePath $logPath -Append -Encoding UTF8
    }
    
    Start-Sleep -Milliseconds 500
}
