import streamlit as st
import requests
import json
import random
from datetime import datetime
import pandas as pd
import uuid
import pycountry
import time

# Set up page configuration
st.set_page_config(
    page_title="Investment License Analysis",
    page_icon="📊",
    layout="wide"
)

# Load CSV data
@st.cache_data
def load_csv_data():
    try:
        df = pd.read_csv('kdipa_arf.csv')
        # Clean up the dataframe - remove empty rows
        df = df.dropna(how='all')
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return pd.DataFrame()

# Get list of country codes for dropdowns
def get_country_list():
    countries = [(country.alpha_2, f"{country.name} ({country.alpha_2})") for country in pycountry.countries]
    countries.sort(key=lambda x: x[1])
    return countries

COUNTRY_LIST = get_country_list()
COUNTRY_CODES = [code for code, _ in COUNTRY_LIST]
COUNTRY_NAMES = {code: name for code, name in COUNTRY_LIST}

# IMPROVEMENT 4: Improved random data generation with more realistic values
def get_random_csv_values():
    df = load_csv_data()
    
    if df.empty:
        # Fallback to original random generation if CSV is empty
        return generate_fallback_random_values()
    
    # Select a random row
    random_row = df.sample(1).iloc[0]
    
    # Generate fallback random values
    fallback_values = generate_fallback_random_values()
    
    # Map CSV values to form fields, with fallback to random values if field is not in CSV
    random_values = {}
    
    # Company details
    random_values["companyName"] = random_row.get("companyName") if "companyName" in random_row and pd.notna(random_row["companyName"]) else fallback_values["companyName"]
    random_values["companyOrigin"] = random_row.get("companyOrigin") if "companyOrigin" in random_row and pd.notna(random_row["companyOrigin"]) else fallback_values["companyOrigin"]
    random_values["companyCity"] = random_row.get("companyCity") if "companyCity" in random_row and pd.notna(random_row["companyCity"]) else fallback_values["companyCity"]
    random_values["companyStreet"] = random_row.get("companyStreet") if "companyStreet" in random_row and pd.notna(random_row["companyStreet"]) else fallback_values["companyStreet"]
    random_values["companyBuilding"] = random_row.get("companyBuilding") if "companyBuilding" in random_row and pd.notna(random_row["companyBuilding"]) else fallback_values["companyBuilding"]
    random_values["companyPostalAddress"] = random_row.get("companyPostalAddress") if "companyPostalAddress" in random_row and pd.notna(random_row["companyPostalAddress"]) else fallback_values["companyPostalAddress"]
    random_values["companyOutput"] = random_row.get("companyOutput") if "companyOutput" in random_row and pd.notna(random_row["companyOutput"]) else fallback_values["companyOutput"]
    
    # Financial details
    random_values["cashAmount"] = float(random_row.get("cashAmount")) if "cashAmount" in random_row and pd.notna(random_row["cashAmount"]) else fallback_values["cashAmount"]
    random_values["contributionAmount"] = float(random_row.get("contributionAmount")) if "contributionAmount" in random_row and pd.notna(random_row["contributionAmount"]) else fallback_values["contributionAmount"]
    random_values["totalCapitalAmount"] = float(random_row.get("totalCapitalAmount")) if "totalCapitalAmount" in random_row and pd.notna(random_row["totalCapitalAmount"]) else fallback_values["totalCapitalAmount"]
    random_values["capitalExpenditure"] = float(random_row.get("capitalExpenditure")) if "capitalExpenditure" in random_row and pd.notna(random_row["capitalExpenditure"]) else fallback_values["capitalExpenditure"]
    random_values["operatingExpense"] = float(random_row.get("operatingExpense")) if "operatingExpense" in random_row and pd.notna(random_row["operatingExpense"]) else fallback_values["operatingExpense"]
    random_values["fixedAssets"] = float(random_row.get("fixedAssets")) if "fixedAssets" in random_row and pd.notna(random_row["fixedAssets"]) else fallback_values["fixedAssets"]
    random_values["totalInvestmentValue"] = float(random_row.get("totalInvestmentValue")) if "totalInvestmentValue" in random_row and pd.notna(random_row["totalInvestmentValue"]) else fallback_values["totalInvestmentValue"]
    
    # Shareholder information
    random_values["shareholderCompanyPartnerName"] = random_row.get("shareholderCompanyPartnerName") if "shareholderCompanyPartnerName" in random_row and pd.notna(random_row["shareholderCompanyPartnerName"]) else fallback_values["shareholderCompanyPartnerName"]
    random_values["shareholderNationality"] = random_row.get("shareholderNationality") if "shareholderNationality" in random_row and pd.notna(random_row["shareholderNationality"]) else fallback_values["shareholderNationality"]
    random_values["shareValue"] = float(random_row.get("shareValue")) if "shareValue" in random_row and pd.notna(random_row["shareValue"]) else fallback_values["shareValue"]
    random_values["valueOfEquityOrShares"] = float(random_row.get("valueOfEquityOrShares")) if "valueOfEquityOrShares" in random_row and pd.notna(random_row["valueOfEquityOrShares"]) else fallback_values["valueOfEquityOrShares"]
    random_values["percentageOfEquityOrShares"] = float(random_row.get("percentageOfEquityOrShares")) if "percentageOfEquityOrShares" in random_row and pd.notna(random_row["percentageOfEquityOrShares"]) else fallback_values["percentageOfEquityOrShares"]
    random_values["numberOfEquityOrShares"] = int(float(random_row.get("numberOfEquityOrShares"))) if "numberOfEquityOrShares" in random_row and pd.notna(random_row["numberOfEquityOrShares"]) else fallback_values["numberOfEquityOrShares"]
    
    # Contribution type
    if "contributionType_cash" in random_row and pd.notna(random_row["contributionType_cash"]):
        random_values["contributionType"] = {"cash": bool(random_row["contributionType_cash"])}
    else:
        random_values["contributionType"] = fallback_values["contributionType"]
    
    # Incentives
    random_values["incentives"] = bool(random_row.get("incentives")) if "incentives" in random_row and pd.notna(random_row["incentives"]) else fallback_values["incentives"]
    
    if "incentiveType_exemptionFromIncomeTax" in random_row and pd.notna(random_row["incentiveType_exemptionFromIncomeTax"]):
        random_values["incentiveType"] = {"exemptionFromIncomeTax": bool(random_row["incentiveType_exemptionFromIncomeTax"])}
    else:
        random_values["incentiveType"] = fallback_values["incentiveType"]
    
    random_values["preferredIncentive"] = random_row.get("preferredIncentive") if "preferredIncentive" in random_row and pd.notna(random_row["preferredIncentive"]) else fallback_values["preferredIncentive"]
    
    # Terms and conditions
    random_values["termsAndConditions"] = bool(random_row.get("termsAndConditions")) if "termsAndConditions" in random_row and pd.notna(random_row["termsAndConditions"]) else fallback_values["termsAndConditions"]
    
    # Application metadata
    random_values["appType"] = random_row.get("appType") if "appType" in random_row and pd.notna(random_row["appType"]) else fallback_values["appType"]
    random_values["licenseType"] = random_row.get("licenseType") if "licenseType" in random_row and pd.notna(random_row["licenseType"]) else fallback_values["licenseType"]
    random_values["submissionDate"] = random_row.get("submissionDate") if "submissionDate" in random_row and pd.notna(random_row["submissionDate"]) else fallback_values["submissionDate"]
    
    # Store the original CSV row for debugging
    random_values["_original_csv_row"] = random_row.to_dict()
    
    return random_values

