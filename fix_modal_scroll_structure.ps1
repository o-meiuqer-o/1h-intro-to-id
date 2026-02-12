$path = "D:\history of id course\index.html"
$content = Get-Content $path -Raw

# Helper function to wrap content in v-scrollable-body
function Wrap-Level1($text) {
    # Find active Level 1 blocks
    # Pattern: Look for v-frequency-container closing div, then capture content until v-level-1 closing div
    
    # We use a specific lookahead to ensure we are in a modal
    # But regex on a massive file is tricky.
    # Let's target specific known IDs if possible, or just the class structure.
    
    # Pattern: 
    # (<div class="v-level-1.*?<div class="v-frequency-container">.*?</div>)(.*?)(</div>\s*<!-- LEVEL 2)
    # Group 1: Header parts
    # Group 2: Body parts (to be wrapped)
    # Group 3: Closing of Level 1 and start of Level 2
    
    # DOTALL mode (?s)
    $pattern = '(?s)(<div class="v-level-1[^>]*>.*?<div class="v-frequency-container">.*?</div>\s*)(.*?)(</div>\s*<!-- LEVEL 2)'
    
    $text = [regex]::Replace($text, $pattern, {
        param($match)
        $header = $match.Groups[1].Value
        $body = $match.Groups[2].Value
        $footer = $match.Groups[3].Value
        
        # Check if already wrapped
        if ($body -match 'v-scrollable-body') {
            return $match.Value
        }
        
        return "${header}`n<div class=`"v-scrollable-body`">`n${body}`n</div>`n${footer}"
    })
    
    return $text
}

function Wrap-Level2($text) {
    # Pattern:
    # (<div class="v-level-2">.*?<div class="v-work-hero.*?>.*?</div>\s*)(.*?)(</div>\s*<!--)
    # Note: Level 2 usually ends with closing div then some comment or closing modal-scroll
    
    # Adjust regex for Level 2
    # It starts after v-work-hero (or v-back-btn if hero is inside/outside? In static, back is first, then hero)
    # We assume v-work-hero is the last fixed element.
    
    $pattern = '(?s)(<div class="v-level-2">.*?<div class="v-work-hero.*?>.*?</div>\s*)(.*?)(\s*</div>\s*<!--|\s*</div>\s*</div>)'
    
    $text = [regex]::Replace($text, $pattern, {
        param($match)
        $header = $match.Groups[1].Value
        $body = $match.Groups[2].Value
        $footer = $match.Groups[3].Value
        
        if ($body -match 'v-scrollable-body') {
            return $match.Value
        }
        
        return "${header}`n<div class=`"v-scrollable-body`">`n${body}`n</div>${footer}"
    })
    
    return $text
}

# Execute
Write-Host "Wrapping Level 1..."
$content = Wrap-Level1 $content

Write-Host "Wrapping Level 2..."
$content = Wrap-Level2 $content

Set-Content $path $content -Encoding UTF8
Write-Host "Done."
