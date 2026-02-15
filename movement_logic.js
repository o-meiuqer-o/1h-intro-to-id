/**
 * MOVEMENT LOGIC
 * DETECTS WHICH MOVEMENTS ARE "ON SCREEN" AND SHOWS POPUPS
 */

(function () {
    // STATE
    const activeMovements = {}; // { 'bauhaus': 5, 'modernism': 2 }
    const popupContainer = document.getElementById('movement-popup-container');
    const modal = document.getElementById('movement-modal');

    // CONFIG
    // Minimum number of designers of a movement required on screen to trigger popup
    // (set to 1 for high responsiveness)
    const THRESHOLD = 1;

    // MAP (Copied from populate_data.py for consistency)
    const MOVEMENT_MAP = {
        'arts_and_crafts': 'ac',
        'art_nouveau': 'an',
        'aesthetic': 'an', // aesthetic movement -> art nouveau generally or its own?
        'modernism': 'modernism',
        'bauhaus': 'bh',
        'functionalism': 'sm',
        'rationalism': 'sm', // italian rationalism or scientific management?
        'streamlining': 'ad',
        'midcentury': 'midcentury',
        'biomorphism': 'biomorphism',
        'minimalism': 'minimalism',
        'pop': 'mem',
        'memphis': 'mem',
        'postmodernism': 'pm',
        'high_tech': 'ht',
        'wedge': 'wedge'
    };

    // HELPERS
    function getMovementColor(themeKey) {
        // Map theme keys to hex/gradients or use CSS variable if possible
        // For simplicity, we'll rely on the existing CSS classes .pat-themeKey
        // But for the CHIP background/border, we might want a specific color.
        // Let's extract from the .pat- classes if possible or hardcode some nice defaults
        const colors = {
            'ac': '#8B4513',
            'an': '#2E8B57',
            'bh': '#E6B800',
            'modernism': '#A0CED9',
            'midcentury': '#008080',
            'biomorphism': '#228B22',
            'ulm': '#555555',
            'sm': '#4682B4',
            'ad': '#704214',
            'minimalism': '#1A1A1A',
            'wedge': '#E65100',
            'pm': '#333333',
            'mem': '#D9027D'
        };
        return colors[themeKey] || '#000';
    }

    // OBSERVER SETUP
    const observerOptions = {
        root: null, // viewport
        rootMargin: '-10% 0px -10% 0px', // Shrink hit area to keep it focused on center screen
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        let needsUpdate = false;

        entries.forEach(entry => {
            const bubble = entry.target;

            // Try to get ID from onclick string
            const onClick = bubble.getAttribute('onclick');
            let designerId = null;
            if (onClick) {
                const match = onClick.match(/'([^']+)'/);
                if (match) {
                    designerId = match[1];
                    // Strip 'mod-' prefix if present (e.g., 'mod-aalto' -> 'aalto')
                    if (designerId.startsWith('mod-')) {
                        designerId = designerId.substring(4);
                    }
                }
            }

            if (!designerId || !DESIGNER_META[designerId]) return;

            const designerMoves = DESIGNER_META[designerId].movements;

            if (entry.isIntersecting) {
                // Add movements
                designerMoves.forEach(m => {
                    // Use global map if valid key not found directly
                    // m.name is like "modernism" or "arts_and_crafts"
                    const key = MOVEMENT_MAP[m.name] || m.name;

                    // Normalize to final key used in MOVEMENT_DETAILS
                    let finalKey = null;
                    if (MOVEMENT_DETAILS[key]) finalKey = key;

                    if (finalKey && MOVEMENT_DETAILS[finalKey]) {
                        activeMovements[finalKey] = (activeMovements[finalKey] || 0) + 1;
                        needsUpdate = true;
                    }
                });
            } else {
                // Remove movements
                designerMoves.forEach(m => {
                    const key = MOVEMENT_MAP[m.name] || m.name;

                    let finalKey = null;
                    if (MOVEMENT_DETAILS[key]) finalKey = key;

                    if (finalKey && MOVEMENT_DETAILS[finalKey]) {
                        activeMovements[finalKey] = Math.max(0, (activeMovements[finalKey] || 0) - 1);
                        needsUpdate = true;
                    }
                });
            }
        });

        if (needsUpdate) updatePopupUI();
    }, observerOptions);

    // INIT OBSERVERS
    function init() {
        // Wait for DOM to be ready and bubbles to exist
        // Bubbles might be injected by main script, so we might need to poll or wait
        // checking if bubbles exist now
        const bubbles = document.querySelectorAll('.v-designer-bubble');
        if (bubbles.length > 0) {
            bubbles.forEach(b => observer.observe(b));
            console.log(`[MovementLogic] Observing ${bubbles.length} bubbles.`);
        } else {
            // Retry in 1s (incase dynamic)
            setTimeout(init, 1000);
        }
    }


    // UI RENDERER
    function updatePopupUI() {
        // Clear current (or diff, but clear is easier)
        popupContainer.innerHTML = '';

        // Get active keys
        const keys = Object.keys(activeMovements).filter(k => activeMovements[k] >= THRESHOLD);

        keys.forEach(key => {
            const data = MOVEMENT_DETAILS[key];
            const color = getMovementColor(data.theme);

            const chip = document.createElement('div');
            chip.className = 'movement-chip';
            chip.onclick = () => openModal(key);

            // Animate in
            setTimeout(() => chip.classList.add('active'), 50);

            const dot = document.createElement('div');
            dot.className = 'chip-dot';
            dot.style.backgroundColor = color;

            const text = document.createElement('span');
            text.className = 'chip-text';
            text.innerText = data.title;

            chip.appendChild(dot);
            chip.appendChild(text);
            popupContainer.appendChild(chip);
        });
    }

    // MODAL LOGIC
    function openModal(key) {
        const data = MOVEMENT_DETAILS[key];
        const color = getMovementColor(data.theme);

        document.getElementById('mov-modal-label').innerText = "Design Movement";
        document.getElementById('mov-modal-label').style.color = color;

        document.getElementById('mov-modal-title').innerText = data.title;
        document.getElementById('mov-modal-dates').innerText = data.dates;

        document.getElementById('mov-modal-quote').innerText = `"${data.quote}"`;
        document.getElementById('mov-modal-quote').style.borderLeftColor = color;

        // Helper to parse simple markdown
        function parseMarkdown(text) {
            if (!text) return '';
            // bold
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            // italic
            text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
            return text;
        }

        document.getElementById('mov-modal-desc').innerHTML = parseMarkdown(data.description);

        // New Fields
        document.getElementById('mov-modal-phil').innerHTML = parseMarkdown(data.philosophy || '');
        document.getElementById('mov-modal-impact').innerHTML = parseMarkdown(data.impact || '');
        document.getElementById('mov-modal-context').innerHTML = parseMarkdown(data.sociopolitical_context || '');

        // Features
        const featContainer = document.getElementById('mov-modal-features');
        featContainer.innerHTML = '';
        data.key_features.forEach(f => {
            const pil = document.createElement('span');
            pil.className = 'mov-pill';
            pil.innerHTML = parseMarkdown(f);
            featContainer.appendChild(pil);
        });

        modal.classList.add('active');
    }

    // CLOSE MODAL
    document.querySelector('.close-mov').onclick = () => {
        modal.classList.remove('active');
    };

    // Close on outside click
    modal.onclick = (e) => {
        if (e.target === modal) modal.classList.remove('active');
    }

    // Start
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
