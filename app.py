import streamlit as st
import db

def filter_events(events, search_query):
    filtered_events = []

    # Check if events is empty
    if not events:
        return filtered_events  # Return empty list

    for event_id, event_data in events.items():
        title = event_data.get('title', '').lower()
        topic = ','.join(event_data.get('tags', [])).lower()
        date = event_data.get('date', '').lower()
        location = event_data.get('location', '').lower() 
        if search_query.lower() in (title + topic + date + location):
            filtered_events.append(event_data)
    return filtered_events

st.title('🎉Chicago Free Events🎉')

text_search = st.text_input("Search by title, topic or date", value="")

events = db.get_data_from_firebase('/events')

filtered_events = filter_events(events,text_search)

# Display filtered events
if filtered_events:
    st.header('Search Results')
    for event in filtered_events:
        st.write('**Title:**', event.get('title', ''))
        st.write('**Date:**', event.get('date', ''))
        st.write('**Location:**', event.get('location', ''))
        st.write('**Tags:**', ', '.join(event.get('tags', [])))
        st.write('**Link:**', event.get('link', ''))
        st.write('---')
else:
    st.write('No events found matching the search criteria.')