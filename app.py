import streamlit as st
import pdfplumber
import requests
import json
from datetime import datetime

# 1. إعدادات الصفحة الأساسية والثيم الأصلي الفخم
st.set_page_config(page_title="تطبيق الزتونة الدراسي | By BoDa", page_icon="📚", layout="wide")

# 2. كود الـ CSS الأسطوري لضبط الاتجاه العربي (RTL) والألوان ومنع البقع البيضاء
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@400;700&family=Amiri:ital@1&display=swap" rel="stylesheet">
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #0E1117 !important;
    }
    
    /* تنسيق شهادة التقدير السحرية الفخمة */
    .certificate-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 10px double #FFA447;
        padding: 40px;
        text-align: center;
        border-radius: 20px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .cert-title { font-family: 'Reem Kufi', sans-serif; color: #41C9E2; font-size: 50px; }
    .cert-name { font-family: 'Amiri', serif; color: #FFA447; font-size: 45px; border-bottom: 2px solid #FFA447; display: inline-block; padding: 0 20px; }
    .cert-text { font-family: 'Reem Kufi', sans-serif; color: #F4F6FF; font-size: 22px; line-height: 1.6; margin-top: 15px; }

    [data-testid="stSidebar"] { 
        background-color: #1A1D24 !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label { 
        color: #F4F6FF !important; 
        font-family: 'Reem Kufi', sans-serif;
        text-align: right !important;
    }
    .main-title { font-size: 3.5rem !important; color: #41C9E2 !important; text-shadow: 2px 2px #000; text-align: center !important; }
    
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl !important;
    }
    .stTabs [data-baseweb="tab"] p { 
        font-size: 1.2rem !important; 
        color: #41C9E2 !important; 
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p { 
        color: #FFA447 !important; 
        font-weight: bold !important; 
    }
    
    div[data-testid="stAlert"] {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. المفتاح السري للذكاء الاصطناعي الخاص بك (ثابت وجاهز)
OPENROUTER_API_KEY = "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"

# 4. إدارة حالة الذاكرة الداخلية الثابتة (Session State) لضمان عدم اختفاء البيانات
if 'summary_data' not in st.session_state: st.session_state['summary_data'] = "📝 لم يتم استخراج الملخص بعد. ارفع المحاضرة واضغط على زر المعالجة!"
if 'exam_capsule' not in st.session_state: st.session_state['exam_capsule'] = "🧠 القاموس والتريكات فارغة حالياً. نحن في انتظار ملفك."
if 'quiz_questions' not in st.session_state: st.session_state['quiz_questions'] = ""
if 'roadmap_data' not in st.session_state: st.session_state['roadmap_data'] = "🗺️ خريطة الطريق فارغة. ارفع الملف وشوف خطة المذاكرة السحرية."
if 'cert_msg' not in st.session_state: st.session_state['cert_msg'] = ""
if 'quiz_evaluated' not in st.session_state: st.session_state['quiz_evaluated'] = False
if 'evaluation_result' not in st.session_state: st.session_state['evaluation_result'] = ""

# 5. لوحة التحكم الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429153.png", width=100)
    st.markdown("<h2 style='text-align: center; color: #41C9E2;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    
    student_name = st.text_input("📝 اكتب اسمك يا بطل عشان الشهادة:", placeholder="مثلاً: عبد الرحمن بودا")
    
    st.write("---")
    st.markdown("<h3 style='color: #4CCEAC;'>📂 خطوة 1: ارفع المحاضرة</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختار ملف بي دي إف (PDF) للمنهج", type=["pdf"], label_visibility="collapsed")
    
    st.write("---")
    st.markdown("<h3 style='color: #4CCEAC;'>🟩 خطوة 2: استخراج الخلاصة</h3>", unsafe_allow_html=True)
    process_btn = st.button("🚀 ابدأ معالجة السحر الذكي", use_container_width=True)
    
    st.write("---")
    st.markdown("<h3 style='color: #FFA447;'>🏆 نظام مكافآت الطلاب</h3>", unsafe_allow_html=True)
    st.info("الرتبة الحالية: بروفيسور الزتونة 🏅")
    st.progress(100)

# دالة الاتصال بالذكاء الاصطناعي عبر OpenRouter
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
        return result['choices'][0]['message']['content'] if 'choices' in result else "حدث خطأ في استجابة السيرفر."
    except:
        return "تعذر الاتصال بالذكاء الاصطناعي، يرجى المحاولة مجدداً."

# 6. معالجة المستندات بقوة المحرك الجديد (pdfplumber) لقراءة وتفلاية العربي بدون لغبطة
if process_btn:
    if uploaded_file is not None and student_name.strip() != "":
        with st.spinner(f"يا {student_name}، جاري فحص المنهج بأقوى محرك قراءة وصناعة الزتونة العربي..."):
            try:
                pdf_text = ""
                # استخدام pdfplumber الجديد بدلاً من pypdf القديم للتحليل الممتاز
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text: pdf_text += text + "\n"
                
                if not pdf_text.strip():
                    st.error("تنبيه: الملف المرفوع فارغ أو عبارة عن صور فقط ولا يحتوي على نصوص مقروءة.")
                else:
                    truncated_text = pdf_text[:15000]
                    
                    # توليد المحتوى من الذكاء الاصطناعي لجميع الأقسام
                    st.session_state['summary_data'] = ask_openrouter(f"قم بقراءة هذا المنهج وتلخيصه بأسلوب أخوي مصري مبسط ومليء بالطاقة الإيجابية وركز على النقاط الذهبية والمصطلحات: {truncated_text}")
                    st.session_state['exam_capsule'] = ask_openrouter(f"استخرج أهم التريكات الخبيثة والأسئلة المتوقعة والمصطلحات الصعبة ليلة الامتحان بناءً على هذا المنهج: {truncated_text}")
                    st.session_state['quiz_questions'] = ask_openrouter(f"قم بإنشاء 3 أسئلة اختيار من متعدد (أ، ب، ج) تركز على التريكات المهمة في هذا المنهج، وفي نهاية النص تماماً اكتب مفتاح الإجابات الصحيحة بوضوح تام بأسلوب (مفتاح الحل: السؤال 1: أ، السؤال 2: ب، السؤال 3: ج). النص: {truncated_text}")
                    st.session_state['roadmap_data'] = ask_openrouter(f"بناءً على هذا المنهج، ضع خريطة طريق (Roadmap) وجدول زمني يوضح للطالب كيف يذاكر هذه المادة بالترتيب الصحيح في يوم واحد فقط: {truncated_text}")
                    st.session_state['cert_msg'] = ask_openrouter(f"اكتب رسالة تهنئة وتشجيع قصيرة جداً ومؤثرة جداً بالطاقة والمحبة للطالب {student_name} بمناسبة تدميره وتفوقه في هذا المنهج الدراسي.")
                    
                    st.session_state['quiz_evaluated'] = False
                    st.session_state['evaluation_result'] = ""
                    
                    st.balloons()
                    st.success(f"🟢 يا بروفيسور {student_name}، نظام الفحص المتطور انتهى وكل ميزات الزتونة جاهزة!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة ملف الـ PDF: {e}")
    else:
        st.warning("⚠️ ارجع للوحة التحكم على اليمين: اكتب اسمك أولاً ثم ارفع ملف الـ PDF واضغط زر المعالجة!")

# 7. الواجهة الرئيسية وعرض التبويبات الشاملة (كل الميزات القديمة والجديدة)
st.markdown("<h1 class='main-title'>📚 تطبيق الزتونة الدراسي</h1>", unsafe_allow_html=True)
st.write("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 تحدي الذكاء", "🗺️ خريطة الطريق", "📝 الملخص الفظيع", "🧠 كبسولة التريكات", "🏆 الشهادة السحرية"])

with tab1:
    st.markdown("<h3 style='color: #41C9E2;'>🔥 قسم تحدي الذكاء مع صاحبك التفاعلي</h3>", unsafe_allow_html=True)
    if st.session_state['quiz_questions'] == "":
        st.info("⚠️ عذراً يا بطل، ارفع الملف من لوحة التحكم أولاً لتوليد الأسئلة.")
    else:
        st.markdown("#### 📜 الأسئلة المستخرجة والتريكات:")
        st.success(st.session_state['quiz_questions'])
        st.write("---")
        st.markdown("#### 📝 اختر إجاباتك هنا يا بطل عشان نصحح بالذكاء الاصطناعي:")
        
        col1, col2, col3 = st.columns(3)
        with col1: q1 = st.radio("إجابة السؤال الأول:", ["أ", "ب", "ج"], key="ans1")
        with col2: q2 = st.radio("إجابة السؤال الثاني:", ["أ", "ب", "ج"], key="ans2")
        with col3: q3 = st.radio("إجابة السؤال الثالث:", ["أ", "ب", "ج"], key="ans3")
        
        if st.button("✅ تسليم الإجابات ومعرفة النتيجة"):
            st.balloons()
            st.snow()
            st.session_state['quiz_evaluated'] = True
            with st.spinner("جاري تقييم أدائك بالملي..."):
                review_prompt = f"بناءً على الاختبار: {st.session_state['quiz_questions']}\nإجابات الطالب هي: 1:{q1}، 2:{q2}، 3:{q3}\nقيمها بأسلوب مصري حماسي وصحح الخطأ وشجعه يروح للشهادة."
                st.session_state['evaluation_result'] = ask_openrouter(review_prompt)
        
        if st.session_state['quiz_evaluated']:
            st.markdown("### 📊 تقرير أداء صاحبك الذكي وتقييم الدرجات:")
            st.info(st.session_state['evaluation_result'])

with tab2:
    st.markdown("<h3 style='color: #41C9E2;'>🗺️ خريطة طريق العباقرة والمذاكرة السريعة</h3>", unsafe_allow_html=True)
    st.write(st.session_state['roadmap_data'])

with tab3:
    st.markdown("<h3 style='color: #41C9E2;'>📝 الملخص المصري الفظيع والمنظم</h3>", unsafe_allow_html=True)
    st.write(st.session_state['summary_data'])

with tab4:
    st.markdown("<h3 style='color: #41C9E2;'>🧠 قاموس الزتونة وكبسولة التريكات</h3>", unsafe_allow_html=True)
    st.write(st.session_state['exam_capsule'])

with tab5:
    st.markdown("<h3 style='color: #FFA447;'>🏆 لوحة الشرف والشهادة الذكية</h3>", unsafe_allow_html=True)
    if st.session_state['cert_msg'] != "" and student_name.strip() != "":
        st.markdown(f"""
        <div class="certificate-box">
            <div class="cert-title">شهادة تقدير وتفوق أسطورية</div>
            <div class="cert-text">يشهد تطبيق الزتونة الدراسي بأن البطل العبقري:</div>
            <div class="cert-name">{student_name}</div>
            <div class="cert-text">قد اجتاز بنجاح مراجعة المنهج الدراسي وحل تحدي الذكاء بنجاح تفاعلي مبهر.</div>
            <div class="cert-text" style="color: #4CCEAC; font-style: italic; font-weight: bold;">" {st.session_state['cert_msg']} "</div>
            <div class="cert-text" style="margin-top:30px; font-size: 16px;">التاريخ: {datetime.now().strftime('%Y-%m-%d')} | المطور المبرمج الأساسي: عبد الرحمن (BoDa) 🇪🇬</div>
        </div>
        """, unsafe_allow_html=True)
        st.success("🥇 لوحة الشرف: المتصدر الأبدي للموقع والمبرمج العبقري: عبد الرحمن (BoDa) 🇪🇬")
    else:
        st.info("👋 اكتب اسمك في لوحة التحكم، ارفع الملف وحل تحدي الذكاء، وهتطلع لك هنا شهادة تقدير أسطورية!")

st.write("---")
st.markdown("<p style='text-align: center; opacity: 0.6;'>تمت الترقية الكاملة لأعلى مستوى أداء بواسطة المبرمج عبد الرحمن (BoDa) 🚀</p>", unsafe_allow_html=True)
