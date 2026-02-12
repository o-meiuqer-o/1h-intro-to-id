$images = @{
    "D:\history of id course\images\rams\rams_et66_calculator_1987.jpg" = "https://upload.wikimedia.org/wikipedia/commons/d/d3/1987_Braun_calculator_ET66_by_Dieter_Rams_%2813964223413%29.jpg";
    "D:\history of id course\images\rams\rams_t1000_radio_1963.jpg" = "https://upload.wikimedia.org/wikipedia/commons/1/10/Braun_T-1000_radio.jpg"
}

foreach ($path in $images.Keys) {
    try {
        Invoke-WebRequest -Uri $images[$path] -OutFile $path -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        Write-Host "Downloaded: $path" -ForegroundColor Green
    } catch {
        Write-Host "Failed to download $path : $_" -ForegroundColor Red
    }
}

# Fetch TP1 page
try {
    $tp1Url = "https://en.wikipedia.org/wiki/Braun_TP_1"
    $page = Invoke-WebRequest -Uri $tp1Url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -UseBasicParsing
    
    # Extract images (basic grep)
    $images = $page.Images | Select-Object -ExpandProperty src
    $tp1Image = $images | Where-Object { $_ -match "Braun_TP_1" -or $_ -match "TP1" } | Select-Object -First 1
    
    if ($tp1Image) {
        if ($tp1Image -notmatch "^http") { $tp1Image = "https:" + $tp1Image }
        Write-Host "Found TP1 Image: $tp1Image" -ForegroundColor Cyan
        
        # Download TP1
        $tp1Path = "D:\history of id course\images\rams\rams_tp1_radio_1959.jpg"
        Invoke-WebRequest -Uri $tp1Image -OutFile $tp1Path -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        Write-Host "Downloaded TP1: $tp1Path" -ForegroundColor Green
    } else {
        Write-Host "No specific TP1 image found in Wikipedia page images" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error fetching TP1 page: $_" -ForegroundColor Red
}
