import streamlit as st
import joblib
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Smart Insurance Predictor",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #071A2F, #0B2A43);
    color: white;
}

h1, h2, h3 {
    color: #FFFFFF;
}

/* Input labels */
label {
    color: #EAF4FF !important;
    font-weight: 600 !important;
}

/* Input text */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    color: #102A43 !important;
    background-color: #F1F6FA !important;
}

/* Selectbox text */
.stSelectbox div[data-baseweb="select"] * {
    color: #102A43 !important;
}

/* Insurance Type - Main Heading */
div[data-testid="stRadio"] > label {
    color: #FFFFFF !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* Health and Vehicle Insurance options */
div[data-testid="stRadio"] label p {
    color: #FFFFFF !important;
    font-size: 21px !important;
    font-weight: 600 !important;
}

/* Space between options */
div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 8px !important;
}

/* Input placeholder */
input::placeholder {
    color: #64748B !important;
}

/* Number input buttons */
.stNumberInput button {
    color: #102A43 !important;
}

.stButton > button {
    background-color: #00BFA6;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #00A890;
}

div[data-testid="stMetric"] {
    background-color: #123653;
    border-radius: 12px;
    padding: 15px;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 32px !important;
}

div[data-testid="stMetricLabel"] {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Prediction amount - white and bold */
div[data-testid="stMetric"] label {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 32px !important;
}

div[data-testid="stExpander"] {
    background-color: #102F4A;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LANGUAGE SELECTION
# =========================================================

col1, col2 = st.columns([3, 1])

with col2:
    language = st.radio(
        "Language",
        ["English", "తెలుగు"],
        horizontal=True
    )

# =========================================================
# TRANSLATIONS
# =========================================================

TEXT= {
    "title": {
        "English": "🤖 AI Smart Insurance Predictor",
        "తెలుగు": "🤖 AI స్మార్ట్ ఇన్సూరెన్స్ ప్రిడిక్టర్"
    },
    "subtitle": {
        "English": "🏥 Health & 🚗 Vehicle Insurance Premium Prediction",
        "తెలుగు": "🏥 ఆరోగ్య & 🚗 వాహన బీమా ప్రీమియం అంచనా"
    },
    "smart_desc": {
        "English": "💡 Smart & Simple Insurance Cost Estimation",
        "తెలుగు": "💡 సులభమైన మరియు స్మార్ట్ బీమా ఖర్చు అంచనా"
    },
    "enter_details": {
        "English": "👤 Enter Your Details",
        "తెలుగు": "👤 మీ వివరాలను నమోదు చేయండి"
    },
    "basic_info": {
        "English": "Please provide your basic health and personal information.",
        "తెలుగు": "మీ ప్రాథమిక ఆరోగ్య మరియు వ్యక్తిగత వివరాలను నమోదు చేయండి."
    },
    "insurance_type": {
        "English": "Insurance Type",
        "తెలుగు": "బీమా రకం"
    },
    "health": {
        "English": "🏥 Health Insurance",
        "తెలుగు": "🏥 ఆరోగ్య బీమా"
    },
    "vehicle": {
        "English": "🚗 Vehicle Insurance",
        "తెలుగు": "🚗 వాహన బీమా"
    },

    # Health
    "age": {
        "English": "Age",
        "తెలుగు": "వయస్సు"
    },
    "sex": {
        "English": "Sex",
        "తెలుగు": "లింగం"
    },
    "female": {
        "English": "Female",
        "తెలుగు": "మహిళ"
    },
    "male": {
        "English": "Male",
        "తెలుగు": "పురుషుడు"
    },
    "height": {
        "English": "Height (cm)",
        "తెలుగు": "ఎత్తు (సెం.మీ)"
    },
    "weight": {
        "English": "Weight (kg)",
        "తెలుగు": "బరువు (కిలోలు)"
    },
    "children": {
        "English": "Number of Children",
        "తెలుగు": "పిల్లల సంఖ్య"
    },
    "smoker": {
        "English": "Smoker",
        "తెలుగు": "ధూమపానం"
    },
    "no": {
        "English": "No",
        "తెలుగు": "లేదు"
    },
    "yes": {
        "English": "Yes",
        "తెలుగు": "అవును"
    },
    "region": {
        "English": "Region",
        "తెలుగు": "ప్రాంతం"
    },
    "northeast": {
        "English": "Northeast",
        "తెలుగు": "ఈశాన్య"
    },
    "northwest": {
        "English": "Northwest",
        "తెలుగు": "వాయువ్య"
    },
    "southeast": {
        "English": "Southeast",
        "తెలుగు": "ఆగ్నేయ"
    },
    "southwest": {
        "English": "Southwest",
        "తెలుగు": "నైరుతి"
    },
    "calculated_bmi": {
        "English": "📊 Calculated BMI",
        "తెలుగు": "📊 లెక్కించిన BMI"
    },
    "predict_health": {
        "English": "💰 Predict Insurance Charges",
        "తెలుగు": "💰 బీమా ఖర్చును అంచనా వేయండి"
    },

    # Additional Health / Insurance Details
    "patient_name": {
        "English": "Patient Name",
        "తెలుగు": "రోగి పేరు"
    },
    "contact_number": {
        "English": "Contact Number",
        "తెలుగు": "కాంటాక్ట్ నంబర్"
    },
    "policy_number": {
        "English": "Policy Number",
        "తెలుగు": "పాలసీ నంబర్"
    },
    "hospital_name": {
        "English": "Hospital Name",
        "తెలుగు": "హాస్పిటల్ పేరు"
    },
    "diagnosis": {
        "English": "Diagnosis",
        "తెలుగు": "వ్యాధి / నిర్ధారణ"
    },
    "length_of_stay": {
        "English": "Length of Stay (days)",
        "తెలుగు": "హాస్పిటల్‌లో ఉన్న రోజులు"
    },
    "medical_expenses": {
        "English": "Medical Expenses (₹)",
        "తెలుగు": "వైద్య ఖర్చులు (₹)"
    },
    "pre_existing": {
        "English": "Pre-existing Disease",
        "తెలుగు": "ముందుగా ఉన్న వ్యాధి"
    },
    "previous_hospitalization": {
        "English": "Previous Hospitalization",
        "తెలుగు": "గతంలో హాస్పిటల్‌లో చేరారా"
    },
    "policy_type": {
        "English": "Policy Type",
        "తెలుగు": "పాలసీ రకం"
    },
    "individual": {
        "English": "Individual",
        "తెలుగు": "వ్యక్తిగత"
    },
    "family": {
        "English": "Family",
        "తెలుగు": "కుటుంబ"
    },
    "coverage_amount": {
        "English": "Coverage Amount",
        "తెలుగు": "కవరేజ్ మొత్తం"
    },
    "previous_claims": {
        "English": "Previous Claims",
        "తెలుగు": "గత క్లెయిమ్స్ సంఖ్య"
    },
    "additional_details": {
        "English": "📋 Additional Insurance & Patient Details",
        "తెలుగు": "📋 అదనపు బీమా & రోగి వివరాలు"
    },
    "personal_details": {
    "English": "👤 Personal Details",
    "తెలుగు": "👤 వ్యక్తిగత వివరాలు"
},
"medical_details": {
    "English": "🩺 Medical Details",
    "తెలుగు": "🩺 వైద్య వివరాలు"
},
"hospital_details": {
    "English": "🏥 Hospital Details",
    "తెలుగు": "🏥 హాస్పిటల్ వివరాలు"
},
"insurance_details": {
    "English": "📋 Insurance Details",
    "తెలుగు": "📋 బీమా వివరాలు"
},
"ai_prediction": {
    "English": "🤖 AI Prediction",
    "తెలుగు": "🤖 AI అంచనా"
},

    # Vehicle
    "vehicle_details": {
        "English": "🚗 Enter Vehicle Details",
        "తెలుగు": "🚗 వాహనం వివరాలు నమోదు చేయండి"
    },
    "vehicle_type": {
        "English": "Vehicle Type",
        "తెలుగు": "వాహనం రకం"
    },
    "car": {
        "English": "Car",
        "తెలుగు": "కారు"
    },
    "two_wheeler": {
        "English": "2 Wheeler",
        "తెలుగు": "2 వీలర్"
    },
    "truck": {
        "English": "Goods Carrying Truck",
        "తెలుగు": "సరుకు రవాణా ట్రక్"
    },
    "agriculture_vehicle": {
        "English": "Agriculture Purpose Vehicle",
        "తెలుగు": "వ్యవసాయ వాహనం"
    },
    "usage_type": {
        "English": "Usage Type",
        "తెలుగు": "వినియోగ రకం"
    },
    "private": {
        "English": "Private",
        "తెలుగు": "వ్యక్తిగత ఉపయోగం"
    },
    "commercial": {
        "English": "Commercial",
        "తెలుగు": "వాణిజ్య ఉపయోగం"
    },
    "agriculture": {
        "English": "Agriculture",
        "తెలుగు": "వ్యవసాయ ఉపయోగం"
    },
    "driver_age": {
        "English": "Driver Age",
        "తెలుగు": "డ్రైవర్ వయస్సు"
    },
    "driver_experience": {
        "English": "Driver Experience (years)",
        "తెలుగు": "డ్రైవర్ అనుభవం (సంవత్సరాలు)"
    },
    "accidents": {
        "English": "Previous Accidents",
        "తెలుగు": "గత ప్రమాదాల సంఖ్య"
    },
    "mileage": {
        "English": "Annual Mileage (x1000 km)",
        "తెలుగు": "వార్షిక మైలేజ్ (x1000 కి.మీ)"
    },
    "manufacturing_year": {
        "English": "Vehicle Manufacturing Year",
        "తెలుగు": "వాహనం తయారీ సంవత్సరం"
    },
    "vehicle_age": {
        "English": "Vehicle Age",
        "తెలుగు": "వాహనం వయస్సు"
    },
    "engine_cc": {
        "English": "Engine CC",
        "తెలుగు": "ఇంజిన్ CC"
    },
    "vehicle_value": {
        "English": "Vehicle Value (INR)",
        "తెలుగు": "వాహనం విలువ (INR)"
    },
    "gross_weight": {
        "English": "Gross Vehicle Weight (KG)",
        "తెలుగు": "వాహనం మొత్తం బరువు (KG)"
    },
    "predict_vehicle": {
        "English": "🚗 Predict Vehicle Insurance Premium",
        "తెలుగు": "🚗 వాహన బీమా ప్రీమియం అంచనా వేయండి"
    },

    # Results
    "prediction_result": {
        "English": "📊 Prediction Result",
        "తెలుగు": "📊 అంచనా ఫలితం"
    },
    "vehicle_result": {
        "English": "📊 Vehicle Insurance Result",
        "తెలుగు": "📊 వాహన బీమా ఫలితం"
    },
    "success": {
        "English": "🎉 Prediction generated successfully!",
        "తెలుగు": "🎉 అంచనా విజయవంతంగా రూపొందించబడింది!"
    },
    "vehicle_success": {
        "English": "🎉 Vehicle insurance premium predicted successfully!",
        "తెలుగు": "🎉 వాహన బీమా ప్రీమియం విజయవంతంగా అంచనా వేయబడింది!"
    },
    "estimated_charges": {
        "English": "💰 Estimated Insurance Charges",
        "తెలుగు": "💰 అంచనా బీమా ఖర్చు"
    },
    "estimated_vehicle": {
        "English": "💰 Estimated Vehicle Insurance Premium",
        "తెలుగు": "💰 అంచనా వాహన బీమా ప్రీమియం"
    },
    "bmi_category": {
        "English": "📌 BMI Category",
        "తెలుగు": "📌 BMI వర్గం"
    },
    "bmi_level": {
        "English": "📊 BMI Level",
        "తెలుగు": "📊 BMI స్థాయి"
    },
    "model_performance": {
        "English": "🤖 Model Performance",
        "తెలుగు": "🤖 మోడల్ పనితీరు"
    },
    "vehicle_performance": {
        "English": "🤖 Vehicle Model Performance",
        "తెలుగు": "🤖 వాహన మోడల్ పనితీరు"
    }
}
def T(key):
    return TEXT[key][language]
    

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.title(T("title"))
st.write(T("subtitle"))

st.markdown(f"### {T('smart_desc')}")

if language == "English":
    st.write(
        "Enter your details below to estimate your insurance charges."
    )
    st.caption(
        "Machine Learning based insurance cost prediction system."
    )
else:
    st.write(
        "మీ బీమా ఖర్చును అంచనా వేయడానికి క్రింద మీ వివరాలను నమోదు చేయండి."
    )
    st.caption(
        "మెషిన్ లెర్నింగ్ ఆధారిత బీమా ఖర్చు అంచనా వ్యవస్థ."
    )

st.divider()


# =========================================================
# LOAD MODELS
# =========================================================

model = joblib.load("models/insurance_model_13_features.pkl")
vehicle_model = joblib.load("models/vehicle_insurance_model.pkl")


# =========================================================
# INSURANCE TYPE
# =========================================================

insurance_type = st.radio(
    T("insurance_type"),
    [T("health"), T("vehicle")]
)
# =========================================================
# REQUIRED DOCUMENTS
# =========================================================

if language == "English":

    with st.expander("📄 Required Documents"):

        if insurance_type == T("health"):

            st.markdown("""
### 🏥 Health Insurance – Commonly Required Documents

- 🪪 Identity Proof
- 🏠 Address Proof
- 🎂 Age / Date of Birth Proof
- 📷 Passport-size Photo (if required)
- 🆔 PAN / KYC Documents (if applicable)
- 🏥 Previous Medical Records
- 💊 Prescriptions
- 🧪 Medical / Diagnostic Test Reports
- 🏨 Hospital Discharge Summary
- 💰 Hospital Bills and Receipts
            """)

        else:

            st.markdown("""
### 🚗 Vehicle Insurance – Commonly Required Documents

- 🪪 Driving Licence (DL)
- 📄 Registration Certificate (RC)
- 🛡️ Existing / Previous Insurance Policy
- 🆔 Identity / KYC Documents
- 🚗 Vehicle-related Documents
- 📋 Claim Form (for insurance claims)
- 🚔 FIR / Police Report (if applicable)
- 🔑 Vehicle Keys (for theft claims, if applicable)
            """)

        st.warning(
            "⚠️ Document requirements can vary depending on the insurer, "
            "policy type, and whether you are purchasing a policy or making a claim."
        )

else:

    with st.expander("📄 అవసరమైన పత్రాలు"):

        if insurance_type == T("health"):

            st.markdown("""
### 🏥 ఆరోగ్య బీమా – సాధారణంగా అవసరమయ్యే పత్రాలు

- 🪪 గుర్తింపు రుజువు
- 🏠 చిరునామా రుజువు
- 🎂 వయస్సు / పుట్టిన తేదీ రుజువు
- 📷 పాస్‌పోర్ట్ సైజ్ ఫోటో (అవసరమైతే)
- 🆔 PAN / KYC పత్రాలు (వర్తిస్తే)
- 🏥 గత వైద్య రికార్డులు
- 💊 డాక్టర్ ప్రిస్క్రిప్షన్లు
- 🧪 మెడికల్ / డయాగ్నస్టిక్ టెస్ట్ రిపోర్టులు
- 🏨 హాస్పిటల్ డిశ్చార్జ్ సమ్మరీ
- 💰 హాస్పిటల్ బిల్లులు మరియు రసీదులు
            """)

        else:

            st.markdown("""
### 🚗 వాహన బీమా – సాధారణంగా అవసరమయ్యే పత్రాలు

- 🪪 డ్రైవింగ్ లైసెన్స్ (DL)
- 📄 రిజిస్ట్రేషన్ సర్టిఫికేట్ (RC)
- 🛡️ ప్రస్తుత / గత బీమా పాలసీ
- 🆔 గుర్తింపు / KYC పత్రాలు
- 🚗 వాహనానికి సంబంధించిన పత్రాలు
- 📋 క్లెయిమ్ ఫారం (బీమా క్లెయిమ్ కోసం)
- 🚔 FIR / పోలీస్ రిపోర్ట్ (వర్తిస్తే)
- 🔑 వాహనం తాళాలు (దొంగతనం క్లెయిమ్‌లో వర్తిస్తే)
            """)

        st.warning(
            "⚠️ అవసరమైన పత్రాలు బీమా కంపెనీ, పాలసీ రకం "
            "మరియు మీరు పాలసీ తీసుకుంటున్నారా లేదా క్లెయిమ్ చేస్తున్నారా "
            "అనే దాని ఆధారంగా మారవచ్చు."
        )


# =========================================================
# VEHICLE INSURANCE
# =========================================================

if insurance_type == T("vehicle"):

    st.subheader(T("vehicle_details"))

    # -----------------------------------------------------
    # Vehicle Type
    # -----------------------------------------------------

    vehicle_type = st.selectbox(
        T("vehicle_type"),
        [
            "Car",
            "2 Wheeler",
            "Goods Carrying Truck",
            "Agriculture Purpose Vehicle"
        ],
        format_func=lambda x: {
            "Car": T("car"),
            "2 Wheeler": T("two_wheeler"),
            "Goods Carrying Truck": T("truck"),
            "Agriculture Purpose Vehicle": T("agriculture_vehicle")
        }[x]
    )

    # -----------------------------------------------------
    # Usage Type
    # -----------------------------------------------------

    usage_type = st.selectbox(
        T("usage_type"),
        [
            "Private",
            "Commercial",
            "Agriculture"
        ],
        format_func=lambda x: {
            "Private": T("private"),
            "Commercial": T("commercial"),
            "Agriculture": T("agriculture")
        }[x]

    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # LEFT COLUMN
    # -----------------------------------------------------

    with col1:

        driver_age = st.number_input(
            T("driver_age"),
            min_value=0,
            max_value=100,
            value=0
        )

        driver_experience = st.number_input(
            T("driver_experience"),
            min_value=0,
            max_value=80,
            value=0
        )

        previous_accidents = st.number_input(
            T("accidents"),
            min_value=0,
            max_value=20,
            value=0
        )

        annual_mileage = st.number_input(
            T("mileage"),
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        manufacturing_year = st.number_input(
            T("manufacturing_year"),
            min_value=0,
            max_value=2026,
            value=0
        )

    # -----------------------------------------------------
    # RIGHT COLUMN
    # -----------------------------------------------------

    with col2:

        vehicle_age = st.number_input(
            T("vehicle_age"),
            min_value=0,
            max_value=50,
            value=0
        )

        engine_cc = st.number_input(
            T("engine_cc"),
            min_value=0,
            max_value=20000,
            value=0
        )

        vehicle_value = st.number_input(
            T("vehicle_value"),
            min_value=0.0,
            max_value=100000000.0,
            value=0.0,
            step=10000.0
        )

        gross_weight = st.number_input(
            T("gross_weight"),
            min_value=0.0,
            max_value=100000.0,
            value=0.0,
            step=50.0
        )

    # -----------------------------------------------------
    # VEHICLE PREDICTION
    # -----------------------------------------------------

    if st.button(
        T("predict_vehicle"),
        use_container_width=True
    ):

        # Check required vehicle details
        missing = (
            driver_age <= 0
            or annual_mileage <= 0
            or manufacturing_year <= 0
            or engine_cc <= 0
            or vehicle_value <= 0
            or gross_weight <= 0
        )

        if missing:

            if language == "English":
                st.warning(
                    "⚠️ Please enter all required vehicle details before predicting."
                )
            else:
                st.warning(
                    "⚠️ అంచనా వేయడానికి ముందుగా అవసరమైన అన్ని వాహన వివరాలను నమోదు చేయండి."
                )

            st.metric(
                T("estimated_vehicle"),
                "₹0.00"
            )

        else:

            # Vehicle AI prediction
            vehicle_input = pd.DataFrame([{
                "Vehicle Type": vehicle_type,
                "Driver Age": driver_age,
                "Driver Experience": driver_experience,
                "Previous Accidents": previous_accidents,
                "Annual Mileage (x1000 km)": annual_mileage,
                "Vehicle Manufacturing Year": manufacturing_year,
                "Vehicle Age": vehicle_age,
                "Engine CC": engine_cc,
                "Vehicle Value (INR)": vehicle_value,
                "Gross Vehicle Weight (KG)": gross_weight,
                "Usage Type": usage_type
            }])

            vehicle_prediction = vehicle_model.predict(
                vehicle_input
            )

            st.divider()

            st.subheader(T("vehicle_result"))

            st.success(T("vehicle_success"))

            st.markdown(
    f"""
    <div style="
        background-color:#123653;
        padding:18px;
        border-radius:12px;
        margin:10px 0;
    ">
        <div style="
            color:white;
            font-size:16px;
            font-weight:700;
        ">
            {T("estimated_vehicle")}
        </div>
        <div style="
            color:white;
            font-size:32px;
            font-weight:900;
            margin-top:5px;
        ">
            ₹{vehicle_prediction[0]:,.2f}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

            st.divider()

            st.subheader(T("vehicle_performance"))

            st.write(
                "📌 Mean Absolute Error (MAE): ₹1,624.73"
            )

            st.write(
                "📌 R² Score: 97.34%"
            )

            if language == "English":
                st.info(
                    "This prediction is generated by a Random Forest "
                    "machine learning model and is intended for educational purposes."
                )
            else:
                st.info(
                    "ఈ అంచనా Random Forest Machine Learning Model ద్వారా రూపొందించబడింది. "
                    "ఇది విద్యా ప్రయోజనాల కోసం మాత్రమే."
                )

if insurance_type == T("health"):
    # =========================================================
    # HEALTH INSURANCE
    # =========================================================

    st.subheader(T("enter_details"))

    if language == "English":
        st.caption(
            "Please provide your basic health and personal information."
        )
    else:
        st.caption(
            "మీ ప్రాథమిక ఆరోగ్య మరియు వ్యక్తిగత వివరాలను నమోదు చేయండి."
        )

    st.divider()
    # =========================================================
    # PERSONAL DETAILS
    # =========================================================

    st.subheader(T("personal_details"))

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input(
            T("patient_name"),
            placeholder="Enter patient name"
        )

        contact_number = st.text_input(
            T("contact_number"),
            placeholder="Enter contact number"
        )

        age = st.number_input(
            T("age"),
            min_value=0,
            max_value=100,
            value=0
        )

    with col2:
        sex = st.selectbox(
            T("sex"),
            ["Female", "Male"],
            format_func=lambda x: {
                "Female": T("female"),
                "Male": T("male")
            }[x]
        )

        children = st.number_input(
            T("children"),
            min_value=0,
            max_value=100,
            value=0
        )

        region = st.selectbox(
            T("region"),
            ["Northeast", "Northwest", "Southeast", "Southwest"],
            format_func=lambda x: {
                "Northeast": T("northeast"),
                "Northwest": T("northwest"),
                "Southeast": T("southeast"),
                "Southwest": T("southwest")
            }[x]
        )

    st.divider()
    # =========================================================
    # MEDICAL DETAILS
    # =========================================================

    st.subheader(T("medical_details"))

    col1, col2 = st.columns(2)

    with col1:
        height_cm = st.number_input(
            T("height"),
            min_value=0.0,
            max_value=250.0,
            value=0.0
        )

        weight_kg = st.number_input(
            T("weight"),
            min_value=0.0,
            max_value=300.0,
            value=0.0
        )

        smoker = st.selectbox(
            T("smoker"),
            ["No", "Yes"],
            format_func=lambda x: {
                "No": T("no"),
                "Yes": T("yes")
            }[x]
        )

    with col2:
        pre_existing_disease = st.selectbox(
            T("pre_existing"),
            ["No", "Yes"],
            format_func=lambda x: {
                "No": T("no"),
                "Yes": T("yes")
            }[x]
        )

        previous_hospitalization = st.selectbox(
            T("previous_hospitalization"),
            ["No", "Yes"],
            format_func=lambda x: {
                "No": T("no"),
                "Yes": T("yes")
            }[x]
        )

        diagnosis = st.text_input(
            T("diagnosis"),
            placeholder="Enter diagnosis"
        )

    if height_cm > 0 and weight_kg > 0:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
    else:
        bmi = 0

    st.info(f"{T('calculated_bmi')}: **{bmi:.2f}**")
    st.divider()
    # =========================================================
    # HOSPITAL DETAILS
    # =========================================================

    st.subheader(T("hospital_details"))

    col1, col2 = st.columns(2)

    with col1:
        hospital_name = st.text_input(
            T("hospital_name"),
            placeholder="Enter hospital name"
        )

        length_of_stay = st.number_input(
            T("length_of_stay"),
            min_value=0,
            max_value=365,
            value=0
        )

    with col2:
        medical_expenses = st.number_input(
            T("medical_expenses"),
            min_value=0.0,
            max_value=100000000.0,
            value=0.0,
            step=1000.0
        )

    st.divider()
    # =========================================================
    # INSURANCE DETAILS
    # =========================================================

    st.subheader(T("insurance_details"))

    col1, col2 = st.columns(2)

    with col1:
        policy_number = st.text_input(
            T("policy_number"),
            placeholder="Enter policy number"
        )

        policy_type = st.selectbox(
            T("policy_type"),
            ["Individual", "Family"],
            format_func=lambda x: {
                "Individual": T("individual"),
                "Family": T("family")
            }[x]
        )

    with col2:
        coverage_amount = st.selectbox(
            T("coverage_amount"),
            [100000, 300000, 500000, 1000000, 2000000, 5000000],
            format_func=lambda x: f"₹{x:,.0f}"
        )

        previous_claims = st.number_input(
            T("previous_claims"),
            min_value=0,
            max_value=50,
            value=0
        )

    st.divider()



    # =========================================================
    # HEALTH PREDICTION
    # =========================================================
    st.subheader(T("ai_prediction"))

    def bmi_category(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    if st.button(
        T("predict_health"),
        use_container_width=True
    ):

        # -----------------------------------------------------
        # Check Required Details
        # -----------------------------------------------------

        missing_fields = []

        if height_cm <= 0:
            missing_fields.append("Height")

        if weight_kg <= 0:
            missing_fields.append("Weight")

        if not patient_name.strip():
            missing_fields.append("Patient Name")

        if not contact_number.strip():
            missing_fields.append("Contact Number")

        if not diagnosis.strip():
            missing_fields.append("Diagnosis")

        if not hospital_name.strip():
            missing_fields.append("Hospital Name")

        if not policy_number.strip():
            missing_fields.append("Policy Number")

        if length_of_stay <= 0:
            missing_fields.append("Length of Stay")

        if medical_expenses <= 0:
            missing_fields.append("Medical Expenses")

        if previous_claims < 0:
            missing_fields.append("Previous Claims")

        # -----------------------------------------------------
        # If Required Details Are Missing
        # -----------------------------------------------------

        if missing_fields:

            if language == "English":
                st.warning(
                    "⚠️ Please enter all required details before predicting."
                )
            else:
                st.warning(
                    "⚠️ అంచనా వేయడానికి ముందుగా అవసరమైన అన్ని వివరాలను నమోదు చేయండి."
                )

            st.metric(
                T("estimated_charges"),
                "₹0.00"
            )

        # -----------------------------------------------------
        # If All Required Details Are Entered
        # -----------------------------------------------------

        else:

            # Encode Sex
            sex_value = 0 if sex == "Female" else 1

            # Encode Smoker
            smoker_value = 0 if smoker == "No" else 1

            # -------------------------------------------------
            # 13-Feature AI Prediction Input
            # -------------------------------------------------

            input_data = pd.DataFrame([{
                "Age": age,
                "Sex": sex,
                "BMI": bmi,
                "Children": children,
                "Smoker": smoker,
                "Region": region,
                "Pre-existing Disease": pre_existing_disease,
                "Previous Hospitalization": previous_hospitalization,
                "Diagnosis": diagnosis,
                "Length of Stay": length_of_stay,
                "Medical Expenses": medical_expenses,
                "Coverage Amount": coverage_amount,
                "Previous Claims": previous_claims
            }])

            # -------------------------------------------------
            # AI Prediction
            # -------------------------------------------------

            prediction = model.predict(input_data)

            category = bmi_category(bmi)

            st.divider()

            st.subheader(T("prediction_result"))

            st.success(T("success"))

            st.markdown(
    f"""
    <div style="
        background-color:#123653;
        padding:18px;
        border-radius:12px;
        margin:10px 0;
    ">
        <div style="
            color:white;
            font-size:16px;
            font-weight:700;
        ">
            {T("estimated_charges")}
        </div>
        <div style="
            color:white;
            font-size:32px;
            font-weight:900;
            margin-top:5px;
        ">
            ₹{prediction[0]:,.2f}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

            # -------------------------------------------------
            # BMI Category Translation
            # -------------------------------------------------

            bmi_translation = {
                "Underweight": "తక్కువ బరువు",
                "Normal": "సాధారణం",
                "Overweight": "అధిక బరువు",
                "Obese": "ఊబకాయం"
            }

            displayed_category = (
                bmi_translation[category]
                if language == "తెలుగు"
                else category
            )

            st.write(
                f"{T('bmi_category')}: **{displayed_category}**"
            )

            st.caption(T("bmi_level"))

            st.progress(
                min(bmi / 40, 1.0)
            )

            # -------------------------------------------------
            # BMI Messages
            # -------------------------------------------------

            if category == "Underweight":

                if language == "English":
                    st.warning(
                        "⚠️ Your BMI is below the normal range."
                    )
                else:
                    st.warning(
                        "⚠️ మీ BMI సాధారణ పరిధి కంటే తక్కువగా ఉంది."
                    )

            elif category == "Normal":

                if language == "English":
                    st.success(
                        "✅ Your BMI is in the normal range."
                    )
                else:
                    st.success(
                        "✅ మీ BMI సాధారణ పరిధిలో ఉంది."
                    )

            elif category == "Overweight":

                if language == "English":
                    st.warning(
                        "⚠️ Your BMI is above the normal range."
                    )
                else:
                    st.warning(
                        "⚠️ మీ BMI సాధారణ పరిధి కంటే ఎక్కువగా ఉంది."
                    )

            else:

                if language == "English":
                    st.warning(
                        "🔴 Your BMI is in the obese range."
                    )
                else:
                    st.warning(
                        "🔴 మీ BMI ఊబకాయం పరిధిలో ఉంది."
                    )

            # -------------------------------------------------
            # Smoking Message
            # -------------------------------------------------

            if smoker == "Yes":

                if language == "English":
                    st.warning(
                        "🚭 Smoking status may significantly increase "
                        "the estimated insurance cost."
                    )
                else:
                    st.warning(
                        "🚭 ధూమపానం స్థితి అంచనా బీమా ఖర్చును గణనీయంగా పెంచవచ్చు."
                    )

            else:

                if language == "English":
                    st.success(
                        "✅ Non-smoker status may help keep the estimated cost lower."
                    )
                else:
                    st.success(
                        "✅ ధూమపానం చేయని స్థితి అంచనా ఖర్చును తక్కువగా ఉంచడంలో సహాయపడవచ్చు."
                    )

    st.divider()

    st.subheader(T("model_performance"))

    st.write(
        "📌 Mean Absolute Error (MAE): 3945.19"
    )

    st.write(
        "📌 R² Score: 85.57%"
    )

    st.divider()

    if language == "English":

        st.info(
            "ℹ️ This prediction is for educational purposes and "
            "should not be considered an actual insurance quote."
        )

        st.caption(
            "🏥 AI Smart Health Insurance Predictor | "
            "Powered by Machine Learning"
        )

    else:

        st.info(
            "ℹ️ ఈ అంచనా విద్యా ప్రయోజనాల కోసం మాత్రమే. "
            "దీనిని నిజమైన బీమా కోట్‌గా పరిగణించకూడదు."
        )

        st.caption(
            "🏥 AI స్మార్ట్ హెల్త్ ఇన్సూరెన్స్ ప్రిడిక్టర్ | "
            "Machine Learning ద్వారా రూపొందించబడింది"
        )