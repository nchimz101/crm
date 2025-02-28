import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import io
import json
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.card import card
import time
import random
import calendar
import altair as alt
from faker import Faker

# Initialize fake data generator for sample data
fake = Faker()

# Set page configuration
st.set_page_config(
    page_title="Netagrow CRM",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved UI/UX
st.markdown("""
<style>
    .main {
        background-color: #f4f6f9;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .stButton button {
        background-color: #2E7D32;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #388E3C;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        transition: all 0.3s ease;
        border-left: 4px solid #2E7D32;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    .growth-positive {
        color: #2E7D32;
        font-weight: bold;
    }
    .growth-negative {
        color: #C62828;
        font-weight: bold;
    }
    .status-active { 
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .status-pending { 
        background-color: #FFF8E1;
        color: #FF8F00;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .status-completed {
        background-color: #E8EAF6;
        color: #3F51B5;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .status-in-progress {
        background-color: #E0F7FA;
        color: #0097A7;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .status-scheduled {
        background-color: #F3E5F5;
        color: #7B1FA2;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 0.9em;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    th {
        background-color: #2E7D32;
        color: #ffffff;
        text-align: left;
        padding: 12px;
    }
    td {
        padding: 12px;
        border-bottom: 1px solid #dddddd;
    }
    tr:nth-child(even) {
        background-color: #f5f5f5;
    }
    tr:hover {
        background-color: #e0e0e0;
        transition: background-color 0.3s ease;
    }
    .custom-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .custom-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    .form-container {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 20px 0;
    }
    .error-message {
        color: #C62828;
        font-size: 0.9em;
        margin-top: 5px;
    }
    .tooltip {
        position: relative;
        display: inline-block;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #2E7D32;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .export-btn {
        float: right;
        margin: 10px;
    }
    /* Dialog styles */
    .dialog-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        justify-content: center;
        align-items: center;
    }
    .dialog-content {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        max-width: 500px;
        text-align: center;
    }
    .dialog-buttons {
        margin-top: 20px;
    }
    .dialog-buttons button {
        margin: 0 10px;
    }
    
    /* Animation for metric cards */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated {
        animation: fadeIn 0.5s ease-out forwards;
    }
    /* Responsive adjustments */
    @media screen and (max-width: 768px) {
        .metric-card {
            margin-bottom: 10px;
            padding: 10px;
        }
        .custom-card {
            padding: 15px;
        }
    }
    /* Active menu item */
    .active-menu-item {
        font-weight: bold !important;
        color: #2E7D32 !important;
        background-color: #E8F5E9 !important;
    }
</style>

<script>
function showConfirmationDialog(message, confirmAction) {
    document.getElementById('dialog-message').innerText = message;
    document.getElementById('dialog-overlay').style.display = 'flex';
    document.getElementById('confirm-btn').onclick = function() {
        eval(confirmAction);
        document.getElementById('dialog-overlay').style.display = 'none';
    };
    document.getElementById('cancel-btn').onclick = function() {
        document.getElementById('dialog-overlay').style.display = 'none';
    };
}
</script>

<div id="dialog-overlay" class="dialog-overlay">
    <div class="dialog-content">
        <h3>Confirmation</h3>
        <p id="dialog-message"></p>
        <div class="dialog-buttons">
            <button id="confirm-btn" class="btn-confirm">Yes, Confirm</button>
            <button id="cancel-btn" class="btn-cancel">Cancel</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'date_range' not in st.session_state:
    st.session_state.date_range = '6M'  # Default to 6 months
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = {}

# Helper functions
def format_number(number):
    return f"{number:,}"

def format_currency(amount):
    return f"ZMW {amount:,}"

def get_status_class(status):
    status = status.lower()
    if status in ["active", "ongoing"]:
        return "status-active"
    elif status in ["pending", "planned"]:
        return "status-pending"
    elif status == "completed":
        return "status-completed"
    elif status == "in progress":
        return "status-in-progress"
    elif status in ["scheduled", "upcoming"]:
        return "status-scheduled"
    else:
        return ""

# Function to generate trend indicators based on growth data
def get_trend_indicator(value, threshold=0):
    if value > threshold:
        return "↑", "growth-positive"
    elif value < threshold:
        return "↓", "growth-negative"
    else:
        return "→", ""

# Function to export data to CSV
def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv" class="btn btn-primary export-btn">Export to CSV</a>'
    return href

# Modify the export_to_excel function to handle missing openpyxl

def export_to_excel(data, filename):
    try:
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_data = output.getvalue()
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx" class="btn btn-primary export-btn">Export to Excel</a>'
        return href
    except ImportError:
        # Fallback if openpyxl is not available
        st.warning("Excel export requires the 'openpyxl' package. Please install it using: pip install openpyxl")
        return f'<a href="#" onclick="alert(\'Please install openpyxl package to enable Excel export.\'); return false;" class="btn btn-primary export-btn disabled">Export to Excel</a>'

# Form validation function
def validate_form(form_data, form_type):
    errors = {}
    if form_type == "deal":
        if not form_data.get("deal_name"):
            errors["deal_name"] = "Deal name is required"
        if form_data.get("deal_value", 0) <= 0:
            errors["deal_value"] = "Deal value must be greater than 0"
        if not form_data.get("company_name"):
            errors["company_name"] = "Company name is required"
    elif form_type == "contact":
        if not form_data.get("name"):
            errors["name"] = "Name is required"
        if not form_data.get("company"):
            errors["company"] = "Company is required"
        if not form_data.get("email"):
            errors["email"] = "Email is required"
        elif "@" not in form_data.get("email", ""):
            errors["email"] = "Please enter a valid email"
    elif form_type == "task":
        if not form_data.get("task"):
            errors["task"] = "Task description is required"
        if not form_data.get("assignedTo"):
            errors["assignedTo"] = "Assignee is required"
    return errors

# Filter data based on date range
def filter_data_by_date_range(data, date_range):
    # In a real application, you would filter your data based on dates
    # For this demo, we'll just return the data as is
    return data

def generate_forecast_data(historical_data, labels, periods_ahead=3):
    """Generate simple forecast based on historical trend"""
    # Calculate average growth rate
    growth_rates = []
    for i in range(1, len(historical_data)):
        if historical_data[i-1] > 0:  # Avoid division by zero
            growth_rate = (historical_data[i] - historical_data[i-1]) / historical_data[i-1]
            growth_rates.append(growth_rate)
    
    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0.05
    
    # Generate forecast
    last_value = historical_data[-1]
    forecast = []
    forecast_labels = []
    
    # Parse last month and year from the last label
    parts = labels[-1].split()
    month_abbr = parts[0]
    year = int(parts[1])
    
    # Get the month number
    month_to_num = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    month_num = month_to_num.get(month_abbr, 1)
    
    for i in range(periods_ahead):
        # Move to next month
        month_num += 1
        if month_num > 12:
            month_num = 1
            year += 1
        
        # Generate forecast value with some randomness
        forecast_value = last_value * (1 + avg_growth_rate + random.uniform(-0.02, 0.02))
        forecast.append(round(forecast_value, 2))
        
        # Add label
        forecast_labels.append(f"{calendar.month_abbr[month_num]} {year}")
        
        # Update last value for next iteration
        last_value = forecast_value
    
    return forecast, forecast_labels

# Fix the generate_recent_activities function to handle all placeholders properly
def generate_recent_activities(count=10):
    """Generate realistic Zambian activities for demo purposes"""
    zambian_names = [
        "Mwamba Chilufya", "Nkandu Mulenga", "Chanda Mutale", "Bwalya Musonda", 
        "Kalumba Tembo", "Mutinta Hichilema", "Mulenga Kapwepwe", "Chilombo Banda", 
        "Chileshe Bwalya", "Chongo Daka", "Nsofwa Mwale", "Mwila Kanyanta"
    ]
    
    zambian_companies = [
        "Lusaka Agri Solutions", "Copperbelt Farming Ltd", "Luangwa Valley Growers", 
        "Zambezi Agricultural Services", "Kafue Basin Farms", "Southern Province Cooperative", 
        "Muchinga Agritech", "Mkushi Farming Block", "Eastern Zambia Producers", 
        "Northern Agro Dealers", "Kariba Harvest Ltd", "Chongwe Farming Collective"
    ]
    
    zambian_tasks = [
        "Farm visit followup", "Irrigation system proposal", "Seed supply agreement", 
        "Equipment demonstration", "Farmer group training", "Mobile payment setup", 
        "Soil testing consultation", "Harvest planning", "Community outreach", 
        "Loan application assistance"
    ]
    
    zambian_campaigns = [
        "Rainy Season Preparation", "Drought-Resistant Seeds", "Community Farming Initiative", 
        "Agricultural Loans Program", "Women Farmers Support", "Young Farmers Fellowship", 
        "Farm Mechanization Drive", "Sustainable Farming Practices", "Crop Diversification"
    ]
    
    # Define different activity types with their respective required variables
    activity_groups = [
        {
            "templates": [
                "Added new contact: {name}",
                "Added note to {name}'s profile"
            ],
            "requires": ["name"]
        },
        {
            "templates": [
                "Updated deal with {company}",
                "Received payment from {company}",
                "Created support ticket for {company}"
            ],
            "requires": ["company"]
        },
        {
            "templates": [
                "Scheduled meeting with {name} at {company}",
                "Sent proposal to {name} from {company}"
            ],
            "requires": ["name", "company"]
        },
        {
            "templates": [
                "Created task: {task} for {company}",
            ],
            "requires": ["task", "company"]
        },
        {
            "templates": [
                "Completed task: {task} for {name}",
            ],
            "requires": ["task", "name"]
        },
        {
            "templates": [
                "Modified campaign: {campaign}",
            ],
            "requires": ["campaign"]
        }
    ]
    
    activities = []
    now = datetime.now()
    
    for i in range(count):
        # Select a random activity group
        group = random.choice(activity_groups)
        # Select a random activity template from this group
        template = random.choice(group["templates"])
        timestamp = now - timedelta(hours=random.randint(1, 72))
        
        # Prepare the parameters for string formatting based on what's required
        params = {}
        if "name" in group["requires"]:
            params["name"] = random.choice(zambian_names)
        if "company" in group["requires"]:
            params["company"] = random.choice(zambian_companies)
        if "task" in group["requires"]:
            params["task"] = random.choice(zambian_tasks)
        if "campaign" in group["requires"]:
            params["campaign"] = random.choice(zambian_campaigns)
        
        # Format the activity text with the parameters
        activity = template.format(**params)
        
        user = random.choice(["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."])
        
        activities.append({
            "activity": activity,
            "timestamp": timestamp,
            "user": user,
            "timeAgo": get_time_ago(timestamp)
        })
    
    # Sort by most recent first
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return activities

def get_time_ago(timestamp):
    """Convert timestamp to human-readable time ago string without 'd ago' for days"""
    now = datetime.now()
    delta = now - timestamp
    
    if delta.days > 0:
        return f"{delta.days}d" # Removed "ago"
    elif delta.seconds >= 3600:
        return f"{delta.seconds // 3600}h ago"
    elif delta.seconds >= 60:
        return f"{delta.seconds // 60}m ago"
    else:
        return "Just now"

# Update the get_upcoming_tasks_events function to generate fewer, more spread-out events
def get_upcoming_tasks_events(data, days=60):  # Increased days range for better spread
    """Generate upcoming tasks and events with strong Zambian context"""
    upcoming = []
    now = datetime.now()
    
    # Add some real tasks from the data
    for task in data["taskActivityTracking"]["activities"]:
        try:
            due_date = datetime.strptime(task["dueDate"], "%Y-%m-%d")
            if due_date > now:
                upcoming.append({
                    "title": task["task"],
                    "date": due_date,
                    "type": "task",
                    "status": task["status"],
                    "assignedTo": task["assignedTo"]
                })
        except:
            pass
    
    # Zambian-specific contexts
    zambian_companies = [
        "Lusaka Agri Solutions", "Copperbelt Farming Ltd", "Luangwa Valley Growers", 
        "Zambezi Agricultural Services", "Kafue Basin Farms", "Southern Province Cooperative"
    ]
    
    zambian_names = [
        "Mwamba Chilufya", "Nkandu Mulenga", "Chanda Mutale", "Bwalya Musonda",
        "Kalumba Tembo", "Mutinta Hichilema"
    ]
    
    zambian_locations = [
        "Lusaka", "Ndola", "Kitwe", "Livingstone", "Chipata", "Kasama"
    ]
    
    zambian_events = [
        "Meeting with {company} in {location}",
        "Demo for {company} at Agricultural Showgrounds",
        "Call with {name} about smart irrigation systems",
        "Precision farming training in {location}"
    ]
    
    zambian_staff = ["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."]
    
    # Create just 4 events spaced apart in time
    time_intervals = [7, 15, 30, 45]  # Days from now for each event
    
    for i, interval in enumerate(time_intervals):
        event_date = now + timedelta(days=interval)
        event_type = zambian_events[i % len(zambian_events)]
        
        name = zambian_names[i % len(zambian_names)]
        company = zambian_companies[i % len(zambian_companies)]
        location = zambian_locations[i % len(zambian_locations)]
        
        if "{name}" in event_type and "{company}" in event_type and "{location}" in event_type:
            title = event_type.format(name=name, company=company, location=location)
        elif "{name}" in event_type and "{company}" in event_type:
            title = event_type.format(name=name, company=company)
        elif "{name}" in event_type and "{location}" in event_type:
            title = event_type.format(name=name, location=location)
        elif "{company}" in event_type and "{location}" in event_type:
            title = event_type.format(company=company, location=location)
        elif "{name}" in event_type:
            title = event_type.format(name=name)
        elif "{company}" in event_type:
            title = event_type.format(company=company)
        elif "{location}" in event_type:
            title = event_type.format(location=location)
        else:
            title = event_type
            
        upcoming.append({
            "title": title,
            "date": event_date,
            "type": "event",
            "status": random.choice(["scheduled", "tentative"]),
            "assignedTo": zambian_staff[i % len(zambian_staff)]
        })
    
    # Sort by date
    upcoming.sort(key=lambda x: x["date"])
    
    return upcoming

def generate_sales_velocity_metrics():
    """Generate sales velocity metrics"""
    return {
        "avgDealSize": 54200,
        "avgSalesCycle": 32,  # days
        "winRate": 68,  # percentage
        "dealsInPipeline": 174,
        "velocityScore": 31280  # ZMW per day
    }

def generate_win_loss_data():
    """Generate win/loss analysis data"""
    reasons_won = {
        "Product Features": 42,
        "Pricing": 28,
        "Customer Service": 15,
        "Brand Reputation": 10,
        "Implementation Timeline": 5
    }
    
    reasons_lost = {
        "Pricing": 38, 
        "Feature Gaps": 25,
        "Competitor Offering": 18,
        "Budget Constraints": 12,
        "Project Timeline": 7
    }
    
    by_product = {
        "NetaBusiness": {"won": 68, "lost": 32},
        "FarmAssist": {"won": 54, "lost": 46},
        "NetaSense": {"won": 76, "lost": 24}
    }
    
    by_deal_size = {
        "Small (<ZMW 10K)": {"won": 82, "lost": 18},
        "Medium (ZMW 10-50K)": {"won": 65, "lost": 35},
        "Large (>ZMW 50K)": {"won": 48, "lost": 52}
    }
    
    return {
        "reasonsWon": reasons_won,
        "reasonsLost": reasons_lost,
        "byProduct": by_product,
        "byDealSize": by_deal_size
    }

def search_contacts(contacts, query):
    """Search contacts by name, company, or location"""
    query = query.lower()
    results = []
    for contact in contacts:
        if (query in contact["name"].lower() or 
            query in contact["company"].lower() or 
            query in contact["location"].lower()):
            results.append(contact)
    return results

def filter_contacts_by_location(contacts, location):
    """Filter contacts by location"""
    if location == "All Locations":
        return contacts
    return [c for c in contacts if c["location"] == location]

def generate_communication_history(contact_name):
    """Generate sample communication history for a contact"""
    history = []
    now = datetime.now()
    
    # Define Zambian users
    zambian_users = ["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."]
    
    communication_types = [
        {"type": "email", "subject": "Follow-up on our meeting", "direction": "outbound"},
        {"type": "email", "subject": "Product information for Netagrow", "direction": "outbound"},
        {"type": "email", "subject": "Re: Product information", "direction": "inbound"},
        {"type": "call", "subject": "Sales call about irrigation systems", "direction": "outbound"},
        {"type": "call", "subject": "Support request", "direction": "inbound"},
        {"type": "meeting", "subject": "Product demonstration", "direction": "outbound"},
        {"type": "email", "subject": "Contract details", "direction": "outbound"},
        {"type": "email", "subject": "Re: Contract details", "direction": "inbound"},
        {"type": "call", "subject": "Follow-up call", "direction": "outbound"}
    ]
    
    # Generate 5-10 communications
    num_communications = random.randint(5, 10)
    for i in range(num_communications):
        comm_type = random.choice(communication_types)
        date = now - timedelta(days=random.randint(1, 60))
        
        history.append({
            "type": comm_type["type"],
            "subject": comm_type["subject"],
            "date": date.strftime("%Y-%m-%d"),
            "direction": comm_type["direction"],
            "content": fake.paragraph() if comm_type["type"] == "email" else fake.text(max_nb_chars=50),
            "user": random.choice(zambian_users)
        })
    
    # Sort by most recent first
    history.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    
    return history

def enhance_netagrow_data(data):
    """Add additional data for enhanced features"""
    # Generate forecasts
    forecasts, forecast_labels = generate_forecast_data(
        data["revenueData"]["data"],
        data["revenueData"]["labels"],
        3
    )
    
    data["revenueData"]["forecast"] = forecasts
    data["revenueData"]["forecastLabels"] = forecast_labels
    
    # Add recent activities
    data["recentActivities"] = generate_recent_activities()
    
    # Add upcoming tasks and events
    data["upcomingTasksEvents"] = get_upcoming_tasks_events(data)
    
    # Add enhanced contact data with groups
    contact_groups = ["Customers", "Leads", "Partners", "Suppliers", "Distributors"]
    
    for contact in data["contactManagement"]["contacts"]:
        contact["group"] = random.choice(contact_groups)
        contact["communicationHistory"] = generate_communication_history(contact["name"])
    
    # Add more contacts for better demonstration
    more_contacts = [
        {"name": "Michael Mwanza", "company": "Southern Farms", "location": "Southern Province", "email": "*****@gmail.com", "phone": "****1122", "group": "Customers"},
        {"name": "Beatrice Chanda", "company": "Western Agri Ltd", "location": "Western Province", "email": "*****@yahoo.com", "phone": "****3344", "group": "Leads"},
        {"name": "Samuel Kapemba", "company": "Northern Technologies", "location": "Northern Province", "email": "*****@outlook.com", "phone": "****5566", "group": "Partners"},
        {"name": "Patricia Mutale", "company": "Luapula Farmers", "location": "Luapula Province", "email": "*****@hotmail.com", "phone": "****7788", "group": "Customers"}
    ]
    
    for contact in more_contacts:
        contact["communicationHistory"] = generate_communication_history(contact["name"])
        data["contactManagement"]["contacts"].append(contact)
    
    # Add unique locations for filtering
    data["contactManagement"]["locations"] = sorted(list(set(c["location"] for c in data["contactManagement"]["contacts"])))
    
    # Add sales velocity metrics
    data["salesVelocityMetrics"] = generate_sales_velocity_metrics()
    
    # Add win/loss analysis data
    data["winLossAnalysis"] = generate_win_loss_data()
    
    return data

# Update the taskActivityTracking activities to use Zambian names and contexts
def get_zambian_task_activities():
    return {
        "activities": [
    {"id": 1, "task": "Follow-up call with Copperbelt Farming leads", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-02-26"},
    {"id": 2, "task": "Send proposal to Lusaka Agri Solutions", "status": "Pending", "assignedTo": "Management", "dueDate": "2025-02-27"},
    {"id": 3, "task": "Schedule demo session for Mkushi Farming Block", "status": "In Progress", "assignedTo": "Marketing Team", "dueDate": "2025-02-28"},
    {"id": 4, "task": "Client onboarding for Kafue Basin Farms", "status": "Scheduled", "assignedTo": "Marketing Team", "dueDate": "2025-03-01"},
    {"id": 5, "task": "Prepare marketing materials for Agritech Expo", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-02-22"},
    {"id": 6, "task": "Conduct training session on Netagrow AI tools", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-02-15"},
    {"id": 7, "task": "Update CRM with new farmer registrations", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-02-12"},
    {"id": 8, "task": "Host webinar on data-driven farming", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-02-08"},
    {"id": 9, "task": "Prepare Q4 performance report", "status": "Completed", "assignedTo": "Management", "dueDate": "2025-01-30"},
    {"id": 10, "task": "Follow up on partnership discussions with AgriBank", "status": "Completed", "assignedTo": "Management", "dueDate": "2025-01-28"},
    {"id": 11, "task": "Deploy software update for Netagrow App", "status": "Completed", "assignedTo": "Developers", "dueDate": "2025-01-25"},
    {"id": 12, "task": "Test Netagrow Device in real farm conditions", "status": "Completed", "assignedTo": "Developers", "dueDate": "2025-01-20"},
    {"id": 13, "task": "Send promotional emails for subscription discount", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-01-18"},
    {"id": 14, "task": "Plan content calendar for Q1 2025", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2025-01-12"},
    {"id": 15, "task": "Review customer feedback and implement improvements", "status": "Completed", "assignedTo": "Management", "dueDate": "2025-01-05"},
    {"id": 16, "task": "Launch social media campaign on smart farming", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2024-12-30"},
    {"id": 17, "task": "Host live Q&A session for Netagrow App users", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2024-12-22"},
    {"id": 18, "task": "Develop video tutorials on AI-powered crop analysis", "status": "Completed", "assignedTo": "Marketing Team", "dueDate": "2024-12-10"},
    {"id": 19, "task": "Analyze market data for expansion strategy", "status": "Completed", "assignedTo": "Management", "dueDate": "2024-12-05"},
    {"id": 20, "task": "Optimize AI models for predictive crop analysis", "status": "Completed", "assignedTo": "Developers", "dueDate": "2024-11-20"},
    {"id": 21, "task": "Secure MOUs with three major agro-cooperatives", "status": "Completed", "assignedTo": "Management", "dueDate": "2024-11-15"},
    {"id": 22, "task": "Pilot test Netagrow Device with 50 farmers", "status": "Completed", "assignedTo": "Developers", "dueDate": "2024-11-10"}
]
    }

# Update load_data function to include these Zambian tasks
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    # Load the basic data
    data = {
        "stats": {
            "totalFarmers": 1350,
            "activeUsers": 900,
            "totalDevices": 42,
            "deviceAdoption": 45,
            "supportTickets": 20,
            "monthlyGrowth": {
                "farmers": 5.8,
                "revenue": 8.2,
                "adoption": 4.1,
                "tickets": -1.9
            }
        },
        "revenueData": {
            "labels": ['Sep 24', 'Oct 24', 'Nov 24', 'Dec 24', 'Jan 25', 'Feb 25'],
            "data": [9800, 11250, 12450, 13100, 15200, 16850],
            "totalRevenue": 68650,
            "monthlyNotes": {
                'Nov 24': 'Agricultural show boost',
                'Dec 24': 'End of year promotions & increased sign-ups',
                'Feb 25': 'New device launch & expanded marketing'
            },
            "breakdown": {
                "netaBusiness": 68,
                "farmAssist": 28,
                "netaSense": 4
            }
        },
        "salesPipeline": {
            "stages": ['Lead', 'Qualified', 'Proposal Sent', 'Negotiation', 'Closed Won', 'Closed Lost'],
            "dealCounts": [60, 40, 30, 22, 15, 7],
            "dealValues": [60000, 42000, 31000, 22000, 16000, 7000],
            "conversionRates": [75, 58, 67, 48, 36, 14]
        },
        "leads": {
            "sources": ['Referrals', 'Social Media', 'Events', 'Website', 'Cold Calls'],
            "percentages": [45, 25, 15, 10, 5]
        },
        "contactManagement": {
            "contacts": [
    {"name": "John Mulenga", "company": "Mwamba Farms", "location": "Eastern Province", "email": "****@gmail.com", "phone": "****3456"},
    {"name": "Mary Phiri", "company": "Lusaka Agritech", "location": "Lusaka", "email": "****@yahoo.com", "phone": "****4567"},
    {"name": "David Tembo", "company": "Central AgriSolutions", "location": "Central", "email": "****@hotmail.com", "phone": "****7654"},
    {"name": "Chileshe Banda", "company": "GreenTech Solutions", "location": "Copperbelt", "email": "****@outlook.com", "phone": "****6789"},
    {"name": "Grace Mwanza", "company": "Southern Harvest", "location": "Southern Province", "email": "****@gmail.com", "phone": "****3456"},
    {"name": "Peter Chilufya", "company": "Northwest Agro", "location": "North-Western Province", "email": "****@yahoo.com", "phone": "****4567"},
    {"name": "Amanda Mumba", "company": "Luapula Crops", "location": "Luapula Province", "email": "****@hotmail.com", "phone": "****7654"},
    {"name": "Victor Chibuye", "company": "Muchinga Farms", "location": "Muchinga Province", "email": "****@outlook.com", "phone": "****6789"},
    {"name": "Sarah Kapata", "company": "Western AgroTech", "location": "Western Province", "email": "****@gmail.com", "phone": "****3456"},
    {"name": "Michael Kaunda", "company": "Zambezi Valley Agro", "location": "Southern Province", "email": "****@yahoo.com", "phone": "****4567"},
    {"name": "Elizabeth Lungu", "company": "FarmLink Zambia", "location": "Lusaka", "email": "****@hotmail.com", "phone": "****7654"},
    {"name": "James Mwale", "company": "AgroCare Ltd", "location": "Central Province", "email": "****@outlook.com", "phone": "****6789"},
    {"name": "Christine Musonda", "company": "EcoFarms", "location": "Copperbelt", "email": "****@gmail.com", "phone": "****3456"},
    {"name": "Robert Chansa", "company": "Future Harvest", "location": "Northern Province", "email": "****@yahoo.com", "phone": "****4567"},
    {"name": "Thandiwe Nkonde", "company": "SmartAgri", "location": "Luapula Province", "email": "****@hotmail.com", "phone": "****7654"},
    {"name": "Wilson Kasongo", "company": "AgroMax Solutions", "location": "Eastern Province", "email": "****@outlook.com", "phone": "****6789"},
    {"name": "Patricia Mwansa", "company": "GreenFields", "location": "Southern Province", "email": "****@gmail.com", "phone": "****3456"},
    {"name": "Andrew Sampa", "company": "CropMaster", "location": "North-Western Province", "email": "****@yahoo.com", "phone": "****4567"},
    {"name": "Esther Mwansa", "company": "AgriPro", "location": "Luapula Province", "email": "****@hotmail.com", "phone": "****7654"},
    {"name": "Brian Chibanda", "company": "HarvestPlus", "location": "Muchinga Province", "email": "****@outlook.com", "phone": "****6789"},
    {"name": "Mercy Mwiimbu", "company": "AgroFresh", "location": "Western Province", "email": "****@gmail.com", "phone": "****3456"},
    {"name": "Frank Mweetwa", "company": "Farmers Alliance", "location": "Lusaka", "email": "****@yahoo.com", "phone": "****4567"},
    {"name": "Dorothy Chisala", "company": "AgroTrend", "location": "Central Province", "email": "****@hotmail.com", "phone": "****7654"},
    {"name": "Brenda Zulu", "company": "EcoFarm Enterprises", "location": "Western Province", "email": "****@yahoo.com", "phone": "****9987"},
    {"name": "Patrick Nkandu", "company": "HarvestTech Ltd.", "location": "Lusaka", "email": "****@hotmail.com", "phone": "****4456"},
    {"name": "Lillian Kapata", "company": "ZamAgro Innovations", "location": "Muchinga", "email": "****@outlook.com", "phone": "****7789"},
    {"name": "Kelvin Simukonda", "company": "Future Farms Ltd.", "location": "Northern Province", "email": "****@gmail.com", "phone": "****3344"},
    {"name": "Agnes Chibwe", "company": "FarmLink Zambia", "location": "Luapula", "email": "****@yahoo.com", "phone": "****5678"},
    {"name": "Henry Mwewa", "company": "AgriEdge Technologies", "location": "Copperbelt", "email": "****@hotmail.com", "phone": "****2233"},
    {"name": "Mutale Ndlovu", "company": "SmartAgro Solutions", "location": "Central Province", "email": "****@outlook.com", "phone": "****9901"},
    {"name": "Esther Chansa", "company": "Sustainable AgriTech", "location": "North-Western Province", "email": "****@gmail.com", "phone": "****6655"},
    {"name": "Oscar Ngoma", "company": "ProHarvest Ltd.", "location": "Lusaka", "email": "****@yahoo.com", "phone": "****8822"},
    {"name": "Mercy Kasonde", "company": "FarmBoost Zambia", "location": "Southern Province", "email": "****@hotmail.com", "phone": "****4433"},
    {"name": "Emmanuel Phiri", "company": "AgroVision Ltd.", "location": "Eastern Province", "email": "****@outlook.com", "phone": "****5566"},
    {"name": "Catherine Mwansa", "company": "GreenHarvest Solutions", "location": "Muchinga", "email": "****@gmail.com", "phone": "****1199"},
    {"name": "Victor Lungu", "company": "Precision Agriculture Zambia", "location": "Western Province", "email": "****@yahoo.com", "phone": "****7788"},
    {"name": "Naomi Bwalya", "company": "TechFarm Innovations", "location": "Copperbelt", "email": "****@hotmail.com", "phone": "****3322"},
    {"name": "Harrison Zimba", "company": "OrganicAgri Solutions", "location": "Northern Province", "email": "****@outlook.com", "phone": "****6644"},
    {"name": "Felix Sikazwe", "company": "Zambia Agro Network", "location": "Luapula", "email": "****@gmail.com", "phone": "****2288"},
    {"name": "Theresa Malama", "company": "AgriConnect Ltd.", "location": "Central Province", "email": "****@yahoo.com", "phone": "****1122"}
]

        },
        "taskActivityTracking": get_zambian_task_activities(),
        "reportingAnalytics": {
            "keyMetrics": {
                "customerLifetimeValue": 5800,
                "churnRate": 7.3,
                "engagementRate": 81,
                "satisfactionScore": 94
            }
        },
        "salesMarketingTools": {
            "activeCampaigns": [
                
    {"name": "Seasonal Discount", "status": "Active", "targetAudience": "Smallholder Farmers"},
    {"name": "Referral Program", "status": "Ongoing", "targetAudience": "Existing Customers"},
    {"name": "Social Media Awareness", "status": "Active", "targetAudience": "New Leads"},
    {"name": "AgriTech Demo Sessions", "status": "Upcoming", "targetAudience": "Potential Partners"},
    {"name": "Email Outreach to Businesses", "status": "Planned", "targetAudience": "Agribusiness Enterprises"},
    {"name": "Local Radio AgriTalks", "status": "Ongoing", "targetAudience": "Rural Farmers"},
    {"name": "Webinar on AI in Agriculture", "status": "Upcoming", "targetAudience": "Tech-Savvy Farmers & Startups"},
    {"name": "Farmer Training Workshops", "status": "Active", "targetAudience": "Cooperative Leaders"},
    {"name": "Mobile SMS Tips & Alerts", "status": "Active", "targetAudience": "Rural Smallholders"},
    {"name": "Agriculture Expo Booth", "status": "Planned", "targetAudience": "Large-Scale Farmers & Investors"},
    {"name": "Partnership Outreach", "status": "Ongoing", "targetAudience": "NGOs & Development Partners"},
    {"name": "YouTube Educational Series", "status": "Active", "targetAudience": "Young Farmers & Agripreneurs"},
    {"name": "Pilot Program for Smart Sensors", "status": "Upcoming", "targetAudience": "Early Adopters"},
    {"name": "Discount on First Subscription", "status": "Active", "targetAudience": "New Users"},
    {"name": "AI-Powered Crop Advisory Launch", "status": "Upcoming", "targetAudience": "Tech-Enabled Farmers"},
    {"name": "Farmers' Market Activation", "status": "Ongoing", "targetAudience": "Local Market Vendors"},
    {"name": "Data-Driven Farming Awareness", "status": "Planned", "targetAudience": "Agricultural Extension Officers"},
    {"name": "Women in Agriculture Initiative", "status": "Active", "targetAudience": "Female Farmers & Entrepreneurs"},
    {"name": "Young Agripreneurs Challenge", "status": "Upcoming", "targetAudience": "University & College Students"},
    {"name": "Smart Farming Equipment Trial", "status": "Planned", "targetAudience": "Commercial Farmers"}
]
        }
    }
    
    # Add enhanced data
    data = enhance_netagrow_data(data)
    
    return data

netagrow_data = load_data()

# Sidebar navigation with icons using streamlit-option-menu
with st.sidebar:
    st.image("https://via.placeholder.com/150x80?text=Netagrow", width=150)
    st.markdown("## Netagrow")
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None, 
        options=["Dashboard", "Sales Pipeline", "Contacts", "Tasks", "Campaigns", "Settings"],
        icons=["speedometer2", "funnel", "people-fill", "list-task", "bullseye", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "green", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#E8F5E9"},
            "nav-link-selected": {"background-color": "#E8F5E9", "color": "#2E7D32"},
        }
    )
    
    st.markdown("---")
    st.info("Netagrow CRM v1.0 - Powering Agricultural Innovation")
    current_date = datetime.now().strftime("%d %b %Y")
    st.text(f"Date: {current_date}")

# Main content based on navigation
if selected == "Dashboard":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Netagrow CRM Dashboard</h1>'
                '<p style="margin: 5px 0;">Accelerate growth with data-driven agricultural intelligence</p></div>',
                unsafe_allow_html=True)
    
    # Date range filter
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            date_filter = st.selectbox(
                "Filter Data by Time Period:",
                ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "All Time"],
                index=2
            )
        with col2:
            st.markdown('<div class="export-container">', unsafe_allow_html=True)
            export_options = st.expander("Export Data")
            with export_options:
                st.markdown(export_to_csv(pd.DataFrame(netagrow_data["revenueData"]["data"], 
                                                       columns=["Revenue"], 
                                                       index=netagrow_data["revenueData"]["labels"]), 
                                           "revenue_data"), 
                            unsafe_allow_html=True)
                st.markdown(export_to_excel(pd.DataFrame(netagrow_data["revenueData"]["data"], 
                                                        columns=["Revenue"], 
                                                        index=netagrow_data["revenueData"]["labels"]), 
                                            "revenue_data"), 
                            unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Key Metrics row with animation
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Key Performance Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    # Add animation delay to each metric card
    for i, col in enumerate([col1, col2, col3, col4]):
        with col:
            if i == 0:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)
                st.markdown(f'<h2>{format_number(netagrow_data["stats"]["totalFarmers"])}</h2>', unsafe_allow_html=True)
                st.markdown('<h4>Total Farmers</h4>', unsafe_allow_html=True)
                growth = netagrow_data["stats"]["monthlyGrowth"]["farmers"]
                symbol, growth_class = get_trend_indicator(growth)
                st.markdown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            elif i == 1:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)
                st.markdown(f'<h2>{format_number(netagrow_data["stats"]["activeUsers"])}</h2>', unsafe_allow_html=True)
                st.markdown('<h4>Active Users</h4>', unsafe_allow_html=True)
                active_percentage = round((netagrow_data["stats"]["activeUsers"] / netagrow_data["stats"]["totalFarmers"]) * 100, 1)
                st.markdown(f'<p>{active_percentage}% of total farmers</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            elif i == 2:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)
                st.markdown(f'<h2>{format_currency(netagrow_data["revenueData"]["totalRevenue"])}</h2>', unsafe_allow_html=True)
                st.markdown('<h4>Total Revenue</h4>', unsafe_allow_html=True)
                growth = netagrow_data["stats"]["monthlyGrowth"]["revenue"]
                symbol, growth_class = get_trend_indicator(growth)
                st.markdown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            elif i == 3:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)
                st.markdown(f'<h2>{netagrow_data["stats"]["deviceAdoption"]}%</h2>', unsafe_allow_html=True)
                st.markdown('<h4>Device Adoption</h4>', unsafe_allow_html=True)
                growth = netagrow_data["stats"]["monthlyGrowth"]["adoption"]
                symbol, growth_class = get_trend_indicator(growth)
                st.markdown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Charts row
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3>Revenue Trend</h3>', unsafe_allow_html=True)
        revenue_df = pd.DataFrame({
            'Month': netagrow_data["revenueData"]["labels"],
            'Revenue': netagrow_data["revenueData"]["data"]
        })
        fig = px.line(revenue_df, x='Month', y='Revenue', markers=True, title="",
                      labels={'Revenue': 'Revenue (ZMW)'}, color_discrete_sequence=['#2E7D32'])
        
        # Enhanced tooltips
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Revenue: ZMW %{y:,.0f}<extra></extra>',
            line=dict(width=3),
            marker=dict(size=8)
        )
        
        # Add annotations with improved visibility
        notes = netagrow_data["revenueData"]["monthlyNotes"]
        for month, note in notes.items():
            month_index = netagrow_data["revenueData"]["labels"].index(month)
            revenue = netagrow_data["revenueData"]["data"][month_index]
            fig.add_annotation(
                x=month, y=revenue, 
                text=note, 
                showarrow=True, 
                arrowhead=2, 
                ax=0, ay=-40, 
                bgcolor="#E8F5E9",
                bordercolor="#2E7D32",
                borderwidth=1,
                borderpad=4,
                font=dict(size=10, color="#2E7D32")
            )
            
        fig.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=20, b=20), 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', 
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<h3>Sales Pipeline</h3>', unsafe_allow_html=True)
        pipeline_df = pd.DataFrame({
            'Stage': netagrow_data["salesPipeline"]["stages"],
            'Deal Count': netagrow_data["salesPipeline"]["dealCounts"],
            'Deal Value': netagrow_data["salesPipeline"]["dealValues"]
        })
        # Interactive tab selection
        tab1, tab2 = st.tabs(["By Count", "By Value"])
        
        with tab1:
            fig = px.funnel(
                pipeline_df, 
                x='Deal Count', 
                y='Stage', 
                title="",
                color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784'],
                # Add custom data for tooltip
                custom_data=['Deal Value']
            )
            # Enhanced tooltips
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Count: %{x}<br>Value: ZMW %{customdata[0]:,.0f}<extra></extra>'
            )
            fig.update_layout(
                height=350, 
                margin=dict(l=20, r=20, t=20, b=20), 
                paper_bgcolor='rgba(0,0,0,0)', 
                yaxis=dict(title=''),
                hoverlabel=dict(bgcolor="white", font_size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            fig = px.funnel(
                pipeline_df, 
                x='Deal Value', 
                y='Stage', 
                title="",
                color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784'],
                # Add custom data for tooltip
                custom_data=['Deal Count']
            )
            # Enhanced tooltips
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Value: ZMW %{x:,.0f}<br>Count: %{customdata[0]}<extra></extra>'
            )
            fig.update_layout(
                height=350, 
                margin=dict(l=20, r=20, t=20, b=20), 
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title=''),
                hoverlabel=dict(bgcolor="white", font_size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Third row - Two cards
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3>Lead Sources</h3>', unsafe_allow_html=True)
        leads_df = pd.DataFrame({
            'Source': netagrow_data["leads"]["sources"],
            'Percentage': netagrow_data["leads"]["percentages"]
        })
        fig = px.pie(
            leads_df, 
            values='Percentage', 
            names='Source', 
            title="",
            hole=0.4,
            color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A']
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value}%<extra></extra>'
        )
        fig.update_layout(
            height=300, 
            margin=dict(l=20, r=20, t=20, b=20), 
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            uniformtext_minsize=12, 
            uniformtext_mode='hide',
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<h3>Revenue Breakdown</h3>', unsafe_allow_html=True)
        breakdown_data = netagrow_data["revenueData"]["breakdown"]
        breakdown_df = pd.DataFrame({
            'Product': ['NetaBusiness', 'FarmAssist', 'NetaSense'],
            'Percentage': [breakdown_data["netaBusiness"], breakdown_data["farmAssist"], breakdown_data["netaSense"]]
        })
        fig = px.bar(breakdown_df, x='Product', y='Percentage', title="",
                     color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047'])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', title='Percentage (%)'))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom row - Recent activities and key metrics
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3>Recent Tasks</h3>', unsafe_allow_html=True)
        tasks_df = pd.DataFrame(netagrow_data["taskActivityTracking"]["activities"])
        task_html = "<table style='width:100%; border-collapse: collapse;'>"
        task_html += "<tr><th>Task</th><th>Assigned To</th><th>Status</th><th>Due Date</th></tr>"
        for _, task in tasks_df.iterrows():
            status_class = get_status_class(task["status"])
            status_html = f"<td class='{status_class}'>{task['status']}</td>"
            task_html += f"<tr><td>{task['task']}</td><td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"
        task_html += "</table>"
        st.markdown(task_html, unsafe_allow_html=True)
        st.button("Add New Task", key="add_new_task")

    with col2:
        st.markdown('<h3>Key Performance Indicators</h3>', unsafe_allow_html=True)
        key_metrics = netagrow_data["reportingAnalytics"]["keyMetrics"]
        metrics_row1, metrics_row2 = st.columns(2)

        with metrics_row1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=key_metrics["customerLifetimeValue"],
                title={'text': "CLV (ZMW)"},
                gauge={
                    'axis': {'range': [None, 10000]},
                    'bar': {'color': "#2E7D32"},
                    'steps': [
                        {'range': [0, 3000], 'color': "#FFEBEE"},
                        {'range': [3000, 6000], 'color': "#FFCDD2"},
                        {'range': [6000, 10000], 'color': "#E8F5E9"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with metrics_row2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=key_metrics["churnRate"],
                title={'text': "Churn Rate (%)"},
                delta={'reference': 10, 'decreasing': {'color': '#2E7D32'}},
                gauge={
                    'axis': {'range': [None, 20]},
                    'bar': {'color': "#C62828"},
                    'steps': [
                        {'range': [0, 5], 'color': "#E8F5E9"},
                        {'range': [5, 10], 'color': "#FFECB3"},
                        {'range': [10, 20], 'color': "#FFCDD2"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        metrics_row3, metrics_row4 = st.columns(2)

        with metrics_row3:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=key_metrics["engagementRate"],
                title={'text': "Engagement (%)"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2E7D32"},
                    'steps': [
                        {'range': [0, 50], 'color': "#FFCDD2"},
                        {'range': [50, 75], 'color': "#FFECB3"},
                        {'range': [75, 100], 'color': "#E8F5E9"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with metrics_row4:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=key_metrics["satisfactionScore"],
                title={'text': "Satisfaction (%)"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2E7D32"},
                    'steps': [
                        {'range': [0, 70], 'color': "#FFCDD2"},
                        {'range': [70, 85], 'color': "#FFECB3"},
                        {'range': [85, 100], 'color': "#E8F5E9"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Add forecast metrics
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Revenue Forecast</h3>", unsafe_allow_html=True)

    # Combine historical and forecast data
    combined_labels = netagrow_data["revenueData"]["labels"] + netagrow_data["revenueData"]["forecastLabels"]
    combined_data = netagrow_data["revenueData"]["data"] + netagrow_data["revenueData"]["forecast"]
    
    # Create a marker for where historical data ends and forecast begins
    is_forecast = [False] * len(netagrow_data["revenueData"]["labels"]) + [True] * len(netagrow_data["revenueData"]["forecastLabels"])
    
    # Create DataFrame for the chart
    forecast_df = pd.DataFrame({
        "Month": combined_labels,
        "Revenue": combined_data,
        "IsForecast": is_forecast
    })
    
    # Create color-coded chart
    fig = px.line(
        forecast_df, 
        x="Month", 
        y="Revenue",
        color="IsForecast",
        color_discrete_map={False: "#2E7D32", True: "#FFA000"},
        markers=True,
        labels={"Revenue": "Revenue (ZMW)", "IsForecast": ""},
        title=""
    )
    
    # Add shaded area under forecast
    for i in range(len(netagrow_data["revenueData"]["labels"]), len(combined_labels)):
        fig.add_shape(
            type="rect",
            x0=i-0.5, x1=i+0.5,
            y0=0, y1=combined_data[i],
            fillcolor="#FFF8E1",
            opacity=0.3,
            line=dict(width=0),
            layer="below"
        )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font_size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add forecast metrics
    last_actual = netagrow_data["revenueData"]["data"][-1]
    next_forecast = netagrow_data["revenueData"]["forecast"][0]
    growth_pct = ((next_forecast - last_actual) / last_actual) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Current Month", 
            f"ZMW {last_actual:,.0f}", 
            ""
        )
    with col2:
        st.metric(
            "Next Month (Forecast)", 
            f"ZMW {next_forecast:,.0f}", 
            f"{growth_pct:.1f}%"
        )
    with col3:
        total_forecast = sum(netagrow_data["revenueData"]["forecast"])
        st.metric(
            "3-Month Forecast", 
            f"ZMW {total_forecast:,.0f}", 
            ""
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add calendar view and activity feed
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h3>Upcoming Tasks & Events</h3>", unsafe_allow_html=True)
        # Calendar view of upcoming tasks and events
        upcoming = netagrow_data["upcomingTasksEvents"][:4]  # Show only 4 entries
        if not upcoming:
            st.write("No upcoming tasks or events")
        else:
            # Group by date
            from collections import defaultdict
            events_by_date = defaultdict(list)
            for event in upcoming:
                date_str = event["date"].strftime("%Y-%m-%d")
                events_by_date[date_str].append(event)
                
            # Display calendar with a more spacious layout
            for date_str, events in sorted(events_by_date.items()):
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                days_until = (date_obj - datetime.now()).days
                
                # Calculate how many days away the event is
                days_suffix = "Today" if days_until == 0 else f"Tomorrow" if days_until == 1 else f"In {days_until} days" if days_until > 0 else f"{abs(days_until)} days ago"
                
                st.markdown(
                    f"<div style='background-color: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #2E7D32; margin-bottom: 20px;'>"
                    f"<h5 style='margin-top: 0; margin-bottom: 5px;'>{date_obj.strftime('%A, %B %d')} <span style='color: #666; font-size: 0.8em;'>({days_suffix})</span></h5>", 
                    unsafe_allow_html=True
                )
                
                for event in events:
                    event_type_icon = "📅" if event["type"] == "event" else "✓"
                    status_class = get_status_class(event["status"])
                    st.markdown(
                        f"<div style='margin: 12px 0; padding: 10px; background-color: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>"
                        f"<div style='display: flex; align-items: center;'>"
                        f"<div style='font-size: 1.2em; margin-right: 15px; color: #2E7D32;'>{event_type_icon}</div>"
                        f"<div style='flex-grow: 1;'>"
                        f"<div style='font-weight: 500; margin-bottom: 5px;'>{event['title']}</div>"
                        f"<div style='font-size: 0.85em; color: #666;'>Assigned to: {event['assignedTo']}</div>"
                        f"</div>"
                        f"<div class='{status_class}' style='font-size: 0.8em;'>{event['status']}</div>"
                        f"</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Add event button below the calendar
            if st.button("+ Add Event", key="add_event_dashboard"):
                st.session_state.show_add_event = True
            
            if st.session_state.get("show_add_event", False):
                with st.form("add_event_form"):
                    event_title = st.text_input("Event Title")
                    event_date = st.date_input("Event Date")
                    event_type = st.selectbox("Event Type", ["Meeting", "Task", "Call", "Demo", "Other"])
                    event_assigned = st.selectbox("Assigned To", 
                                                 ["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."])
                    
                    submitted = st.form_submit_button("Save Event")
                    if submitted:
                        st.success("Event added!")
                        st.session_state.show_add_event = False

    with col2:
        st.markdown("<h3>Recent Activity</h3>", unsafe_allow_html=True)
        activities = netagrow_data["recentActivities"]
        
        for activity in activities[:7]:  # Show only top 7 activities
            st.markdown(
                f"<div style='border-bottom: 1px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 10px;'>"
                f"<div style='color: #2E7D32; font-weight: 500;'>{activity['activity']}</div>"
                f"<div style='display: flex; justify-content: space-between; font-size: 0.8em; color: #757575;'>"
                f"<span>by {activity['user']}</span><span>{activity['timeAgo']}</span>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='#'>View All Activity</a></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Sales Pipeline":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Sales Pipeline</h1>'
                '<p style="margin: 5px 0;">Convert more leads with strategic pipeline management</p></div>',
                unsafe_allow_html=True)
    
    # Summary metrics for the pipeline
    col1, col2, col3, col4 = st.columns(4)

    total_deals = sum(netagrow_data["salesPipeline"]["dealCounts"])
    total_value = sum(netagrow_data["salesPipeline"]["dealValues"])
    avg_deal_size = total_value / total_deals if total_deals > 0 else 0
    win_rate = netagrow_data["salesPipeline"]["dealCounts"][-2] / (
                netagrow_data["salesPipeline"]["dealCounts"][-2] + netagrow_data["salesPipeline"]["dealCounts"][-1]) * 100

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_number(total_deals)}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Total Deals</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_currency(total_value)}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Pipeline Value</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_currency(avg_deal_size)}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{win_rate:.1f}%</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Pipeline visualization
    st.markdown('<h3>Sales Pipeline Overview</h3>', unsafe_allow_html=True)
    pipeline_df = pd.DataFrame({
        'Stage': netagrow_data["salesPipeline"]["stages"],
        'Deal Count': netagrow_data["salesPipeline"]["dealCounts"],
        'Deal Value': netagrow_data["salesPipeline"]["dealValues"],
        'Conversion Rate': netagrow_data["salesPipeline"]["conversionRates"]
    })

    tab1, tab2 = st.tabs(["Pipeline by Deal Count", "Pipeline by Deal Value"])

    with tab1:
        fig = px.bar(pipeline_df, y='Stage', x='Deal Count', color='Stage', text='Deal Count', orientation='h',
                     color_discrete_sequence=px.colors.sequential.Greens, labels={'Deal Count': 'Number of Deals'})
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = px.bar(pipeline_df, y='Stage', x='Deal Value', color='Stage',
                     text=[f'ZMW {v:,}' for v in pipeline_df['Deal Value']], orientation='h',
                     color_discrete_sequence=px.colors.sequential.Greens, labels={'Deal Value': 'Deal Value (ZMW)'})
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3>Stage Conversion Rates</h3>', unsafe_allow_html=True)
    fig = px.line(pipeline_df, x='Stage', y='Conversion Rate', markers=True,
                  labels={'Conversion Rate': 'Conversion Rate (%)'}, color_discrete_sequence=['#2E7D32'])
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3>Add New Deal</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        deal_name = st.text_input("Deal Name")
        deal_value = st.number_input("Deal Value (ZMW)", min_value=0, step=1000)
        deal_stage = st.selectbox("Stage", netagrow_data["salesPipeline"]["stages"])

    with col2:
        company_name = st.text_input("Company Name")
        contact_name = st.text_input("Contact Name")
        expected_close = st.date_input("Expected Close Date")

    st.button("Add Deal", key="add_deal")

    # Add sales velocity metrics section
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Sales Velocity Metrics</h3>", unsafe_allow_html=True)

    velocity_metrics = netagrow_data["salesVelocityMetrics"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_currency(velocity_metrics["avgDealSize"])}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{velocity_metrics["avgSalesCycle"]} days</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Avg. Sales Cycle</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{velocity_metrics["winRate"]}%</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:  
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_currency(velocity_metrics["velocityScore"])}/day</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Velocity Score</h4>', unsafe_allow_html=True)
        st.tooltip = st.markdown('<div class="tooltip">ⓘ<span class="tooltiptext">Revenue generated per day: (Deal Size × Win Rate × Deals) ÷ Sales Cycle</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add win/loss analysis section
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Win/Loss Analysis</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Win Reasons", "Loss Reasons", "By Product", "By Deal Size"])
    
    win_loss_data = netagrow_data["winLossAnalysis"]
    
    with tab1:
        reasons_won = pd.DataFrame({
            "Reason": win_loss_data["reasonsWon"].keys(),
            "Percentage": win_loss_data["reasonsWon"].values()
        })
        
        fig = px.bar(
            reasons_won, 
            x="Percentage", 
            y="Reason", 
            orientation='h',
            title="",
            color_discrete_sequence=['#2E7D32'],
            text=reasons_won["Percentage"].apply(lambda x: f"{x}%")
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title="Percentage of Wins",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        reasons_lost = pd.DataFrame({
            "Reason": win_loss_data["reasonsLost"].keys(),
            "Percentage": win_loss_data["reasonsLost"].values()
        })
        
        fig = px.bar(
            reasons_lost, 
            x="Percentage", 
            y="Reason", 
            orientation='h',
            title="",
            color_discrete_sequence=['#C62828'],
            text=reasons_lost["Percentage"].apply(lambda x: f"{x}%")
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title="Percentage of Losses",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        by_product_data = []
        for product, data in win_loss_data["byProduct"].items():
            by_product_data.extend([
                {"Product": product, "Status": "Won", "Percentage": data["won"]},
                {"Product": product, "Status": "Lost", "Percentage": data["lost"]}
            ])
        by_product_df = pd.DataFrame(by_product_data)
        
        fig = px.bar(
            by_product_df,
            x="Product",
            y="Percentage",
            color="Status",
            barmode="group",
            color_discrete_map={"Won": "#2E7D32", "Lost": "#C62828"},
            text=by_product_df["Percentage"].apply(lambda x: f"{x}%")
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Percentage",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        by_deal_size_data = []
        for size, data in win_loss_data["byDealSize"].items():
            by_deal_size_data.extend([
                {"Deal Size": size, "Status": "Won", "Percentage": data["won"]},
                {"Deal Size": size, "Status": "Lost", "Percentage": data["lost"]}
            ])
        by_deal_size_df = pd.DataFrame(by_deal_size_data)
        
        fig = px.bar(
            by_deal_size_df,
            x="Deal Size",
            y="Percentage",
            color="Status",
            barmode="group",
            color_discrete_map={"Won": "#2E7D32", "Lost": "#C62828"},
            text=by_deal_size_df["Percentage"].apply(lambda x: f"{x}%"),
            category_orders={"Deal Size": ["Small (<ZMW 10K)", "Medium (ZMW 10-50K)", "Large (>ZMW 50K)"]}
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Percentage",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add drag-and-drop pipeline section
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Pipeline Management</h3>", unsafe_allow_html=True)
    
    # st.markdown("""
    # <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    #     <p>🔄 Drag and drop functionality requires additional JavaScript integration. In a full implementation,
    #     you would be able to drag deals between pipeline stages, with state updates managed by the backend.</p>
    # </div>
    # """, unsafe_allow_html=True)

    # Create columns for each pipeline stage
    cols = st.columns(len(netagrow_data["salesPipeline"]["stages"]))

elif selected == "Contacts":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Contact Management</h1>'
                '<p style="margin: 5px 0;">Build stronger relationships with your agricultural network</p></div>',
                unsafe_allow_html=True)
    
    st.markdown('<h3>Contact List</h3>', unsafe_allow_html=True)
    contacts_df = pd.DataFrame(netagrow_data["contactManagement"]["contacts"])
    contact_html = "<table style='width:100%; border-collapse: collapse;'>"
    contact_html += "<tr><th>Name</th><th>Company</th><th>Location</th><th>Email</th><th>Phone</th></tr>"
    for _, contact in contacts_df.iterrows():
        contact_html += f"<tr><td>{contact['name']}</td><td>{contact['company']}</td><td>{contact['location']}</td><td>{contact['email']}</td><td>{contact['phone']}</td></tr>"
    contact_html += "</table>"
    st.markdown(contact_html, unsafe_allow_html=True)

    st.button("Add New Contact", key="add_new_contact")

elif selected == "Tasks":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Task Management</h1>'
                '<p style="margin: 5px 0;">Prioritize activities and boost team productivity</p></div>',
                unsafe_allow_html=True)

    tasks_df = pd.DataFrame(netagrow_data["taskActivityTracking"]["activities"])
    task_html = "<table style='width:100%; border-collapse: collapse;'>"
    task_html += "<tr><th>Task</th><th>Assigned To</th><th>Status</th><th>Due Date</th></tr>"
    for _, task in tasks_df.iterrows():
        status_class = get_status_class(task["status"])
        status_html = f"<td class='{status_class}'>{task['status']}</td>"
        task_html += f"<tr><td>{task['task']}</td><td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"
    task_html += "</table>"
    st.markdown(task_html, unsafe_allow_html=True)
    st.button("Add New Task", key="add_new_task")

