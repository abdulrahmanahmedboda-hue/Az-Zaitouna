import streamlit as st
import pypdf
import requests
import json

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="تطبيق الزتونة الدراسي | By BoDa", page_icon="📚", layout="wide")

# 2. أكواد التصميم (CSS) الخارقة لضبط اللغة العربية (RTL) والألوان الفخمة
st.markdown("""
    <style>
    /* إجبار التطبيق بالكامل على الاتجاه من اليمين لليسار عشان العربي يظبط */
    .stApp, .stMarkdown, div[data-testid="stSidebar"], div.stButton > button {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* خلفية التطبيق الأساسية (أسود فخم) */
    .stApp {
        background-color: #0E1117 !important;
    }
    
    /* خلفية القائمة الجانبية وضبط ألوانها */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        background-color: #1A1D24 !important;
        border-left: 1px solid #333 !important; /* الخط الفاصل على اليسار الآن */
    }
    
    /* توحيد لون النصوص باللون الفاتح لتقرأ بوضوح في كل مكان */
    h1, h2, h3, h4, h5, h6, p, span, label, div.stMarkdown p {
        color: #F4F6FF !important;
    }
    
    /* تلوين نصوص التبويبات (Tabs) وتكبيرها */
    .stTabs [data-baseweb="tab"] p {
        color: #41C9E2 !important;
        font-size: 1.2rem !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: #FFA447 !important;
        font-weight: bold !important;
    }
    
    /* رسائل التنبيه والنجاح (تنسيق أنيق) */
    div[data-testid="stAlert"] {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

# العناوين الرئيسية للتطبيق
st.markdown("<h1 style='text-align: center; color: #41C9E2 !important;'>📚 تطبيق الزتونة الدراسي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #F4F6FF !important;'>صاحبك الذكي في المذاكرة - تلخيص حقيقي وتشجيع من القلب 🚀</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFA447 !important;'>💪 (By BoDa) تطوير وإعداد المبرمج: عبد الرحمن 🇪🇬</h3>", unsafe_allow_html=True)
st.write("---")

# 3. المفتاح السري للذكاء الاصطناعي (مثبت كما طلبت)
OPENROUTER_API_KEY = "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"

# 4. قاعدة البيانات الداخلية (Session State)
if 'summary_data' not in st.session_state:
    st.session_state['summary_data'] = "📝 لم يتم استخراج الملخص بعد. ارفع المحاضرة واضغط على زر المعالجة!"
if 'exam_capsule' not in st.session_state:
    st.session_state['exam_capsule'] = "🧠 القاموس فارغ حالياً. نحن في انتظار الملف الخاص بك لإنشاء كبسولة الامتحان."
if 'quiz_questions' not in st.session_state:
    st.session_state['quiz_questions'] = ""

# 5. لوحة التحكم الجانبية (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='color: #41C9E2 !important;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("<h3 style='color: #4CCEAC !important;'>📂 خطوة 1: ارفع المحاضرة</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختار ملف بي دي إف (PDF) للمنهج", type=["pdf"])
    
    st.write("---")
    st.markdown("<h3 style='color: #4CCEAC !important;'>🟩 خطوة 2: استخراج الخلاصة</h3>", unsafe_allow_html=True)
    process_btn = st.button("🚀 ابدأ معالجة السحر الذكي", use_container_width=True)
    
    st.write("---")
    st.markdown("<h3 style='color: #FFA447 !important;'>🏆 مكافآت الطلاب</h3>", unsafe_allow_html=True)
    st.info("الرتبة الحالية: بروفيسور الزتونة 🏅")
    st.progress(100)

# دالة الاتصال بالذكاء الاصطناعي
def ask_openrouter(prompt_text):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "google/gemini-pro-1.5:free",
            "messages": [{"role": "user", "content": prompt_text}]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        result = response.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        else:
            return "حدث خطأ غير متوقع من السيرفر، يرجى المحاولة لاحقاً."
    except Exception as e:
        return f"تعذر الاتصال بالذكاء الاصطناعي: {e}"

# 6. معالجة الملف عند الضغط على الزر
if process_btn:
    if uploaded_file is not None:
        with st.spinner("جاري تشغيل السحر الذكي وقراءة المنهج بواسطة صاحبك الذكي..."):
            try:
                pdf_reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text
                
                if not pdf_text.strip():
                    st.error("الملف المرفوع فارغ أو عبارة عن صور فقط ولا يحتوي على نصوص قابلة للقراءة.")
                else:
                    # أخذ أول 15000 حرف لتجنب الضغط على السيرفر
                    truncated_text = pdf_text[:15000]
                    
                    summary_prompt = f"قم بقراءة هذا المنهج وتلخيصه بأسلوب أخوي مصري مبسط، مليء بالطاقة الإيجابية والتشجيع وركز على النقاط الذهبية: {truncated_text}"
                    st.session_state['summary_data'] = ask_openrouter(summary_prompt)
                    
                    capsule_prompt = f"استخرج خلاصة الخلاصة وأهم الأسئلة المتوقعة بناءً على هذا المنهج بأسلوب يهدئ روع الطالب ليلة الامتحان: {truncated_text}"
                    st.session_state['exam_capsule'] = ask_openrouter(capsule_prompt)
                    
                    quiz_prompt = f"قم بإنشاء 3 أسئلة اختيار من متعدد (أ، ب، ج) بناءً على هذا المنهج، وفي نهاية النص تماماً اكتب مفتاح الإجابات الصحيحة بوضوح مثلا (السؤال الأول: أ، السؤال الثاني: ب، السؤال الثالث: ج). النص: {truncated_text}"
                    st.session_state['quiz_questions'] = ask_openrouter(quiz_prompt)
                    
                    st.balloons()
                    st.success("🟢 نظام الفحص الذكي: تم قراءة المستند بنجاح والتطبيق جاهز للتحدي! 🤖")
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
    else:
        st.warning("⚠️ يرجى رفع ملف المحاضرة أولاً من القائمة الجانبية قبل البدء!")

# 7. الأقسام والتبويبات
tab1, tab2, tab3, tab4 = st.tabs(["🔥 تحدي الذكاء", "🧠 قاموس الزتونة", "📝 الملخص الفظيع", "🏆 لوحة الشرف"])

with tab1:
    st.markdown("<h3 style='color: #41C9E2 !important;'>🔥 قسم تحدي الذكاء مع صاحبك التفاعلي</h3>", unsafe_allow_html=True)
    
    if st.session_state['quiz_questions'] == "":
        st.info("⚠️ عذراً يا بطل، لم يتم توليد اختبار حتى الآن. يرجى رفع الملف بصيغة بي دي إف والضغط على زر المعالجة أولاً.")
    else:
        st.markdown("#### 📜 الأسئلة المستخرجة من المنهج:")
        st.success(st.session_state['quiz_questions'])
        
        st.write("---")
        st.markdown("#### 📝 اختار إجاباتك هنا يا بطل:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            q1 = st.radio("إجابة السؤال الأول:", ["أ", "ب", "ج"], key="ans1")
        with col2:
            q2 = st.radio("إجابة السؤال الثاني:", ["أ", "ب", "ج"], key="ans2")
        with col3:
            q3 = st.radio("إجابة السؤال الثالث:", ["أ", "ب", "ج"], key="ans3")
        
        st.write("")
        submit_quiz = st.button("✅ تسليم الإجابات ومعرفة النتيجة")
        
        if submit_quiz:
            st.snow()
            with st.spinner("جاري فحص إجاباتك وتقييم الأداء..."):
                review_prompt = f"""
                بناءً على الاختبار التالي:
                {st.session_state['quiz_questions']}
                
                إجابات الطالب هي:
                1: {q1}
                2: {q2}
                3: {q3}
                
                حلل إجابات الطالب بأسلوب مصري حماسي جداً، وصحح الأخطاء ببساطة وشجعه بقوة.
                """
                review_result = ask_openrouter(review_prompt)
                st.markdown("### 📊 تقرير صاحبك الذكي:")
                st.info(review_result)

with tab2:
    st.markdown("<h3 style='color: #41C9E2 !important;'>🧠 قاموس الزتونة ومراجعة آخر الدقائق</h3>", unsafe_allow_html=True)
    st.write(st.session_state['exam_capsule'])
    
with tab3:
    st.markdown("<h3 style='color: #41C9E2 !important;'>📝 الخلاصة والتحليل الفظيع للمنهج</h3>", unsafe_allow_html=True)
    st.write(st.session_state['summary_data'])
    
with tab4:
    st.markdown("<h3 style='color: #FFA447 !important;'>🏆 لوحة الشرف وأبطال الزتونة الدراسي</h3>", unsafe_allow_html=True)
    st.success("🥇 المتصدر الأبدي ومطور التطبيق الرائع: عبد الرحمن (BoDa) 🇪🇬")
    st.balloons()
