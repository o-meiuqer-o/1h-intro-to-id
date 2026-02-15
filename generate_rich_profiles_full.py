
import csv
import os

# FULL ACADEMIC + PLAYFUL PROFILES (33 Designers)
RICH_PROFILES = {
    # --- BATCH 1 (Already done, included for completeness) ---
    "dresser": {
        "Bio": "Dr. Christopher Dresser (1834–1904) was a Victorian design radical disguised as a botanist. A graduate of the Government School of Design, he earned a doctorate in botany from the University of Jena, a background that fundamentally structured his design approach. Unlike his contemporary William Morris, who looked backward to medieval guilds, Dresser embraced the industrial machine. He was the first European designer to visit Japan (1876) as an official guest of the Emperor, a journey that revolutionized his understanding of form and void. He acted as an 'art advisor' to over 50 manufacturers, effectively inventing the role of the consultant industrial designer before the term existed.",
        "Philosophy": "Dresser's philosophy was rooted in **'Scientific Botany'** and **'Truth to Materials'**. He believed that ornament should not disguise the construction but articulate it. Influenced by Owen Jones's *The Grammar of Ornament*, Dresser argued that natural forms should be geometricized—flattened and abstracted—to suit the medium of production. His maxim was that design is not art, but a regulated science. He detested the 'sham' of painting wood to look like marble, insisting that a teapot should look like a vessel for pouring, not a Rococo sculpture. He was a functionalist in a velvet frock coat.",
        "Integration": "Dresser's integration of **Botany and Industry** was unprecedented. He applied the structural logic of plant stems to metal toast racks, creating objects that were structurally rigid yet visually lightweight. His Electroplate designs for James Dixon & Sons (circa 1880) are startlingly modern, anticipating the Bauhaus by half a century. He proved that mass production could yield high art, democratizing 'Good Design' for the burgeoning middle class. His work stands as the bridge between the decorative excesses of the Victorian era and the clean lines of Modernism."
    },
    "behrens": {
        "Bio": "Peter Behrens (1868–1940) is the formidable 'Godfather' of German Modernism. Originally a painter and a founding member of the Munich Secession, he pivoted to architecture and design with a singular, totalizing vision. In 1907, he was appointed artistic consultant to AEG (Allgemeine Elektricitäts-Gesellschaft), becoming the world's first corporate designer. His studio was the crucible of the 20th century: Walter Gropius, Ludwig Mies van der Rohe, and Le Corbusier all worked under him simultaneously, presumably terrified by his imposing mustache and rigorous standards.",
        "Philosophy": "Behrens championed the **'Gesamtkunstwerk'** (Total Work of Art) within an industrial context. He rejected the 19th-century habit of masking factories as gothic castles, arguing instead for **'Sachlichkeit'** (objectivity/simplicity). He believed that the rhythm of the machine should dictate the form of the object. For Behrens, a turbine factory was a temple of labor, and a tea kettle was a piece of domestic architecture. He sought to tame the chaos of the industrial age through geometry and classical proportion.",
        "Integration": "Behrens invented **Corporate Identity**. For AEG, he designed everything: the massive turbine factory, the electric fans, the Arc lamps, the letterhead, and the logo itself. This was a radical integration of architecture, graphic design, and product design into a cohesive brand language. He demonstrated that industry wasn't just about efficiency; it was about culture. By giving the machine a dignified form, he civilized the Industrial Revolution and set the stage for the Deutscher Werkbund."
    },
    "loewy": {
        "Bio": "Raymond Loewy (1893–1986), the French-American styling wizard, was the first designer to become a media celebrity. Arriving in New York in 1919 with nothing but a sharp suit and a sharper eye, he transformed the look of mid-century America. He appeared on the cover of *Time* magazine in 1949, surrounded by his creations—locomotives, cars, and packaging. Loewy understood that in the capitalist West, design was effectively a sales tool. He streamlined everything, from pencil sharpeners to the Studebaker Avanti, making the future look fast, shiny, and irresistible.",
        "Philosophy": "Loewy's guiding principle was **MAYA: 'Most Advanced Yet Acceptable'**. He argued that the consumer desires novelty but fears the unfamiliar. The designer's job is to push the envelope just far enough to excite, but not so far as to alienate (the 'shock zone'). He believed in **Streamlining** not just as aerodynamic science, but as a visual metaphor for friction-free progress. To Loewy, a curve was a line of beauty that also happened to reduce drag and increase sales figures.",
        "Integration": "Loewy integrated **Psychology and Engineering**. He took the clunky, exposed machinery of the depression era (like the coldspot refrigerator) and encased it in sleek, white shells. He branded the 'American Dream' itself—designing the livery for Air Force One, the Shell logo, and the Lucky Strike pack. He proved that aesthetic styling was a vital economic engine, successfully merging the role of the artist with that of the marketing executive."
    },
    "dreyfuss": {
        "Bio": "Henry Dreyfuss (1904–1972) was the conscience of American industrial design. Unlike the flamboyant Loewy, Dreyfuss was a pragmatist who wore a suit and carried a tape measure. He opened his office in 1929 and focused on the long-term relationship between the user and the object. He was a man of systems, analyzing the phone system for Bell Labs and the passenger train for New York Central. He wrote *Designing for People* (1955), a seminal text that shifted the focus from styling to usability.",
        "Philosophy": "Dreyfuss pioneered **proto-ergonomics**. He refused to design an object until he understood the anatomy of the user. He created **'Joe' and 'Josephine'**, statistical anthropometric composites of the average American male and female, to ensure his designs fit the human body. His philosophy was that the machine should adapt to the man, not vice versa. If a design required a user to strain their back or squint their eyes, Dreyfuss considered it a failure of design, no matter how beautiful it looked.",
        "Integration": "Dreyfuss integrated **Human Factors** into the design process. His work on the Bell 300 (the classic black rotary phone) is a masterclass in tactile and auditory feedback. He verified the weight of the handset, the angle of the dial, and the sound of the ring. He integrated safety with efficiency, redesigning the John Deere tractor seat to reduce fatigue and the Honeywell thermostat to be readable from across the room. He made the modern world habitable."
    },
    "geddes": {
        "Bio": "Norman Bel Geddes (1893–1958) was a visionary, a showman, and a bit of a megalomaniac. Originally a theatrical set designer, he brought the drama of the stage to the industrial landscape. He visualized a future that didn't exist yet. He is best known for the **Futurama** exhibit at the 1939 New York World's Fair, a massive diorama that predicted the interstate highway system and the car-centric culture of 1960s America. He didn't just design objects; he designed scenarios.",
        "Philosophy": "Geddes believed in **'The World of Tomorrow'**. He was a proponent of **Teardrop Streamlining**, applying aerodynamic principles to cars, trains, and even ocean liners (which looked like giant floating whales). His philosophy was one of optimistic determinism: technology would solve all social ills if we just built bigger, faster roads. He saw design as a tool for social engineering, using spectacle to manufacture consent for a modernist future.",
        "Integration": "Geddes integrated **Speculative Design** with corporate ambition. He worked with General Motors to visualize a friction-free world of speed. His designs were often impractical (like his massive flying wing airliner), but they were incredibly influential as cultural artifacts. He integrated the role of the designer as a prophet, showing the public not what they needed today, but what they would dream of tomorrow."
    },
    "gropius": {
        "Bio": "Walter Gropius (1883–1969) is the founder of the Bauhaus and the great educator of Modernism. He was an architect who saw the catastrophe of World War I as a reason to reboot civilization. In 1919, he merged the Weimar Academy of Fine Art with the School of Arts and Crafts to create the **Bauhaus** ('House of Building'). He assembled a faculty of superstars (Klee, Kandinsky, Breuer) and created a curriculum that is still the blueprint for every design school in the world today.",
        "Philosophy": "Gropius believed in the **'Unity of Art and Technology'**. He rejected the 19th-century schism between the 'high art' of the salon and the 'low craft' of the trades. His philosophy was collaboration: the building was the ultimate aim of all artistic activity. He championed **Standardization** and pre-fabrication, believing that the artist must master the machine to create housing and goods for the masses. He famously stated, 'The ultimate goal of all art is the building.'",
        "Integration": "Gropius integrated the **Guild System** with the **Industrial Factory**. His 'Vorkurs' (Preliminary Course) forced students to unlearn academic traditions and experiment with basic materials and forms. He integrated the curriculum components—color theory, carpentry, metalwork—into a holistic education. He successfully migrated the Bauhaus idea from Germany to Harvard (GSD), effectively defining the International Style that would dominate corporate architecture for decades."
    },
    "breuer": {
        "Bio": "Marcel Breuer (1902–1981) was the quintessential Bauhaus student-turned-master. A Hungarian modernist with a calm demeanor and a revolutionary mind, he transformed the landscape of furniture design before he turned 25. Inspired by the handlebars of his 'Adler' bicycle, he realized that tubular steel could be bent to create strong, lightweight frames. This epiphany led to the **Wassily Chair** (1925), a constructivist skeleton of leather and steel that looked like it belonged in a spaceship rather than a parlor.",
        "Philosophy": "Breuer focused on **'Weightlessness'** and **'Transparency'**. He wanted furniture to be 'a line in space,' dissolving the heavy mass of the traditional armchair. His philosophy was one of continuous structural loops—the cantilever. He believed that modern materials allowed for a separation of 'structure' and 'surface', peeling the upholstery away from the frame to reveal the logic of the object. He later applied this same structural logic to brutalist architecture with concrete.",
        "Integration": "Breuer integrated **Industrial Materials** into the **Domestic Interior**. He brought the cold, hygienic steel of the hospital and the factory into the living room, rendering it warm through impeccable proportion and the use of leather or wicker (Cesca Chair). He integrated the concept of the 'floating' support, effectively retiring the four-legged chair in favor of the S-shaped cantilever that used the tensile strength of steel to provide pneumatic comfort."
    },
    "brandt": {
        "Bio": "Marianne Brandt (1893–1983) was a powerhouse of the Bauhaus Metal Workshop, and eventually its director (one of the few women to achieve such a rank in that male-dominated environment). A painter by training, she attacked metalwork with a geometric rigor that put her male peers to shame. While Gropius preached standardization, Brandt practiced it. Her designs for teapots and ashtrays are among the purest expressions of the Bauhaus aesthetic, fetching record prices at auction today, which is ironic given her socialist intent.",
        "Philosophy": "Brandt's philosophy was **'Geometric Purity'** and **'Functionality'**. She decomposed objects into their primary solid forms—spheres, cylinders, and circles. She avoided all superfluous ornament; the visual interest came from the juxtaposition of materials (ebony wood handles against silver or brass) and the perfection of the form. She anticipated the needs of mass production, designing objects that could be stamped and spun from sheet metal, though initially, they were laboriously hand-crafted.",
        "Integration": "Brandt integrated **Gender Equality** with **Industrial Mastery**. She shattered the glass ceiling of the 'hard' workshops (metal, wood) which women were typically discouraged from entering. She integrated the constructivist art theories of Moholy-Nagy with the practical requirements of the teapot (non-drip spouts, heat-resistant handles). Her lighting fixtures for the Bauhaus building in Dessau demonstrate a seamless integration of adjusting mechanisms and simple shades, defining the artifact as a tool for living."
    },
    "wagenfeld": {
        "Bio": "Wilhelm Wagenfeld (1900–1990) was the ideal Bauhaus student who successfully made the leap to industrial mass production. He is immortalized by the **WA 24** 'Bauhaus Lamp' (1924), a glass and metal table lamp that looks as modern today as it did a century ago. Unlike many of his peers who fled the Nazis, Wagenfeld stayed in Germany, navigating the difficult political landscape to continue working in the glass and porcelain industries, striving to bring good design to the proletariat.",
        "Philosophy": "Wagenfeld championed **'Cheap Beauty'** (billige Schönheit) or **'The Moral Object'**. He believed that everyday household goods—butter dishes, salt shakers, stacking glass containers—should be designed with the same care as luxury items. He rejected the idea that quality was reserved for the rich. His philosophy was 'organic functionality'; his glass containers (Kubus, 1938) were modular, stackable, and transparent, solving the problem of storage and visibility in the modern kitchen.",
        "Integration": "Wagenfeld integrated **Craft Proficiency** with **Industrial Scale**. He worked directly with manufacturers like WMF and Jenaer Glas to optimize designs for the molding process. He proved that standard pressed glass could be refined and elegant. He integrated the 'social responsibility' of the designer into the product, insisting that a well-designed cup made the coffee taste better and the worker's life slightly more dignified."
    },
    "aalto": {
        "Bio": "Alvar Aalto (1898–1976), the Finnish maestro, humanized Modernism. While the Central Europeans (Bauhaus) were bending cold steel, Aalto was bending warm birch wood. He was a nationalist and a humanist, deeply connected to the Finnish landscape of forests and lakes. His architecture and furniture (founded Artek in 1935) were designed as a total physiological experience. He was famously concerned with the 'little man'—the user—ensuring that door handles felt good to the hand and light entered rooms gently.",
        "Philosophy": "Aalto's philosophy was **'Human Modernism'**. He rejected the 'dictatorship of the right angle' and the machine aesthetic. He believed that biology, not geometry, should be the model for design. His 'Paimio Chair' was designed for tuberculosis patients; the angle of the back was calculated to help them breathe. He used **Bent Wood** technology not just for strength, but to create continuous, organic curves that mimicked the natural world. He famously said, 'Form must have a content, and that content is nature.'",
        "Integration": "Aalto integrated **Nature** and **Technology**. He developed a way to bend solid wood (using saw cuts and steam) that allowed it to act like steel, creating the L-leg system which became the standard for millions of stools (Stool 60). He integrated the building into the landscape, and the furniture into the building. His Savoy Vase is an integration of the fluid dynamics of water and the rigidity of glass, a frozen wave that serves a domestic function."
    },
    
    # --- BATCH 2 ---
    "eames": {
        "Bio": "Charles (1907–1978) and Ray Eames (1912–1988) were the dynamic duo of American mid-century design. Operating out of the 'Eames Office' in Venice, California, they approached design as a joyous, collaborative experiment. Charles, the architect, and Ray, the artist, famously finished each other's sentences and sketches. Their work spanned furniture, film, architecture, and toys. They are best known for their pioneering work with molded plywood and fiberglass, creating furniture that was mass-producible, affordable, and incredibly comfortable.",
        "Philosophy": "Their philosophy was **'The Best for the Most for the Least'**. They believed that design was a method of action, not just a result. They famously treated furniture as a 'system' rather than sculpture. Their approach was playful yet rigorous; they would iterate a curve of plywood thousands of times until it perfectly matched the human spine. They embraced the concept of **'Serious Play'**, believing that toys were the prelude to serious ideas.",
        "Integration": "The Eameses integrated **Technology and Whimsy**. They took the wartime technology of molded plywood splints (which they designed for the Navy) and applied it to domestic furniture (the LCW Chair). They integrated film and communication into design education (e.g., 'Powers of Ten'). Their home, Case Study House No. 8, was an integration of off-the-shelf industrial parts into a warm, lived-in space, defining the California lifestyle."
    },
    "rams": {
        "Bio": "Dieter Rams (b. 1932) is the stoic philosopher-king of German design. As the head of design at **Braun** from 1961 to 1995, he oversaw a golden age of consumer electronics. Rams originally trained as an architect, and he brought an architectural stillness to radios, shavers, and calculators. His aesthetic—matte white, geometric, unobtrusive—became the visual language of 'High Fidelity'. He is widely cited as the primary inspiration for Apple's design language under Jony Ive.",
        "Philosophy": "Rams is famous for his **'Ten Principles for Good Design'**, the first of which is 'Good design is innovative.' But the most important is **'Good design is as little design as possible'** (Weniger, aber besser - Less, but better). He hates 'visual pollution' and 'chaos'. He believes objects should be **'Silent Butlers'**—unobtrusive, waiting in the background until needed. He rejects fashion and obsolescence, aiming instead for longevity and timelessness.",
        "Integration": "Rams integrated **Order and Function**. He cleared the clutter of knobs and dials, organizing control surfaces with strict grid logic. He integrated the device into the home environment by making it neutral. His **SK 4 Record Player** (the 'Snow White's Coffin') integrated a clear acrylic lid, turning the mechanics of the turntable into a visible, celebrated element, forever changing how electronics were displayed in the home."
    },
    "nelson": {
        "Bio": "George Nelson (1908–1986) was the articulate intellectual of American Modernism. As the Design Director of **Herman Miller** for over 20 years, he didn't just design furniture; he curated an entire culture. He had a genius for spotting talent, hiring Charles Eames, Isamu Noguchi, and Alexander Girard. A graduate of Yale, Nelson was a writer and editor before he was a designer, and he approached design problems with a narrative clarity. He invented the 'Storage Wall' and the 'Family Room'.",
        "Philosophy": "Nelson believed in **'Total Design'**. He saw the corporate office and the modern home as systems that needed organizing. He argued that 'Design is a response to social change.' His **Marshmallow Sofa** and **Ball Clock** reveal his philosophy that modernism didn't have to be serious; it could be witty and sculptural. He introduced the concept of the **'Action Office'**, the precursor to the cubicle, though he later horrified by what it became.",
        "Integration": "Nelson integrated **European Modernism** with **American Business**. He packaged high-concept design as a viable commercial product. He integrated the atomic age anxiety with atomic age optimism—his clock designs are essentially exploded atoms frozen in time. He proved that a furniture company could be a patron of the arts and a cultural leader, not just a manufacturer of chairs."
    },
    "jacobsen": {
        "Bio": "Arne Jacobsen (1902–1971) was a Danish perfectionist who operated at every scale, from the tea spoon to the skyscraper. Although he considered himself primarily an architect, he is world-famous for his furniture. He was a difficult, demanding master who reportedly fired employees for drawing a line too thick. This obsession with detail resulted in some of the most coherent environments of the 20th century, most notably the SAS Royal Hotel in Copenhagen.",
        "Philosophy": "Jacobsen's philosophy was **'Total Art'** (Gesamtkunstwerk) filtered through **Organic Modernism**. Unlike the geometric Bauhaus, Jacobsen embraced the curve. He focused on **Proportion**. He believed that the landscape, the building, and the furniture should form a single, seamless composition. His **Egg** and **Swan** chairs were designed as organic, sculptural counterpoints to the rigid glass grid of the hotel they sat in.",
        "Integration": "Jacobsen integrated the **Texture of Nature** with the **Precision of Industry**. He pushed the technology of molded foam and upholstery to its limits to create liquid-like forms. He integrated the concept of privacy in public spaces—the high back of the Egg Chair creates a 'room within a room'. His cutlery design for the film '2001: A Space Odyssey' (actually designed earlier) shows his integration of extreme minimalism with functional ergonomics."
    },
    "sapper": {
        "Bio": "Richard Sapper (1932–2015) was a German designer who found his spiritual home in Milan. He combined German engineering precision with Italian flair and chaos. He worked for Mercedes-Benz, Gio Ponti, and IBM. Sapper was a master of the complex mechanism hidden inside a simple shell. He was fascinated by movement and balance. His **Tizio Lamp** (1972) for Artemide remains the best-selling lamp in modern history, a marvel of counterweighted equilibrium.",
        "Philosophy": "Sapper focused on **'Technical Innovation as Aesthetics'**. He didn't just style a box; he reinvented the mechanism. He believed objects should have a 'life'. He famously said, 'I want to make objects that have the intelligence of a machine but the soul of a living thing.' His designs often feature surprise or humor—a kettle that whistles a harmonic chord (Alessi 9091) instead of a shriek.",
        "Integration": "Sapper integrated **Conductivity and Structure**. In the Tizio lamp, the arms *are* the wires, conducting the electricity to the bulb, eliminating cables entirely. He integrated the 'Black Box' aesthetic into the corporate world with the **IBM ThinkPad** (1992). He looked to the Japanese bento box for inspiration, integrating a simple black exterior with a surprise red 'TrackPoint' inside, defining the look of business computing."
    },
    "ponti": {
        "Bio": "Gio Ponti (1891–1979) was the exuberant father figure of 20th-century Italian design. An architect, designer, poet, and the founder of *Domus* magazine, he was a tireless promoter of 'Italianita'. While the rest of Europe was getting colder and more minimal, Ponti was getting lighter and more decorative. He worked until he was 88, designing skyscrapers (Pirelli Tower) and toilets with equal enthusiasm. He was a true Renaissance man who refused to specialize.",
        "Philosophy": "Ponti championed **'The Superleggera'** (Super-lightness). He obsessed over removing weight, both physical and visual. He believed architecture should be a crystal—precise, faceted, and transparent. He rejected the separation of old and new, happily mixing modern geometric forms with classical Italian craft traditions. His philosophy was **'Love implies participation'**; he believed architecture was a stage for life.",
        "Integration": "Ponti integrated **Art, Craft, and Industry**. He revitalized the Italian ceramics industry. His **Superleggera Chain** (1957) is the ultimate integration of traditional Chiavari craftsmanship with modern engineering—it is so light (1.7kg) it can be lifted with a pinky finger, yet strong enough to be thrown out a window (which he did, to test it). He integrated the role of the editor with that of the creator, curating the Italian design identity for half a century."
    },
    "castiglioni": {
        "Bio": "Achille Castiglioni (1918–2002), typically working with his brother Pier Giacomo, was the master of the 'Ready-made'. He was a chain-smoking, joke-telling professor who treated design as a process of problem-solving through observation. He filled his studio with curious objects found on the street. He is famous for the **Arco Lamp** (1962), designed to light a table without hanging from the ceiling, inspired by a street lamp.",
        "Philosophy": "Castiglioni's philosophy was **'Design demands observation'**. He believed in the **'Principal Design Component'**—identifying the core function and stripping away everything else. He was a master of the **'Ready-made'**, repurposing existing industrial parts (tractor seats, car headlights, fishing rods) into new domestic contexts. He rejected 'styling' in favor of 'solution'. He famously said, 'Delete, delete, delete and at the end find the core design.'",
        "Integration": "Castiglioni integrated **Humor and Rigor**. His **Mezzadro Stool** (a tractor seat on a bent steel bar) is a Dadaist joke that is also comfortably functional. He integrated the 'anonymous design' of everyday tools into high-end furniture. He proved that a switch from a vacuum cleaner could be the perfect foot pedal for a lamp, integrating industrial catalogue parts into the domestic landscape with wit and elegance."
    },
    "sottsass": {
        "Bio": "Ettore Sottsass (1917–2007) was the rock star of Italian anti-design. After decades of designing tasteful office machines for Olivetti (like the Valentine typewriter), he rebelled. In 1981, in his 60s, he founded **Memphis**, a design collective that exploded the rules of 'Good Taste'. They used plastic laminate, clashing colors, and animal prints. Sottsass was a spiritual traveler (spending time in India) who saw design as a way to ward off the existential darkness.",
        "Philosophy": "Sottsass believed design should be **'Sensorial'** and **'Ritualistic'**. He rejected Functionalism as a straitjacket. He wanted objects to be 'presences' in the room—totems that demanded attention. He championed **'Bad Taste'** as a way to liberate creativity from the bourgeois constraints of modernism. His **Carlton Bookcase** is less a place to store books and more a statue of a god made of plastic.",
        "Integration": "Sottsass integrated **Spirituality with Consumerism**. He tried to give mass-produced objects the aura of ancient artifacts. He integrated the 'low culture' of suburban diners (Formica patterns) into 'high culture' museum pieces. He fundamentally broke the narrative of Modernism, integrating emotion, memory, and chaos into the clean white room of design history."
    },
    "nizzoli": {
        "Bio": "Marcello Nizzoli (1887–1969) was the man who gave the machine a sex appeal. Originally a painter and poster designer (influenced by Futurism), he became the chief design consultant for Olivetti in the 1930s. He transformed the typewriter and the calculator from clunky mechanical contraptions into smooth, sculptural objects. His **Lettera 22** (1950) is widely considered the most beautiful typewriter ever made.",
        "Philosophy": "Nizzoli believed the machine should be an **'Extension of the Body'**. He softened the hard edges of technology, encasing mechanisms in organic, flowing aluminum shells. His philosophy was **'Sculptural Functionalism'**. He treated the casing not just as a cover, but as a skin. He believed that office work was drudgery, but the tools of office work should be inspiring and beautiful.",
        "Integration": "Nizzoli integrated the **Artist's Hand** into **Mass Production**. He brought a graphical, painterly sensibility to 3D objects. He integrated the mechanism and the casing into a unified whole, hiding the screws and joints. He effectively created the 'biomorphic' look of 1950s technology, integrating the softness of the human form with the precision of the clockwork mechanism."
    },
    "bellini": {
        "Bio": "Mario Bellini (b. 1935) is an Italian architect and design chameleon. He succeeded Nizzoli at Olivetti, designing over 35 machines. He was instrumental in the success of B&B Italia (furniture) and has won 8 Compasso d'Orio awards. Bellini is a thinker who designs 'relationships' rather than just forms. His work ranges from the **Camaleonda** sofa (a modular infinite landscape) to the **Divisumma 18** calculator.",
        "Philosophy": "Bellini focuses on the **'Skin'** of the object. He treated electronics as soft, anthropomorphic creatures. His philosophy is **'The object as a companion'**. He rejected the 'hard box' aesthetic of computers. His Divisumma 18 is covered in a continuous yellow rubber skin with nipples for buttons, asking to be touched. He believes furniture should be a 'dynamic composition', adaptable to the changing needs of the user.",
        "Integration": "Bellini integrated **Touch and Technology**. He introduced rubberized, soft-touch interfaces to office machines, predicting the tactile nature of modern smartphones. He integrated the 'variable geometry' into furniture—his Cab Chair is a steel skeleton wearing a zippered leather suit, integrating structure and upholstery into a single, inseparable entity."
    },
    "giugiaro": {
        "Bio": "Giorgetto Giugiaro (b. 1938) was named 'Car Designer of the Century' in 1999. He founded **Italdesign** and is the father of the 'Folded Paper' aesthetic. While others were designing curves, Giugiaro designed sharp lines and wedges. He is responsible for the **VW Golf Mk1**, the **Fiat Panda**, and the **DeLorean**. He proved that a box could be beautiful.",
        "Philosophy": "Giugiaro focused on **'Rational Beauty'** and **'Packaging'**. Unlike Gandini's wild concepts, Giugiaro designed for mass production. He believed that the primary duty of the car designer was to solve the spatial puzzle of passengers and engine. His philosophy was 'The Line'—a crisp, architectural edge that defined the form. He championed the hatchback as the ultimate democratic vehicle.",
        "Integration": "Giugiaro integrated **Geometry with Manufacturing Constraints**. He made sharpness affordable. He integrated the 'folded paper' look (origami) into steel stamping. He integrated the needs of the factory (flat panels are easier to press) with the desire of the public for a modern look, defining the visual language of the 1970s and 80s streets."
    },
    "gandini": {
        "Bio": "Marcello Gandini (1938–2024) was the wizard of automotive drama. Working for Bertone, he designed the most radical supercars of the 20th century. He gave the world the **Lamborghini Miura** (the first supercar) and the **Lamborghini Countach**. While Giugiaro was rational, Gandini was emotional. He didn't care if you could see out of the rear window; he cared if the car looked like a spaceship landing.",
        "Philosophy": "His philosophy was **'The Wedge'**. He rejected the sensual curves of the 60s for sharp, aggressive, geometric lines that looked like they were moving at light speed even when parked. He believed a sports car should be **'Architecture in Motion'**. He famously invented the 'scissor doors' not just for style, but because the chassis was too wide to open a normal door.",
        "Integration": "Gandini integrated **Aerodynamics with Pure Drama**. He proved that a car's primary function is not just transport, but 'emotional impact' and futuristic projection. He integrated the radical 'cab-forward' layout into reality. His Lancia Stratos integrated the brutality of a rally car with the compact logic of a geometric puzzle."
    },
    "pininfarina": {
        "Bio": "Battista 'Pinin' Farina (1893–1966) founded the legendary design house **Pininfarina**. (His son Sergio continued the legacy). He is synonymous with **Ferrari**, designing almost every road car for the marque for 50 years. He brought the fluidity of the wind into the metal of the car. He was the master of proportion and elegance.",
        "Philosophy": "His philosophy was **'Aerodynamic Elegance'**. He believed that speed should look fluid, wind-swept, and organic, reacting to the air rather than cutting it. He championed the **'Italian Line'**—a sensual, continuous curve that runs from the headlight to the taillight. He believed a car should be a 'sculpture in motion'.",
        "Integration": "Pininfarina integrated **Wind Tunnel Science with Sculptural Art**. He was one of the first to use wind tunnels, but he refused to let the numbers dictate the form entirely. He integrated the technical requirement of cooling intakes into the smile of the grille. His **Cisitalia 202** is the only car in MoMA's permanent collection, integrated as 'rolling sculpture'."
    },
    "earl": {
        "Bio": "Harley Earl (1893–1969), the towering 6'4\" boss of GM's 'Art and Color Section', invented the modern car industry. He was the first to build a clay model of a car. He brought the principles of Hollywood styling (he started building chariots for movies) to Detroit. He gave us the tailfin, the concept car, and the Corvette.",
        "Philosophy": "Earl believed in **'Dynamic Obsolescence'** (planned obsolescence). He argued that by changing the style every year, you could make the old model look outdated, driving new sales. He believed in **'The Longer, Lower, Wider'** aesthetic. To Earl, the car was a dream machine, a status symbol, a rocket ship for the suburbs. He famously said, 'I want to design a car so that you can't tell if it's coming or going.'",
        "Integration": "Earl integrated **Fashion with Engineering**. He employed female designers ('The Damsels of Design') to integrate fashion trends into interior fabrics. He integrated the jet-age iconography (intakes, fins, afterburners) onto the family sedan. He made the car an object of desire and fantasy, effectively integrating the automobile into the psycho-sexual landscape of America."
    },
    "ive": {
        "Bio": "Sir Jony Ive (b. 1967) was the Chief Design Officer at **Apple** (1992–2019) and the spiritual partner of Steve Jobs. He redefined the relationship between humans and technology in the digital age. From the translucent iMac to the iPhone, Ive turned computing into a lifestyle. He is a devotee of Dieter Rams, applying the principles of German functionalism to Silicon Valley technology.",
        "Philosophy": "Ive focuses on **'Inevitability'**. He believes an object should look like it is the 'only possible solution' to the problem. He champions **'Care'**—the idea that even the inside of the computer, which you never see, should be beautiful. He pushes for **'Seamlessness'**—removing screw heads, shut lines, and buttons until the device appears to be a single, magical slab of material (unibody).",
        "Integration": "Ive integrated **Hardware and Material Science**. He pushed manufacturing to impossible limits (milling macbooks from solid aluminum). He integrated the software interface with the physical device (the round corners of the icon matching the round corners of the screen). He integrated the high-tech 'black box' into the world of luxury goods, making the phone a piece of jewelry."
    },
    "dyson": {
        "Bio": "Sir James Dyson (b. 1947) is the British inventor-industrialist who made the vacuum cleaner sexy. Frustrated by a clogging dustbag, he spent 5 years and 5,127 prototypes developing the **Dual Cyclone** technology. He runs his company as an engineering lab. He is a vocal critic of 'style over substance', though his products are undeniably stylish.",
        "Philosophy": "His philosophy is **'Form follows Engineering'**. He uses transparent plastics to show the dirt and the mechanism, celebrating the **'Functional Guts'** of the machine. He believes failure is the key to success. He champions **'Structural Color'**—using bright colors to denote function (red buttons, yellow clips) rather than fashion.",
        "Integration": "Dyson integrated **Heavy Industrial Engineering** into the **Domestic Sphere**. He applied the physics of a sawmill cyclone to a carpet cleaner. He integrated the 'inventor-hero' narrative into the brand. His Airblade and Supersonic hairdryer integrate fluid dynamics motors into ergonomic handles, turning noisy chores into high-tech experiences."
    },
    "starck": {
        "Bio": "Philippe Starck (b. 1949) is the French 'enfant terrible' of design. He is prolific, designing hotels, yachts, wind turbines, and toothbrushes. He famously designed the **Juicy Salif** (lemon squeezer) on a placemat while eating calamari. Starck sees himself not as a designer but as a 'subversive'. He uses design to provoke, amuse, and question.",
        "Philosophy": "Starck champions **'Democratic Design'**. He collaborated with Target to bring high design to the masses. However, he also believes in **'The Stage'**. He argues that function is secondary to emotion. The Juicy Salif doesn't work very well, but it starts conversations. He believes objects should have 'ghosts' or 'humor'. His philosophy is to upgrade the 'service' the object provides to a 'friendship'.",
        "Integration": "Starck integrated **Entertainment with Utility**. He turned the hotel lobby into a theater (Royalton, Delano). He integrated the concept of the 'blobject' with transparency (Ghost Chair). He integrated the surrealism of Dali into mass production, proving that a plastic chair could be a piece of high-status art."
    },
    "newson": {
        "Bio": "Marc Newson (b. 1963) is the Australian globetrotter of 'Biomorphism'. He is one of the most influential designers of his generation. He works with forms that look like they were melted or grown. His **Lockheed Lounge** (a riveted aluminum chaise) set the world record for prices at auction. He has worked for Apple, Qantas, and Louis Vuitton.",
        "Philosophy": "Newson focuses on **'Smoothness'**. His objects have no sharp edges; they are continuous, fluid functionality. He is obsessed with the **'Monocoque'**—the single shell. He looks to the future of the 1960s (retro-futurism) for inspiration. He believes materials should be pushed to their limits to look liquid.",
        "Integration": "Newson integrated the **Luxury World** with **Industrial Design**. He blurred the line between furniture and fine art sculpture. He integrated aerospace technology into furniture. He integrated the 'cool' of surf culture with the precision of Swiss watchmaking (Ikepod). His work integrates the digital spline curve into physical, tactile reality."
    },
    "fukasawa": {
        "Bio": "Naoto Fukasawa (b. 1956) is the master of Japanese minimalism and the driving force behind **MUJI**. He worked in America (IDEO) before returning to Japan. He is famous for his Wall-Mounted CD Player. He observes human behavior to find the natural solutions to problems we didn't know we had.",
        "Philosophy": "His concept is **'Without Thought'** (or Super Normal). He designs for the unconscious behavior of humans. He believes objects should dissolve into the background of daily life. He rejects 'design' that screams for attention. He finds beauty in the ordinary interaction—the way an umbrella handle has a notch to hang a grocery bag.",
        "Integration": "Fukasawa integrated **Intuition into Form**. His CD player is pulled like a kitchen fan, linking the digital music experience to the analog memory of ventilation. He integrated the philosophy of 'Zen' with modern manufacturing. He integrates the object into the 'affordance' of the environment, making things that feel like they have always existed."
    },
    "rashid": {
        "Bio": "Karim Rashid (b. 1960) is the self-proclaimed 'Prince of Plastic'. Dressed always in white or pink, he is a walking brand. He has over 3000 designs in production. He hates the past, nostalgia, and 'rustic' aesthetics. He loves the digital, the artificial, and the synthetic.",
        "Philosophy": "He calls for **'Sensual Minimalism'** or 'Blobjects'. He rejects the straight lines of modernism for fluid, digital curves. He believes in **'Karimanifesto'**—that design is about shaping the future, not repeating history. He champions the use of pink and cyan as the colors of the digital age. He wants to 'soften' the world.",
        "Integration": "Rashid integrated **Digital Tools** into **Physical Reality**. He proved that cheap plastic could be poetic, democratic, and high-design (Garbo trash can). He integrated the 'avatar' personality into the design profession. He integrates the blob aesthetic into everything from radiators to subway stations, creating a seamless, liquid world."
    },
    "lihotzky": {
        "Bio": "Margarete Schutte-Lihotzky (1897–2000) was the first female Austrian architect and a pioneer of social housing. She is best known for the **Frankfurt Kitchen** (1926), the forerunner of every modern fitted kitchen in the world. Working for the city of Frankfurt, she approached the kitchen not as a room, but as a laboratory.",
        "Philosophy": "She believed in **'Scientific Housekeeping'** (Taylorism). She used stopwatch studies to track the movement of housewives, optimizing the kitchen layout to reduce steps and fatigue. She believed that 'housework is work' and deserved the same rational planning as factory work. Her philosophy was deeply political—socialist emancipation through efficiency.",
        "Integration": "Lihotzky integrated **Industrial Efficiency** with the **Domestic Hearth**. She integrated labeled aluminum bins (for flour, sugar) directly into the cabinetry, invention of the 'fitted' concept. She integrated a fold-out ironing board and specific workspaces. She integrated the role of the architect into social reform, saving millions of hours of labor for women, though she ironically barely cooked herself."
    }
}

