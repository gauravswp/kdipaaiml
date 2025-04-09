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

# Function to get random values from CSV
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

# Fallback random value generator (original function)
def generate_fallback_random_values():
    random_values = {
        "companyName": f"Company {random.randint(1000, 9999)}",
        "companyOrigin": random.choice(COUNTRY_CODES),
        "companyCity": random.choice(["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Fujairah"]),
        "companyStreet": f"Street {random.randint(1, 100)}",
        "companyBuilding": f"Building {random.choice(['A', 'B', 'C', 'D'])}",
        "companyPostalAddress": f"P.O. Box {random.randint(10000, 99999)}",
        "companyOutput": f"Manufacturing {random.choice(['Electronics', 'Textiles', 'Food Products', 'Construction Materials'])}",
        "cashAmount": round(random.uniform(100000, 1000000), 2),
        "contributionAmount": round(random.uniform(100000, 2000000), 2),
        "totalCapitalAmount": round(random.uniform(500000, 5000000), 2),
        "capitalExpenditure": round(random.uniform(100000, 1000000), 2),
        "operatingExpense": round(random.uniform(50000, 500000), 2),
        "fixedAssets": round(random.uniform(200000, 2000000), 2),
        "totalInvestmentValue": round(random.uniform(1000000, 10000000), 2),
        "shareholderCompanyPartnerName": f"Shareholder {random.randint(100, 999)}",
        "shareholderNationality": random.choice(COUNTRY_CODES),
        "shareValue": round(random.uniform(10, 1000), 2),
        "valueOfEquityOrShares": round(random.uniform(100000, 1000000), 2),
        "percentageOfEquityOrShares": round(random.uniform(10, 100), 2),
        "numberOfEquityOrShares": random.randint(100, 10000),
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

# Function to make API request
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
        # Display a loading spinner
        with st.spinner("Analyzing application..."):
            response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
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

# Application title and description
st.title("Investment License Analysis")
st.markdown("Complete the application form below to analyze your investment license application.")

# Initialize session state for application data
if 'application_data' not in st.session_state:
    st.session_state.application_data = None

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# Create a form with tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Company Details", "Financial Details", "Shareholder Information", "Submission", "Debug"])

# Create form for user input
with st.form("application_form"):
    # Random values generator button
    random_button = st.form_submit_button("🎲 Get Random Data from CSV", type="secondary")
    
    if random_button:
        st.session_state.random_values = get_random_csv_values()
    
    # Initialize random values if not in session state
    if 'random_values' not in st.session_state:
        st.session_state.random_values = {}
    
    # Helper function to get a random value
    def get_random_value(key, default=""):
        return st.session_state.random_values.get(key, default) if hasattr(st.session_state, 'random_values') else default
    
    # Tab 1: Company Details
    with tab1:
        st.header("Company Details")
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", value=get_random_value("companyName"))
            company_origin = st.selectbox(
                "Country of Origin", 
                options=[code for code, _ in COUNTRY_LIST],
                format_func=lambda x: COUNTRY_NAMES.get(x, x),
                index=COUNTRY_CODES.index(get_random_value("companyOrigin")) if get_random_value("companyOrigin") in COUNTRY_CODES else 0
            )
            company_city = st.text_input("City", value=get_random_value("companyCity"))
            company_street = st.text_input("Street Address", value=get_random_value("companyStreet"))
        
        with col2:
            company_building = st.text_input("Building Name", value=get_random_value("companyBuilding"))
            company_postal = st.text_input("Postal Address", value=get_random_value("companyPostalAddress"))
            company_output = st.text_area("Company Output (Description)", value=get_random_value("companyOutput"))
    
    # Tab 2: Financial Details
    with tab2:
        st.header("Financial Details")
        col1, col2 = st.columns(2)
        
        with col1:
            cash_amount = st.number_input("Cash Amount (AED)", 
                                          min_value=0.0, 
                                          value=float(get_random_value("cashAmount", 0.0)),
                                          format="%.2f")
            
            contribution_amount = st.number_input("Contribution Amount (AED)", 
                                                min_value=0.0, 
                                                value=float(get_random_value("contributionAmount", 0.0)),
                                                format="%.2f")
            
            total_capital_amount = st.number_input("Total Capital Amount (AED)", 
                                                 min_value=0.0, 
                                                 value=float(get_random_value("totalCapitalAmount", 0.0)),
                                                 format="%.2f")
            
            capital_expenditure = st.number_input("Capital Expenditure (AED)", 
                                                min_value=0.0, 
                                                value=float(get_random_value("capitalExpenditure", 0.0)),
                                                format="%.2f")
        
        with col2:
            operating_expense = st.number_input("Operating Expense (AED)", 
                                              min_value=0.0, 
                                              value=float(get_random_value("operatingExpense", 0.0)),
                                              format="%.2f")
            
            fixed_assets = st.number_input("Fixed Assets (AED)", 
                                         min_value=0.0, 
                                         value=float(get_random_value("fixedAssets", 0.0)),
                                         format="%.2f")
            
            total_investment_value = st.number_input("Total Investment Value (AED)", 
                                                   min_value=0.0, 
                                                   value=float(get_random_value("totalInvestmentValue", 0.0)),
                                                   format="%.2f")
    
    # Tab 3: Shareholder Information
    with tab3:
        st.header("Shareholder Information")
        col1, col2 = st.columns(2)
        
        with col1:
            shareholder_name = st.text_input("Shareholder/Company Partner Name", 
                                           value=get_random_value("shareholderCompanyPartnerName"))
            
            shareholder_nationality = st.selectbox(
                "Nationality", 
                options=[code for code, _ in COUNTRY_LIST],
                format_func=lambda x: COUNTRY_NAMES.get(x, x),
                index=COUNTRY_CODES.index(get_random_value("shareholderNationality")) if get_random_value("shareholderNationality") in COUNTRY_CODES else 0
            )
            
            share_value = st.number_input("Share Value per Unit (AED)", 
                                        min_value=0.0, 
                                        value=float(get_random_value("shareValue", 0.0)),
                                        format="%.2f")
            
            value_of_shares = st.number_input("Total Value of Equity/Shares (AED)", 
                                            min_value=0.0, 
                                            value=float(get_random_value("valueOfEquityOrShares", 0.0)),
                                            format="%.2f")
        
        with col2:
            percentage_of_shares = st.number_input("Percentage of Equity/Shares (%)", 
                                                 min_value=0.0, 
                                                 max_value=100.0, 
                                                 value=float(get_random_value("percentageOfEquityOrShares", 0.0)),
                                                 format="%.2f")
            
            number_of_shares = st.number_input("Number of Shares", 
                                             min_value=0, 
                                             value=int(float(get_random_value("numberOfEquityOrShares", 0))),
                                             step=1)
            
            st.subheader("Contribution Type")
            cash_contribution = st.checkbox("Cash Contribution", 
                                          value=get_random_value("contributionType", {}).get("cash", False))
    
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
    submit_button = st.form_submit_button("Submit Application for Analysis")

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