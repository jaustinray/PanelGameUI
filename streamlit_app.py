import streamlit as st
import random
import os

# --- Configuration ---
CLICK_SOUND_FILE = "soundreality-ding-411634.mp3"
WIN_SOUND_FILE = "universfield-interface-124464.mp3"

# --- Game Logic Functions ---

def flip_symbol(s):
    return 'O' if s == 'X' else 'X'

def press_panel_logic(grid, row, col):
    """Flips the clicked cell and its neighbors."""
    grid[row][col] = flip_symbol(grid[row][col])
    
    neighbors = [
        (row - 1, col), (row + 1, col), 
        (row, col - 1), (row, col + 1)
    ]
    
    for r, c in neighbors:
        if 0 <= r < 3 and 0 <= c < 3:
            grid[r][c] = flip_symbol(grid[r][c])

def check_win(grid):
    return all(cell == 'X' for row in grid for cell in row)

def create_initial_grid():
    """Creates a solved grid and scrambles it with 80 random moves."""
    grid = [['X' for _ in range(3)] for _ in range(3)]
    
    for _ in range(80):
        r = random.randint(0, 2)
        c = random.randint(0, 2)
        press_panel_logic(grid, r, c)
        
    return grid

# --- Streamlit App Setup ---

st.set_page_config(page_title="Lights Out", page_icon="🔦")
st.title("🔦 Lights Out Puzzle")
st.markdown("Click tiles to flip them and their neighbors. Goal: Make all tiles **X**.")

# Initialize Session State
if 'grid' not in st.session_state:
    st.session_state.grid = create_initial_grid()
    st.session_state.won = False
    st.session_state.click_count = 0

# --- Audio Handling ---
# We use a trick: serve the audio via a direct URL that bypasses the iframe issue
# by using st.query_params or a direct file path if the server allows.
# However, the most reliable way in Streamlit Cloud/Render is to use st.audio 
# to preload, or rely on the fact that static files in the root are served correctly 
# IF we access them via the main domain, not the iframe srcdoc.

# Let's try a simpler approach: Use st.audio to preload the audio in the background
# This forces the browser to load the file with the correct MIME type from the main page context.
try:
    # Preload sounds (hidden)
    st.audio(CLICK_SOUND_FILE, format='audio/mp3', loop=False)
    st.audio(WIN_SOUND_FILE, format='audio/mp3', loop=False)
except Exception as e:
    st.warning(f"Could not preload audio: {e}. Ensure files are in the root directory.")

