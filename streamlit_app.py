import streamlit as st
import random

# --- Constants ---
CLICK_SOUND = "soundreality-ding-411634.mp3"
WIN_SOUND = "universfield-interface-124464.mp3"

# --- Game Logic ---

def flip_symbol(symbol: str) -> str:
    return "O" if symbol == "X" else "X"

def press_panel(grid: list[list[str]], row: int, col: int) -> None:
    grid[row][col] = flip_symbol(grid[row][col])
    neighbors = [
        (row - 1, col), (row + 1, col),
        (row, col - 1), (row, col + 1)
    ]
    for r, c in neighbors:
        if 0 <= r < 3 and 0 <= c < 3:
            grid[r][c] = flip_symbol(grid[r][c])

def check_win(grid: list[list[str]]) -> bool:
    return all(cell == "X" for row in grid for cell in row)

def create_scrambled_grid() -> list[list[str]]:
    grid = [["X" for _ in range(3)] for _ in range(3)]
    for _ in range(80):
        r, c = random.randint(0, 2), random.randint(0, 2)
        press_panel(grid, r, c)
    return grid

# --- Audio Injection (Optimized) ---
# We use a unique ID to ensure we don't duplicate observers if the script re-runs
SCRIPT_ID = "lights-out-audio-script"

AUDIO_SCRIPT = f"""
<script>
// Prevent duplicate initialization
if (document.getElementById('{SCRIPT_ID}')) {{
    console.log('Audio script already loaded');
    return;
}}

const clickAudio = new Audio('{CLICK_SOUND}');
const winAudio = new Audio('{WIN_SOUND}');

function playSound(audio) {{
    audio.currentTime = 0;
    audio.play().catch(() => {{}});
}}

// Use a flag to prevent multiple observers
let observerAttached = false;

document.addEventListener('click', (e) => {{
    if (e.target.tagName === 'BUTTON') {{
        const text = e.target.innerText.trim();
        if (text === 'X' || text === 'O') {{
            playSound(clickAudio);
        }}
    }}
}}, true);

// Attach observer only once
if (!observerAttached) {{
    const observer = new MutationObserver((mutations) => {{
        mutations.forEach(m => m.addedNodes.forEach(n => {{
            if (n.textContent && n.textContent.includes('Congratulations')) {{
                playSound(winAudio);
            }}
        }}));
    }});
    observer.observe(document.body, {{ childList: true, subtree: true }});
    observerAttached = true;
}}

// Mark script as loaded
const marker = document.createElement('div');
marker.id = '{SCRIPT_ID}';
marker.style.display = 'none';
document.body.appendChild(marker);
</script>
"""

# --- App Layout ---

st.set_page_config(page_title="Lights Out", page_icon="🔦")
st.title("🔦 Lights Out Puzzle")
st.markdown("Click tiles to flip them and neighbors. Goal: Make all tiles **X**.")

# Initialize State
if 'grid' not in st.session_state:
    st.session_state.grid = create_scrambled_grid()
    st.session_state.won = False
    st.session_state.moves = 0

# Inject Audio Script (Only runs once effectively due to ID check in JS)
st.write(AUDIO_SCRIPT, unsafe_allow_html=True)

# Render Grid
cols = st.columns(3)
for r in range(3):
    for c in range(3):
        with cols[c]:
            val = st.session_state.grid[r][c]
            btn_type = "primary" if val == "O" else "secondary"
            
            # The key is unique per cell, ensuring Streamlit tracks state correctly
            if st.button(val, key=f"{r}_{c}", use_container_width=True, type=btn_type):
                if not st.session_state.won:
                    press_panel(st.session_state.grid, r, c)
                    st.session_state.moves += 1
                    if check_win(st.session_state.grid):
                        st.session_state.won = True
                        st.rerun()

# Win Screen
if st.session_state.won:
    st.balloons()
    st.success("🎉 Congratulations! You solved the puzzle!")
    st.write(f"Total moves: {st.session_state.moves}")
    
    if st.button("Play Again"):
        st.session_state.grid = create_scrambled_grid()
        st.session_state.won = False
        st.session_state.moves = 0
        st.rerun()
