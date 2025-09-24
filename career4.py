import pandas as pd
import streamlit as st
import sys


# --- Mappings and Static Data (Unchanged) ---
option_map = {"A": "R", "B": "I", "C": "A", "D": "S", "E": "E", "F": "C"}
subject_domains = {
    "Natural Sciences": ["Biology", "Botany", "Zoology", "Microbiology", "Chemistry", "Physics", "Mathematics", "Statistics", "Geology", "Geography", "Environmental Science", "Environmental Studies", "Science (Pure & Applied)"],
    "Medical & Health Sciences": ["Anatomy", "Anesthesia", "Audiology", "Biomedical Engineering", "Biotechnology", "Cardiac Technology", "Dentistry", "Dialysis", "Medical Imaging", "Medical & Healthcare", "Medicine", "Nursing", "Occupational Therapy", "Optometry", "Pathology", "Perfusion", "Pharmacology", "Pharmacy", "Physiotherapy", "Radiology", "Respiratory Therapy", "Veterinary Science"],
    "Engineering & Technology": ["Engineering", "Engineering & Technology", "Mechanical Engineering", "Civil Engineering", "Automotive Engineering", "Computer Science", "IT & Software", "Networking", "Cybersecurity", "Artificial Intelligence", "Algorithms", "Robotics", "Materials Science", "Textile Engineering"],
    "Agricultural & Allied Sciences": ["Agriculture", "Agriculture & Environment", "Agronomy", "Dairy Technology", "Food Science"],
    "Arts, Humanities & Social Sciences": ["Art", "Fine Arts", "Drawing", "Photography", "Literature", "Linguistics", "Philosophy", "Psychology", "Sociology", "Political Science", "History", "Ethics", "Humanities & Social Sciences", "Social Sciences", "Communication", "Creativity"],
    "Business, Management & Commerce": ["Accountancy", "Business & Management", "Business Studies", "Economics", "Finance", "Finance & Banking", "Human Resources", "International Business", "Management", "Marketing", "Marketing & Sales", "Logistics", "Public Administration"],
    "Education & Pedagogy": ["Education", "Education Studies", "Child Development", "Pedagogy"],
    "Design, Media & Creative Studies": ["Animation", "Animation & VFX", "Arts & Design", "Design", "Fashion Design", "Film & Television", "Film Studies", "Interior Design", "Jewellery Design", "Textile Design", "Textile Science", "Urban Planning"],
    "Media, Journalism & Mass Communication": ["Journalism", "Journalism & Mass Comm", "Mass Comm", "Mass Communication"],
    "Hospitality, Travel & Tourism": ["Hospitality", "Hospitality & Tourism", "Hotel Management", "Tourism", "Culinary Arts", "Sports Science"],
    "Law, Governance & Public Service": ["Law & Public Service", "Legal Studies"],
    "Miscellaneous / General": ["Archaeology", "Architecture", "Child Development", "Foreign Language", "General Knowledge", "Library & Information Science", "Navigation"]
}

# --- Core Logic Functions (Unchanged) ---
@st.cache_data
def load_data(file_path, file_type='Excel'):
    try:
        if file_type == 'Excel':
            return pd.read_excel(file_path)
        elif file_type == 'CSV':
            return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please make sure it's in the same folder."); sys.exit()
    except Exception as e:
        st.error(f"An error occurred: {e}"); sys.exit()

def calculate_and_rank_careers(careers_df, quiz_scores, subjects, interests, num_questions):
    df = careers_df.copy()
    def riasec_scorer(row):
        score = sum(quiz_scores[code] for code in "RIASEC" if row[code] == 1)
        return (score / num_questions) * 100
    def subject_scorer(row):
        required = {s.strip() for s in row['required_subjects'].split(';')}
        matched = len(required.intersection(subjects))
        return (matched / len(subjects)) * 100 if subjects else 0
    def interest_scorer(row):
        return 100 if row['Suitable_Interests'] in interests else 0
    df['riasec_score'] = df.apply(riasec_scorer, axis=1)
    df['subject_score'] = df.apply(subject_scorer, axis=1)
    df['interest_score'] = df.apply(interest_scorer, axis=1)
    df['final_score'] = (0.5 * df['riasec_score']) + (0.3 * df['subject_score']) + (0.2 * df['interest_score'])
    return df.sort_values(by='final_score', ascending=False)

