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
    page_title="NetaGrow Zambia CRM",
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

# Update the generate_recent_activities function with Zambian names and companies
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
    
    activity_types = [
        "Added new contact: {name}",
        "Updated deal with {company}",
        "Scheduled meeting with {name} at {company}",
        "Sent proposal to {name} from {company}",
        "Received payment from {company}",
        "Created task: {task} for {company}",
        "Completed task: {task} for {name}",
        "Added note to {name}'s profile",
        "Modified campaign: {campaign}",
        "Created support ticket for {company}"
    ]
    
    activities = []
    now = datetime.now()
    
    for i in range(count):
        activity_type = random.choice(activity_types)
        timestamp = now - timedelta(hours=random.randint(1, 72))
        
        name = random.choice(zambian_names)
        company = random.choice(zambian_companies)
        task = random.choice(zambian_tasks)
        campaign = random.choice(zambian_campaigns)
        
        if "{name}" in activity_type and "{company}" in activity_type:
            activity = activity_type.format(name=name, company=company)
        elif "{name}" in activity_type:
            activity = activity_type.format(name=name)
        elif "{company}" in activity_type:
            activity = activity_type.format(company=company)
        elif "{task}" in activity_type and "{company}" in activity_type:
            activity = activity_type.format(task=task, company=company)
        elif "{task}" in activity_type and "{name}" in activity_type:
            activity = activity_type.format(task=task, name=name)
        elif "{task}" in activity_type:
            activity = activity_type.format(task=task)
        elif "{campaign}" in activity_type:
            activity = activity_type.format(campaign=campaign)
        else:
            activity = activity_type
        
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
    """Convert timestamp to human-readable time ago string"""
    now = datetime.now()
    delta = now - timestamp
    
    if delta.days > 0:
        return f"{delta.days}d ago"
    elif delta.seconds >= 3600:
        return f"{delta.seconds // 3600}h ago"
    elif delta.seconds >= 60:
        return f"{delta.seconds // 60}m ago"
    else:
        return "Just now"

# Update the get_upcoming_tasks_events function to generate stronger Zambian context
def get_upcoming_tasks_events(data, days=30):
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
        "Zambezi Agricultural Services", "Kafue Basin Farms", "Southern Province Cooperative", 
        "Muchinga Agritech", "Mkushi Farming Block", "Eastern Zambia Producers", 
        "Northern Agro Dealers", "Kariba Harvest Ltd", "Chongwe Farming Collective",
        "Zambeef Products", "Zamseed", "Zambia National Farmers Union", "Zambia Sugar",
        "NWK Agri-Services", "Good Nature Agro", "Seed Co Zambia", "AgriServe Zambia"
    ]
    
    zambian_names = [
        "Mwamba Chilufya", "Nkandu Mulenga", "Chanda Mutale", "Bwalya Musonda", 
        "Kalumba Tembo", "Mutinta Hichilema", "Mulenga Kapwepwe", "Chilombo Banda", 
        "Chileshe Bwalya", "Chongo Daka", "Nsofwa Mwale", "Mwila Kanyanta",
        "Lubinda Haabazoka", "Kasonde Mwenda", "Monde Sitwala", "Namakau Mukelabai",
        "Changala Siame", "Muyunda Mwangala", "Choolwe Beyani", "Mweetwa Sitali"
    ]
    
    zambian_locations = [
        "Lusaka", "Ndola", "Kitwe", "Livingstone", "Chipata", "Kasama", 
        "Mongu", "Solwezi", "Kabwe", "Choma", "Mansa", "Monze", "Chingola",
        "Mpika", "Mumbwa", "Mazabuka", "Kapiri Mposhi", "Kafue", "Siavonga"
    ]
    
    zambian_events = [
        "Meeting with {company} in {location}",
        "Demo for {company} at Agricultural Showgrounds",
        "Call with {name} about irrigation systems",
        "Farmer training session in {location}",
        "NetaGrow demonstration at {location} Expo",
        "Agricultural Cooperative meeting in {location}",
        "Equipment installation at {company} in {location}",
        "Field visit with {name} to {company}",
        "Stakeholder meeting at Ministry of Agriculture",
        "NetaSense deployment at {company}'s farms",
        "Crop monitoring system setup for {company}",
        "Farmer group training in {location}",
        "NetaGrow showcase at {location} Agricultural Fair",
        "Drought mitigation workshop with {company}"
    ]
    
    zambian_staff = ["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T.", 
                    "Lubinda K.", "Mwenya C.", "Kalinda B.", "Nchimunya M."]
    
    for _ in range(10):
        event_date = now + timedelta(days=random.randint(1, days))
        event_type = random.choice(zambian_events)
        
        name = random.choice(zambian_names)
        company = random.choice(zambian_companies)
        location = random.choice(zambian_locations)
        
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
            "assignedTo": random.choice(zambian_staff)
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
o M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."]
def search_contacts(contacts, query):
    """Search contacts by name, company, or location"""
    query = query.lower()},
    results = []ems", "direction": "outbound"},
    tion": "inbound"},
    for contact in contacts:und"},
        if (query in contact["name"].lower() or ound"},
            query in contact["company"].lower() or d"},
            query in contact["location"].lower()):on": "outbound"},
            results.append(contact)   {"type": "email", "subject": "Re: NetaGrow contract details", "direction": "inbound"},
        {"type": "call", "subject": "Implementation follow-up", "direction": "outbound"}
    return results

def filter_contacts_by_location(contacts, location):
    """Filter contacts by location"""
    if location == "All Locations":
        return contactscomm_type = random.choice(communication_types)
    edelta(days=random.randint(1, 60))
    return [c for c in contacts if c["location"] == location]

def generate_communication_history(contact_name):
    """Generate sample communication history for a contact"""
    history = []
    now = datetime.now()
      "content": fake.paragraph() if comm_type["type"] == "email" else fake.text(max_nb_chars=50),
    communication_types = [        "user": random.choice(zambian_users)
        {"type": "email", "subject": "Follow-up on our meeting", "direction": "outbound"},
        {"type": "email", "subject": "Product information", "direction": "outbound"},
        {"type": "email", "subject": "Re: Product information", "direction": "inbound"},# Sort by most recent first
        {"type": "call", "subject": "Sales call", "direction": "outbound"},ey=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
        {"type": "call", "subject": "Support request", "direction": "inbound"},    
        {"type": "meeting", "subject": "Product demo", "direction": "outbound"},
        {"type": "email", "subject": "Contract details", "direction": "outbound"},
        {"type": "email", "subject": "Re: Contract details", "direction": "inbound"}, data
        {"type": "call", "subject": "Follow-up call", "direction": "outbound"}a(data):
    ]
    
    # Generate 5-10 communicationsate_forecast_data(
    num_communications = random.randint(5, 10)ata["revenueData"]["data"],
    for i in range(num_communications):   data["revenueData"]["labels"],
        comm_type = random.choice(communication_types)    3
        date = now - timedelta(days=random.randint(1, 60))
        
        history.append({data["revenueData"]["forecast"] = forecasts
            "type": comm_type["type"],recastLabels"] = forecast_labels
            "subject": comm_type["subject"],
            "date": date.strftime("%Y-%m-%d"),# Add recent activities
            "direction": comm_type["direction"],rate_recent_activities()
            "content": fake.paragraph() if comm_type["type"] == "email" else fake.text(max_nb_chars=50),
            "user": random.choice(["John D.", "Mary P.", "Alex S.", "Sarah K."])# Add upcoming tasks and events
        })ing_tasks_events(data)
    
    # Sort by most recent first# Add enhanced contact data with groups
    history.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)Suppliers", "Distributors"]
    
    return history
    contact["group"] = random.choice(contact_groups)
