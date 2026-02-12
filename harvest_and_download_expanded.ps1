$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$baseDir = "D:\history of id course\images"
$csvPath = "D:\history of id course\expanded_designers.csv"
$logPath = "D:\history of id course\harvest_log_expanded.txt"

# Mimic browser to avoid blocks
$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

function Log-Message ($msg) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    try { Add-Content -Path $logPath -Value "[$timestamp] $msg" } catch {}
    Write-Host "[$timestamp] $msg"
}

$designers = Import-Csv -Path $csvPath

foreach ($d in $designers) {
    if (-not $d.CategoryName) { continue }
    
    $folderPath = Join-Path $baseDir $d.Folder
    if (-not (Test-Path $folderPath)) {
        New-Item -ItemType Directory -Force -Path $folderPath | Out-Null
    }
    
    Log-Message "Harvesting Category: $($d.CategoryName) -> $($d.Folder)"
    
    # 1. Get Category Members (Files) via API
    # generator=categorymembers & gcmtitle=Category:Name & gcmtype=file & gcmlimit=12
    # prop=imageinfo & iiprop=url|size|extmetadata
    
    $apiUrl = "https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:$($d.CategoryName)&gcmtype=file&gcmlimit=12&prop=imageinfo&iiprop=url|size&format=json"
    
    try {
        $json = Invoke-RestMethod -Uri $apiUrl -UserAgent $userAgent
        
        if (-not $json.query -or -not $json.query.pages) {
            Log-Message "  [WARN] No files found for category"
            continue
        }
        
        $pages = $json.query.pages
        
        # Iterate over properties of the pages object
        foreach ($key in $pages.PSObject.Properties.Name) {
            $page = $pages.$key
            if (-not $page.imageinfo) { continue }
            
            $url = $page.imageinfo[0].url
            $size = $page.imageinfo[0].size
            
            if ($size -lt 20000) { continue } # Skip small icons
            
            $fileName = [IO.Path]::GetFileName($url)
            $localPath = Join-Path $folderPath $fileName
            
            if (Test-Path $localPath) {
                # Log-Message "  [SKIP] Exists: $fileName"
                continue
            }
            
            Log-Message "  [DOWNLOADING] $fileName ($([math]::Round($size/1KB)) KB)"
            
            try {
                Invoke-WebRequest -Uri $url -OutFile $localPath -UserAgent $userAgent -TimeoutSec 30
                Start-Sleep -Milliseconds 500 # Be polite
            } catch {
                Log-Message "  [ERROR] Download failed: $($_.Exception.Message)"
            }
        }
        
    } catch {
        Log-Message "  [ERROR] API request failed: $($_.Exception.Message)"
    }
    
    Start-Sleep -Seconds 1
}

Log-Message "Harvesting Complete."
