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
st.title("🔦 Lig