# --- Streamlit App UI with Custom Styling ---
st.set_page_config(page_title="PathFinder", layout="wide")

# --- Define the Home Page URL here for easy access ---
HOME_PAGE_URL = "http://127.0.0.1:5501/index.html"

# Custom CSS and HTML for Header and Side Menu
st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-blue: #0077B6; --secondary-blue: #00B4D8; --dark-blue: #03045E;
            --tertiary-blue: #caf0f8; --card-bg: #ffffff; --text-dark: #2A3644;
            --text-light: #52667A; --border-light: #e0e0e0;
        }}
        body, .main, .stApp {{
            font-family: 'Poppins', sans-serif !important;
            background-color: var(--tertiary-blue) !important;
            color: var(--text-dark) !important;
        }}
        .header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 1rem 3rem; background-color: var(--card-bg);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); position: fixed;
            top: 0; left: 0; width: 100%; z-index: 1000;
        }}
        .header-left {{ display: flex; align-items: center; }}
        .menu-icon {{ font-size: 1.5rem; color: var(--text-dark); cursor: pointer; margin-right: 1.5rem; }}
        .logo {{ font-size: 1.5rem; font-weight: 700; color: var(--primary-blue); display: flex; align-items: center; }}
        .logo i {{ margin-right: 0.5rem; }}
        .st-emotion-cache-18ni7ap {{ display: none !important; text-decoration: none; }}
        .side-menu {{
            position: fixed; top: 0; left: -250px; width: 250px; height: 100%;
            background-color: #fff; box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            display: flex; flex-direction: column; padding-top: 5rem;
            transition: left 0.3s ease-in-out; z-index: 1000;
        }}
        .side-menu.active {{ left: 0; }}
        .side-menu .menu-item {{
            text-decoration: none; color: var(--text-dark); padding: 1rem 2rem;
            font-size: 1.1rem; font-weight: 500; transition: background-color 0.3s, color 0.3s;
        }}
        .side-menu .menu-item:hover, .side-menu .menu-item.active {{
            background-color: var(--tertiary-blue); color: var(--primary-blue);
        }}
        .block-container {{ padding-top: 5rem; }}
        .card-container {{
            background-color: var(--card-bg); padding: 1.5rem; border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); margin-bottom: 1.5rem;
        }}
        /* Streamlit's native button style */
        .stButton button {{
            background-color: var(--secondary-blue); color: white; border-radius: 5px;
            border: none; padding: 10px 20px; font-weight: 600;
            transition: background-color 0.3s, transform 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
        }}
        .stButton button:hover {{ 
            background-color: var(--primary-blue);
            transform: translateY(-2px);
        }}
            
        
        /* New CSS for custom button consistency */
        /* This class will now be applied to both "Back" and "Next" buttons */
        .custom-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: var(--secondary-blue);
            color: #fff !important;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 600;
            transition: background-color 0.3s, transform 0.2s;
            border: none;
            width: 100%;
        }}
        .custom-button:hover {{
            background-color: var(--primary-blue);
            color: #fff !important;
            transform: translateY(-2px);
        }}
    </style>

    <header class="header">
        <div class="header-left">
            <div class="menu-icon" id="menu-toggle">
                <i class="fas fa-bars"></i>
            </div>
            <div class="logo">
                <i class="fas fa-graduation-cap"></i> PathFinder
            </div>
        </div>
        <div class="header-right">
             <a href="{HOME_PAGE_URL}" class="custom-button" target="_self">🏠 Back to Home Page</a>
        </div>
    </header>

    <nav class="side-menu" id="side-menu">
        <a href="{HOME_PAGE_URL}" class="menu-item active">Home</a>
        <a href="#" class="menu-item">Dashboard</a>
        <a href="#" class="menu-item">Quiz</a>
        <a href="#" class="menu-item">Institutions</a>
        <a href="#" class="menu-item">Subjects</a>
        <a href="#" class="menu-item">About Us</a>
    </nav>
    
    <script>
        setTimeout(() => {{
            const menuToggle = document.getElementById('menu-toggle');
            const sideMenu = document.getElementById('side-menu');
            if (menuToggle && sideMenu) {{
                menuToggle.addEventListener('click', function() {{
                    sideMenu.classList.toggle('active');
                }});
            }}
        }}, 500);
    </script>
