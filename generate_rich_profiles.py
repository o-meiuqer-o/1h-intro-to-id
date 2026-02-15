
import csv
import os

# Define the rich content dictionary
# Academic tone with 10% playfulness
RICH_PROFILES = {
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
    }
}

CSV_PATH = r"d:\history of id course\expanded_designers_v2.csv"
OUTPUT_CSV_PATH = r"d:\history of id course\expanded_designers_rich.csv" # Create new intermediate file

def update_csv():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    # Read existing CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Check indices
    try:
        key_idx = header.index('designer_key') # Assuming expanded_designers_v2 structure
    except ValueError:
        try:
             # Fallback to rank structure if v1
            key_idx = header.index('Folder')
        except:
            print("Could not verify key column")
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
        # Pad row if existing fields missing (simple robustness)
        while len(row) < len(header):
            row.append("")
            
        key = row[key_idx].lower().strip()
        
        # Prepare rich data
        rich_data = RICH_PROFILES.get(key)
        
        # If we have rich data, append or update it
        # Note: If reusing row, we need to handle if columns already existed
        
        # Create a new row of correct length
        new_row = row + [""] * (len(new_header) - len(row))
        
        if rich_data:
            print(f"Enriching {key}...")
            new_row[bio_idx] = rich_data["Bio"]
            new_row[phil_idx] = rich_data["Philosophy"]
            new_row[int_idx] = rich_data["Integration"]
        
        updated_rows.append(new_row)

    # Write to new CSV
    with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        writer.writerows(updated_rows) # Fixed: writerows instead of writerow
        
    print(f"Success! Written {len(updated_rows)} enriched profiles to {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    update_csv()
