const MOVEMENT_DETAILS = {
    "ac": {
        "title": "Arts & Crafts",
        "dates": "c. 1880–1920",
        "theme": "ac",
        "quote": "Truth to Materials",
        "description": "A direct counter-response to the perceived ugliness and 'soullessness' of mass-produced goods. It championed honest construction, exposed joinery, and the 'Total Work of Art' where architecture and furnishings formed a cohesive whole.",
        "key_features": ["Rejection of the Machine", "Honest Construction", "Nature-inspired Patterns"]
    },
    "an": {
        "title": "Art Nouveau",
        "dates": "c. 1890–1910",
        "theme": "an",
        "quote": "The First International Style",
        "description": "Inspired by nature but stylized into 'whiplash' curves and dynamic, asymmetrical lines. It embraced new materials like iron and glass, seeking to design everything from the building to the spoon inside it.",
        "key_features": ["Organic Abstraction", "Whiplash Curves", "Unity of Art"]
    },
    "ae": {
        "title": "Aesthetic Movement",
        "dates": "c. 1860–1900",
        "theme": "an",
        "quote": "Art for Art's Sake",
        "description": "A movement focused on the creation of 'pure beauty' rather than moral or social messaging. It emphasized sensuality, nature, and the cult of beauty in everyday objects.",
        "key_features": ["Ebonized Wood", "Peacock Feathers", "Japanese Influence"]
    },
    "sm": {
        "title": "Scientific Management",
        "dates": "c. 1910s–1920s",
        "theme": "sm",
        "quote": "Efficiency is Beauty",
        "description": "Driven by Taylorism, this era treated the home and workplace as machines. The goal was to optimize every move for maximum output, leading to the first 'fitted' kitchens and standardized tools.",
        "key_features": ["Frankfurt Kitchen", "Motion Studies", "Standardization"]
    },
    "bh": {
        "title": "The Bauhaus",
        "dates": "1919–1933",
        "theme": "bh",
        "quote": "Form Follows Function",
        "description": "Substituted the 'arbitrary' curves of Art Nouveau with universal geometric shapes. It championed the use of industrial materials like tubular steel and glass in domestic furniture.",
        "key_features": ["Geometric Purity", "Tubular Steel", "Workshop Learning"]
    },
    "modernism": {
        "title": "Modernism",
        "dates": "c. 1920–1960",
        "theme": "modernism", // Custom color in CSS
        "quote": "Less is More",
        "description": "A broad movement encompassing Bauhaus, De Stijl, and International Style. It rejected ornament and embraced minimalism, rationality, and the use of modern industrial materials.",
        "key_features": ["Rejection of Ornament", "Focus on Volume", "Industrial Materials"]
    },
    "ad": {
        "title": "Art Deco & Streamlining",
        "dates": "c. 1925–1939",
        "theme": "ad",
        "quote": "The Style of Speed",
        "description": "Applied the aerodynamics of aircraft to stationary objects to symbolize modernity. It was the birth of the 'Industrial Designer' as a celebrity who could make sales curves go up.",
        "key_features": ["Teardrop Shapes", "Speed Lines", "Chrome & Bakelite"]
    },
    "midcentury": {
        "title": "Mid-Century Modern",
        "dates": "c. 1945–1965",
        "theme": "midcentury",
        "quote": "Good Design is Good Business",
        "description": "A softer, more human version of Modernism. Fueled by post-war technologies like molded plywood and fiberglass, it brought organic curves and color into the American home.",
        "key_features": ["Molded Plywood", "Organic Curves", "Open Floor Plans"]
    },
    "biomorphism": {
        "title": "Biomorphism",
        "dates": "c. 1935–1955",
        "theme": "biomorphism",
        "quote": "Flowing Natural Forms",
        "description": "A design style that models artistic design elements on naturally occurring patterns or shapes reminiscent of nature and living organisms.",
        "key_features": ["Kidney Shapes", "Amoeba Forms", "Soft Edges"]
    },
    "ulm": {
        "title": "Ulm School",
        "dates": "1953–1968",
        "theme": "ulm",
        "quote": "Design is a System",
        "description": "The spiritual successor to the Bauhaus. It moved design towards a scientific, methodological discipline, heavily influencing Braun and the corporate identity of Lufthansa.",
        "key_features": ["Modular Systems", "Matte Finishes", "Extreme Rationalism"]
    },
    "italian_rationalism": {
        "title": "Italian Rationalism",
        "dates": "c. 1960–1980",
        "theme": "sm", // Reusing rationalism color
        "quote": "Tradition and Modernity",
        "description": "A distinct Italian approach that balanced modern manufacturing with a deep respect for history and classic proportions, leading to the sophisticated 'Italian Line' of the 60s.",
        "key_features": ["Elegant Proportions", "Bold Plastics", "Cultural Depth"]
    },
    "minimalism": {
        "title": "Minimalism",
        "dates": "c. 1960–Present",
        "theme": "minimalism",
        "quote": "Less, but Better",
        "description": "stripping a product down to its essential qualities. It avoids decoration and focuses on the purity of form, material, and function.",
        "key_features": ["Simplicity", "Neutral Colors", "Clean Lines"]
    },
    "wedge": {
        "title": "Wedge Era",
        "dates": "c. 1968–1985",
        "theme": "wedge",
        "quote": "The Future is Sharp",
        "description": "Dominated by Italian car design, this era threw out curves for aggressive, sharp angles and flat planes, symbolizing high speed and a break from the past.",
        "key_features": ["Sharp Angles", "Flat Planes", "Aggressive Stance"]
    },
    "pm": {
        "title": "Post-Modernism",
        "dates": "c. 1980–1995",
        "theme": "pm",
        "quote": "Form Follows Fun",
        "description": "A reaction against the 'blandness' of Modernism. Designers embraced color, humor, historical references, and emotion. Function was no longer the only master.",
        "key_features": ["Humor & Kitsch", "Bold Colors", "Historical Pastiche"]
    },
    "mem": {
        "title": "Memphis Group",
        "dates": "1981–1987",
        "theme": "mem",
        "quote": "A New International Style",
        "description": "An Italian design and architecture group founded by Ettore Sottsass. They designed colorful, abstract furniture that looked more like art installations than functional objects.",
        "key_features": ["Clashing Patterns", "Laminate materials", "Totemic shapes"]
    },
    "ht": {
        "title": "High-Tech",
        "dates": "c. 1970–1990",
        "theme": "sm",
        "quote": "The Machine Aesthetic",
        "description": "A style that celebrates the display of the building's or object's technical and functional components, often using industrial materials like steel, glass, and pipework in domestic settings.",
        "key_features": ["Exposed Structure", "Industrial Materials", "Functional Aesthetics"]
    }
};
