# Enrich Gallery Manifest with Bio and Philosophy Data
# This script injects rich text content into gallery_manifest.json
# Uses Here-Strings to avoid quote escaping issues.

$manifestPath = "D:\history of id course\gallery_manifest.json"
$outputPath = "D:\history of id course\gallery_manifest.json"

# Load existing manifest
$data = Get-Content -Path $manifestPath | ConvertFrom-Json

# Define Rich Content Library
$richContent = @{
    "castiglioni" = @{
        bio = @"
Achille Castiglioni was a master of Italian design, known for his playful and ironic approach. Working often with his brother Pier Giacomo, he turned mundane objects into witty, functional art.
"@
        philosophy = @"
His philosophy was 'Design demands observation.' He believed in the 'Ready-made' concept, repurposing existing industrial parts (like tractor seats and car headlights) into new domestic contexts.
"@
        integration = @"
Castiglioni proved that rigor and humor could coexist. His work bridged the gap between the strict rationality of modernism and the expressive freedom of postmodernism.
"@
    }
    "ponti" = @{
        bio = @"
Gio Ponti was the father of modern Italian design. An architect, editor (of Domus), and designer, his career spanned six decades, moving from neoclassical ceramics to the ultra-lightweight Modernism of the Pirelli Tower.
"@
        philosophy = @"
He championed 'The Italian House' - a space of color, light, and ceramic surfaces. He believed architecture should be a crystal: precise, faceted, and transparent.
"@
        integration = @"
Ponti integrated all arts. He designed the building, the cutlery, the toilet, and the magazine that published them. He defined the 'Made in Italy' brand as a fusion of craft and industry.
"@
    }
    "sapper" = @{
        bio = @"
Richard Sapper was a German industrial designer based in Milan, known for combining German precision with Italian flair. He worked for Mercedes, Fiat, and IBM.
"@
        philosophy = @"
He focused on 'Technical Innovation as Aesthetics'. His objects often featured complex engineered movements (like the Tizio lamp counterweights) exposed as visual features.
"@
        integration = @"
Sapper integrated high-tech functionality with sculptural silence. His ThinkPad design defined the 'Black Box' aesthetic of mobile computing for decades.
"@
    }
    "nizzoli" = @{
        bio = @"
Marcello Nizzoli was the chief designer for Olivetti in the 1950s. Originally a painter, he brought a sensual, sculptural quality to office machines.
"@
        philosophy = @"
He believed the machine should be an extension of the body. He softened the hard edges of technology, encasing mechanisms in organic, flowing aluminum shells.
"@
        integration = @"
Nizzoli integrated the artist's hand into mass production. His Lettera 22 wasn't just a typewriter; it was a portable sculpture that made office work feel elegant.
"@
    }
    "gandini" = @{
        bio = @"
Marcello Gandini is the wizard of automotive styling. Working for Bertone, he designed the most radical supercars of the 20th century, including the Lamborghini Miura and Countach.
"@
        philosophy = @"
His philosophy was 'The Wedge'. He rejected the sensual curves of the 60s for sharp, aggressive, geometric lines that looked like they were moving at light speed.
"@
        integration = @"
Gandini integrated aerodynamics with pure drama. He proved that a car's primary function is not just transport, but emotional impact and futuristic projection.
"@
    }
    "giugiaro" = @{
        bio = @"
Giorgetto Giugiaro was named Car Designer of the Century. Founder of Italdesign, he is responsible for the 'Folded Paper' era of car design.
"@
        philosophy = @"
He focused on 'Rational Beauty'. Unlike Gandini's wild concepts, Giugiaro designed for mass production (VW Golf, Fiat Panda), proving that boxy, efficient shapes could be stylish.
"@
        integration = @"
Giugiaro integrated geometry with manufacturing constraints. He made sharpness affordable, defining the visual language of the 1970s and 80s streets.
"@
    }
    "pininfarina" = @{
        bio = @"
Sergio Pininfarina led the famous design house founded by his father. He became synonymous with Ferrari, designing almost every road car for the marque for 50 years.
"@
        philosophy = @"
His philosophy was 'Aerodynamic Elegance'. He believed that speed should look fluid, wind-swept, and organic, reacting to the air rather than cutting it.
"@
        integration = @"
Pininfarina integrated wind tunnel science with sculptural sculpting. His work defined the 'Italian Line' - sensual, red, and fast.
"@
    }
    "earl" = @{
        bio = @"
Harley Earl was the first head of design at General Motors. He invented the 'Concept Car' and brought the principles of Hollywood styling to Detroit.
"@
        philosophy = @"
He believed in 'Planned Obsolescence' and 'Dynamic Obsolescence' - changing the style every year to make the old one look outdated. He pioneered the tailfin and chrome era.
"@
        integration = @"
Earl integrated fashion with engineering. He made the car a status symbol, proving that Americans bought dreams, not just transportation.
"@
    }
    "dyson" = @{
        bio = @"
Sir James Dyson is a British inventor who revolutionized the vacuum cleaner. Frustrated by clogging bags, he applied industrial cyclone technology to home appliances.
"@
        philosophy = @"
His philosophy is 'Form follows Engineering'. He uses transparent plastics to show the dirt and the mechanism, celebrating the 'functional guts' of the machine.
"@
        integration = @"
Dyson integrated heavy industrial engineering into the domestic sphere. He made the vacuum cleaner an object of male desire and status.
"@
    }
    "newson" = @{
        bio = @"
Marc Newson is an Australian designer known for his 'biomorphic' style. He has designed everything from the Apple Watch to airplanes and luxury beds.
"@
        philosophy = @"
He focuses on 'Smoothness'. His objects have no sharp edges; they are continuous, fluid functionality, often looking like they were grown rather than built.
"@
        integration = @"
Newson integrated the luxury world with industrial design. His Lockheed Lounge set auction records, blurring the line between furniture and fine art sculpture.
"@
    }
    "fukasawa" = @{
        bio = @"
Naoto Fukasawa is a Japanese minimalist known for his work with MUJI. He focuses on 'Super Normal' design.
"@
        philosophy = @"
His concept is 'Without Thought'. He designs for the unconscious behavior of humans, creating objects that dissolve into the background of daily life.
"@
        integration = @"
Fukasawa integrated intuition into form. His wall-mounted CD player is pulled like a fan, linking the digital music experience to the analog memory of ventilation.
"@
    }
    "rashid" = @{
        bio = @"
Karim Rashid is the 'Prince of Plastic'. A prolific designer with over 3000 designs, he champions a digital, blobject aesthetic.
"@
        philosophy = @"
He calls for 'Sensual Minimalism'. He rejects the straight lines of modernism for fluid, digital curves and vibrant pinks and cyans that reflect the information age.
"@
        integration = @"
Rashid integrated the digital spline into physical reality. He proved that cheap plastic could be poetic, democratic, and high-design.
"@
    }
    "starck" = @{
        bio = @"
Philippe Starck is a French creator known for his prolific output and subversive humor. He has designed hotels, juicers, yachts, and wind turbines.
"@
        philosophy = @"
His philosophy is 'Democratic Design'. He aims to lower the cost of beauty while increasing its emotional punch. He often subverts function for the sake of drama (Juicy Salif).
"@
        integration = @"
Starck integrated entertainment with utility. He turned the hotel lobby into a theater and the toothbrush into a sculpture, making design a mass-media event.
"@
    }
    "nelson" = @{
        bio = @"
George Nelson was the design director at Herman Miller. He sought to bring structure to the American office and home.
"@
        philosophy = @"
He believed in 'Total Design'. He introduced the concept of the 'family room' and the 'storage wall', organizing post-war clutter with modular logic.
"@
        integration = @"
Nelson integrated European Modernism into American corporate culture. He discovered Eames and Noguchi, curating the 'American Modern' look.
"@
    }
    "aalto" = @{
        bio = @"
Alvar Aalto was a Finnish architect and designer. He humanized modernism by introducing natural materials (wood, brick) and organic curves.
"@
        philosophy = @"
He championed 'Human Modernism'. Unlike the steel/glass of the Bauhaus, Aalto's work was warm, tactile, and bent to fit the human body (Paimio Chair).
"@
        integration = @"
Aalto integrated nature with the machine. His bent-wood experiments proved that industrial standardization could still yield organic, warm results.
"@
    }
    "bellini" = @{
        bio = @"
Mario Bellini is an Italian architect and designer. He designed 35 machines for Olivetti and iconic furniture for B&B Italia.
"@
        philosophy = @"
He focused on the 'Skin' of the object. He treated electronics as soft, anthropomorphic creatures (Divisumma 18) rather than hard boxes.
"@
        integration = @"
Bellini integrated touch and technology. He introduced rubberized, soft-touch interfaces to office machines, predicting the tactile nature of modern devices.
"@
    }
    "sottsass" = @{
        bio = @"
Ettore Sottsass was the grand master of Italian anti-design. Founder of Memphis, he rejected the 'good taste' of functionalism.
"@
        philosophy = @"
He believed design should be 'sensorial'. He used color, pattern, and totem-like forms to create objects that demanded emotional interaction.
"@
        integration = @"
Sottsass integrated spirituality with consumerism. His objects were meant to be present, like characters in a room, rather than silent servants.
"@
    }
    "morris" = @{
        bio = @"
William Morris was a poet, activist, and designer who founded the Arts & Crafts movement. He fought against the soullessness of the Industrial Revolution.
"@
        philosophy = @"
He believed in 'Truth to Materials' and 'Joy in Labor'. He argued that things should be made by happy craftsmen, not factories.
"@
        integration = @"
Morris integrated art with daily life. He proved that a wallpaper or a chair could be a vehicle for moral and social reform.
"@
    }
    "bill" = @{
        bio = @"
Max Bill was a Swiss polymath: architect, artist, painter, and designer. He studied at the Bauhaus and founded the Ulm School of Design.
"@
        philosophy = @"
He championed 'Die Gute Form' (Good Form). He believed design should be based on mathematical laws and absolute economy of means.
"@
        integration = @"
Bill integrated art and geometry. His work proved that the most strictly logical solution was often the most beautiful.
"@
    }
    "behrens" = @{
        bio = @"
Peter Behrens was the first industrial designer. Originally a painter, he became the artistic consultant for AEG in 1907.
"@
        philosophy = @"
He invented 'Corporate Identity'. He designed the factory, the product, and the logo as a single consistent system.
"@
        integration = @"
Behrens integrated art and industry. He paved the way for Modernism by mentoring Gropius, Mies, and Le Corbusier.
"@
    }
    "gropius" = @{
        bio = @"
Walter Gropius founded the Bauhaus. He was an educator who believed in the unification of all arts under the roof of architecture.
"@
        philosophy = @"
He focused on 'Standardization' and 'Teamwork'. He believed the machine was the modern medium of design and should be mastered, not rejected.
"@
        integration = @"
Gropius integrated the guild with the factory. His curriculum defined modern design education: Foundation course first, specialization second.
"@
    }
    "dreyfuss" = @{
        bio = @"
Henry Dreyfuss was the pioneer of ergonomics. He designed for the American telephone system, railways, and John Deere.
"@
        philosophy = @"
He focused on 'Designing for People'. He used anthropometrics (Joe and Josephine) to ensure machines fit the human body.
"@
        integration = @"
Dreyfuss integrated safety with style. His telephone designs defined the communication interface for 50 years.
"@
    }
    "loewy" = @{
        bio = @"
Raymond Loewy was the father of streamlining. He designed everything from locomotives to the Coca-Cola bottle.
"@
        philosophy = @"
He championed 'MAYA' (Most Advanced Yet Acceptable). He believed design was a tool to improve sales by making the future look familiar.
"@
        integration = @"
Loewy integrated psychology with commerce. He proved that aesthetic styling was a vital economic engine.
"@
    }
    "rams" = @{
        bio = @"
Dieter Rams is the head of design at Braun. His '10 Principles of Good Design' are the commandments of minimalism.
"@
        philosophy = @"
He believes in 'Less, but better'. He strips away the non-essential to reveal the pure function of the object.
"@
        integration = @"
Rams integrated strict logic with domestic harmony. His objects are silent but essential, defining the modern appliance.
"@
    }
    "ive" = @{
        bio = @"
Sir Jony Ive was the Chief Design Officer at Apple. He translated Rams' functionalism into the digital age.
"@
        philosophy = @"
He focuses on 'Inevitability'. An object should look like it is the only possible solution to the problem.
"@
        integration = @"
Ive integrated hardware and software. His unibody aluminum designs made the computer feel like a single, solid jewel.
"@
    }
    "eames" = @{
        bio = @"
Charles and Ray Eames were the golden couple of American design. They revolutionized furniture with bent plywood and fiberglass.
"@
        philosophy = @"
They believed in 'The Best for the Most for the Least'. Design should be democratic, playful, and mass-produced.
"@
        integration = @"
The Eameses integrated play with serious production. They proved that mass manufacturing could have a human, whimsical soul.
"@
    }
    "brandt" = @{
        bio = @"
Marianne Brandt was the only woman to lead the Bauhaus Metal workshop. She created some of the most iconic Bauhaus table objects.
"@
        philosophy = @"
She focused on 'Geometric Purity'. Her teapots and lamps were composed of simple spheres, cylinders, and circles.
"@
        integration = @"
Brandt integrated gender equality with industrial mastery. She proved that the harsh environment of the metal shop could yield delicate, perfect forms.
"@
    }
    "guimard" = @{
        bio = @"
Hector Guimard was the leading figure of French Art Nouveau. He is best known for his Paris Metro entrances.
"@
        philosophy = @"
He believed in 'Structural Logic of Nature'. He used iron not as a beam, but as a stalk or a vine, imitating growth.
"@
        integration = @"
Guimard integrated the industrial girder with the botanical curve. He made the subway entrance a portal to a fantasy world.
"@
    }
    "breuer" = @{
        bio = @"
Marcel Breuer was a champion of the Bauhaus furniture workshop. He invented tubular steel furniture, inspired by the handlebars of his bicycle.
"@
        philosophy = @"
He focused on 'Weightlessness'. He wanted furniture to be 'a line in space', sitting on air rather than on heavy legs.
"@
        integration = @"
Breuer integrated industrial materials with domestic comfort. His Wassily and Cesca chairs proved that cold steel could be warm and inviting in the home.
"@
    }
    "geddes" = @{
        bio = @"
Norman Bel Geddes was an American theatrical and industrial designer. He focused on aerodynamics and futuristic concepts, including the 'Futurama' exhibit.
"@
        philosophy = @"
He believed in 'The World of Tomorrow'. He used streamlining not just for speed, but to create a sense of optimism and progress in a depressed economy.
"@
        integration = @"
Geddes integrated theater with industry. His designs were dramatic, stage-managed visions of a frictionless future.
"@
    }
    "jacobsen" = @{
        bio = @"
Arne Jacobsen was a Danish architect and designer. He is the master of 'Danish Modern', blending functionalism with organic forms.
"@
        philosophy = @"
He focused on 'Proportion'. Whether designing a spoon or a skyscraper (SAS Royal Hotel), he insisted on total control of every detail.
"@
        integration = @"
Jacobsen integrated the landscape with the building. His Egg and Swan chairs were organic counterpoints to the rigid grids of his architecture.
"@
    }
    "lihotzky" = @{
        bio = @"
Margarete Schutte-Lihotzky was the first female Austrian architect. She is best known for the Frankfurt Kitchen, the forerunner of all modern fitted kitchens.
"@
        philosophy = @"
She believed in 'Scientific Housekeeping'. She engaged in time-motion studies to optimize the workflow of the domestic laborer (the housewife).
"@
        integration = @"
Lihotzky integrated Taylorism with the home. She treated the kitchen as a factory for nutrition, saving millions of hours of labor for women.
"@
    }
    "wagenfeld" = @{
        bio = @"
Wilhelm Wagenfeld was a German industrial designer and Bauhaus student. He created the 'Bauhaus Lamp' (WA 24), the quintessential object of the movement.
"@
        philosophy = @"
He focused on 'Cheap Beauty'. He believed that everyday objects should be affordable, durable, and beautiful enough for the poor to enjoy.
"@
        integration = @"
Wagenfeld integrated glass and metal with perfect proportion. His work proved that mass-produced goods could have the soul of a handcrafted object.
"@
    }
}