# Add to your load_data function or create enhanced datate_communication_history(contact["name"])
def enhance_netagrow_data(data):
    """Add additional data for enhanced features"""
    # Generate forecasts
    forecasts, forecast_labels = generate_forecast_data(
        data["revenueData"]["data"],
        data["revenueData"]["labels"],   {"name": "Samuel Kapemba", "company": "Northern Technologies", "location": "Northern Province", "email": "*****@outlook.com", "phone": "****5566", "group": "Partners"},
        3    {"name": "Patricia Mutale", "company": "Luapula Farmers", "location": "Luapula Province", "email": "*****@hotmail.com", "phone": "****7788", "group": "Customers"}
    )
    
    data["revenueData"]["forecast"] = forecasts
    data["revenueData"]["forecastLabels"] = forecast_labels    contact["communicationHistory"] = generate_communication_history(contact["name"])
    cts"].append(contact)
    # Add recent activities
    data["recentActivities"] = generate_recent_activities()# Add unique locations for filtering
    ocations"] = sorted(list(set(c["location"] for c in data["contactManagement"]["contacts"])))
    # Add upcoming tasks and events
    data["upcomingTasksEvents"] = get_upcoming_tasks_events(data)# Add sales velocity metrics
     = generate_sales_velocity_metrics()
    # Add enhanced contact data with groups
    contact_groups = ["Customers", "Leads", "Partners", "Suppliers", "Distributors"]# Add win/loss analysis data
    ssAnalysis"] = generate_win_loss_data()
    for contact in data["contactManagement"]["contacts"]:    
        contact["group"] = random.choice(contact_groups)
        contact["communicationHistory"] = generate_communication_history(contact["name"])
    
    # Add more contacts for better demonstration # Cache data for 1 hour
    more_contacts = [a():
        {"name": "Michael Mwanza", "company": "Southern Farms", "location": "Southern Province", "email": "*****@gmail.com", "phone": "****1122", "group": "Customers"},ic data
        {"name": "Beatrice Chanda", "company": "Western Agri Ltd", "location": "Western Province", "email": "*****@yahoo.com", "phone": "****3344", "group": "Leads"},
        {"name": "Samuel Kapemba", "company": "Northern Technologies", "location": "Northern Province", "email": "*****@outlook.com", "phone": "****5566", "group": "Partners"},
        {"name": "Patricia Mutale", "company": "Luapula Farmers", "location": "Luapula Province", "email": "*****@hotmail.com", "phone": "****7788", "group": "Customers"}0,
    ]
    
    for contact in more_contacts:45,
        contact["communicationHistory"] = generate_communication_history(contact["name"])0,
        data["contactManagement"]["contacts"].append(contact)
    
    # Add unique locations for filtering
    data["contactManagement"]["locations"] = sorted(list(set(c["location"] for c in data["contactManagement"]["contacts"])))   "adoption": 4.1,
          "tickets": -1.9
    # Add sales velocity metrics
    data["salesVelocityMetrics"] = generate_sales_velocity_metrics()
    
    # Add win/loss analysis dataOct 24', 'Nov 24', 'Dec 24', 'Jan 25', 'Feb 25'],
    data["winLossAnalysis"] = generate_win_loss_data()250, 12450, 13100, 15200, 16850],
    
    return data

# Load the data  'Dec 24': 'End of year promotions & increased sign-ups',
@st.cache_data(ttl=3600)  # Cache data for 1 hour'New device launch & expanded marketing'
def load_data():
    # Load the basic data
    data = {: 68,
        "stats": {   "farmAssist": 28,
            "totalFarmers": 1350,      "netaSense": 4
            "activeUsers": 900,
            "totalDevices": 42,
            "deviceAdoption": 45,
            "supportTickets": 20,ation', 'Closed Won', 'Closed Lost'],
            "monthlyGrowth": {
                "farmers": 5.8,  "dealValues": [60000, 42000, 31000, 22000, 16000, 7000],
                "revenue": 8.2,rsionRates": [75, 58, 67, 48, 36, 14]
                "adoption": 4.1,
                "tickets": -1.9
            }  "sources": ['Referrals', 'Social Media', 'Events', 'Website', 'Cold Calls'],
        },, 25, 15, 10, 5]
        "revenueData": {
            "labels": ['Sep 24', 'Oct 24', 'Nov 24', 'Dec 24', 'Jan 25', 'Feb 25'],
            "data": [9800, 11250, 12450, 13100, 15200, 16850],
            "totalRevenue": 68650,
            "monthlyNotes": {
                'Nov 24': 'Agricultural show boost',   {"name": "David Tembo", "company": "Central AgriSolutions", "location": "Central", "email": "*****@hotmail.com", "phone": "****9876"},
                'Dec 24': 'End of year promotions & increased sign-ups',      {"name": "Chileshe Banda", "company": "GreenTech Solutions", "location": "Copperbelt", "email": "*****@outlook.com", "phone": "****5567"}
                'Feb 25': 'New device launch & expanded marketing'
            },
            "breakdown": {
                "netaBusiness": 68,
                "farmAssist": 28,,
                "netaSense": 4,
            }   {"id": 3, "task": "Schedule demo session", "status": "In Progress", "assignedTo": "Sales Rep 3", "dueDate": "2025-02-28"},
        },      {"id": 4, "task": "Client onboarding session", "status": "Scheduled", "assignedTo": "Sales Rep 4", "dueDate": "2025-03-01"}
        "salesPipeline": {
            "stages": ['Lead', 'Qualified', 'Proposal Sent', 'Negotiation', 'Closed Won', 'Closed Lost'],
            "dealCounts": [60, 40, 30, 22, 15, 7],
            "dealValues": [60000, 42000, 31000, 22000, 16000, 7000],
            "conversionRates": [75, 58, 67, 48, 36, 14]e": 5800,
        },
        "leads": {   "engagementRate": 81,
            "sources": ['Referrals', 'Social Media', 'Events', 'Website', 'Cold Calls'],      "satisfactionScore": 94
            "percentages": [45, 25, 15, 10, 5]
        },
        "contactManagement": {
            "contacts": [
                {"name": "John Mulenga", "company": "Mwamba Farms", "location": "Eastern Province", "email": "*****@gmail.com", "phone": "****6789"},rs"},
                {"name": "Mary Phiri", "company": "Lusaka Agritech", "location": "Lusaka", "email": "*****@yahoo.com", "phone": "****2345"},
                {"name": "David Tembo", "company": "Central AgriSolutions", "location": "Central", "email": "*****@hotmail.com", "phone": "****9876"},
                {"name": "Chileshe Banda", "company": "GreenTech Solutions", "location": "Copperbelt", "email": "*****@outlook.com", "phone": "****5567"}   {"name": "AgriTech Demo Sessions", "status": "Upcoming", "targetAudience": "Potential Partners"},
            ]       {"name": "Email Outreach to Businesses", "status": "Planned", "targetAudience": "Agribusiness Enterprises"}
        },       ]
        "taskActivityTracking": {    }
            "activities": [
                {"id": 1, "task": "Follow-up call with lead", "status": "Completed", "assignedTo": "Sales Rep 1", "dueDate": "2025-02-26"},
                {"id": 2, "task": "Send proposal to new client", "status": "Pending", "assignedTo": "Sales Rep 2", "dueDate": "2025-02-27"},# Add enhanced data
                {"id": 3, "task": "Schedule demo session", "status": "In Progress", "assignedTo": "Sales Rep 3", "dueDate": "2025-02-28"},nce_netagrow_data(data)
                {"id": 4, "task": "Client onboarding session", "status": "Scheduled", "assignedTo": "Sales Rep 4", "dueDate": "2025-03-01"}    
            ]
        },
        "reportingAnalytics": {
            "keyMetrics": {
                "customerLifetimeValue": 5800,
                "churnRate": 7.3,
                "engagementRate": 81,via.placeholder.com/150x80?text=NetaGrow", width=150)
                "satisfactionScore": 94st.markdown("## NetaGrow Zambia")
            }
        },
        "salesMarketingTools": {
            "activeCampaigns": [
                {"name": "Seasonal Discount", "status": "Active", "targetAudience": "Smallholder Farmers"},rd", "Sales Pipeline", "Contacts", "Tasks", "Campaigns", "Settings"],
                {"name": "Referral Program", "status": "Ongoing", "targetAudience": "Existing Customers"},ter2", "funnel", "people-fill", "list-task", "bullseye", "gear"],
                {"name": "Social Media Awareness", "status": "Active", "targetAudience": "New Leads"},n="cast",
                {"name": "AgriTech Demo Sessions", "status": "Upcoming", "targetAudience": "Potential Partners"},
                {"name": "Email Outreach to Businesses", "status": "Planned", "targetAudience": "Agribusiness Enterprises"}
            ]
        }
    }   "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#E8F5E9"},
           "nav-link-selected": {"background-color": "#E8F5E9", "color": "#2E7D32"},
    # Add enhanced data    }
    data = enhance_netagrow_data(data)
    
    return data

