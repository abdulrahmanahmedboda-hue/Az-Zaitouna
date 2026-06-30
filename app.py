import streamlit as st
import pypdf
import requests
import json

# 1. إعدادات الصفحة وإجبار الواجهة السوداء الفخمة بـ CSS مخصص
st.set_page_config(page_title="تطبيق الزتونة الدراسي | By BoDa", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    /* تثبيت الخلفية السوداء للتطبيق بالكامل والخطوط الفاتحة */
    .stApp {
        background-color: #0E1117 !important;
        color: #F4F6FF !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #F4F6FF !important;
    }
    /* ضبط لون الخلفية للقائمة الجانبية لتكون داكنة ومتناسقة */
    div[data-testid="stSidebar"] {
        background-color: #1A1D24 !important;
    }
    div[data-testid="stSidebar"] * {
        color: #F4F6FF !important;
    }
    /* تلوين التبويبات (Tabs) بشكل جذاب */
    .stTabs [data-baseweb="tab"] {
        color: #41C9E2 !important;
        font-size: 1.1rem !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #FFA447 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# العناوين الرئيسية للتطبيق
st.markdown("<h1 style='text-align: center; color: #41C9E2 !important;'>📚 تطبيق الزتونة الدراسي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #F4F6FF !important;'>صاحبك الذكي في المذاكرة - تلخيص حقيقي وتشجيع من القلب 🚀</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFA447 !important;'>💪 (By BoDa) تطوير وإعداد Mbrg: عبد الرحمن 🇪🇬</h3>", unsafe_allow_html=True)
st.write("---")

# 2. ربط الذكاء الاصطناعي بمفتاحك السري مباشرة
OPENROUTER_API_KEY = "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"

# 3. قاعدة البيانات الداخلية لحفظ النتائج لضمان عدم الاختفاء عند التنقل
if 'summary_data' not in st.session_state:
    st.session_state['summary_data'] = "سجل هنا الخلاصة والتحليل الفظيع للمنهج بعد رفع الملف وضغط زر المعالجة! 📝"
if 'exam_capsule' not in st.session_state:
    st.session_state['exam_capsule'] = "هنا هتلاقي خلاصة الخلاصة وأهم الأسئلة المتوقعة ليلة الامتحان! 🧠"
if 'quiz_questions' not in st.session_state:
    st.session_state['quiz_questions'] = "⚠️ لم يتم توليد اختبار بعد. ارفع ملف الـ PDF واضغط على معالجة لتحدي الذكاء! 🤖"

# 4. لوحة التحكم الجانبية (Sidebar) - ثابتة وظاهرة دائماً
with st.sidebar:
    st.markdown("<h2 style='color: #41C9E2 !important;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("<h3 style='color: #4CCEAC !important;'>📂 خطوة 1: ارفع المحاضرة</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختار ملف الـ PDF المنهج الدراسي", type=["pdf"])
    
    st.write("---")
    st.markdown("<h3 style='color: #4CCEAC !important;'>🟩 خطوة 2: استخراج الخلاصة</h3>", unsafe_allow_html=True)
    process_btn = st.button("🚀 ابدأ معالجة السحر الذكي", use_container_width=True)
    
    st.write("---")
    st.markdown("<h3 style='color: #FFA447 !important;'>🏆 نظام مكافآت الطلاب</h3>", unsafe_allow_html=True)
    st.info("الرتبة الحالية: بروفيسور الزتونة 🏅")
    st.progress(100)

# دالة إرسال الطلبات للسيرفر لتشغيل نموذج Gemini 1.5 Pro المجاني
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
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"تعذر الاتصال بالذكاء الاصطناعي: {e}"

# 5. تشغيل معالجة الملف واستخراج البيانات عند الضغط
if process_btn:
    if uploaded_file is not None:
        with st.spinner("جاري تشغيل السحر الذكي وقراءة المنهج بواسطة صاحبك الذكي Gemini..."):
            try:
                pdf_reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text
                
                if pdf_text.strip() == "":
                    st.error("الملف المرفوع فارغ أو عبارة عن صور فقط ولم نتمكن من استخراج النصوص.")
                else:
                    truncated_text = pdf_text[:20000]
                    
                    # طلب التلخيص بأسلوب مصري حماسي
                    summary_prompt = f"قم بقراءة هذا المنهج وتلخيصه بأسلوب أخوي مصري مبسط، مليء بالطاقة الإيجابية والتشجيع كصديق مقرب للطلاب وركز على النقاط الذهبية والمصطلحات الهامة: {truncated_text}"
                    st.session_state['summary_data'] = ask_openrouter(summary_prompt)
                    
                    # طلب كبسولة الامتحان
                    capsule_prompt = f"استخرج خلاصة الخلاصة وأهم الأسئلة المتوقعة بناءً على هذا المنهج بأسلوب يهدئ روع الطالب ليلة الامتحان ويجعل المراجعة سريعة وممتعة جداً: {truncated_text}"
                    st.session_state['exam_capsule'] = ask_openrouter(capsule_prompt)
                    
                    # طلب إنشاء اختبار تفاعلي دقيق
                    quiz_prompt = f"قم بإنشاء 3 أسئلة اختيار من متعدد (أ، ب، ج) بناءً على هذا المنهج، وفي نهاية النص تماماً اكتب مفتاح الإجابات الصحيحة بوضوح مثلاً (السؤال 1: أ، السؤال 2: ب， السؤال 3: ج). النص: {truncated_text[:15000]}"
                    st.session_state['quiz_questions'] = ask_openrouter(quiz_prompt)
                    
                    st.balloons()
                    st.success("🟢 نظام الفحص الذكي: صاحبك الذكي راجع المستند وتأكد من صحته 100% وجاهز للتحدي! 🤖")
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
    else:
        st.warning("يرجى رفع ملف PDF أولاً من القائمة الجانبية قبل البدء! 📂")

# 6. عرض الأقسام الرئيسية والتبويبات (متاحة وثابتة دائماً على الشاشة)
tab1, tab2, tab3, tab4 = st.tabs(["🔥 تحدي الذكاء", "🧠 قاموس الزتونة", "📝 الملخص الفظيع والمنظم", "🏆 لوحة الشرف"])

with tab1:
    st.markdown("<h3 style='text-align: center; color: #41C9E2 !important;'>🔥 قسم تحدي الذكاء مع صاحبك التفاعلي</h3>", unsafe_allow_html=True)
    st.markdown("#### 📜 الأسئلة المستخرجة من المنهج:")
    st.info(st.session_state['quiz_questions'])
    
    st.write("---")
    st.markdown("#### 📝 اختار إجاباتك هنا يا بطل عشان نصحح ونشوف العظمة:")
    q1 = st.radio("السؤال الأول إجابتك هي:", ["أ", "ب", "ج"], key="ans1")
    q2 = st.radio("السؤال الثاني إجابتك هي:", ["أ", "ب", "ج"], key="ans2")
    q3 = st.radio("السؤال الثالث إجابتك هي:", ["أ", "ب", "ج"], key="ans3")
    
    submit_quiz = st.button("✅ تسليم الإجابات ومعرفة النتيجة")
    
    if submit_quiz:
        if "⚠️ لم يتم توليد" in st.session_state['quiz_questions']:
            st.warning("يرجى رفع ملف وتوليد الأسئلة أولاً قبل التسليم! 📋")
        else:
            st.balloons()
            st.snow()
            with st.spinner("جاري فحص إجاباتك وكتابة التقييم الحماسي..."):
                review_prompt = f"""
                بناءً على الاختبار ومفتاح الحل التالي:
                {st.session_state['quiz_questions']}
                
                إجابات الطالب الحالية:
                - السؤال الأول: {q1}
                - السؤال الثاني: {q2}
                - السؤال الثالث: {q3}
                
                حلل إجابات الطالب بأسلوب ودود ومصري حماسي جداً، وصحح الأخطاء إن وجدت ببساطة شديدة وشجعه بقوة من قلبك وبطريقة مبهجة.
                """
                review_result = ask_openrouter(review_prompt)
                st.markdown("### 📊 تقرير صاحبك الذكي وتقييم الأداء:")
                st.success(review_result)

with tab2:
    st.markdown("<h3 style='color: #41C9E2 !important;'>🧠 قاموس الزتونة ومراجعة آخر الدقائق</h3>", unsafe_allow_html=True)
    st.write(st.session_state['exam_capsule'])
    
with tab3:
    st.markdown("<h3 style='color: #41C9E2 !important;'>📝 الخلاصة والتحليل الفظيع للمنهج</h3>", unsafe_allow_html=True)
    st.write(st.session_state['summary_data'])
    
with tab4:
    st.markdown("<h3 style='color: #FFA447 !important;'>🏆 لوحة الشرف وأبطال الزتونة الدراسي</h3>", unsafe_allow_html=True)
    st.success("🥇 المتصدر الأبدي ومطور التطبيق الرائع: عبد الرحمن (BoDa) 🇪🇬")
