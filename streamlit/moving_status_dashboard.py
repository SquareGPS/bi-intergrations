import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import datetime
import time
import os
from dotenv import load_dotenv
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# Define function to load theme
def load_theme():
    # Check saved theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    return st.session_state.theme

# Page configuration
st.set_page_config(
    page_title="Moving Status Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit/issues',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues/new',
        'About': 'Moving Status Dashboard - Real-time vehicle monitoring'
    }
)

# Get current theme
current_theme = load_theme()

# Theme switcher in sidebar
with st.sidebar:
    st.markdown("### Options")
    if st.button("🌓 " + ("Dark mode" if current_theme == "light" else "Light mode")):
        st.session_state.theme = "dark" if current_theme == "light" else "light"
        st.rerun()

# Set CSS variables based on theme
if current_theme == "light":
    theme_vars = {
        "text-color": "#2c3e50",
        "secondary-text-color": "#7f8c8d",
        "background-color": "white",
        "alternate-bg-color": "#f9f9f9",
        "header-bg-color": "#f8f9fa",
        "border-color": "#e9ecef",
        "hover-color": "#f8f9fa",
        "button-text-color": "#2c3e50",
    }
else:  # dark
    theme_vars = {
        "text-color": "#f1f1f1",
        "secondary-text-color": "#cccccc",
        "background-color": "#262730",
        "alternate-bg-color": "#1E1E1E",
        "header-bg-color": "#333333",
        "border-color": "#555555",
        "hover-color": "#444444",
        "button-text-color": "#f1f1f1",
    }

# Create CSS with variables
css_vars = ":root {\n"
for var, value in theme_vars.items():
    css_vars += f"    --{var}: {value};\n"
css_vars += "}\n"

# Apply CSS variables
st.markdown(f"<style>{css_vars}</style>", unsafe_allow_html=True)

# Apply CSS for theme button
st.markdown("""
<style>
div[data-testid="stButton"] button {
    color: var(--button-text-color) !important;
}
div[data-testid="stDownloadButton"] button {
    color: var(--button-text-color) !important;
}
</style>
""", unsafe_allow_html=True)