netagrow_data = load_data()    current_date = datetime.now().strftime("%d %b %Y")
")
# Sidebar navigation with icons using streamlit-option-menu
with st.sidebar:
    st.image("https://via.placeholder.com/150x80?text=NetaGrow", width=150)
    st.markdown("## NetaGrow Zambia")tom: 20px;">'
    st.markdown("---")>NetaGrow Zambia CRM Dashboard</h1>'
                '<p style="margin: 5px 0;">A comprehensive view of your agricultural technology business</p></div>',
    selected = option_menu(allow_html=True)
        menu_title=None, 
        options=["Dashboard", "Sales Pipeline", "Contacts", "Tasks", "Campaigns", "Settings"],
        icons=["speedometer2", "funnel", "people-fill", "list-task", "bullseye", "gear"],ner():
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"}, Data by Time Period:",
            "icon": {"color": "green", "font-size": "16px"},   ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "All Time"],
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#E8F5E9"},dex=2
            "nav-link-selected": {"background-color": "#E8F5E9", "color": "#2E7D32"},
        }
    )ass="export-container">', unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("CRM Version 1.0.0")
    current_date = datetime.now().strftime("%d %b %Y")ns=["Revenue"], 
    st.text(f"Date: {current_date}")    index=netagrow_data["revenueData"]["labels"]), 

# Main content based on navigation
if selected == "Dashboard":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'ns=["Revenue"], 
                '<h1 style="margin: 0;">NetaGrow Zambia CRM Dashboard</h1>'     index=netagrow_data["revenueData"]["labels"]), 
                '<p style="margin: 5px 0;">A comprehensive view of your agricultural technology business</p></div>',"), 
                unsafe_allow_html=True)                            unsafe_allow_html=True)
    safe_allow_html=True)
    # Date range filter
    with st.container():
        col1, col2 = st.columns([4, 1])", unsafe_allow_html=True)
        with col1:    st.markdown("<h3>Key Performance Metrics</h3>", unsafe_allow_html=True)
            date_filter = st.selectbox(
                "Filter Data by Time Period:",
                ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "All Time"],on delay to each metric card
                index=2erate([col1, col2, col3, col4]):
            )
        with col2:
            st.markdown('<div class="export-container">', unsafe_allow_html=True)ion-delay: {i*0.1}s;">', unsafe_allow_html=True)
            export_options = st.expander("Export Data")talFarmers"])}</h2>', unsafe_allow_html=True)
            with export_options:_html=True)
                st.markdown(export_to_csv(pd.DataFrame(netagrow_data["revenueData"]["data"], 
                                                       columns=["Revenue"], owth)
                                                       index=netagrow_data["revenueData"]["labels"]), own(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
                                           "revenue_data"), 
                            unsafe_allow_html=True)
                st.markdown(export_to_excel(pd.DataFrame(netagrow_data["revenueData"]["data"], tion-delay: {i*0.1}s;">', unsafe_allow_html=True)
                                                        columns=["Revenue"], 
                                                        index=netagrow_data["revenueData"]["labels"]), 
                                            "revenue_data"), ts"]["activeUsers"] / netagrow_data["stats"]["totalFarmers"]) * 100, 1)
                            unsafe_allow_html=True)own(f'<p>{active_percentage}% of total farmers</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Key Metrics row with animationion-delay: {i*0.1}s;">', unsafe_allow_html=True)
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)ta"]["totalRevenue"])}</h2>', unsafe_allow_html=True)
    st.markdown("<h3>Key Performance Metrics</h3>", unsafe_allow_html=True)_html=True)
    col1, col2, col3, col4 = st.columns(4)