""", unsafe_allow_html=True)

st.title("Career Quiz")

# --- Main App Logic (Unchanged from here down) ---
# Load Data
quiz_df = load_data("RIASEC_Quiz_500_Questions_V3.xlsx", file_type='Excel')
careers_df_original = load_data("Book1.xlsx", file_type='Excel')
institute_df = load_data("institue_institue_.xlsx", file_type='Excel')

# Filter out postgraduate degrees
postgrad_keywords = ['Ph.D.', 'Master', 'M.Sc', 'M.A.', 'M.Tech', 'M.Com', 'MBA', 'MCA', 'PGDM', 'Post Graduate Diploma', 'M.D.', 'M.S.']
filtered_careers_df = careers_df_original[~careers_df_original['career_name'].str.contains('|'.join(postgrad_keywords), case=False, na=False)]

# State Management
if 'stage' not in st.session_state:
    st.session_state.stage = 'preferences'
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = quiz_df.sample(15).reset_index(drop=True)
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

# STAGE 1: User Preferences
if st.session_state.stage == 'preferences':
    st.subheader("Step 1: Tell Us About Your Interests")
    with st.container(border=True):
        domain_list = list(subject_domains.keys())
        selected_domain = st.selectbox("Select Your Broad Domain of Interest:", options=domain_list)
        subject_list = subject_domains[selected_domain]
        selected_subjects = st.multiselect("Select Specific Subjects You Like:", options=subject_list)
        interest_list = sorted(filtered_careers_df['Suitable_Interests'].unique())
        selected_interests = st.multiselect("Select a General Career Interest Area:", options=interest_list)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next: Start Personality Quiz"):
        if not selected_subjects or not selected_interests:
            st.warning("Please select at least one subject and one interest area.")
        else:
            st.session_state.selected_subjects = selected_subjects
            st.session_state.selected_interests = selected_interests
            st.session_state.stage = 'quiz'
            st.rerun()

# STAGE 2: RIASEC Quiz
if st.session_state.stage == 'quiz':
    st.subheader("Step 2: RIASEC Personality Quiz")
    with st.container(border=True):
        questions_to_ask = st.session_state.quiz_questions
        q_index = st.session_state.question_index
        
        if q_index < len(questions_to_ask):
            current_question = questions_to_ask.iloc[q_index]
            st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold;'>Question {q_index + 1}/{len(questions_to_ask)}</p>", unsafe_allow_html=True)
            st.progress((q_index + 1) / len(questions_to_ask))
            st.write(current_question['Question'])
            
            options = [
                current_question['Option_A'], current_question['Option_B'], current_question['Option_C'],
                current_question['Option_D'], current_question['Option_E'], current_question['Option_F']
            ]
            
            answer = st.radio("Choose one:", options, key=f"q_{q_index}", label_visibility="collapsed")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if q_index > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state.question_index -= 1
                        st.rerun()
            with col3:
                if st.button("Next ➡️" if q_index < len(questions_to_ask) - 1 else "Finish Quiz 🏁"):
                    if answer:
                        selected_option_index = options.index(answer)
                        selected_option_letter = list(option_map.keys())[selected_option_index]
                        st.session_state.quiz_answers[q_index] = selected_option_letter
                        
                        if q_index < len(questions_to_ask) - 1:
                            st.session_state.question_index += 1
                        else:
                            st.session_state.stage = 'results'
                        st.rerun()
                    else:
                        st.warning("Please select an option.")
        else:
            st.success("Quiz complete! Calculating results...")
            st.session_state.stage = 'results'
            st.rerun()

# STAGE 3: Show Career Results
if st.session_state.stage == 'results':
    st.subheader("✨ Step 3: Your Personalized Career Rankings")
    
    quiz_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    for q_index, ans_letter in st.session_state.quiz_answers.items():
        riasec_code = option_map[ans_letter]
        quiz_scores[riasec_code] += 1

    ranked_careers_df = calculate_and_rank_careers(
        filtered_careers_df,
        quiz_scores,
        st.session_state.selected_subjects,
        st.session_state.selected_interests,
        len(st.session_state.quiz_questions)
    )

    st.markdown("Here are your top career and degree recommendations, ranked by overall match score:")
    st.session_state.top_careers = ranked_careers_df.head(3)

    for i, (_, row) in enumerate(st.session_state.top_careers.iterrows()):
        st.markdown(f"""
            <div class="card-container">
                <p class="card-title" style="font-size: 1.2rem; font-weight: bold;">{i+1}. {row['career_name']}</p>
                <div style="margin-top: 10px;">
                    <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px;">
                        <div style="width: {int(row['final_score'])}%; height: 10px; background-color: var(--primary-blue); border-radius: 5px;"></div>
                    </div>
                </div>
                <p style="text-align: right; font-weight: bold; margin-top: 5px; color: var(--text-dark);">Overall Score: {row['final_score']:.1f}%</p>
                <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                    <div style="text-align: center;">
                        <p style="font-weight: bold; color: var(--text-dark);">Personality Match</p>
                        <p style="color: var(--primary-blue);">{row['riasec_score']:.1f}%</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="font-weight: bold; color: var(--text-dark);">Subject Match</p>
                        <p style="color: var(--primary-blue);">{row['subject_score']:.1f}%</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="font-weight: bold; color: var(--text-dark);">Interest Match</p>
                        <p style="color: var(--primary-blue);">{row['interest_score']:.1f}%</p>
                    </div>
                </div>
                <div style="margin-top: 15px;">
                    <p style="font-weight: bold; color: var(--text-dark);">Subjects Required:</p>
                    <p style="color: var(--text-dark);">{row['required_subjects']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<a href="{HOME_PAGE_URL}" target="_self" class="custom-button">⬅️ Back to Home Page</a>',
            unsafe_allow_html=True
        )

    with col2:
        if st.button("Next → See Matching Institutes", type="primary"):
            st.session_state.stage = "institutes"
            st.rerun()