CSV_PATH = r"d:\history of id course\expanded_designers_v2.csv"
OUTPUT_CSV_PATH = r"d:\history of id course\expanded_designers_rich.csv" # Create new intermediate file

def update_csv():
    # Read existing CSV
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Detect Key Column
    key_idx = -1
    for col in ['designer_key', 'Folder', 'rank']: # Try likely columns
        if col in header:
            key_idx = header.index(col)
            break
            
    if key_idx == -1 and 'Rank' in header: # Fallback for V1
         key_idx = header.index('Folder')

    if key_idx == -1:
        print("Could not find key column")
        return

    # Extend header if needed
    new_header = header.copy()
    if 'Bio' not in new_header:
        new_header.extend(['Bio', 'Philosophy', 'Integration'])
    
    bio_idx = new_header.index('Bio')
    phil_idx = new_header.index('Philosophy')
    int_idx = new_header.index('Integration')

    updated_rows = []
    
    for row in rows:
        # Pad row
        while len(row) < len(new_header):
            row.append("")
            
        key = row[key_idx].lower().strip()
        
        # Look for rich data
        rich_data = RICH_PROFILES.get(key)
        
        if rich_data:
            print(f"Enriching {key}...")
            row[bio_idx] = rich_data["Bio"]
            row[phil_idx] = rich_data["Philosophy"]
            row[int_idx] = rich_data["Integration"]
        
        updated_rows.append(row)

    # Write to new CSV
    with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        writer.writerows(updated_rows)
        
    print(f"Success! Written {len(updated_rows)} enriched profiles to {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    update_csv()
