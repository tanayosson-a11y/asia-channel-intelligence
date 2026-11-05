import json
import requests
import streamlit as st

GOOGLE_SCRIPT_URL = ("https://script.google.com/macros/s/AKfycbyq6eeltu92qxTflIt-BWamPw2ev2FzZOj5j7qiMrj3lHYyyBNArf1zmLF0g2PDuS3-Jg/exec")

DEFAULT_ASIA_COUNTRIES = [
    "Vietnam",
    "Indonesia",
    "Thailand",
    "Malaysia",
    "Philippines",
    "Singapore",
    "India",
    "Taiwan",
    "Myanmar",
    "Cambodia",
    "Laos",
    "Pakistan",
    "Brunei",
]

st.set_page_config(
    page_title="Asia Regional Channel Intelligence 2027",
    page_icon="🌏",
    layout="wide",
)

st.title("🌏 Asia Regional Channel Intelligence & Growth Plan 2027")
st.markdown(
    "Welcome! Please use this friendly portal to submit your country channel"
    " assessments, competitor insights, and 2027 growth initiatives. Data flows"
    " directly into our master Google Sheet automatically."
)

st.sidebar.header("⚙️ Admin Panel")
st.sidebar.subheader("Manage Asia Countries")
country_input = st.sidebar.text_area(
    "Country List:", "\n".join(DEFAULT_ASIA_COUNTRIES)
)
countries = [c.strip() for c in country_input.split("\n") if c.strip()]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📋 Instructions & Metadata",
        "📊 Country Assessment (Sheet 1)",
        "🏢 Competitor Analysis (Sheet 2)",
        "🚀 Growth & Investment Plan (Sheet 3)",
        "📖 Admin & User Manual",
    ]
)

with tab1:
  st.header("Project Timeline & Submission Details")
  st.info(
      "**Target Submission Date:** 30th Nov 2026 | **Consolidation Body:** Asia"
      " Regional Marketing & Channel Strategy Team"
  )
  col1, col2 = st.columns(2)
  with col1:
    selected_country = st.selectbox("Select Your Country / Region", countries)
    submitter_name = st.text_input(
        "Completed By / Title", placeholder="e.g., John Doe / Country Manager"
    )
  with col2:
    submission_date = st.date_input("Submission Date")
    regional_reviewer = st.text_input(
        "Regional Reviewer", placeholder="e.g., Regional Strategy Director"
    )

with tab2:
  st.header("Sheet 1: Country Channel Assessment (PCR & TBR Segmented)")
  col_pcr, col_tbr = st.columns(2)
  with col_pcr:
    st.subheader("🚗 PCR Segment (Passenger Car Radial)")
    pcr_model = st.selectbox(
        "PCR Main Channel Model",
        [
            "Sole Distributor",
            "Regional Distributor", 
            "Wholesale Direct",
            "Dealer", 
            "SCS Retail Flagship",
            "Multi-Brand Retail",
            "KA",
        ],
        key="pcr_m",
    )
    pcr_partners = st.text_input(
        "PCR Key Channel Partners",
        "Key PCR Distributors & Master Dealers",
        key="pcr_p",
    )
    pcr_margin = st.slider("PCR Average Channel Margin (%)", 5, 35, 15, key="pcr_mg")
    pcr_rating = st.selectbox(
        "PCR Logistics & Delivery Rating",
        ["Strong", "Medium", "Weak"],
        key="pcr_r",
    )
  with col_tbr:
    st.subheader("🚛 TBR Segment (Truck & Bus Radial)")
    tbr_model = st.selectbox(
        "TBR Main Channel Model",
        [
            "Sole Distributor",
            "Regioanl Distributor", 
            "Dealer",
            "STS Retail Flagship",
            "KA",
        ],
        key="tbr_m",
    )
    tbr_partners = st.text_input(
        "TBR Key Channel Partners",
        "Key TBR Fleet Distributors & Dealers",
        key="tbr_p",
    )
    tbr_margin = st.slider("TBR Average Channel Margin (%)", 5, 35, 12, key="tbr_mg")
    tbr_rating = st.selectbox(
        "TBR Logistics & Delivery Rating",
        ["Strong", "Medium", "Weak"],
        key="tbr_r",
    )

  if st.button("💾 Save Country Assessment to Google Sheets", type="primary"):
    payload = {
        "tabName": "Country Channel Assessment",
        "rowValues": [
            str(submission_date),
            selected_country,
            submitter_name,
            pcr_model,
            pcr_partners,
            pcr_margin,
            pcr_rating,
            tbr_model,
            tbr_partners,
            tbr_margin,
            tbr_rating,
        ],
    }
    try:
      res = requests.post(GOOGLE_SCRIPT_URL, json=payload)
      if res.status_code == 200:
        st.success("✅ Successfully saved to Google Sheets!")
      else:
        st.error("❌ Failed to reach endpoint.")
    except Exception as e:
      st.error(f"Error: {e}")

