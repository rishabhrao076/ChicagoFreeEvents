from bs4 import BeautifulSoup
import requests
import time
import pprint
import llm_query_tool
import db

BASE_URL = "https://do312.com"
EVENT_DATA = []
QUERY = "output format should clean and only be the comma separated values and nothing else. provided the given metadata what semantically unique genres and categories comma separated. Do not give explanation, guesses, numbering, no need for geographic or date information, list 1 to 4 most appropriate categories, no '.etc' in the output:\n{event} "

# event_data = {
#     'date': 'Sep 20',
#     'link': 'https://do312.com/events/2024/9/20/world-music-festival-chicago-tickets',
#     'location': 'City of Chicago',
#     'start_time': '\n               9:00AM\n              \n            ',
#     'title': 'World Music Festival Chicago'
# }

# categories = llm_query_tool.query(QUERY.format(event=str(event_data)))
# categories = llm_query_tool.query("Can you please let us know more details about your ")


# print(categories)
# raise SystemExit


url = BASE_URL+'/free'

def fetch_html(url):
    response = requests.get(url)
    return response.text

def parse_events(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    dates = soup.find_all(class_="ds-events-group")
    events_data = []
    for date_html in dates:
        date = date_html.find_next(class_="ds-list-break-date").text
        events = date_html.find_all(class_="event-card")
        for event_html in events:
            title = event_html.find_next(class_="ds-listing-event-title-text").text
            start_time = event_html.find_next(class_="ds-event-time").text
            location = event_html.find_next(class_="ds-venue-name").find("span", itemprop="name").text
            link = BASE_URL + event_html.find_next("a", itemprop="url").get('href')
            events_data.append({
                'title': title,
                'start_time': start_time,
                'date': date,
                'location': location,
                'link': link
            })
    return events_data

def scrape_events(url):
    html_content = fetch_html(url)
    events_data = parse_events(html_content)
    EVENT_DATA.extend(events_data)
    return get_next_page_link(html_content)

def scrape_all_pages(start_url):
    url = start_url
    while url:
        print("Scraping:", url)
        url = scrape_events(url)

def get_next_page_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    next_page_link = soup.find(class_="ds-paging").find("a",class_="ds-next-page")
    if next_page_link:
        # print(next_page_link.get("href"))
        # time.sleep(5)
        return BASE_URL + next_page_link.get("href")
    else:
        return None

# categorize using AI And store in database.
def add_or_update_events():
    events = db.get_data_from_firebase('/events')
    # print(events)
    for event in EVENT_DATA:      
        
        # Find if the event with the same title already exists
        event_title = event['title']
        if events:
            existing_event = next((e[1] for e in events.items() if e[1]['title'] == event_title), None)
        else:
            existing_event = None
        
        if existing_event:
            # Update existing event
            db.update_data_in_firebase(event, '/events/' + existing_event['id'])
        else:
            # Fetch categories for the current event
            categories = llm_query_tool.query(QUERY.format(event=str(event)))
            # Update the 'categories' key in the event dictionary
            event['tags'] = categories.strip().split(',')
            # Add new event
            db.push_data_to_firebase(event, '/events')

def fetch_categories_from_llm(event):
        # Fetch categories for the current event
    categories = llm_query_tool.query(QUERY.format(event=str(event)))

scrape_all_pages(url)
add_or_update_events()
# print(EVENT_DATA[0])