owth)
    # Add animation delay to each metric cardown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
    for i, col in enumerate([col1, col2, col3, col4]):
        with col:
            if i == 0:n-delay: {i*0.1}s;">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)%</h2>', unsafe_allow_html=True)
                st.markdown(f'<h2>{format_number(netagrow_data["stats"]["totalFarmers"])}</h2>', unsafe_allow_html=True)ow_html=True)
                st.markdown('<h4>Total Farmers</h4>', unsafe_allow_html=True)
                growth = netagrow_data["stats"]["monthlyGrowth"]["farmers"]owth)
                symbol, growth_class = get_trend_indicator(growth)lass}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)"</div>", unsafe_allow_html=True)
            elif i == 1:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)
                st.markdown(f'<h2>{format_number(netagrow_data["stats"]["activeUsers"])}</h2>', unsafe_allow_html=True)    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                st.markdown('<h4>Active Users</h4>', unsafe_allow_html=True) = st.columns(2)
                active_percentage = round((netagrow_data["stats"]["activeUsers"] / netagrow_data["stats"]["totalFarmers"]) * 100, 1)
                st.markdown(f'<p>{active_percentage}% of total farmers</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)tml=True)
            elif i == 2:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True)  'Month': netagrow_data["revenueData"]["labels"],
                st.markdown(f'<h2>{format_currency(netagrow_data["revenueData"]["totalRevenue"])}</h2>', unsafe_allow_html=True)
                st.markdown('<h4>Total Revenue</h4>', unsafe_allow_html=True)
                growth = netagrow_data["stats"]["monthlyGrowth"]["revenue"]fig = px.line(revenue_df, x='Month', y='Revenue', markers=True, title="",
                symbol, growth_class = get_trend_indicator(growth)s={'Revenue': 'Revenue (ZMW)'}, color_discrete_sequence=['#2E7D32'])
                st.markdown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            elif i == 3:
                st.markdown(f'<div class="metric-card animated" style="animation-delay: {i*0.1}s;">', unsafe_allow_html=True){x}</b><br>Revenue: ZMW %{y:,.0f}<extra></extra>',
                st.markdown(f'<h2>{netagrow_data["stats"]["deviceAdoption"]}%</h2>', unsafe_allow_html=True)   line=dict(width=3),
                st.markdown('<h4>Device Adoption</h4>', unsafe_allow_html=True)    marker=dict(size=8)
                growth = netagrow_data["stats"]["monthlyGrowth"]["adoption"]
                symbol, growth_class = get_trend_indicator(growth)
                st.markdown(f'<p class="{growth_class}">{symbol} {abs(growth)}%</p>', unsafe_allow_html=True)isibility
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
row_data["revenueData"]["labels"].index(month)
    # Charts row"revenueData"]["data"][month_index]
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)ion(
    col1, col2 = st.columns(2)ue, 

    with col1:e, 
        st.markdown('<h3>Revenue Trend</h3>', unsafe_allow_html=True)
        revenue_df = pd.DataFrame({
            'Month': netagrow_data["revenueData"]["labels"],E9",
            'Revenue': netagrow_data["revenueData"]["data"]"#2E7D32",
        })
        fig = px.line(revenue_df, x='Month', y='Revenue', markers=True, title="",   borderpad=4,
                      labels={'Revenue': 'Revenue (ZMW)'}, color_discrete_sequence=['#2E7D32'])    font=dict(size=10, color="#2E7D32")
        
        # Enhanced tooltips
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Revenue: ZMW %{y:,.0f}<extra></extra>',
            line=dict(width=3),b=20), 
            marker=dict(size=8))',
        )
        lse),
        # Add annotations with improved visibility0,0.1)'),
        notes = netagrow_data["revenueData"]["monthlyNotes"]   hovermode="x unified",
        for month, note in notes.items():=12)
            month_index = netagrow_data["revenueData"]["labels"].index(month)        )
            revenue = netagrow_data["revenueData"]["data"][month_index]tly_chart(fig, use_container_width=True)
            fig.add_annotation(
                x=month, y=revenue, 
                text=note, ml=True)
                showarrow=True, 
                arrowhead=2, 
                ax=0, ay=-40,  'Deal Count': netagrow_data["salesPipeline"]["dealCounts"],
                bgcolor="#E8F5E9",    'Deal Value': netagrow_data["salesPipeline"]["dealValues"]
                bordercolor="#2E7D32",
                borderwidth=1,
                borderpad=4,# Interactive tab selection
                font=dict(size=10, color="#2E7D32") = st.tabs(["By Count", "By Value"])
            )
            
        fig.update_layout(
            height=350, , 
            margin=dict(l=20, r=20, t=20, b=20), ount', 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', 
            xaxis=dict(showgrid=False),#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784'],
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),   # Add custom data for tooltip
            hovermode="x unified",eal Value']
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        st.plotly_chart(fig, use_container_width=True)ig.update_traces(
'<b>%{y}</b><br>Count: %{x}<br>Value: ZMW %{customdata[0]:,.0f}<extra></extra>'
    with col2:
        st.markdown('<h3>Sales Pipeline</h3>', unsafe_allow_html=True)
        pipeline_df = pd.DataFrame({
            'Stage': netagrow_data["salesPipeline"]["stages"],0, t=20, b=20), 
            'Deal Count': netagrow_data["salesPipeline"]["dealCounts"],
            'Deal Value': netagrow_data["salesPipeline"]["dealValues"]   yaxis=dict(title=''),
        })=12)
        )
        # Interactive tab selectiontly_chart(fig, use_container_width=True)
        tab1, tab2 = st.tabs(["By Count", "By Value"])
        
        with tab1:
            fig = px.funnel(, 
                pipeline_df, alue', 
                x='Deal Count', 
                y='Stage', 
                title="",#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784'],
                color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784'],   # Add custom data for tooltip
                # Add custom data for tooltipeal Count']
                custom_data=['Deal Value']
            )
            # Enhanced tooltipsig.update_traces(
            fig.update_traces('<b>%{y}</b><br>Value: ZMW %{x:,.0f}<br>Count: %{customdata[0]}<extra></extra>'
                hovertemplate='<b>%{y}</b><br>Count: %{x}<br>Value: ZMW %{customdata[0]:,.0f}<extra></extra>'
            )
            fig.update_layout(
                height=350, 0, t=20, b=20), 
                margin=dict(l=20, r=20, t=20, b=20), 
                paper_bgcolor='rgba(0,0,0,0)',   yaxis=dict(title=''),
                yaxis=dict(title=''),=12)
                hoverlabel=dict(bgcolor="white", font_size=12)
            )            st.plotly_chart(fig, use_container_width=True)
            st.plotly_chart(fig, use_container_width=True)nsafe_allow_html=True)
            
        with tab2:
            fig = px.funnel(    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                pipeline_df,  = st.columns(2)
                x='Deal Value', 
                y='Stage', 
                title="",w_html=True)
                color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784'],
                # Add custom data for tooltip  'Source': netagrow_data["leads"]["sources"],
                custom_data=['Deal Count']ge': netagrow_data["leads"]["percentages"]
            )
            # Enhanced tooltips
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Value: ZMW %{x:,.0f}<br>Count: %{customdata[0]}<extra></extra>'rcentage', 
            )urce', 
            fig.update_layout(
                height=350,    hole=0.4,
                margin=dict(l=20, r=20, t=20, b=20), _sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A']
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title=''),
                hoverlabel=dict(bgcolor="white", font_size=12)
            )   textinfo='percent+label',
            st.plotly_chart(fig, use_container_width=True)'<b>%{label}</b><br>%{value}%<extra></extra>'
    st.markdown("</div>", unsafe_allow_html=True)

    # Third row - Two cards
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)0,0)',
"h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    with col1:
        st.markdown('<h3>Lead Sources</h3>', unsafe_allow_html=True)   uniformtext_mode='hide',
        leads_df = pd.DataFrame({=12)
            'Source': netagrow_data["leads"]["sources"],        )
            'Percentage': netagrow_data["leads"]["percentages"]tly_chart(fig, use_container_width=True)
        })
        fig = px.pie(
            leads_df, kdown</h3>', unsafe_allow_html=True)
            values='Percentage', 
            names='Source', 
            title="",   'Product': ['NetaBusiness', 'FarmAssist', 'NetaSense'],
            hole=0.4,["farmAssist"], breakdown_data["netaSense"]]
            color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A']
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',, xaxis=dict(showgrid=False),
            hovertemplate='<b>%{label}</b><br>%{value}%<extra></extra>'e, gridcolor='rgba(0,0,0,0.1)', title='Percentage (%)'))
        )        st.plotly_chart(fig, use_container_width=True)
        fig.update_layout(
            height=300, 
            margin=dict(l=20, r=20, t=20, b=20), vities and key metrics
            paper_bgcolor='rgba(0,0,0,0)',    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), = st.columns(2)
            uniformtext_minsize=12, 
            uniformtext_mode='hide',
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        st.plotly_chart(fig, use_container_width=True)0%; border-collapse: collapse;'>"
<th>Status</th><th>Due Date</th></tr>"
    with col2:
        st.markdown('<h3>Revenue Breakdown</h3>', unsafe_allow_html=True)
        breakdown_data = netagrow_data["revenueData"]["breakdown"] class='{status_class}'>{task['status']}</td>"
        breakdown_df = pd.DataFrame({<td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"
            'Product': ['NetaBusiness', 'FarmAssist', 'NetaSense'],
            'Percentage': [breakdown_data["netaBusiness"], breakdown_data["farmAssist"], breakdown_data["netaSense"]]        st.markdown(task_html, unsafe_allow_html=True)
        })ton("Add New Task", key="add_new_task")
        fig = px.bar(breakdown_df, x='Product', y='Percentage', title="",
                     color_discrete_sequence=['#2E7D32', '#388E3C', '#43A047'])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',s</h3>', unsafe_allow_html=True)
                          plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False),        key_metrics = netagrow_data["reportingAnalytics"]["keyMetrics"]
                          yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', title='Percentage (%)'))ics_row2 = st.columns(2)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom row - Recent activities and key metrics
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)ey_metrics["customerLifetimeValue"],
    col1, col2 = st.columns(2)

    with col1:range': [None, 10000]},
        st.markdown('<h3>Recent Tasks</h3>', unsafe_allow_html=True)
        tasks_df = pd.DataFrame(netagrow_data["taskActivityTracking"]["activities"])
        task_html = "<table style='width:100%; border-collapse: collapse;'>"
        task_html += "<tr><th>Task</th><th>Assigned To</th><th>Status</th><th>Due Date</th></tr>"   {'range': [3000, 6000], 'color': "#FFCDD2"},
        for _, task in tasks_df.iterrows():       {'range': [6000, 10000], 'color': "#E8F5E9"}
            status_class = get_status_class(task["status"])      ]
            status_html = f"<td class='{status_class}'>{task['status']}</td>"
            task_html += f"<tr><td>{task['task']}</td><td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"
        task_html += "</table>"            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown(task_html, unsafe_allow_html=True)t(fig, use_container_width=True)
        st.button("Add New Task", key="add_new_task")

    with col2:
        st.markdown('<h3>Key Performance Indicators</h3>', unsafe_allow_html=True)
        key_metrics = netagrow_data["reportingAnalytics"]["keyMetrics"]
        metrics_row1, metrics_row2 = st.columns(2)'text': "Churn Rate (%)"},
