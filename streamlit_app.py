import streamlit as st
import random

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

# Initialize Session State (persists across reruns)
if 'grid' not in st.session_state:
    st.session_state.grid = create_initial_grid()
    st.session_state.won = False

# Handle button clicks using a callback approach
def handle_press(row, col):
    if not st.session_state.won:
        press_panel_logic(st.session_state.grid, row, col)
        
        if check_win(st.session_state.grid):
            st.session_state.won = True

# Display the Grid
cols = st.columns(3)
for r in range(3):
    for c in range(3):
        with cols[c]:
            current_val = st.session_state.grid[r][c]
            
            # Use on_click callback to ensure proper state update
            if st.button(
                current_val, 
                key=f"{r}_{c}", 
                use_container_width=True,
                type="primary" if current_val == 'O' else "secondary"
            ):
                handle_press(r, c)
                st.rerun()  # Force immediate rerun after click

# Win Message
if st.session_state.won:
    st.balloons()
    st.success("🎉 Congratulations! You solved the puzzle!")
    
    if st.button("Play Again"):
        st.session_state.grid = create_initial_grid()
        st.session_state.won = False
        st.rerun()
