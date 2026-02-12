$urls = @(
    "https://commons.wikimedia.org/wiki/File:1987_Braun_calculator_ET66_by_Dieter_Rams_(13964223413).jpg",
    "https://commons.wikimedia.org/wiki/File:Braun_T-1000_radio.jpg"
)

$results = @{}

foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -UseBasicParsing
        if ($response.Content -match 'href="(https://upload.wikimedia.org/wikipedia/commons/[^"]+)"') {
            $imageUrl = $matches[1]
            $results[$url] = $imageUrl
            Write-Host "Found URL for $url : $imageUrl" -ForegroundColor Green
        } else {
             Write-Host "No image URL found in $url" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "Error fetching $url : $_" -ForegroundColor Red
    }
}

$results | ConvertTo-Json | Set-Content -Path "D:\history of id course\extracted_image_urls.json"