elif selected == "Campaigns":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Campaign Management</h1>'
                '<p style="margin: 5px 0;">Drive engagement with targeted agricultural marketing</p></div>',
                unsafe_allow_html=True)

    campaigns_df = pd.DataFrame(netagrow_data["salesMarketingTools"]["activeCampaigns"])
    campaign_html = "<table style='width:100%; border-collapse: collapse;'>"
    campaign_html += "<tr><th>Campaign Name</th><th>Status</th><th>Target Audience</th></tr>"
    for _, campaign in campaigns_df.iterrows():
        status_class = get_status_class(campaign["status"])
        status_html = f"<td class='{status_class}'>{campaign['status']}</td>"
        campaign_html += f"<tr><td>{campaign['name']}</td>{status_html}<td>{campaign['targetAudience']}</td></tr>"
    campaign_html += "</table>"
    st.markdown(campaign_html, unsafe_allow_html=True)

    st.button("Add New Campaign", key="add_new_campaign")

elif selected == "Settings":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Settings</h1>'
                '<p style="margin: 5px 0;">Customize your Netagrow experience</p></div>',
                unsafe_allow_html=True)

    st.markdown('<h3>User Settings</h3>', unsafe_allow_html=True)
    st.text_input("Username")
    st.text_input("Email")
    st.text_input("Password", type="password")
    
    st.markdown('<h3>System Settings</h3>', unsafe_allow_html=True)
    st.checkbox("Enable Dark Mode")
    st.checkbox("Enable Notifications")
    st.selectbox("Language", ["English", "French", "Spanish"])

    st.button("Save Settings", key="save_settings")