g': {'color': '#2E7D32'}},
        with metrics_row1:
            fig = go.Figure(go.Indicator(range': [None, 20]},
                mode="gauge+number",
                value=key_metrics["customerLifetimeValue"],
                title={'text': "CLV (ZMW)"},
                gauge={   {'range': [5, 10], 'color': "#FFECB3"},
                    'axis': {'range': [None, 10000]},       {'range': [10, 20], 'color': "#FFCDD2"}
                    'bar': {'color': "#2E7D32"},      ]
                    'steps': [
                        {'range': [0, 3000], 'color': "#FFEBEE"},
                        {'range': [3000, 6000], 'color': "#FFCDD2"},            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
                        {'range': [6000, 10000], 'color': "#E8F5E9"}th=True)
                    ]
                }ics_row4 = st.columns(2)
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with metrics_row2:ey_metrics["engagementRate"],
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=key_metrics["churnRate"],range': [None, 100]},
                title={'text': "Churn Rate (%)"},
                delta={'reference': 10, 'decreasing': {'color': '#2E7D32'}},
                gauge={
                    'axis': {'range': [None, 20]},   {'range': [50, 75], 'color': "#FFECB3"},
                    'bar': {'color': "#C62828"},       {'range': [75, 100], 'color': "#E8F5E9"}
                    'steps': [      ]
                        {'range': [0, 5], 'color': "#E8F5E9"},
                        {'range': [5, 10], 'color': "#FFECB3"},
                        {'range': [10, 20], 'color': "#FFCDD2"}            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
                    ]t(fig, use_container_width=True)
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
ey_metrics["satisfactionScore"],
        metrics_row3, metrics_row4 = st.columns(2)

        with metrics_row3:range': [None, 100]},
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=key_metrics["engagementRate"],
                title={'text': "Engagement (%)"},  {'range': [70, 85], 'color': "#FFECB3"},
                gauge={[85, 100], 'color': "#E8F5E9"}
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2E7D32"},
                    'steps': [olor': "green", 'width': 4},
                        {'range': [0, 50], 'color': "#FFCDD2"},   'thickness': 0.75,
                        {'range': [50, 75], 'color': "#FFECB3"},       'value': 90
                        {'range': [75, 100], 'color': "#E8F5E9"}      }
                    ]
                }
            ))dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')            st.plotly_chart(fig, use_container_width=True)
            st.plotly_chart(fig, use_container_width=True)unsafe_allow_html=True)

        with metrics_row4:
            fig = go.Figure(go.Indicator(st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                mode="gauge+number",", unsafe_allow_html=True)
                value=key_metrics["satisfactionScore"],
                title={'text': "Satisfaction (%)"},
                gauge={combined_labels = netagrow_data["revenueData"]["labels"] + netagrow_data["revenueData"]["forecastLabels"]
                    'axis': {'range': [None, 100]},["revenueData"]["forecast"]
                    'bar': {'color': "#2E7D32"},
                    'steps': [# Create a marker for where historical data ends and forecast begins
                        {'range': [0, 70], 'color': "#FFCDD2"},grow_data["revenueData"]["labels"]) + [True] * len(netagrow_data["revenueData"]["forecastLabels"])
                        {'range': [70, 85], 'color': "#FFECB3"},
                        {'range': [85, 100], 'color': "#E8F5E9"}art
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},  "Revenue": combined_data,
                        'thickness': 0.75,    "IsForecast": is_forecast
                        'value': 90
                    }
                }ded chart
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)') 
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
cast",
    # Add forecast metrics,
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)True,
    st.markdown("<h3>Revenue Forecast</h3>", unsafe_allow_html=True)   labels={"Revenue": "Revenue (ZMW)", "IsForecast": ""},
        title=""
    # Combine historical and forecast data
    combined_labels = netagrow_data["revenueData"]["labels"] + netagrow_data["revenueData"]["forecastLabels"]
    combined_data = netagrow_data["revenueData"]["data"] + netagrow_data["revenueData"]["forecast"]under forecast
    etagrow_data["revenueData"]["labels"]), len(combined_labels)):
    # Create a marker for where historical data ends and forecast begins
    is_forecast = [False] * len(netagrow_data["revenueData"]["labels"]) + [True] * len(netagrow_data["revenueData"]["forecastLabels"])
    
    # Create DataFrame for the chartbined_data[i],
    forecast_df = pd.DataFrame({,
        "Month": combined_labels,
        "Revenue": combined_data,   line=dict(width=0),
        "IsForecast": is_forecast        layer="below"
    })
    
    # Create color-coded chart
    fig = px.line(
        forecast_df,  b=20),
        x="Month", )',
        y="Revenue",
        color="IsForecast",lse),
        color_discrete_map={False: "#2E7D32", True: "#FFA000"},,0.1)'),
        markers=True, unified",
        labels={"Revenue": "Revenue (ZMW)", "IsForecast": ""},lor="white", font_size=12),
        title=""
    )tion="h",
    ,
    # Add shaded area under forecast02,
    for i in range(len(netagrow_data["revenueData"]["labels"]), len(combined_labels)):"right",
        fig.add_shape(   x=1,
            type="rect",       title=""
            x0=i-0.5, x1=i+0.5,    )
            y0=0, y1=combined_data[i],
            fillcolor="#FFF8E1",
            opacity=0.3,
            line=dict(width=0),
            layer="below"next_forecast = netagrow_data["revenueData"]["forecast"][0]
        )ast_actual) / last_actual) * 100
    
    fig.update_layout(l3 = st.columns(3)
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',urrent Month", 
        plot_bgcolor='rgba(0,0,0,0)',   f"ZMW {last_actual:,.0f}", 
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font_size=12),
        legend=dict(t)", 
            orientation="h",   f"ZMW {next_forecast:,.0f}", 
            yanchor="bottom",{growth_pct:.1f}%"
            y=1.02,
            xanchor="right",
            x=1,agrow_data["revenueData"]["forecast"])
            title=""
        )-Month Forecast", 
    )   f"ZMW {total_forecast:,.0f}", 
            ""
    # Add forecast metrics
    last_actual = netagrow_data["revenueData"]["data"][-1]
    next_forecast = netagrow_data["revenueData"]["forecast"][0]st.plotly_chart(fig, use_container_width=True)
    growth_pct = ((next_forecast - last_actual) / last_actual) * 100ml=True)
    
    col1, col2, col3 = st.columns(3)y feed
    with col1:st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.metric( = st.columns([1, 1])
            "Current Month", 
            f"ZMW {last_actual:,.0f}",  col1:
            "">", unsafe_allow_html=True)
        )
    with col2:# Calendar view of upcoming tasks and events
        st.metric(row_data["upcomingTasksEvents"][:10]  # Show only 10 entries
            "Next Month (Forecast)", 
            f"ZMW {next_forecast:,.0f}", t upcoming:
            f"{growth_pct:.1f}%"coming tasks or events")
        )
    with col3:
        total_forecast = sum(netagrow_data["revenueData"]["forecast"])t defaultdict
        st.metric(
            "3-Month Forecast", 
            f"ZMW {total_forecast:,.0f}",     date_str = event["date"].strftime("%Y-%m-%d")
            ""[date_str].append(event)
        )
    
    st.plotly_chart(fig, use_container_width=True)ents in sorted(events_by_date.items()):
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add calendar view and activity feednd-color: #E8F5E9; padding: 8px; border-left: 4px solid #2E7D32; margin-bottom: 10px;'>"
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)   f"<h5 style='margin-top: 0; margin-bottom: 10px;'>{date_obj.strftime('%A, %B %d')}</h5>", 
    col1, col2 = st.columns([1, 1])    unsafe_allow_html=True
    
    with col1:
        st.markdown("<h3>Upcoming Tasks & Events</h3>", unsafe_allow_html=True)
        con = "📅" if event["type"] == "event" else "✓"
        # Calendar view of upcoming tasks and events
        upcoming = netagrow_data["upcomingTasksEvents"][:10]  # Show only 10 entries
        px; display: flex; align-items: center;'>"
        if not upcoming:icon}</div>"
            st.write("No upcoming tasks or events")
        else:trong>{event['title']}</strong></div>"
            # Group by date
            from collections import defaultdict
            events_by_date = defaultdict(list)class}' style='font-size: 0.8em;'>{event['status']}</div>"
            for event in upcoming:   f"</div>",
                date_str = event["date"].strftime("%Y-%m-%d")        unsafe_allow_html=True
                events_by_date[date_str].append(event)
                
            # Display calendarsafe_allow_html=True)
            for date_str, events in sorted(events_by_date.items()):
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")if st.button("+ Add Event"):
                st.markdown(
                    f"<div style='background-color: #E8F5E9; padding: 8px; border-left: 4px solid #2E7D32; margin-bottom: 10px;'>"
                    f"<h5 style='margin-top: 0; margin-bottom: 10px;'>{date_obj.strftime('%A, %B %d')}</h5>", 
                    unsafe_allow_html=True
                )
                
                for event in events:event_type = st.selectbox("Event Type", ["Meeting", "Task", "Call", "Demo", "Other"])                 ["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T.", 
                    event_type_icon = "📅" if event["type"] == "event" else "✓"Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."])alinda B.", "Nchimunya M."])
                    status_class = get_status_class(event["status"])
                    st.markdown(ton("Save Event")ton("Save Event")
                        f"<div style='margin-bottom: 8px; display: flex; align-items: center;'>"
                        f"<div style='margin-right: 10px;'>{event_type_icon}</div>"                    st.success("Event added!")                    st.success("Event added!")
                        f"<div style='flex-grow: 1;'>"          st.session_state.show_add_event = False          st.session_state.show_add_event = False
                        f"<div><strong>{event['title']}</strong></div>"
                        f"<div style='font-size: 0.8em;'>Assigned to: {event['assignedTo']}</div>" col2: col2:
                        f"</div>"_allow_html=True)_allow_html=True)
                        f"<div class='{status_class}' style='font-size: 0.8em;'>{event['status']}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
            </div>"</div>"
            if st.button("+ Add Event"):yle='display: flex; justify-content: space-between; font-size: 0.8em; color: #757575;'>"yle='display: flex; justify-content: space-between; font-size: 0.8em; color: #757575;'>"
                st.session_state.show_add_event = True {activity['user']}</span><span>{activity['timeAgo']}</span>" {activity['user']}</span><span>{activity['timeAgo']}</span>"
            
            if st.session_state.get("show_add_event", False):   f"</div>",   f"</div>",
                with st.form("add_event_form"):    unsafe_allow_html=True    unsafe_allow_html=True
                    event_title = st.text_input("Event Title")
                    event_date = st.date_input("Event Date")                
                    event_type = st.selectbox("Event Type", ["Meeting", "Task", "Call", "Demo", "Other"])er; margin-top: 10px;'><a href='#'>View All Activity</a></div>", unsafe_allow_html=True)er; margin-top: 10px;'><a href='#'>View All Activity</a></div>", unsafe_allow_html=True)
                    event_assigned = st.selectbox("Assigned To", ["Chongo M.", "Mwape L.", "Kapembwa J.", "Nanyangwe T."])        
                    llow_html=True)llow_html=True)
                    submitted = st.form_submit_button("Save Event")
                    if submitted:
                        st.success("Event added!")us: 10px; margin-bottom: 20px;">'us: 10px; margin-bottom: 20px;">'
                        st.session_state.show_add_event = False>Sales Pipeline</h1>'>Sales Pipeline</h1>'
                    '<p style="margin: 5px 0;">Track and manage your sales opportunities</p></div>',                '<p style="margin: 5px 0;">Track and manage your sales opportunities</p></div>',
    with col2:))
        st.markdown("<h3>Recent Activity</h3>", unsafe_allow_html=True)
            # Summary metrics for the pipeline    # Summary metrics for the pipeline
        activities = netagrow_data["recentActivities"]
        
        for activity in activities[:7]:  # Show only top 7 activities
            st.markdown(
                f"<div style='border-bottom: 1px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 10px;'>"
                f"<div style='color: #2E7D32; font-weight: 500;'>{activity['activity']}</div>"    win_rate = netagrow_data["salesPipeline"]["dealCounts"][-2] / (    win_rate = netagrow_data["salesPipeline"]["dealCounts"][-2] / (
                f"<div style='display: flex; justify-content: space-between; font-size: 0.8em; color: #757575;'>"  netagrow_data["salesPipeline"]["dealCounts"][-2] + netagrow_data["salesPipeline"]["dealCounts"][-1]) * 100  netagrow_data["salesPipeline"]["dealCounts"][-2] + netagrow_data["salesPipeline"]["dealCounts"][-1]) * 100
                f"<span>by {activity['user']}</span><span>{activity['timeAgo']}</span>"
                f"</div>"
                f"</div>",True)True)
                unsafe_allow_html=True}</h2>', unsafe_allow_html=True)}</h2>', unsafe_allow_html=True)
            )        st.markdown('<h4>Total Deals</h4>', unsafe_allow_html=True)        st.markdown('<h4>Total Deals</h4>', unsafe_allow_html=True)
            kdown('</div>', unsafe_allow_html=True)kdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='#'>View All Activity</a></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)e)e)
