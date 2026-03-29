import streamlit as st
import random

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

# --- Audio Injection (JavaScript) ---
# We inject JS to handle audio because Streamlit buttons don't natively trigger sound
js_code = f"""
<script>
// Define audio objects
const clickAudio = new Audio('{CLICK_SOUND_FILE}');
const winAudio = new Audio('{WIN_SOUND_FILE}');

// Helper to play sound safely (handles browser autoplay policies)
function playSound(audioObj) {{
    audioObj.currentTime = 0;
    audioObj.play().catch(error => {{
        console.warn('Audio play failed (likely due to browser policy):', error);
    }});
}}

// Listen for ANY click on the page to initialize audio context (browser requirement)
let audioInitialized = false;
document.addEventListener('click', function(e) {{
    if (!audioInitialized) {{
        // Try to play a silent sound or just initialize
        clickAudio.load(); 
        audioInitialized = true;
    }}
    
    // If a button was clicked, play the click sound
    if (e.target.tagName === 'BUTTON') {{
        playSound(clickAudio);
    }}
}}, {{ once: false }});

// Observe DOM for the "Congratulations" message to play win sound
const observer = new MutationObserver(function(mutations) {{
    mutations.forEach(function(mutation) {{
        mutation.addedNodes.forEach(function(node) {{
            if (node.nodeType === 3) {{ // Text node
                if (node.textContent.includes('Congratulations')) {{
                    playSound(winAudio);
                }}
            }} else if (node.textContent && node.textContent.includes('Congratulations')) {{
                playSound(winAudio);
            }}
        }});
    }});
}});

observer.observe(document.body, {{ childList: true, subtree: true }});
</script>
"""

# Inject the script at the top (height 0 to hide iframe)
st.components.v1.html(js_code, height=0)

# --- Game UI ---

# Display the Grid
cols = st.columns(3)
for r in range(3):
    for c in range(3):
        with cols[c]:
            current_val = st.session_state.grid[r][c]
            
            # Button styling: Primary for 'O' (needs flipping), Secondary for 'X'
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
