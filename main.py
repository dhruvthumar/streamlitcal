import streamlit as st
from datetime import datetime
import calendar
import json
import os

# Set page title
st.title("Dhruv's Calendar App")

# Get current month and year automatically
current_date = datetime.now()
year = current_date.year
month = current_date.month

# Display current month and year as a big heading
month_name = calendar.month_name[month]
st.header(f"{month_name} {year}")

# File to store events
EVENTS_FILE = "events.json"

# Function to load events from the JSON file
def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r") as f:
            return json.load(f)
    return []

# Function to save events to the JSON file
def save_events(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, default=str)

# Load existing events
if "events" not in st.session_state:
    st.session_state.events = load_events()

# Generate the calendar
cal = calendar.monthcalendar(year, month)

# Replace zeroes with empty strings
for week in cal:
    for i in range(len(week)):
        if week[i] == 0:
            week[i] = ""

# Check which dates have events
event_dates = set()
for event in st.session_state.events:
    event_date = datetime.strptime(str(event["date"]), "%Y-%m-%d").date()
    if event_date.year == year and event_date.month == month:
        event_dates.add(event_date.day)

# Custom CSS for the calendar table and layout
calendar_css = """
<style>
.calendar-table {
    width: 100%;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
    margin-right: 20px;  /* Add space between calendar and events */
}
.calendar-table th, .calendar-table td {
    border: 1px solid #ddd;
    text-align: center;
    padding: 1px;  /* Increased padding for more internal space */
    width: 60px;  /* Slightly larger cells */
    height: 50px;  /* Slightly larger cells */
    vertical-align: top;
}
.calendar-table th {
    background-color: #f0f0f0;
    font-weight: bold;
}
.calendar-table td {
    background-color: #fff;
}
.day-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}
.event-dot {
    display: inline-block;
    width: 6px;  /* Slightly larger dot for visibility */
    height: 6px;
    background-color: #FF4B4B;  /* Streamlit's orange-red accent color */
    border-radius: 50%;
    margin-top: 8px;  /* More space between number and dot */
}
.event-section {
    padding-left: 20px;  /* Add space on the left of the event section */
}
.event-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2px 0;  /* Reduced padding to save space */
    margin: 0;  /* Remove any extra margin */
}
.event-item-text {
    flex-grow: 1;  /* Allow the text to take up available space */
    font-size: 14px;  /* Smaller font size to save space */
    margin-right: 10px;  /* Space between text and button */
}
.delete-button {
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 3px 8px;  /* Smaller padding for a more compact button */
    cursor: pointer;
    font-size: 12px;
    line-height: 0.5;  /* Prevent extra vertical space */
}
.delete-button:hover {
    background-color: #e04343;  /* Slightly darker on hover */
}
</style>
"""

# Generate the calendar as an HTML table
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
html = '<table class="calendar-table"><tr>' + ''.join(f'<th>{day}</th>' for day in days) + '</tr>'
for week in cal:
    html += '<tr>'
    for day in week:
        # Check if the day has an event
        has_event = day and day in event_dates
        dot_html = '<div class="event-dot"></div>' if has_event else ''
        html += f'<td><div class="day-container">{day if day else ""}{dot_html}</div></td>'
    html += '</tr>'
html += '</table>'

# Create two columns with more balanced spacing
col1, col2 = st.columns([4, 3])  # Adjusted ratio for better balance

# Calendar in the left column
with col1:
    st.markdown(calendar_css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)

# Events and event management in the right column
with col2:
    # Add a container with padding for the event section
    with st.container():
        st.markdown('<div class="event-section">', unsafe_allow_html=True)
        
        # Event management section
        st.subheader("Add an Event")
        event_date = st.date_input("Event Date", value=current_date)
        event_name = st.text_input("Event Name")

        # Use a single button with a unique key
        if st.button("Save Event", key="save_event_button"):
            if event_name and event_date:
                # Append the new event
                st.session_state.events.append({"name": event_name, "date": event_date})
                # Save to JSON file
                save_events(st.session_state.events)
                st.success(f"Event '{event_name}' saved for {event_date}")
                st.rerun()  # Rerun the app to refresh the calendar and show the dot
            else:
                st.error("Please provide both an event name and date.")

        # Display saved events with delete option
        st.subheader("Saved Events")
        if st.session_state.events:
            for idx, event in enumerate(st.session_state.events):
                with st.container():
                    st.markdown('<div class="event-item">', unsafe_allow_html=True)
                    # Event text
                    st.markdown(
                        f'<div class="event-item-text">{event["date"]}: {event["name"]}</div>',
                        unsafe_allow_html=True
                    )
                    # Delete button
                    if st.button("Delete", key=f"delete_event_{idx}"):
                        # Remove the event from the list
                        st.session_state.events.pop(idx)
                        # Save the updated list to the JSON file
                        save_events(st.session_state.events)
                        # Fixed f-string syntax
                        st.success(f"Event '{event['name']}' deleted.")
                        st.rerun()  # Rerun the app to refresh the UI
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No events saved yet.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Add some vertical spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
