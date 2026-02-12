$path = "D:\history of id course\index.html"
$content = Get-Content $path -Raw

# Helper function to wrap content in v-scrollable-body
function Wrap-Level1($text) {
    # LEVEL 1 PATTERN:
    # 1. Start: <div class="v-level-1 active"> ... <div class="v-frequency-container"> ... </div>
    # 2. Content: ... (The stuff we want to wrap)
    # 3. End: </div> <!-- Close .v-level-1 -->
    
    # PROBLEM: Nested divs inside v-frequency-container.
    # SOLUTION: Use the text "INFLUENCE FREQUENCY / ..." as an anchor.
    # The structure is:
    # <div class="v-frequency-container">
    #    ... INFLUENCE FREQUENCY / ... </div>
    # </div>  <-- THIS is where we want to insert <div class="v-scrollable-body">
    
    # Regex:
    # Match from start of v-level-1 active...
    # Through "INFLUENCE FREQUENCY / ..."
    # Through the NEXT closing div </div> (which closes the container)
    # Capture everything after that until the closing </div> of v-level-1
    
    # Let's target the Insertion Point more surgically.
    # Find: (INFLUENCE FREQUENCY / [^<]*</div>\s*</div>)(\s*)
    # Replace: $1$2<div class="v-scrollable-body">
    
    # Find closing of Level 1: (</div>\s*<!-- LEVEL 2)
    # Replace: </div>$1
    # BUT this is risky if there are other closing divs.
    
    # Better Approach: Match the whole block.
    # The block ends with "<!-- LEVEL 2" usually.
    
    $pattern = '(?s)(<div class="v-level-1[^>]*>.*?INFLUENCE FREQUENCY.*?</div>\s*</div>)(\s*)(.*?)(</div>\s*<!-- LEVEL 2)'
    
    $text = [regex]::Replace($text, $pattern, {
        param($match)
        $header = $match.Groups[1].Value
        $space = $match.Groups[2].Value
        $body = $match.Groups[3].Value
        $footer = $match.Groups[4].Value
        
        # Check if already wrapped
        if ($body -match 'v-scrollable-body') {
            return $match.Value
        }
        
        return "${header}${space}<div class=`"v-scrollable-body`">`n${body}`n</div>`n${footer}"
    })
    
    return $text
}

function Wrap-Level2($text) {
    # LEVEL 2 PATTERN:
    # 1. Start: <div class="v-level-2"> ... <div class="v-work-hero ..."> ... </div>
    # 2. Content: The stuff to wrap
    # 3. End: </div> <!-- LEVEL 2 close -->
    
    # Anchor: v-work-hero usually contains "HD IMAGE PLACEHOLDER" or just class="v-work-hero"
    # Wait, dynamic ones have id="rams-work-hero".
    # And they contain "HD IMAGE PLACEHOLDER" inside a div inside the hero.
    
    # Structure:
    # <div class="v-work-hero ...">
    #    <div ...> HD IMAGE PLACEHOLDER </div>
    # </div> <-- Insert here
    
    # Regex:
    # Match <div class="v-level-2">
    # Match content until <div class="v-work-hero
    # Match content until "HD IMAGE PLACEHOLDER"
    # Match until next </div> (closes placeholder text div)
    # Match until next </div> (closes work-hero div)
    
    # OR simpler: Match (<div class="v-work-hero.*?</div>\s*</div>)(\s*)
    # Wait, does work-hero have 2 closing divs?
    # No, work-hero is one div. Inside it is one div with text.
    # So: <div class="v-work-hero"> <div>text</div> </div>
    
    $pattern = '(?s)(<div class="v-level-2">.*?<div class="v-work-hero.*?</div>\s*</div>)(\s*)(.*?)(\s*</div>\s*<!--|\s*</div>\s*</div>\s*<div id=")'
    
    $text = [regex]::Replace($text, $pattern, {
        param($match)
        $header = $match.Groups[1].Value
        $space = $match.Groups[2].Value
        $body = $match.Groups[3].Value
        $footer = $match.Groups[4].Value
        
        if ($body -match 'v-scrollable-body') {
            return $match.Value
        }
        
        return "${header}${space}<div class=`"v-scrollable-body`">`n${body}`n</div>${footer}"
    })
    
    return $text
}

Write-Host "Wrapping Level 1..."
$content = Wrap-Level1 $content

Write-Host "Wrapping Level 2..."
$content = Wrap-Level2 $content

Set-Content $path $content -Encoding UTF8
Write-Host "Done."
