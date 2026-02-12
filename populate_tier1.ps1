# Populate Tier 1 placeholders using `populate_placeholders.ps1`

$scriptPath = "D:\history of id course\populate_placeholders.ps1"

# 3. Jonathan Ive
& $scriptPath -DesignerFolder "ive" -Works @(
    "iPod", "iPad", "Apple Watch", "iMac Pro", "Mac Pro", "AirPods", "Apple Park", "iOS 7", "Power Mac G4 Cube"
)

# 4. Peter Behrens
& $scriptPath -DesignerFolder "behrens" -Works @(
    "AEG Turbine Factory", "AEG Kettle", "AEG Logo", "Typography", "Posters", "AEG Fan", "AEG Clock", "Peter Behrens House", "Hoechst Administration Building"
)

# 5. Walter Gropius
& $scriptPath -DesignerFolder "gropius" -Works @(
    "Portrait", "Harvard Graduate Center", "Gropius House", "Bauhaus Manifesto", "Fagus Factory", "Pan Am Building", "Bauhaus Archive", "MetLife Building", "Chicago Tribune Tower Entry", "Total Theater"
)

# 6. Marcel Breuer
& $scriptPath -DesignerFolder "breuer" -Works @(
    "Whitney Museum", "UNESCO Building", "Breuer House", "Cesca Chair", "Wassily Chair", "Laccio Table", "Isokon Long Chair", "Short Chair", "Murray Lincoln Campus Center", "St John's Abbey Church"
)

# 7. Charles & Ray Eames
& $scriptPath -DesignerFolder "eames" -Works @(
    "LCW", "Lounge Chair", "Molded Plastic Chair", "Eames House", "Hang-It-All", "Aluminum Group", "Wire Chair", "Eames Elephant", "La Chaise", "Powers of Ten"
)

# 8. Raymond Loewy
& $scriptPath -DesignerFolder "loewy" -Works @(
    "Studebaker Starliner", "Coldspot Refrigerator", "Greyhound Bus", "Air Force One Livery", "Coca-Cola Bottle", "Shell Logo", "Exxon Logo", "Pennsylvania Railroad S1", "Lucky Strike Package", "Skylab"
)

# 9. Henry Dreyfuss
& $scriptPath -DesignerFolder "dreyfuss" -Works @(
    "Portrait", "20th Century Limited Train", "Princess Telephone", "Honeywell Thermostat", "John Deere Tractor", "Big Ben Clock", "Trimline Phone", "Western Electric 302", "Polaroid SX-70", "Humanscale"
)

# 10. Arne Jacobsen
& $scriptPath -DesignerFolder "jacobsen" -Works @(
    "Egg Chair", "Swan Chair", "Series 7 Chair", "Ant Chair", "SAS Royal Hotel", "AJ Lamp", "Cylinda Line", "Oxford Chair", "Drop Chair", "Grand Prix Chair"
)