# CSS for sticky table header
st.markdown("""
<style>
table {
    border-collapse: collapse;
    width: 100%;
}

table thead {
    position: sticky;
    top: 0;
    background-color: var(--header-bg-color);
    z-index: 10;
    border-bottom: 2px solid var(--border-color);
}

table thead th {
    padding: 8px;
    text-align: left;
    font-weight: bold;
}

table tbody td {
    padding: 6px 8px;
    border-bottom: 1px solid var(--border-color);
}

table tbody tr:nth-child(even) {
    background-color: var(--alternate-bg-color);
}

table tbody tr:hover {
    background-color: var(--hover-color);
}

.sticky-table-container {
    max-height: 600px;
    overflow-y: auto;
    border: 1px solid var(--border-color);
    border-radius: 4px;
}

/* CSS for scrollable device list */
div[data-testid="stVerticalBlock"] > div[data-testid="stFrameContainer"] {
    max-height: 200px;
    overflow-y: auto;
}

/* Styles for Device ID frame */
.device-id-frame {
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: var(--background-color);
}

/* Styles for search */
.search-input {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# Force theme class
st.markdown(f"""
<script>
    document.body.classList.add('{current_theme}');
    document.querySelector('.main').classList.add('{current_theme}');
</script>
""", unsafe_allow_html=True)

# Apply additional themes from CSS file
with open('style.css', encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_database_connection():
    return create_engine(
        f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
    )

# Load data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_current_status():
    query = """
        WITH filtered_tracking_data AS (
        SELECT *
        FROM raw_telematics_data.tracking_data_core
        WHERE device_time > now() - INTERVAL '1 days'
        ),
        latest_tracking AS (
        SELECT DISTINCT ON (device_id)
            device_id,
            device_time,
            event_id,
            speed,
            longitude,
            latitude,
            altitude
        FROM filtered_tracking_data
        WHERE event_id IN (2, 802, 803, 804, 811)
        ORDER BY device_id, device_time DESC
        ),
        latest_positions AS (
        SELECT DISTINCT ON (device_id)
            device_id,
            longitude,
            latitude
        FROM filtered_tracking_data
        ORDER BY device_id, device_time DESC
        ),
        zones_match AS (
        SELECT
            z.zone_label,
            lp.device_id
        FROM raw_business_data.zones z
        JOIN latest_positions lp ON ST_DWithin(
            ST_SetSRID(ST_MakePoint(lp.longitude / 1e7, lp.latitude / 1e7), 4326)::geography,
            ST_SetSRID(ST_MakePoint(z.circle_center_longitude, z.circle_center_latitude), 4326)::geography,
            z.radius
        )
        WHERE z.zone_type = 'circle'
        )

        -- main query:
        SELECT
        o.object_id,
        o.device_id,
        o.object_label,
        e.first_name,
        e.last_name,
        t.device_time,
        t.event_id,
        t.speed / 1e2 AS speed,
        string_agg(DISTINCT zones_match.zone_label, ', ') AS geozones,
        t.longitude / 1e7 AS longitude,
        t.latitude / 1e7 AS latitude,
        t.altitude / 1e7 AS altitude,
        EXTRACT(EPOCH FROM (now() - t.device_time)) AS last_connect,
        TO_CHAR(
            make_interval(secs => EXTRACT(EPOCH FROM (now() - t.device_time))),
            'HH24:MI:SS'
        ) AS last_connect_formatted,
        CASE
            WHEN t.device_time IS NULL THEN 'offline'
            WHEN EXTRACT(EPOCH FROM (now() - t.device_time)) <= 60 THEN 'active'
            WHEN EXTRACT(EPOCH FROM (now() - t.device_time)) <= 300 THEN 'idle'
            ELSE 'offline'
        END AS Connection_status,
        CASE
            WHEN t.device_time IS NULL THEN 'parked'
            WHEN t.speed > 3 AND EXTRACT(EPOCH FROM (now() - t.device_time)) <= 300 THEN 'moving'
            WHEN t.speed <= 3 AND EXTRACT(EPOCH FROM (now() - t.device_time)) <= 300 THEN 'stopped'
            ELSE 'parked'
        END AS moving_status
        FROM raw_business_data.objects AS o
        LEFT JOIN latest_tracking AS t ON o.device_id = t.device_id
        LEFT JOIN raw_business_data.employees AS e ON o.object_id = e.object_id
        LEFT JOIN zones_match ON zones_match.device_id = t.device_id
        GROUP BY
        o.object_id,
        o.device_id,
        o.object_label,
        e.first_name,
        e.last_name,
        t.device_time,
        t.event_id,
        t.speed,
        t.longitude,
        t.latitude,
        t.altitude
        ORDER BY
        t.device_time DESC NULLS LAST
    """
    return pd.read_sql(query, get_database_connection())

# Sidebar with filters
st.sidebar.title("Filters")

# Get data
try:
    df = load_current_status()
    
    # Filters
    moving_statuses = st.sidebar.multiselect(
        "Movement Status",
        options=sorted(df['moving_status'].unique()),
        default=None
    )
    
    connection_statuses = st.sidebar.multiselect(
        "Connection Status",
        options=sorted(df['connection_status'].unique()),
        default=None
    )
    
    # Device ID Filter
    st.sidebar.markdown("### Device ID Filter")
    
    # Initialize device lists in session state
    if 'devices_list' not in st.session_state:
        st.session_state.devices_list = []
        
    if 'selected_devices' not in st.session_state:
        st.session_state.selected_devices = []
    
    # Create device options dictionary
    device_options = {}
    for _, row in df.iterrows():
        device_id = str(row['device_id'])
        label = row['object_label']
        if pd.notna(label):
            device_options[device_id] = f"{label} ({device_id})"
        else:
            device_options[device_id] = device_id
    
    # Update device list if empty or changed
    if not st.session_state.devices_list or set(st.session_state.devices_list) != set(device_options.keys()):
        st.session_state.devices_list = list(device_options.keys())
    
    # Create device filter frame
    with st.sidebar.container():
        st.markdown("<div class='device-id-frame'>", unsafe_allow_html=True)
        
        # Search field
        search_term = st.text_input(
            "Search devices", 
            key="device_search",
            help="Search by device ID or label"
        )
        
        # Filter devices by search term
        if search_term:
            filtered_devices = {k: v for k, v in device_options.items() 
                              if search_term.lower() in v.lower()}
        else:
            filtered_devices = device_options
        
        # Select/Clear buttons
        col1, col2 = st.columns(2)
        
        # Define button click handlers
        def on_select_all():
            st.session_state.selected_devices = list(filtered_devices.keys())
            
        def on_clear_all():
            # Remove all filtered devices from selection
            st.session_state.selected_devices = [d for d in st.session_state.selected_devices 
                                             if d not in filtered_devices.keys()]
        
        # Display buttons with callbacks
        with col1:
            st.button("Select All", key="select_all_devices", on_click=on_select_all)
        with col2:
            st.button("Clear All", key="clear_all_devices", on_click=on_clear_all)

        # Display checkboxes for each device in filtered list
        st.write("Select devices:")
        
        # Create scrollable container for checkboxes
        with st.container(height=200):
            for device_id, label in filtered_devices.items():
                # Get current state
                is_checked = device_id in st.session_state.selected_devices
                
                # Create unique key for checkbox
                checkbox_key = f"device_{device_id}"
                
                # Show checkbox and handle state change
                new_state = st.checkbox(label, value=is_checked, key=checkbox_key)
                
                # Update selected devices based on checkbox state
                if new_state and device_id not in st.session_state.selected_devices:
                    st.session_state.selected_devices.append(device_id)
                elif not new_state and device_id in st.session_state.selected_devices:
                    st.session_state.selected_devices.remove(device_id)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display selected device count
        if st.session_state.selected_devices:
            st.write(f"Selected: {len(st.session_state.selected_devices)} device(s)")
    
    # Apply filters
    if moving_statuses:
        df = df[df['moving_status'].isin(moving_statuses)]
    if connection_statuses:
        df = df[df['connection_status'].isin(connection_statuses)]
    if st.session_state.selected_devices:
        df = df[df['device_id'].astype(str).isin(st.session_state.selected_devices)]
    
    # Top panel
    st.title("Device Movement Dashboard")
    
    # Total objects
    total_objects = len(df['device_id'].unique())
    st.metric("Total devices", total_objects)
    
    # Status headers
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Movement Status")
    with col2:
        st.subheader("Tracker Status")
    
    # Movement stats
    movement_stats = df['moving_status'].value_counts()
    connection_stats = df['connection_status'].value_counts()
    
    # All metrics in one row
    cols = st.columns(6)
    
    # Movement stats
    with cols[0]:
        st.metric("Moving", movement_stats.get('moving', 0))
    with cols[1]:
        st.metric("Stopped", movement_stats.get('stopped', 0))
    with cols[2]:
        st.metric("Parked", movement_stats.get('parked', 0))
    
    # Connection stats
    with cols[3]:
        st.metric("Active", connection_stats.get('active', 0))
    with cols[4]:
        st.metric("Idle", connection_stats.get('idle', 0))
    with cols[5]:
        st.metric("Offline", connection_stats.get('offline', 0))
    
    # Charts in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Convert to DataFrame to avoid warnings
        movement_df = pd.DataFrame({
            'status': movement_stats.index,
            'count': movement_stats.values
        })
        fig1 = px.pie(
            movement_df,
            values='count',
            names='status',
            title="Movement Status Distribution",
            color='status',
            color_discrete_map={
                'moving': '#2ecc71',  # green
                'stopped': '#f1c40f',  # yellow
                'parked': '#95a5a6'    # gray
            }
        )
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Convert to DataFrame to avoid warnings
        connection_df = pd.DataFrame({
            'status': connection_stats.index,
            'count': connection_stats.values
        })
        fig2 = px.pie(
            connection_df,
            values='count',
            names='status',
            title="Connection Status Distribution",
            color='status',
            color_discrete_map={
                'active': '#2ecc71',   # green
                'idle': '#f1c40f',     # yellow
                'offline': '#95a5a6'   # gray
            }
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Current status table and map in two columns
    st.subheader("Current Status")
    
    col_table, col_map = st.columns([1, 1])
    
    with col_table:
        st.subheader("Sheet")
        
        # Get data for table
        display_df = df[[
            'device_id',
            'object_label',
            'first_name',
            'last_name',
            'speed',
            'moving_status',
            'connection_status',
            'last_connect_formatted'
        ]].sort_values('last_connect_formatted')
        
        # Rename columns for display
        display_df.columns = [
            'Device ID',
            'Vehicle',
            'First Name',
            'Last Name',
            'Speed (km/h)',
            'Movement Status',
            'Connection Status',
            'Last Connection'
        ]
        
        # Use HTML table with sticky header
        html = display_df.to_html(index=False, classes="data-table")
        st.markdown(
            f"""
            <div class="sticky-table-container">
                {html}
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_map:
        st.subheader("Location Map")
        
        # Filter rows with valid coordinates
        map_data = df.dropna(subset=['latitude', 'longitude']).copy()
        
        if not map_data.empty:
            # Create color scheme based on movement status
            color_map = {
                'moving': '#2ecc71',  # green
                'stopped': '#f1c40f',  # yellow
                'parked': '#95a5a6'   # gray
            }
            
            # Add information for tooltips
            map_data['hover_info'] = map_data.apply(
                lambda row: f"<b>{row['object_label']}</b><br>" + 
                           f"Device ID: {row['device_id']}<br>" +
                           (f"{row['first_name']} {row['last_name']}<br>" if pd.notna(row['first_name']) else "") +
                           f"Status: {row['moving_status']}<br>" +
                           f"Connection: {row['connection_status']}<br>" +
                           f"Speed: {row['speed']:.1f} km/h<br>" +
                           f"Last update: {row['last_connect_formatted']}" +
                           (f"<br>Geozones: {row['geozones']}" if pd.notna(row['geozones']) else ""),
                axis=1
            )
            
            # Create map with markers
            fig_map = px.scatter_mapbox(
                map_data,
                lat='latitude',
                lon='longitude',
                color='moving_status',
                color_discrete_map=color_map,
                hover_name='object_label',
                hover_data={
                    'latitude': False,
                    'longitude': False,
                    'object_label': False,
                    'moving_status': False,
                    'hover_info': True
                },
                zoom=10,
                height=600
            )
            
            # Configure map style
            fig_map.update_layout(
                mapbox_style="open-street-map",
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(
                    title="Status",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Add custom markers
            for status in color_map:
                status_data = map_data[map_data['moving_status'] == status]
                if not status_data.empty:
                    fig_map.add_trace(
                        go.Scattermapbox(
                            lat=status_data['latitude'],
                            lon=status_data['longitude'],
                            mode='markers',
                            marker=dict(
                                size=12,
                                color=color_map[status],
                                opacity=0.8
                            ),
                            text=status_data['hover_info'],
                            hoverinfo='text',
                            name=status.capitalize()
                        )
                    )
            
            # Display map
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No location data available for the selected devices.")

    # Download full dataset button
    st.download_button(
        label="Download full data",
        data=display_df.to_csv(index=False).encode('utf-8'),
        file_name='moving_status_data.csv',
        mime='text/csv',
    )

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.error("Please check your database connection and try again.")

# Auto-refresh
if st.sidebar.checkbox("Auto-refresh", value=True):
    time.sleep(300)  # Refresh every 5 minutes
    st.rerun() 