# Update the Manifest
# Get list of properties efficiently
$keys = $data.PSObject.Properties.Name

foreach ($key in $keys) {
    if ($richContent.ContainsKey($key)) {
        # Check if property exists before adding, or remove/re-add
        if ($data.PSObject.Properties[$key].Value.PSObject.Properties["bio"]) {
             # Update if exists? Only if string.
             # Actually, ConvertFrom-Json creates PSCustomObjects.
             # We can add members.
             try {
                $data.$key | Add-Member -MemberType NoteProperty -Name "bio" -Value $richContent[$key].bio -Force
                $data.$key | Add-Member -MemberType NoteProperty -Name "philosophy" -Value $richContent[$key].philosophy -Force
                $data.$key | Add-Member -MemberType NoteProperty -Name "integration" -Value $richContent[$key].integration -Force
             } catch {
                Write-Host "Error updating $key : $_"
             }
        } else {
             $data.$key | Add-Member -MemberType NoteProperty -Name "bio" -Value $richContent[$key].bio -Force
             $data.$key | Add-Member -MemberType NoteProperty -Name "philosophy" -Value $richContent[$key].philosophy -Force
             $data.$key | Add-Member -MemberType NoteProperty -Name "integration" -Value $richContent[$key].integration -Force
        }
    }
}

# Save updated manifest
$data | ConvertTo-Json -Depth 5 | Set-Content -Path $outputPath -Encoding UTF8

Write-Host "Enriched gallery_manifest.json with bio/philosophy data."