e)}</h2>', unsafe_allow_html=True)e)}</h2>', unsafe_allow_html=True)
elif selected == "Sales Pipeline":        st.markdown('<h4>Pipeline Value</h4>', unsafe_allow_html=True)        st.markdown('<h4>Pipeline Value</h4>', unsafe_allow_html=True)
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'kdown('</div>', unsafe_allow_html=True)kdown('</div>', unsafe_allow_html=True)
                '<h1 style="margin: 0;">Sales Pipeline</h1>'
                '<p style="margin: 5px 0;">Track and manage your sales opportunities</p></div>',
                unsafe_allow_html=True)e)e)
ize)}</h2>', unsafe_allow_html=True)ize)}</h2>', unsafe_allow_html=True)
    # Summary metrics for the pipeline        st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)        st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)kdown('</div>', unsafe_allow_html=True)kdown('</div>', unsafe_allow_html=True)

    total_deals = sum(netagrow_data["salesPipeline"]["dealCounts"])
    total_value = sum(netagrow_data["salesPipeline"]["dealValues"])ml=True)ml=True)
    avg_deal_size = total_value / total_deals if total_deals > 0 else 0fe_allow_html=True)fe_allow_html=True)
    win_rate = netagrow_data["salesPipeline"]["dealCounts"][-2] / (        st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)        st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)
                netagrow_data["salesPipeline"]["dealCounts"][-2] + netagrow_data["salesPipeline"]["dealCounts"][-1]) * 100, unsafe_allow_html=True), unsafe_allow_html=True)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)_allow_html=True)_allow_html=True)
        st.markdown(f'<h2>{format_number(total_deals)}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Total Deals</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
  'Deal Value': netagrow_data["salesPipeline"]["dealValues"],  'Deal Value': netagrow_data["salesPipeline"]["dealValues"],
    with col2:        'Conversion Rate': netagrow_data["salesPipeline"]["conversionRates"]        'Conversion Rate': netagrow_data["salesPipeline"]["conversionRates"]
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_currency(total_value)}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Pipeline Value</h4>', unsafe_allow_html=True) = st.tabs(["Pipeline by Deal Count", "Pipeline by Deal Value"]) = st.tabs(["Pipeline by Deal Count", "Pipeline by Deal Value"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:n='h',n='h',
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)s'})s'})
        st.markdown(f'<h2>{format_currency(avg_deal_size)}</h2>', unsafe_allow_html=True)n=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',n=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
        st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True), xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),, xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        st.markdown('</div>', unsafe_allow_html=True)                          showlegend=False)                          showlegend=False)
tly_chart(fig, use_container_width=True)tly_chart(fig, use_container_width=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{win_rate:.1f}%</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)W)'})W)'})
n=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',n=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
    # Pipeline visualization, xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),, xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    st.markdown('<h3>Sales Pipeline Overview</h3>', unsafe_allow_html=True)                          showlegend=False)                          showlegend=False)
    pipeline_df = pd.DataFrame({
        'Stage': netagrow_data["salesPipeline"]["stages"],
        'Deal Count': netagrow_data["salesPipeline"]["dealCounts"],
        'Deal Value': netagrow_data["salesPipeline"]["dealValues"],
        'Conversion Rate': netagrow_data["salesPipeline"]["conversionRates"]rete_sequence=['#2E7D32'])rete_sequence=['#2E7D32'])
    })bgcolor='rgba(0,0,0,0)',bgcolor='rgba(0,0,0,0)',
, xaxis=dict(showgrid=False),, xaxis=dict(showgrid=False),
    tab1, tab2 = st.tabs(["Pipeline by Deal Count", "Pipeline by Deal Value"])                      yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'))                      yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'))

    with tab1:
        fig = px.bar(pipeline_df, y='Stage', x='Deal Count', color='Stage', text='Deal Count', orientation='h',    st.markdown('<h3>Add New Deal</h3>', unsafe_allow_html=True)    st.markdown('<h3>Add New Deal</h3>', unsafe_allow_html=True)
                     color_discrete_sequence=px.colors.sequential.Greens, labels={'Deal Count': 'Number of Deals'}) = st.columns(2) = st.columns(2)
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)        deal_value = st.number_input("Deal Value (ZMW)", min_value=0, step=1000)        deal_value = st.number_input("Deal Value (ZMW)", min_value=0, step=1000)
tage = st.selectbox("Stage", netagrow_data["salesPipeline"]["stages"])tage = st.selectbox("Stage", netagrow_data["salesPipeline"]["stages"])
    with tab2:
        fig = px.bar(pipeline_df, y='Stage', x='Deal Value', color='Stage',
                     text=[f'ZMW {v:,}' for v in pipeline_df['Deal Value']], orientation='h',
                     color_discrete_sequence=px.colors.sequential.Greens, labels={'Deal Value': 'Deal Value (ZMW)'})        contact_name = st.text_input("Contact Name")        contact_name = st.text_input("Contact Name")
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',xpected Close Date")xpected Close Date")
                          plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                          showlegend=False)))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3>Stage Conversion Rates</h3>', unsafe_allow_html=True)st.markdown("<div class='custom-card'>", unsafe_allow_html=True)st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    fig = px.line(pipeline_df, x='Stage', y='Conversion Rate', markers=True,low_html=True)low_html=True)
                  labels={'Conversion Rate': 'Conversion Rate (%)'}, color_discrete_sequence=['#2E7D32'])
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',sVelocityMetrics"]sVelocityMetrics"]
                      plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')), col3, col4 = st.columns(4), col3, col4 = st.columns(4)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3>Add New Deal</h3>', unsafe_allow_html=True)e)e)
    col1, col2 = st.columns(2)etrics["avgDealSize"])}</h2>', unsafe_allow_html=True)etrics["avgDealSize"])}</h2>', unsafe_allow_html=True)
st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)
    with col1:kdown('</div>', unsafe_allow_html=True)kdown('</div>', unsafe_allow_html=True)
        deal_name = st.text_input("Deal Name")
        deal_value = st.number_input("Deal Value (ZMW)", min_value=0, step=1000)
        deal_stage = st.selectbox("Stage", netagrow_data["salesPipeline"]["stages"])
Cycle"]} days</h2>', unsafe_allow_html=True)Cycle"]} days</h2>', unsafe_allow_html=True)
    with col2:st.markdown('<h4>Avg. Sales Cycle</h4>', unsafe_allow_html=True)st.markdown('<h4>Avg. Sales Cycle</h4>', unsafe_allow_html=True)
        company_name = st.text_input("Company Name")kdown('</div>', unsafe_allow_html=True)kdown('</div>', unsafe_allow_html=True)
        contact_name = st.text_input("Contact Name")
        expected_close = st.date_input("Expected Close Date")
ml=True)ml=True)
    st.button("Add Deal", key="add_deal")]}%</h2>', unsafe_allow_html=True)]}%</h2>', unsafe_allow_html=True)