with tab3:
  st.header("Sheet 2: Top 3 Competitors Analysis")
  with st.form("competitor_form"):
    comp_brand = st.text_input(
        "Competitor Brand Name",
        placeholder="e.g., Bridgestone, Michelin, GT Radial",
    )
    col_c1, col_c2 = st.columns(2)
    with col_c1:
      comp_segment = st.selectbox(
          "Product Segment", ["PCR", "TBR", "Both", "Joint"]
      )
      comp_tier = st.text_input(
          "Brand Positioning & Price Tier",
          "Tier 1 Premium (100% Price Index)",
      )
      comp_threat = st.selectbox("Threat Level", ["High", "Medium", "Low"])
    with col_c2:
      comp_adv = st.text_area(
          "Distribution Advantage", "Dominant OEM fitments and dealer ties"
      )
      comp_weak = st.text_input(
          "Main Weakness", "High price point in budget fleets"
      )
    comp_strategy = st.text_area(
        "Recommended Counter-Strategy",
        "Target fleet cost-per-km efficiency with TBR programs",
    )
    if st.form_submit_button("🚀 Submit Competitor Analysis", type="primary"):
      payload = {
          "tabName": "Top 3 Competitors",
          "rowValues": [
              selected_country,
              comp_brand,
              comp_segment,
              comp_tier,
              comp_adv,
              comp_weak,
              comp_threat,
              comp_strategy,
          ],
      }
      requests.post(GOOGLE_SCRIPT_URL, json=payload)
      st.success("✅ Competitor recorded!")

with tab4:
  st.header("Sheet 3: 2027 Growth & Investment Plan (New Initiative Builder)")
  with st.form("initiative_form"):
    init_title = st.text_input(
        "Strategic Initiative / Action Title",
        "Retail Shopfront Signboard & POSM Upgrade",
    )
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
      init_segment = st.selectbox(
          "Product Segment", ["PCR", "TBR", "Both", "Joint"], key="init_seg"
      )
      baseline_vol = st.number_input(
          "2026 Baseline Volume (pcs)", value=20000, step=500
      )
    with col_i2:
      region_chan = st.text_input("Region / Channel", "North Region")
      target_vol = st.number_input(
          "2027 Target Volume (pcs)", value=35000, step=500
      )
    with col_i3:
      investment_usd = st.number_input(
          "Estimated Investment (USD)", value=15000, step=1000
      )
      cost_cat = st.selectbox(
          "Cost Category",
          [
              "Channel Development",
              "Marketing Support",
              "Commercial Support",
          ],
      )

    col_i4, col_i5, col_i6 = st.columns(3)
    with col_i4:
      owner = st.text_input("Responsible Owner", "Sales - PCR Lead")
      priority = st.selectbox("Priority Level", ["High", "Medium", "Low"])
    with col_i5:
      target_date = st.date_input("Target Completion Date")
      status = st.selectbox(
          "Status", ["Planned", "In Progress", "Under Review", "Completed"]
      )
    with col_i6:
      roi = st.text_input("Expected ROI / Payback", "18 Months")
      support_req = st.text_input(
          "Regional Support Required", "POSM Design & Co-op Budget"
      )

    talent_req = st.text_input(
        "Talent & Capability Requirement",
        "Retail visual merchandising & training",
    )
    digital_tool = st.text_input(
        "Digital Enablement Tool / Platform", "Digital Signage Asset Portal"
    )
    risk_mitigation = st.text_input(
        "Channel Conflict Mitigation Risk",
        "Standardized co-op guidelines",
    )

    if st.form_submit_button(
        "🚀 Submit New Strategic Initiative", type="primary"
    ):
      vol_growth = target_vol - baseline_vol
      payload = {
          "tabName": "2027 Growth & Investment Plan",
          "rowValues": [
              selected_country,
              init_title,
              init_segment,
              region_chan,
              baseline_vol,
              target_vol,
              vol_growth,
              investment_usd,
              cost_cat,
              roi,
              owner,
              str(target_date),
              priority,
              support_req,
              status,
              talent_req,
              digital_tool,
              risk_mitigation,
          ],
      }
      requests.post(GOOGLE_SCRIPT_URL, json=payload)
      st.success("✅ New Strategic Initiative saved!")

with tab5:
  st.header("📖 Manual Book for Admins & Users")
  st.markdown("""
    ### 👋 Welcome to the Asia Channel Intelligence Portal!
    This web app was built to collect regional data seamlessly into your Google Sheet.
    """)