# IMPROVEMENT 4: Better random data generation with more realistic values
def generate_fallback_random_values():
    # More realistic company names
    company_types = ["Technologies", "Solutions", "Industries", "Group", "Holdings", "Investments", "International", "Corporation"]
    company_prefixes = ["Global", "Advanced", "Elite", "Prime", "Superior", "Next-Gen", "Innovative", "Strategic"]
    company_core = ["Tech", "Data", "Energy", "Trade", "Construct", "Finance", "Med", "Agri", "Petro", "Eco"]
    
    # Generate a more realistic company name
    company_name = f"{random.choice(company_prefixes)} {random.choice(company_core)} {random.choice(company_types)}"
    
    # Ensure financial values are internally consistent
    share_value = round(random.uniform(10, 100), 2)
    number_of_shares = random.randint(1000, 10000)
    value_of_shares = round(share_value * number_of_shares, 2)
    
    # Base capital expenditure
    capital_expenditure = round(random.uniform(500000, 5000000), 2)
    
    # Operating expense typically 20-40% of capital expenditure
    operating_expense = round(capital_expenditure * random.uniform(0.2, 0.4), 2)
    
    # Fixed assets typically 40-60% of capital expenditure
    fixed_assets = round(capital_expenditure * random.uniform(0.4, 0.6), 2)
    
    # Total investment = capital + operating + some margin
    total_investment = round(capital_expenditure + operating_expense + random.uniform(100000, 1000000), 2)
    
    random_values = {
        "companyName": company_name,
        "companyOrigin": random.choice(COUNTRY_CODES),
        "companyCity": random.choice(["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Fujairah", "Kuwait City", "Doha", "Riyadh", "Manama"]),
        "companyStreet": f"{random.choice(['Sheikh Zayed', 'Al Wasl', 'Jumeirah', 'Al Maktoum', 'Al Fahidi'])} Road",
        "companyBuilding": f"{random.choice(['Al Fattan', 'Emirates', 'Business Central', 'Dubai Gate', 'Marina Plaza'])} Tower {random.choice(['A', 'B', 'C'])}",
        "companyPostalAddress": f"P.O. Box {random.randint(10000, 99999)}",
        "companyOutput": f"Manufacturing and distribution of {random.choice(['advanced electronic components', 'industrial automation systems', 'renewable energy solutions', 'medical equipment', 'construction materials', 'consumer electronics'])}",
        "cashAmount": round(random.uniform(100000, 1000000), 2),
        "contributionAmount": round(random.uniform(50000, 500000), 2),
        "totalCapitalAmount": round(random.uniform(500000, 5000000), 2),
        "capitalExpenditure": capital_expenditure,
        "operatingExpense": operating_expense,
        "fixedAssets": fixed_assets,
        "totalInvestmentValue": total_investment,
        "shareholderCompanyPartnerName": f"{random.choice(['Al', 'Bin', 'El', 'Abu'])} {random.choice(['Mohammed', 'Ahmed', 'Saeed', 'Sultan', 'Khalid'])} {random.choice(['Holding', 'Investment', 'Group', 'Partners'])}",
        "shareholderNationality": random.choice(COUNTRY_CODES),
        "shareValue": share_value,
        "valueOfEquityOrShares": value_of_shares,
        "percentageOfEquityOrShares": round(random.uniform(10, 100), 2),
        "numberOfEquityOrShares": number_of_shares,
        "contributionType": {"cash": True},
        "incentives": random.choice([True, False]),
        "incentiveType": {"exemptionFromIncomeTax": random.choice([True, False])},
        "preferredIncentive": random.choice(["Tax Exemption", "Land Allocation", "Reduced Fees", "None"]),
        "termsAndConditions": True,
        "appType": "ApplicationInvestmentLicenseA",
        "licenseType": "ApplicationInvestmentLicenseA",
        "submissionDate": datetime.now().isoformat()
    }
    return random_values