# STAGE 4: Show Institutes
if st.session_state.stage == 'institutes':
    st.subheader("🎓 Step 4: Institute Recommendations")
    primary_fields = st.session_state.top_careers['Suitable_Interests'].unique()

    if "Primary Fields" in institute_df.columns:
        for field in primary_fields:
            st.markdown(f"<h3 class='sub-heading'>Institutes for: {field}</h3>", unsafe_allow_html=True)
            matched_institutes = institute_df[institute_df["Primary Fields"] == field]
            if not matched_institutes.empty:
                for _, inst_row in matched_institutes.iterrows():
                    st.markdown(f"""
                        <div class="card-container">
                            <p class="card-title" style="font-size: 1.1rem; font-weight: bold;">{inst_row.get('Institution', 'N/A')}</p>
                            <p class="card-meta" style="color: var(--text-light);">{inst_row.get('Type', 'N/A')}, {inst_row.get('City', 'N/A')}, {inst_row.get('State', 'N/A')}</p>
                            <p style="margin-top: 10px; color: var(--text-dark);">One of the leading engineering institutes in India...</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No institutes found in your file for the field: {field}")
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("⚠️ Your institute file ('institue_institue_.xlsx') does not have a 'Primary Fields' column. Please check the file.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<a href="{HOME_PAGE_URL}" target="_self" class="custom-button">⬅️ Back to Home Page</a>',
            unsafe_allow_html=True
        )
            
    with col2:
        if st.button("🔄 Start Over", type="primary"):
            st.session_state.clear()
            st.rerun()