# JavaScript to trigger playback
# We use a unique ID to track if we've played sound yet to avoid browser blocking
js_code = """
<script>
let audioContext = null;

function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playSound(url) {
    initAudio();
    const audio = new Audio(url);
    audio.play().catch(e => console.warn('Playback failed:', e));
}

// Listen for clicks on buttons
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'BUTTON') {
        // Play click sound
        const clickUrl = window.location.origin + '/soundreality-ding-411634.mp3';
        playSound(clickUrl);
    }
});

// Observe for win message
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
            if (node.textContent && node.textContent.includes('Congratulations')) {
                const winUrl = window.location.origin + '/universfield-interface-124464.mp3';
                playSound(winUrl);
            }
        });
    });
});
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""

st.components.v1.html(js_code, height=0)

# --- Game UI ---

cols = st.columns(3)
for r in range(3):
    for c in range(3):
        with cols[c]:
            current_val = st.session_state.grid[r][c]
            btn_type = "primary" if current_val == 'O' else "secondary"
            
            if st.button(
                current_val, 
                key=f"{r}_{c}", 
                use_container_width=True,
                type=btn_type
            ):
                if not st.session_state.won:
                    press_panel_logic(st.session_state.grid, r, c)
                    st.session_state.click_count += 1
                    
                    if check_win(st.session_state.grid):
                        st.session_state.won = True
                        st.rerun()

# Win Message
if st.session_state.won:
    st.balloons()
    st.success("🎉 Congratulations! You solved the puzzle!")
    st.write(f"Total moves: {st.session_state.click_count}")
    
    if st.button("Play Again"):
        st.session_state.grid = create_initial_grid()
        st.session_state.won = False
        st.session_state.click_count = 0
        st.rerun()import streamlit as st
import random
import os

# --- Configuration ---
CLICK_SOUND_FILE = "soundreality-ding-411634.mp3"
WIN_SOUND_FILE = "universfield-interface-124464.mp3"

# --- Game Logic Functions ---

def flip_symbol(s):
    return 'O' if s == 'X' else 'X'

def press_panel_logic(grid, row, col):
    """Flips the clicked cell and its neighbors."""
    grid[row][col] = flip_symbol(grid[row][col])
    
    neighbors = [
        (row - 1, col), (row + 1, col), 
        (row, col - 1), (row, col + 1)
    ]
    
    for r, c in neighbors:
        if 0 <= r < 3 and 0 <= c < 3:
            grid[r][c] = flip_symbol(grid[r][c])

def check_win(grid):
    return all(cell == 'X' for row in grid for cell in row)

def create_initial_grid():
    """Creates a solved grid and scrambles it with 80 random moves."""
    grid = [['X' for _ in range(3)] for _ in range(3)]
    
    for _ in range(80):
        r = random.randint(0, 2)
        c = random.randint(0, 2)
        press_panel_logic(grid, r, c)
        
    return grid

# --- Streamlit App Setup ---

st.set_page_config(page_title="Lights Out", page_icon="🔦")
st.title("🔦 Lights Out Puzzle")
st.markdown("Click tiles to flip them and their neighbors. Goal: Make all tiles **X**.")

# Initialize Session State
if 'grid' not in st.session_state:
    st.session_state.grid = create_initial_grid()
    st.session_state.won = False
    st.session_state.click_count = 0

# --- Audio Handling ---
# We use a trick: serve the audio via a direct URL that bypasses the iframe issue
# by using st.query_params or a direct file path if the server allows.
# However, the most reliable way in Streamlit Cloud/Render is to use st.audio 
# to preload, or rely on the fact that static files in the root are served correctly 
# IF we access them via the main domain, not the iframe srcdoc.

# Let's try a simpler approach: Use st.audio to preload the audio in the background
# This forces the browser to load the file with the correct MIME type from the main page context.
try:
    # Preload sounds (hidden)
    st.audio(CLICK_SOUND_FILE, format='audio/mp3', loop=False)
    st.audio(WIN_SOUND_FILE, format='audio/mp3', loop=False)
except Exception as e:
    st.warning(f"Could not preload audio: {e}. Ensure files are in the root directory.")

# JavaScript to trigger playback
# We use a unique ID to track if we've played sound yet to avoid browser blocking
js_code = """
<script>
let audioContext = null;

function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playSound(url) {
    initAudio();
    const audio = new Audio(url);
    audio.play().catch(e => console.warn('Playback failed:', e));
}

// Listen for clicks on buttons
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'BUTTON') {
        // Play click sound
        const clickUrl = window.location.origin + '/soundreality-ding-411634.mp3';
        playSound(clickUrl);
    }
});

// Observe for win message
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
            if (node.textContent && node.textContent.includes('Congratulations')) {
                const winUrl = window.location.origin + '/universfield-interface-124464.mp3';
                playSound(winUrl);
            }
        });
    });
});
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""

st.components.v1.html(js_code, height=0)

# --- Game UI ---

cols = st.columns(3)
for r in range(3):
    for c in range(3):
        with cols[c]:
            current_val = st.session_state.grid[r][c]
            btn_type = "primary" if current_val == 'O' else "secondary"
            
            if st.button(
                current_val, 
                key=f"{r}_{c}", 
                use_container_width=True,
                type=btn_type
            ):
                if not st.session_state.won:
                    press_panel_logic(st.session_state.grid, r, c)
                    st.session_state.click_count += 1
                    
                    if check_win(st.session_state.grid):
                        st.session_state.won = True
                        st.rerun()

# Win Message
if st.session_state.won:
    st.balloons()
    st.success("🎉 Congratulations! You solved the puzzle!")
    st.write(f"Total moves: {st.session_state.click_count}")
    
    if st.button("Play Again"):
        st.session_state.grid = create_initial_grid()
        st.session_state.won = False
        st.session_state.click_count = 0
        st.rerun()