st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)
    # Add sales velocity metrics sectionkdown('</div>', unsafe_allow_html=True)kdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Sales Velocity Metrics</h3>", unsafe_allow_html=True)
    e)e)
    velocity_metrics = netagrow_data["salesVelocityMetrics"]
    _allow_html=True)_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)    st.tooltip = st.markdown('<div class="tooltip">ⓘ<span class="tooltiptext">Revenue generated per day: (Deal Size × Win Rate × Deals) ÷ Sales Cycle</span></div>', unsafe_allow_html=True)    st.tooltip = st.markdown('<div class="tooltip">ⓘ<span class="tooltiptext">Revenue generated per day: (Deal Size × Win Rate × Deals) ÷ Sales Cycle</span></div>', unsafe_allow_html=True)
    rue)rue)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)low_html=True)low_html=True)
        st.markdown(f'<h2>{format_currency(velocity_metrics["avgDealSize"])}</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Avg. Deal Size</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)st.markdown("<div class='custom-card'>", unsafe_allow_html=True)st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True) "Loss Reasons", "By Product", "By Deal Size"]) "Loss Reasons", "By Product", "By Deal Size"])
        st.markdown(f'<h2>{velocity_metrics["avgSalesCycle"]} days</h2>', unsafe_allow_html=True)
        st.markdown('<h4>Avg. Sales Cycle</h4>', unsafe_allow_html=True)ata = netagrow_data["winLossAnalysis"]ata = netagrow_data["winLossAnalysis"]
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)  "Reason": win_loss_data["reasonsWon"].keys(),  "Reason": win_loss_data["reasonsWon"].keys(),
        st.markdown(f'<h2>{velocity_metrics["winRate"]}%</h2>', unsafe_allow_html=True)    "Percentage": win_loss_data["reasonsWon"].values()    "Percentage": win_loss_data["reasonsWon"].values()
        st.markdown('<h4>Win Rate</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:  
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{format_currency(velocity_metrics["velocityScore"])}/day</h2>', unsafe_allow_html=True)", ", 
        st.markdown('<h4>Velocity Score</h4>', unsafe_allow_html=True)
        st.tooltip = st.markdown('<div class="tooltip">ⓘ<span class="tooltiptext">Revenue generated per day: (Deal Size × Win Rate × Deals) ÷ Sales Cycle</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)   color_discrete_sequence=['#2E7D32'],   color_discrete_sequence=['#2E7D32'],
    on["Percentage"].apply(lambda x: f"{x}%")on["Percentage"].apply(lambda x: f"{x}%")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add win/loss analysis section
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True) b=20), b=20),
    st.markdown("<h3>Win/Loss Analysis</h3>", unsafe_allow_html=True)or='rgba(0,0,0,0)',or='rgba(0,0,0,0)',
    
    tab1, tab2, tab3, tab4 = st.tabs(["Win Reasons", "Loss Reasons", "By Product", "By Deal Size"])
    
    win_loss_data = netagrow_data["winLossAnalysis"]   showgrid=True,   showgrid=True,
           gridcolor='rgba(0,0,0,0.1)'       gridcolor='rgba(0,0,0,0.1)'
    with tab1:
        reasons_won = pd.DataFrame({    )    )
            "Reason": win_loss_data["reasonsWon"].keys(),tly_chart(fig, use_container_width=True)tly_chart(fig, use_container_width=True)
            "Percentage": win_loss_data["reasonsWon"].values()
        })
        
        fig = px.bar(  "Reason": win_loss_data["reasonsLost"].keys(),  "Reason": win_loss_data["reasonsLost"].keys(),
            reasons_won,     "Percentage": win_loss_data["reasonsLost"].values()    "Percentage": win_loss_data["reasonsLost"].values()
            x="Percentage", 
            y="Reason", 
            orientation='h',
            title="",, , 
            color_discrete_sequence=['#2E7D32'],
            text=reasons_won["Percentage"].apply(lambda x: f"{x}%")", ", 
        )
        fig.update_layout(
            height=300,   color_discrete_sequence=['#C62828'],   color_discrete_sequence=['#C62828'],
            margin=dict(l=20, r=20, t=20, b=20),ost["Percentage"].apply(lambda x: f"{x}%")ost["Percentage"].apply(lambda x: f"{x}%")
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title="Percentage of Wins", b=20), b=20),
                showgrid=True,or='rgba(0,0,0,0)',or='rgba(0,0,0,0)',
                gridcolor='rgba(0,0,0,0.1)'
            )
        )",",
        st.plotly_chart(fig, use_container_width=True)   showgrid=True,   showgrid=True,
           gridcolor='rgba(0,0,0,0.1)'       gridcolor='rgba(0,0,0,0.1)'
    with tab2:
        reasons_lost = pd.DataFrame({    )    )
            "Reason": win_loss_data["reasonsLost"].keys(),tly_chart(fig, use_container_width=True)tly_chart(fig, use_container_width=True)
            "Percentage": win_loss_data["reasonsLost"].values()
        })
        
        fig = px.bar(
            reasons_lost, 
            x="Percentage",   {"Product": product, "Status": "Won", "Percentage": data["won"]},  {"Product": product, "Status": "Won", "Percentage": data["won"]},
            y="Reason",         {"Product": product, "Status": "Lost", "Percentage": data["lost"]}        {"Product": product, "Status": "Lost", "Percentage": data["lost"]}
            orientation='h',
            title="",
            color_discrete_sequence=['#C62828'], = pd.DataFrame(by_product_data) = pd.DataFrame(by_product_data)
            text=reasons_lost["Percentage"].apply(lambda x: f"{x}%")
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(   color_discrete_map={"Won": "#2E7D32", "Lost": "#C62828"},   color_discrete_map={"Won": "#2E7D32", "Lost": "#C62828"},
                title="Percentage of Losses",t_df["Percentage"].apply(lambda x: f"{x}%")t_df["Percentage"].apply(lambda x: f"{x}%")
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        ) b=20), b=20),
        st.plotly_chart(fig, use_container_width=True))',)',
    r='rgba(0,0,0,0)',r='rgba(0,0,0,0)',
    with tab3:se),se),
        by_product_data = []
        for product, data in win_loss_data["byProduct"].items():
            by_product_data.extend([   showgrid=True,   showgrid=True,
                {"Product": product, "Status": "Won", "Percentage": data["won"]},       gridcolor='rgba(0,0,0,0.1)'       gridcolor='rgba(0,0,0,0.1)'
                {"Product": product, "Status": "Lost", "Percentage": data["lost"]}
            ])    )    )
        tly_chart(fig, use_container_width=True)tly_chart(fig, use_container_width=True)
        by_product_df = pd.DataFrame(by_product_data)
        
        fig = px.bar(
            by_product_df,
            x="Product",
            y="Percentage",  {"Deal Size": size, "Status": "Won", "Percentage": data["won"]},  {"Deal Size": size, "Status": "Won", "Percentage": data["won"]},
            color="Status",        {"Deal Size": size, "Status": "Lost", "Percentage": data["lost"]}        {"Deal Size": size, "Status": "Lost", "Percentage": data["lost"]}
            barmode="group",
            color_discrete_map={"Won": "#2E7D32", "Lost": "#C62828"},
            text=by_product_df["Percentage"].apply(lambda x: f"{x}%")df = pd.DataFrame(by_deal_size_data)df = pd.DataFrame(by_deal_size_data)
        )
        fig.update_layout(
            height=300,,,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Percentage",   text=by_deal_size_df["Percentage"].apply(lambda x: f"{x}%"),   text=by_deal_size_df["Percentage"].apply(lambda x: f"{x}%"),
                showgrid=True,s={"Deal Size": ["Small (<ZMW 10K)", "Medium (ZMW 10-50K)", "Large (>ZMW 50K)"]}s={"Deal Size": ["Small (<ZMW 10K)", "Medium (ZMW 10-50K)", "Large (>ZMW 50K)"]}
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        st.plotly_chart(fig, use_container_width=True) b=20), b=20),
    )',)',
    with tab4:r='rgba(0,0,0,0)',r='rgba(0,0,0,0)',
        by_deal_size_data = []se),se),
        for size, data in win_loss_data["byDealSize"].items():
            by_deal_size_data.extend([
                {"Deal Size": size, "Status": "Won", "Percentage": data["won"]},   showgrid=True,   showgrid=True,
                {"Deal Size": size, "Status": "Lost", "Percentage": data["lost"]}       gridcolor='rgba(0,0,0,0.1)'       gridcolor='rgba(0,0,0,0.1)'
            ])
            )    )
        by_deal_size_df = pd.DataFrame(by_deal_size_data)True)True)
        
        fig = px.bar(tml=True)tml=True)
            by_deal_size_df,
            x="Deal Size",
            y="Percentage",st.markdown("<div class='custom-card'>", unsafe_allow_html=True)st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            color="Status",3>Pipeline Management</h3>", unsafe_allow_html=True)3>Pipeline Management</h3>", unsafe_allow_html=True)
            barmode="group",
            color_discrete_map={"Won": "#2E7D32", "Lost": "#C62828"},
            text=by_deal_size_df["Percentage"].apply(lambda x: f"{x}%"),
            category_orders={"Deal Size": ["Small (<ZMW 10K)", "Medium (ZMW 10-50K)", "Large (>ZMW 50K)"]}>🔄 Drag and drop functionality requires additional JavaScript integration. In a full implementation, >🔄 Drag and drop functionality requires additional JavaScript integration. In a full implementation, 
        )g deals between pipeline stages, with state updates managed by the backend.</p>g deals between pipeline stages, with state updates managed by the backend.</p>
        fig.update_layout(</div></div>
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',    # Create columns for each pipeline stage    # Create columns for each pipeline stage
            plot_bgcolor='rgba(0,0,0,0)',tagrow_data["salesPipeline"]["stages"]))tagrow_data["salesPipeline"]["stages"]))
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Percentage",us: 10px; margin-bottom: 20px;">'us: 10px; margin-bottom: 20px;">'
                showgrid=True,>Contact Management</h1>'>Contact Management</h1>'
                gridcolor='rgba(0,0,0,0.1)'                '<p style="margin: 5px 0;">Manage your customer and partner contacts</p></div>',                '<p style="margin: 5px 0;">Manage your customer and partner contacts</p></div>',
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True) border-collapse: collapse;'>" border-collapse: collapse;'>"
    
    # Add drag-and-drop pipeline section_df.iterrows():_df.iterrows():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)td><td>{contact['company']}</td><td>{contact['location']}</td><td>{contact['email']}</td><td>{contact['phone']}</td></tr>"td><td>{contact['company']}</td><td>{contact['location']}</td><td>{contact['email']}</td><td>{contact['phone']}</td></tr>"
    st.markdown("<h3>Pipeline Management</h3>", unsafe_allow_html=True)    contact_html += "</table>"    contact_html += "</table>"
    
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 20px;">ntact", key="add_new_contact")ntact", key="add_new_contact")
        <p>🔄 Drag and drop functionality requires additional JavaScript integration. In a full implementation, 
        you would be able to drag deals between pipeline stages, with state updates managed by the backend.</p>
    </div>rder-radius: 10px; margin-bottom: 20px;">'rder-radius: 10px; margin-bottom: 20px;">'
    """, unsafe_allow_html=True)>Task Management</h1>'>Task Management</h1>'
                    '<p style="margin: 5px 0;">Manage your tasks and activities</p></div>',                '<p style="margin: 5px 0;">Manage your tasks and activities</p></div>',
    # Create columns for each pipeline stage
    cols = st.columns(len(netagrow_data["salesPipeline"]["stages"]))

elif selected == "Contacts":0%; border-collapse: collapse;'>"0%; border-collapse: collapse;'>"
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'<th>Status</th><th>Due Date</th></tr>"<th>Status</th><th>Due Date</th></tr>"
                '<h1 style="margin: 0;">Contact Management</h1>'
                '<p style="margin: 5px 0;">Manage your customer and partner contacts</p></div>',
                unsafe_allow_html=True) class='{status_class}'>{task['status']}</td>" class='{status_class}'>{task['status']}</td>"
<td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"<td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"
    st.markdown('<h3>Contact List</h3>', unsafe_allow_html=True)    task_html += "</table>"    task_html += "</table>"
    contacts_df = pd.DataFrame(netagrow_data["contactManagement"]["contacts"])))
    contact_html = "<table style='width:100%; border-collapse: collapse;'>"
    contact_html += "<tr><th>Name</th><th>Company</th><th>Location</th><th>Email</th><th>Phone</th></tr>" key="add_new_task") key="add_new_task")
    for _, contact in contacts_df.iterrows():
        contact_html += f"<tr><td>{contact['name']}</td><td>{contact['company']}</td><td>{contact['location']}</td><td>{contact['email']}</td><td>{contact['phone']}</td></tr>"
    contact_html += "</table>"order-radius: 10px; margin-bottom: 20px;">'order-radius: 10px; margin-bottom: 20px;">'
    st.markdown(contact_html, unsafe_allow_html=True)>Campaign Management</h1>'>Campaign Management</h1>'
                '<p style="margin: 5px 0;">Manage your marketing campaigns</p></div>',                '<p style="margin: 5px 0;">Manage your marketing campaigns</p></div>',
    st.button("Add New Contact", key="add_new_contact")

elif selected == "Tasks":
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'border-collapse: collapse;'>"border-collapse: collapse;'>"
                '<h1 style="margin: 0;">Task Management</h1>'/th><th>Target Audience</th></tr>"/th><th>Target Audience</th></tr>"
                '<p style="margin: 5px 0;">Manage your tasks and activities</p></div>',
                unsafe_allow_html=True)
ss='{status_class}'>{campaign['status']}</td>"ss='{status_class}'>{campaign['status']}</td>"
    tasks_df = pd.DataFrame(netagrow_data["taskActivityTracking"]["activities"])/td>{status_html}<td>{campaign['targetAudience']}</td></tr>"/td>{status_html}<td>{campaign['targetAudience']}</td></tr>"
    task_html = "<table style='width:100%; border-collapse: collapse;'>"    campaign_html += "</table>"    campaign_html += "</table>"
    task_html += "<tr><th>Task</th><th>Assigned To</th><th>Status</th><th>Due Date</th></tr>"
    for _, task in tasks_df.iterrows():
        status_class = get_status_class(task["status"])ign", key="add_new_campaign")ign", key="add_new_campaign")
        status_html = f"<td class='{status_class}'>{task['status']}</td>"
        task_html += f"<tr><td>{task['task']}</td><td>{task['assignedTo']}</td>{status_html}<td>{task['dueDate']}</td></tr>"
    task_html += "</table>"x; border-radius: 10px; margin-bottom: 20px;">'x; border-radius: 10px; margin-bottom: 20px;">'
    st.markdown(task_html, unsafe_allow_html=True)>Settings</h1>'>Settings</h1>'
                '<p style="margin: 5px 0;">Configure your CRM settings</p></div>',                '<p style="margin: 5px 0;">Configure your CRM settings</p></div>',
    st.button("Add New Task", key="add_new_task")

elif selected == "Campaigns":Settings</h3>', unsafe_allow_html=True)Settings</h3>', unsafe_allow_html=True)
    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'
                '<h1 style="margin: 0;">Campaign Management</h1>'    st.text_input("Email")    st.text_input("Email")
                '<p style="margin: 5px 0;">Manage your marketing campaigns</p></div>',
                unsafe_allow_html=True)
3>', unsafe_allow_html=True)3>', unsafe_allow_html=True)
    campaigns_df = pd.DataFrame(netagrow_data["salesMarketingTools"]["activeCampaigns"])ish", "French", "Spanish"])ish", "French", "Spanish"])
    campaign_html = "<table style='width:100%; border-collapse: collapse;'>"    st.checkbox("Enable Notifications")    st.checkbox("Enable Notifications")
    campaign_html += "<tr><th>Campaign Name</th><th>Status</th><th>Target Audience</th></tr>"
    for _, campaign in campaigns_df.iterrows():


























    st.button("Save Settings", key="save_settings")    st.checkbox("Enable Dark Mode")    st.checkbox("Enable Notifications")    st.selectbox("Language", ["English", "French", "Spanish"])    st.markdown('<h3>System Settings</h3>', unsafe_allow_html=True)    st.text_input("Password", type="password")    st.text_input("Email")    st.text_input("Username")    st.markdown('<h3>User Settings</h3>', unsafe_allow_html=True)                unsafe_allow_html=True)                '<p style="margin: 5px 0;">Configure your CRM settings</p></div>',                '<h1 style="margin: 0;">Settings</h1>'    st.markdown('<div style="background-color: #2E7D32; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">'elif selected == "Settings":    st.button("Add New Campaign", key="add_new_campaign")    st.markdown(campaign_html, unsafe_allow_html=True)    campaign_html += "</table>"        campaign_html += f"<tr><td>{campaign['name']}</td>{status_html}<td>{campaign['targetAudience']}</td></tr>"        status_html = f"<td class='{status_class}'>{campaign['status']}</td>"        status_class = get_status_class(campaign["status"])

    st.button("Save Settings", key="save_settings")    st.button("Save Settings", key="save_settings")
