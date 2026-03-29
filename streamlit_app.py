import streamlit as st
import random

# --- Configuration ---
CLICK_SOUND_URL = "soundreality-ding-411634.mp3"
WIN_SOUND_URL = "universfield-interface-124464.mp3"

# --- Game Logic Functions ---

def flip_symbol(s):
    return 'O' if s == 'X' else 'X'

def press_panel_logic(grid, row, col):
    grid[row][col] = flip_symbol(grid[row][col])
    neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    for r, c in neighbors:
        if 0 <= r < 3 and 0 <= c < 3:
            grid[r][c] = flip_symbol(grid[r][c])

def check_win(grid):
    return all(cell == 'X' for row in grid for cell in row)

def create_initial_grid():
    grid = [['X' for _ in range(3)] for _ in range(3)]
    for _ in range(80):
        r, c = random.randint(0, 2), random.randint(0, 2)
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
    st.session_state.sound_trigger = 0  # Counter to force audio reload

# --- Audio Injection (Main Page Context) ---
# We use st.write with 'unsafe_allow_html=True' to inject JS into the MAIN page,
# bypassing the iframe isolation of st.components.v1.html.

js_code = f"""
<script>
// Preload audio
const clickAudio = new Audio('{CLICK_SOUND_URL}');
const winAudio = new Audio('{WIN_SOUND_URL}');

// Function to play sound
function playSound(audio) {{
    audio.currentTime = 0;
    audio.play().catch(e => console.warn('Audio blocked:', e));
}}

// Listen for clicks on ANY button in the document
document.addEventListener('click', function(e) {{
    // Check if the clicked element is a Streamlit button (usually has class 'stButton' or is a button tag)
    if (e.target.tagName === 'BUTTON' || e.target.closest('.stButton')) {{
        // Check if this is a game button (has a specific key pattern or text)
        // We assume all game buttons are the ones we care about.
        // To be safe, we can check if the button text is 'X' or 'O'
        const btnText = e.target.innerText.trim();
        if (btnText === 'X' || btnText === 'O') {{
            playSound(clickAudio);
        }}
    }}
}}, true); // Use capture phase to catch events early

// Observe for win message
const observer = new MutationObserver(function(mutations) {{
    mutations.forEach(function(mutation) {{
        mutation.addedNodes.forEach(function(node) {{
            if (node.textContent && node.textContent.includes('Congratulations')) {{
                playSound(winAudio);
            }}
        }});
    }});
}});
observer.observe(document.body, {{ childList: true, subtree: true }});
</script>
"""

# Inject the script directly into the page body
st.write(js_code, unsafe_allow_html=True)

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