# IMPROVEMENT 1: Enhanced Error Handling
def analyze_application(application_data):
    api_url = "https://webapp-kdipa-ai-ajazdff5c3facrf9.switzerlandnorth-01.azurewebsites.net/analyze-application"
    payload = {
        "application_data": application_data,
        "filter_expr": None,
        "top_similar": 3
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # IMPROVEMENT 3: Progress feedback during API call
        with st.status("Analyzing application...") as status:
            status.update(label="Preparing application data...", state="running", expanded=True)
            time.sleep(0.5)  # Simulate processing time
            
            status.update(label="Connecting to analysis service...", state="running")
            time.sleep(0.5)  # Simulate connection time
            
            status.update(label="Sending data for analysis...", state="running")
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            
            status.update(label="Processing results...", state="running")
            time.sleep(0.5)  # Simulate processing time

            if response.status_code == 200:
                status.update(label="Analysis complete!", state="complete")
                return response.json()
            elif response.status_code == 400:
                status.update(label="Analysis failed - Invalid data", state="error")
                st.error(f"Bad Request (400): The server couldn't process your application data. Please check your inputs.")
                try:
                    error_details = response.json()
                    st.error(f"Error details: {error_details.get('detail', 'No details provided')}")
                except:
                    st.error(f"Error details: {response.text}")
                return None
            elif response.status_code == 401 or response.status_code == 403:
                status.update(label="Analysis failed - Authentication error", state="error")
                st.error(f"Authentication Error ({response.status_code}): Not authorized to access the analysis service.")
                return None
            elif response.status_code == 404:
                status.update(label="Analysis failed - Service not found", state="error")
                st.error("Error 404: The analysis service endpoint could not be found. Please contact support.")
                return None
            elif response.status_code >= 500:
                status.update(label="Analysis failed - Server error", state="error")
                st.error(f"Server Error ({response.status_code}): The analysis service is experiencing issues. Please try again later.")
                return None
            else:
                status.update(label="Analysis failed", state="error")
                st.error(f"Unexpected Error: {response.status_code} - {response.text}")
                return None
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Could not connect to the analysis service. Please check your internet connection and try again.")
        return None
    except requests.exceptions.Timeout:
        st.error("Timeout Error: The request to the analysis service timed out. The service might be experiencing high traffic or issues.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return None

# Function to prepare application data from form input
def prepare_application_data(form_data):
    # Clean and prepare the data to match expected schema
    application_data = {
        "uuid": str(uuid.uuid4()),
        **form_data,
        "submissionDate": datetime.now().isoformat()
    }
    
    # Ensure numeric values are floats
    numeric_fields = [
        "cashAmount", "contributionAmount", "totalCapitalAmount", 
        "capitalExpenditure", "operatingExpense", "fixedAssets", 
        "totalInvestmentValue", "shareValue", "valueOfEquityOrShares", 
        "percentageOfEquityOrShares", "numberOfEquityOrShares"
    ]
    
    for field in numeric_fields:
        if field in application_data and application_data[field]:
            try:
                application_data[field] = float(application_data[field])
            except (ValueError, TypeError):
                application_data[field] = 0.0
    
    return application_data

# Function to clear form fields
def clear_form():
    if 'random_values' in st.session_state:
        del st.session_state.random_values
    
    # Clear application data and analysis result
    st.session_state.application_data = None
    st.session_state.analysis_result = None
    
    # Rerun the app to refresh the form
    st.rerun()

# IMPROVEMENT 2: Form validation
def validate_form_data(form_data):
    errors = []
    
    # Required fields validation
    required_fields = ["companyName", "companyOrigin", "shareholderCompanyPartnerName", "shareholderNationality"]
    for field in required_fields:
        if not form_data.get(field):
            errors.append(f"{field.replace('company', 'Company ').replace('shareholder', 'Shareholder ')} is required.")
    
    # Financial validation
    if form_data.get("numberOfEquityOrShares", 0) > 0 and form_data.get("shareValue", 0) > 0:
        calculated_value = form_data.get("numberOfEquityOrShares", 0) * form_data.get("shareValue", 0)
        declared_value = form_data.get("valueOfEquityOrShares", 0)
        
        # Check if there's a significant discrepancy (more than 5%)
        if abs(calculated_value - declared_value) / (calculated_value + 0.01) > 0.05:
            errors.append(f"Share value discrepancy detected: {form_data.get('numberOfEquityOrShares')} shares × {form_data.get('shareValue')} AED per share = {calculated_value} AED, but declared value is {declared_value} AED.")
    
    # Percentage validation
    if form_data.get("percentageOfEquityOrShares", 0) > 100:
        errors.append("Percentage of equity/shares cannot exceed 100%.")
    
    # Investment validation
    total_investment = form_data.get("totalInvestmentValue", 0)
    cap_ex = form_data.get("capitalExpenditure", 0)
    op_ex = form_data.get("operatingExpense", 0)
    
    if total_investment > 0 and (cap_ex + op_ex) > 0 and (cap_ex + op_ex) > total_investment * 1.5:
        errors.append(f"Total investment value ({total_investment} AED) seems inconsistent with capital expenditure ({cap_ex} AED) and operating expenses ({op_ex} AED).")
    
    return errors

# Application title and description
st.title("Investment License Analysis")

# IMPROVEMENT 5: Better user experience with context and instructions
with st.expander("About this application", expanded=False):
    st.markdown("""
    ## Investment License Analysis Tool
    
    This application helps evaluate investment license applications for potential approval. 
    
    ### How to use:
    1. Fill out the application form with company and investment details
    2. Use the "Get Data" button to pre-fill with sample data if needed
    3. Review all fields for accuracy
    4. Submit your application for analysis
    5. View results and recommendations
    
    The analysis will evaluate your application based on multiple factors and provide recommendations.
    """)

st.markdown("Complete the application form below to analyze your investment license application.")

# Initialize session state for application data
if 'application_data' not in st.session_state:
    st.session_state.application_data = None

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Create a form with tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Company Details", "Financial Details", "Shareholder Information", "Submission", "Debug"])

# Create form for user input
with st.form("application_form", clear_on_submit=False):
    # Random values generator and Clear Form buttons
    col1, col2 = st.columns(2)
    with col1:
        random_button = st.form_submit_button("Get Data", type="secondary")
    with col2:
        clear_button = st.form_submit_button("Clear Form", type="secondary")
    
    if random_button:
        st.session_state.random_values = get_random_csv_values()
    
    if clear_button:
        clear_form()
    
    # Initialize random values if not in session state
    if 'random_values' not in st.session_state:
        st.session_state.random_values = {}
    
    # Helper function to get a random value
    def get_random_value(key, default=""):
        return st.session_state.random_values.get(key, default) if hasattr(st.session_state, 'random_values') else default
    
    # Tab 1: Company Details
    with tab1:
        st.header("Company Details")
        
        # IMPROVEMENT 5: Adding tooltips and better field organization
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name", 
                value=get_random_value("companyName"),
                help="Enter the legal name of the company applying for the license"
            )
            
            company_origin = st.selectbox(
                "Country of Origin", 
                options=[code for code, _ in COUNTRY_LIST],
                format_func=lambda x: COUNTRY_NAMES.get(x, x),
                index=COUNTRY_CODES.index(get_random_value("companyOrigin")) if get_random_value("companyOrigin") in COUNTRY_CODES else 0,
                help="Select the country where the company is legally registered"
            )
            
            company_city = st.text_input(
                "City", 
                value=get_random_value("companyCity"),
                help="City where the company headquarters is located"
            )
            
            company_street = st.text_input(
                "Street Address", 
                value=get_random_value("companyStreet"),
                help="Main street address of the company"
            )
        
        with col2:
            company_building = st.text_input(
                "Building Name", 
                value=get_random_value("companyBuilding"),
                help="Building name or number"
            )
            
            company_postal = st.text_input(
                "Postal Address", 
                value=get_random_value("companyPostalAddress"),
                help="P.O. Box or postal code for correspondence"
            )
            
            company_output = st.text_area(
                "Company Output (Description)", 
                value=get_random_value("companyOutput"),
                help="Describe the main products or services the company provides"
            )
    
    # Tab 2: Financial Details
    with tab2:
        st.header("Financial Details")
        
        # IMPROVEMENT 5: Adding descriptions for financial terms
        st.info("All financial values should be entered in AED (United Arab Emirates Dirham)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cash_amount = st.number_input(
                "Cash Amount (AED)", 
                min_value=0.0, 
                value=float(get_random_value("cashAmount", 0.0)),
                format="%.2f",
                help="Liquid cash available for investment"
            )
            
            contribution_amount = st.number_input(
                "Contribution Amount (AED)", 
                min_value=0.0, 
                value=float(get_random_value("contributionAmount", 0.0)),
                format="%.2f",
                help="Total amount being contributed to the investment"
            )
            
            total_capital_amount = st.number_input(
                "Total Capital Amount (AED)", 
                min_value=0.0, 
                value=float(get_random_value("totalCapitalAmount", 0.0)),
                format="%.2f",
                help="Total capital of the company"
            )
            
            capital_expenditure = st.number_input(
                "Capital Expenditure (AED)", 
                min_value=0.0, 
                value=float(get_random_value("capitalExpenditure", 0.0)),
                format="%.2f",
                help="Funds used to acquire or upgrade physical assets (property, equipment, etc.)"
            )
        
        with col2:
            operating_expense = st.number_input(
                "Operating Expense (AED)", 
                min_value=0.0, 
                value=float(get_random_value("operatingExpense", 0.0)),
                format="%.2f",
                help="Ongoing costs for running the business (rent, salaries, utilities, etc.)"
            )
            
            fixed_assets = st.number_input(
                "Fixed Assets (AED)", 
                min_value=0.0, 
                value=float(get_random_value("fixedAssets", 0.0)),
                format="%.2f",
                help="Long-term tangible assets (property, equipment, vehicles, etc.)"
            )
            
            total_investment_value = st.number_input(
                "Total Investment Value (AED)", 
                min_value=0.0, 
                value=float(get_random_value("totalInvestmentValue", 0.0)),
                format="%.2f",
                help="Total value of the investment being proposed"
            )
    
    # Tab 3: Shareholder Information
    with tab3:
        st.header("Shareholder Information")
        col1, col2 = st.columns(2)
        
        with col1:
            shareholder_name = st.text_input(
                "Shareholder/Company Partner Name", 
                value=get_random_value("shareholderCompanyPartnerName"),
                help="Name of the primary shareholder or partner company"
            )
            
            shareholder_nationality = st.selectbox(
                "Nationality", 
                options=[code for code, _ in COUNTRY_LIST],
                format_func=lambda x: COUNTRY_NAMES.get(x, x),
                index=COUNTRY_CODES.index(get_random_value("shareholderNationality")) if get_random_value("shareholderNationality") in COUNTRY_CODES else 0,
                help="Country of nationality for the shareholder (individual) or registration (company)"
            )
            
            share_value = st.number_input(
                "Share Value per Unit (AED)", 
                min_value=0.0, 
                value=float(get_random_value("shareValue", 0.0)),
                format="%.2f",
                help="Value of each individual share"
            )
            
            value_of_shares = st.number_input(
                "Total Value of Equity/Shares (AED)", 
                min_value=0.0, 
                value=float(get_random_value("valueOfEquityOrShares", 0.0)),
                format="%.2f",
                help="Total value of all shares (should approximately equal share value × number of shares)"
            )
        
        with col2:
            percentage_of_shares = st.number_input(
                "Percentage of Equity/Shares (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=float(get_random_value("percentageOfEquityOrShares", 0.0)),
                format="%.2f",
                help="Percentage of total company shares owned by this shareholder"
            )
            
            number_of_shares = st.number_input(
                "Number of Shares", 
                min_value=0, 
                value=int(float(get_random_value("numberOfEquityOrShares", 0))),
                step=1,
                help="Total number of shares owned by this shareholder"
            )
            
            st.subheader("Contribution Type")
            cash_contribution = st.checkbox(
                "Cash Contribution", 
                value=get_random_value("contributionType", {}).get("cash", False),
                help="Check if the contribution is in cash form"
            )

    # Tab 4: Incentives and Legal
    with tab4:
        st.header("Incentives")
        incentives_requested = st.checkbox("Are Incentives Requested?", 
                                         value=get_random_value("incentives", False))
        
        if incentives_requested:
            exemption_income_tax = st.checkbox("Exemption From Income Tax", 
                                             value=get_random_value("incentiveType", {}).get("exemptionFromIncomeTax", False))
            
            preferred_incentive = st.selectbox(
                "Preferred Incentive", 
                options=["Tax Exemption", "Land Allocation", "Reduced Fees", "None"],
                index=["Tax Exemption", "Land Allocation", "Reduced Fees", "None"].index(get_random_value("preferredIncentive", "None")) if get_random_value("preferredIncentive", "None") in ["Tax Exemption", "Land Allocation", "Reduced Fees", "None"] else 0
            )
        else:
            exemption_income_tax = False
            preferred_incentive = "None"
        
        st.header("Legal/Consent")
        terms_conditions = st.checkbox("I agree to the Terms and Conditions", 
                                     value=get_random_value("termsAndConditions", False))
        
        st.header("Application Metadata")
        st.info("These fields will be auto-populated upon submission")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Application Type", value="ApplicationInvestmentLicenseA", disabled=True)
        with col2:
            st.text_input("License Type", value="ApplicationInvestmentLicenseA", disabled=True)
    
    # Submit button
    submit_button = st.form_submit_button("Submit Application")

# Tab 5: Debug tab (outside the form)
with tab5:
    st.header("Debugging Information")
    
    # CSV Data Debug
    with st.expander("CSV Data", expanded=False):
        df = load_csv_data()
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No CSV data loaded")
    
    # Input JSON Debug
    with st.expander("Input JSON (Application Data)", expanded=False):
        if st.session_state.application_data:
            st.json(st.session_state.application_data)
        else:
            st.info("No application data available. Submit the form first.")
            
    # Output JSON Debug
    with st.expander("Output JSON (Analysis Result)", expanded=False):
        if st.session_state.analysis_result:
            st.json(st.session_state.analysis_result)
        else:
            st.info("No analysis result available. Submit the form first.")
    
    # Original CSV Row (if using random from CSV)
    with st.expander("Original CSV Row", expanded=False):
        if 'random_values' in st.session_state and '_original_csv_row' in st.session_state.random_values:
            st.json(st.session_state.random_values['_original_csv_row'])
        else:
            st.info("No original CSV row data available.")

# Process form submission
if submit_button:
    # Validate required fields
    if not company_name or not terms_conditions:
        st.error("Please fill in all required fields and agree to the terms and conditions.")
    else:
        # Prepare application data
        application_data = prepare_application_data({
            "companyName": company_name,
            "companyOrigin": company_origin,
            "companyCity": company_city,
            "companyStreet": company_street,
            "companyBuilding": company_building,
            "companyPostalAddress": company_postal,
            "companyOutput": company_output,
            "cashAmount": cash_amount,
            "contributionAmount": contribution_amount,
            "totalCapitalAmount": total_capital_amount,
            "capitalExpenditure": capital_expenditure,
            "operatingExpense": operating_expense,
            "fixedAssets": fixed_assets,
            "totalInvestmentValue": total_investment_value,
            "shareholderCompanyPartnerName": shareholder_name,
            "shareholderNationality": shareholder_nationality,
            "shareValue": share_value,
            "valueOfEquityOrShares": value_of_shares,
            "percentageOfEquityOrShares": percentage_of_shares,
            "numberOfEquityOrShares": number_of_shares,
            "contributionType": {"cash": cash_contribution},
            "incentives": incentives_requested,
            "incentiveType": {"exemptionFromIncomeTax": exemption_income_tax},
            "preferredIncentive": preferred_incentive,
            "termsAndConditions": terms_conditions,
            "appType": "ApplicationInvestmentLicenseA",
            "licenseType": "ApplicationInvestmentLicenseA"
        })
        
        # Store the application data in session state for debugging
        st.session_state.application_data = application_data
        
        # Analyze the application
        analysis_result = analyze_application(application_data)
        
        # Store the analysis result in session state for debugging
        st.session_state.analysis_result = analysis_result
        
        if analysis_result:
            # Display analysis results
            st.markdown("## Analysis Results")
            
            # Extract the analysis result
            analysis = analysis_result.get("analysis_result", {})
            
            # Decision Summary Section
            st.markdown("### Decision Summary")
            
            # Create columns for decision and explanation
            col1, col2 = st.columns([1, 3])
            
            decision = analysis.get("Decision")
            with col1:
                if decision == "ACCEPTED":
                    st.success("✅ ACCEPTED")
                elif decision == "REJECTED":
                    st.error("❌ REJECTED")
                # else:
                #     st.warning("⚠️ UNKNOWN")
            
            with col2:
                with st.expander("Decision Explanation", expanded=True):
                    st.write(analysis.get("DecisionExplanation", "No explanation provided."))
            
            # Similar Applications Section
            st.markdown("### Similar Applications")
            
            # Debug expander for raw response
            with st.expander("Raw Analysis Response (Debug)", expanded=False):
                st.json(analysis)
            
            # Look for the top similar applications in the analysis
            top_similar = analysis.get("Top3SimilarApplications", [])
            
            if top_similar and isinstance(top_similar, list) and len(top_similar) > 0:
                st.write(f"Found {len(top_similar)} similar applications")
                
                # Display each similar application in a card-like format
                for i, app in enumerate(top_similar):
                    with st.container():
                        col1, col2, col3 = st.columns([1, 3, 1])
                        
                        with col1:
                            # Handle different possible key names for similarity percentage
                            percentage = app.get("PercentageMatching", 
                                             app.get("Similarity", 
                                                 app.get("percentage_matching", 
                                                     app.get("similarity", "N/A"))))
                            
                            # Clean up percentage format
                            if isinstance(percentage, str) and "%" in percentage:
                                percentage = percentage.replace("%", "").strip()
                            
                            try:
                                percentage_value = float(percentage)
                                st.metric("Match", f"{percentage_value:.1f}%")
                            except (ValueError, TypeError):
                                st.metric("Match", str(percentage))
                        
                        with col2:
                            st.subheader(f"Application #{i+1}")
                            
                            # Handle different possible key names for UUID
                            uuid_value = app.get("UUID", 
                                             app.get("uuid", 
                                                 app.get("id", "N/A")))
                            st.markdown(f"**UUID:** {uuid_value}")
                            
                            # Handle different possible key names for description
                            description = app.get("Description", 
                                              app.get("description", 
                                                  app.get("companyName", 
                                                      app.get("company_name", "N/A"))))
                            st.markdown(f"**Description:** {description}")
                        
                        with col3:
                            # Handle different possible key names for status/decision
                            status = app.get("Status", 
                                         app.get("status", 
                                             app.get("Decision", 
                                                 app.get("decision", "N/A"))))
                            
                            if status and isinstance(status, str):
                                status_upper = status.upper()
                                if "ACCEPT" in status_upper:
                                    st.success("ACCEPTED")
                                elif "REJECT" in status_upper:
                                    st.error("REJECTED")
                                else:
                                    st.info(status)
                            else:
                                st.info("N/A")
                    
                    st.divider()
            else:
                st.info("No similar applications found in the response.")
            
            # Recommendations Section
            st.markdown("### Recommendations")
            recommendations = analysis.get("Recommendations", "No recommendations provided.")
            
            if isinstance(recommendations, list):
                for rec in recommendations:
                    st.markdown(f"- {rec}")
            else:
                st.write(recommendations)
            
            # Risk Assessment Section
            st.markdown("### Risk Assessment")
            risks = analysis.get("RisksIdentified", "No risks identified.")

            # Handle different formats of risks data
            if isinstance(risks, dict):
                # If it's a dictionary, convert to string representation
                risk_text = json.dumps(risks, indent=2)
                st.code(risk_text)
            elif isinstance(risks, list):
                # If it's a list, display as bullet points
                for risk in risks:
                    st.markdown(f"- {risk}")
            else:
                # Convert to string and then lowercase for comparison
                risks_str = str(risks)
                risks_lower = risks_str.lower()
                if "no risk" in risks_lower or "no known risk" in risks_lower or "no potential risk" in risks_lower:
                    st.success(risks_str)
                else:
                    st.warning(risks_str)

    
