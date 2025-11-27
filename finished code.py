import streamlit as st
import sqlite3
import pandas as pd
import time # Used for a brief pause after updates

DATABASE_NAME = 'data.db'

# --- 1. DATABASE CONNECTION AND CRUD FUNCTIONS (Your databasetest.py Logic) ---

@st.cache_resource
def get_db_connection():
    """Initializes and returns the SQLite connection object."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row # Allows fetching results as dictionaries
    return conn

def initialize_db(conn):
    """Creates the 'players' table if it does not exist."""
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            kills INTEGER,
            deaths INTEGER
        );
    """)
    conn.commit()

# --- CUD Operations (Create, Update, Delete) ---

def add_player(conn, name, kills, deaths):
    """Inserts a new player record."""
    c = conn.cursor()
    c.execute("INSERT INTO players (name, kills, deaths) VALUES (?, ?, ?)", 
              (name, kills, deaths))
    conn.commit()

def update_player(conn, player_id, name, kills, deaths):
    """Updates an existing player record."""
    c = conn.cursor()
    c.execute("UPDATE players SET name = ?, kills = ?, deaths = ? WHERE id = ?",
              (name, kills, deaths, player_id))
    conn.commit()

def delete_player(conn, player_id):
    """Deletes a player record by ID."""
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()

# --- Read Operation (Data Fetching) ---

# Use st.cache_data to prevent re-querying the database unless explicitly cleared
@st.cache_data(show_spinner="Loading player data...")
def get_all_players(conn):
    """Fetches all player data and returns it as a list of dictionaries."""
    c = conn.cursor()
    c.execute("SELECT id, name, kills, deaths FROM players ORDER BY kills DESC")
    # Convert Row objects to standard dictionaries for easier use
    players = [dict(row) for row in c.fetchall()]
    return players

# --- 2. STREAMLIT APPLICATION SETUP ---

# Initialize the database connection and schema
db_conn = get_db_connection()
initialize_db(db_conn)

# --- Callback Function to force data refresh after CUD operations ---
def set_data_refreshed():
    """Sets a session state flag to signal a data refresh is needed."""
    st.session_state['data_refresh'] = True
    # Clear the cache for the fetching function
    get_all_players.clear()

# Initialize session state for refreshing
if 'data_refresh' not in st.session_state:
    st.session_state['data_refresh'] = False

# --- 3. UI LAYOUT ---

st.set_page_config(layout="wide", page_title="Mini-NEA Player Dashboard")

st.title("Player Statistics Management 🎮")
st.markdown("A Streamlit UI connected directly to your SQLite database code.")

# --- Tabbed Interface for CRUD ---
tab_view, tab_add, tab_update, tab_delete = st.tabs([
    "View Dashboard", 
    "Add New Player", 
    "Update Player Stats", 
    "Delete Player"
])

# --- VIEW DASHBOARD TAB ---
with tab_view:
    st.header("Current Player Roster")
    
    # Check the refresh state and re-fetch if needed
    if st.session_state['data_refresh']:
        st.session_state['data_refresh'] = False # Reset flag
        # The cache is already cleared by set_data_refreshed, so this fetches fresh data
    
    player_data = get_all_players(db_conn)
    
    if player_data:
        df = pd.DataFrame(player_data)
        
        # Calculate statistics
        total_players = len(df)
        total_kills = df['kills'].sum()
        highest_kills = df['kills'].max() if not df.empty else 0
        
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Players", total_players)
        col2.metric("Total Kills", total_kills)
        col3.metric("Highest Kills (Single Player)", highest_kills)
        
        st.subheader("Roster Data Table (Sorted by Kills)")
        # Display the data table
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No players found in the database. Use the 'Add New Player' tab to get started.")

# --- ADD PLAYER TAB ---
with tab_add:
    st.header("Add New Player")
    
    with st.form("add_player_form"):
        name = st.text_input("Player Name", max_chars=50)
        kills = st.number_input("Kills", min_value=0, step=1, value=0)
        deaths = st.number_input("Deaths", min_value=0, step=1, value=0)
        
        submitted = st.form_submit_button("Add Player", on_click=set_data_refreshed)
        
        if submitted:
            if name:
                try:
                    add_player(db_conn, name, kills, deaths)
                    st.success(f"Successfully added player: **{name}**")
                    time.sleep(1) # Pause to let success message display
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding player: {e}")
            else:
                st.warning("Player Name cannot be empty.")

# --- UPDATE PLAYER TAB ---
with tab_update:
    st.header("Update Existing Player Statistics")
    
    current_players = get_all_players(db_conn)
    if not current_players:
        st.info("No players available to update.")
    else:
        # Create a dictionary for mapping: "Name (ID: X)" -> ID
        player_options = {
            f"{p['name']} (ID: {p['id']})": p['id'] 
            for p in current_players
        }
        
        player_selection_label = "Select Player to Update"
        selected_option = st.selectbox(player_selection_label, options=list(player_options.keys()))
        
        if selected_option:
            selected_id = player_options[selected_option]
            
            # Find the selected player's current data
            selected_player = next(p for p in current_players if p['id'] == selected_id)

            with st.form("update_player_form"):
                st.markdown(f"**Updating Stats for: {selected_player['name']}**")
                
                # Pre-fill inputs with current values
                new_name = st.text_input("New Name", value=selected_player['name'], key="update_name")
                new_kills = st.number_input("New Kills", min_value=0, step=1, value=selected_player['kills'], key="update_kills")
                new_deaths = st.number_input("New Deaths", min_value=0, step=1, value=selected_player['deaths'], key="update_deaths")
                
                updated = st.form_submit_button("Apply Update", on_click=set_data_refreshed)
                
                if updated:
                    if new_name:
                        try:
                            update_player(db_conn, selected_id, new_name, new_kills, new_deaths)
                            st.success(f"Successfully updated player ID **{selected_id}** to **{new_name}**")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating player: {e}")
                    else:
                        st.warning("Name cannot be empty.")

# --- DELETE PLAYER TAB ---
with tab_delete:
    st.header("Delete a Player")
    
    current_players = get_all_players(db_conn)
    if not current_players:
        st.info("No players available to delete.")
    else:
        player_options = {
            f"{p['name']} (ID: {p['id']})": p['id'] 
            for p in current_players
        }

        with st.form("delete_player_form"):
            selected_option_delete = st.selectbox(
                "Select Player to Delete (PERMANENT ACTION)", 
                options=list(player_options.keys()),
                key="delete_select"
            )
            
            confirm_delete = st.checkbox(f"I confirm I want to permanently delete {selected_option_delete}")
            
            deleted = st.form_submit_button("Delete Player", on_click=set_data_refreshed)
            
            if deleted:
                if confirm_delete and selected_option_delete:
                    selected_id = player_options[selected_option_delete]
                    try:
                        delete_player(db_conn, selected_id)
                        st.success(f"Successfully deleted player: **{selected_option_delete}**")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting player: {e}")
                else:
                    st.warning("Please confirm deletion before proceeding.")

# --- FINAL CLEANUP ---
# Note: Since we use @st.cache_resource, the connection manages itself.
# We don't need a manual close() here, but you would normally close connections
# in non-Streamlit apps.
