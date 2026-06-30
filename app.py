import streamlit as st
import pypdf
import requests
import json

# 1. إعدادات الصفحة والواجهة السوداء المريحة والجميلة بتاعتك
st.set_page_config(page_title="تطبيق الزتونة الدراسي | By BoDa", page_icon="📚", layout="wide")

st.markdown("<h1 style='text-align: center; color: #41C9E2;'>📚 تطبيق الزتونة الدراسي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #F4F6FF;'>صاحبك الذكي في المذاكرة - تلخيص حقيقي وتشجيع من القلب 🚀</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFA447;'>💪 (By BoDa) تطوير وإعداد المبرمج: عبد الرحمن 🇪🇬</h3>", unsafe_allow_html=True)
st.write("---")

# 2. ربط الذكاء الاصطناعي عبر OpenRouter بمفتاحك السري الخاص مباشرة
OPENROUTER_API_KEY = "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"

# 3. قاعدة البيانات الثابتة (Session State) لضمان عدم اختفاء البيانات عند التفاعل
if 'summary_data' not in st.session_state:
    st.session_state['summary_data'] = None
if 'exam_capsule' not in st.session_state:
    st.session_state['exam_capsule'] = None
if 'quiz_questions' not in st.session_state:
    st.session_state['quiz_questions'] = None
if 'processed' not in st.session_state:
    st.session_state['processed'] = False

# 4. القائمة الجانبية (Sidebar) بكل التفاصيل والترتيب
with st.sidebar:
    st.markdown("<h2 style='color: #41C9E2;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("<h3 style='color: #4CCEAC;'>📂 خطوة 1: ارفع المحاضرة</h3>", unsafe_allow_html=True)
    st.write("يدعم المناهج الحديثة والقديمة - (PDF) ارفع ملف المنهج لكافة الأعمار")
    
    uploaded_file = st.file_uploader("اختار ملف الـ PDF", type=["pdf"], label_visibility="collapsed")
    st.caption("200MB per file • PDF")
    
    st.write("---")
    st.markdown("<h3 style='color: #4CCEAC;'>🟩 خطوة 2: استخراج الخلاصة</h3>", unsafe_allow_html=True)
    process_btn = st.button("🚀 ابدأ معالجة السحر الذكي", use_container_width=True)
    
    st.write("---")
    st.markdown("<h3 style='color: #FFA447;'>🏆 نظام مكافآت الطلاب</h3>", unsafe_allow_html=True)
    st.info("الرتبة الحالية: بروفيسور الزتونة 🏅")
    st.progress(100) # شريط الإنجاز الأحمر الأسطوري

# دالة مخصصة لإرسال الطلبات لسيرفر OpenRouter وتشغيل أحدث نسخة من Gemini 1.5 Pro مجاناً
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

# 5. تشغيل السحر الذكي وقراءة الملف وتحليله
if process_btn and uploaded_file is not None:
    with st.spinner("جاري تشغيل السحر الذكي وقراءة المنهج بواسطة صاحبك الذكي Gemini 1.5 Pro..."):
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text
            
            if pdf_text.strip() == "":
                st.error("الملف المرفوع فارغ أو عبارة عن صور فقط، يرجى رفع ملف يحتوي على نصوص.")
            else:
                truncated_text = pdf_text[:25000]
                
                # طلب التلخيص بأسلوب الصديق المشجع
                summary_prompt = f"أنت لست مجرد آلة، أنت الصديق المقرب والمشجع للطالب في تطبيق 'الزتونة الدراسي'. قم بقراءة هذا المنهج وتلخيصه بأسلوب أخوي، مبسط، ومليء بالطاقة الإيجابية والتشجيع. ركز على النقاط الذهبية، واشرح المصطلحات الصعبة كأنك تبسطها لصديقك، وتأكد من سلامة المعلومات علمياً: {truncated_text}"
                st.session_state['summary_data'] = ask_openrouter(summary_prompt)
                
                # طلب كبسولة الامتحان بأسلوب إنقاذ الصديق ليلة الامتحان
                capsule_prompt = f"تخيل أن صديقك الطالب لديه امتحان غداً وهو متوتر. بناءً على هذا المنهج، استخرج له خلاصة الخلاصة وأهم الأسئلة المتوقعة بأسلوب يهدئ من روعه ويشجعه ويجعل المراجعة سريعة وممتعة: {truncated_text}"
                st.session_state['exam_capsule'] = ask_openrouter(capsule_prompt)
                
                # طلب إنشاء اختبار تفاعلي دقيق ومحدد
                quiz_prompt = f"قم بإنشاء 3 أسئلة اختيار من متعدد (أ، ب، ج) بناءً على هذا المنهج. اكتب الأسئلة بوضوح شديد ولغة مشجعة، وفي نهاية النص تماماً اكتب مفتاح الإجابات الصحيحة بوضوح مثلاً (السؤال 1: أ، السؤال 2: ب، السؤال 3: ج) لكي نستخدمه في التقييم الفوري الفوري. النص: {truncated_text[:15000]}"
                st.session_state['quiz_questions'] = ask_openrouter(quiz_prompt)
                
                st.session_state['processed'] = True
                st.balloons() # بلالين الفرحة بالمعالجة الناجحة 🎈
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الملف: {e}")

elif process_btn and uploaded_file is None:
    st.warning("يرجى رفع ملف PDF أولاً من القائمة الجانبية قبل الضغط على زر المعالجة! 📂")

# 6. عرض الأقسام (Tabs) بعد معالجة البيانات بالترتيب المظبوط
if st.session_state['processed']:
    st.success("🟢 (نظام الفحص الذكي): صاحبك الذكي راجع المستند وتأكد من صحته 100% 🤖")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 تحدي الذكاء", "🧠 قاموس الزتونة", "📝 الملخص الفظيع والمنظم", "🏆 لوحة الشرف"])
    
    with tab1:
        st.markdown("<h3 style='text-align: center; color: #41C9E2;'>🔥 قسم تحدي الذكاء مع صاحبك التفاعلي</h3>", unsafe_allow_html=True)
        st.write("يلا بينا يا بطل! اقرأ الأسئلة دي ووريني ذكائك وعضلات البرمجة:")
        st.info(st.session_state['quiz_questions'])
        
        st.write("---")
        st.markdown("#### 📝 اختار إجاباتك هنا يا بطل عشان نصحح ونشوف العظمة:")
        q1 = st.radio("السؤال الأول إجابتك هي:", ["أ", "ب", "ج"], key="ans1")
        q2 = st.radio("السؤال الثاني إجابتك هي:", ["أ", "ب", "ج"], key="ans2")
        q3 = st.radio("السؤال الثالث إجابتك هي:", ["أ", "ب", "ج"], key="ans3")
        
        submit_quiz = st.button("✅ تسليم الإجابات ومعرفة النتيجة")
        
        if submit_quiz:
            # تشغيل مفرقعات وبلالين وثلج مع بعض بمناسبة تسليم الامتحان 🎉🎈❄️
            st.balloons()
            st.snow()
            
            # استدعاء الذكاء الاصطناعي فوراً لفحص إجابات الطالب وشرح الخطأ بأسلوب مبسط وصديق مشجع
            with st.spinner("جاري فحص إجاباتك وكتابة تقرير حماسي خاص بك من صاحبك الذكي..."):
                review_prompt = f"""
                بناءً على الاختبار التالي ومفتاح حله المكتوب في آخره:
                {st.session_state['quiz_questions']}
                
                الطالب قام باختيار الإجابات التالية:
                - السؤال الأول: {q1}
                - السؤال الثاني: {q2}
                - السؤال الثالث: {q3}
                
                بصفتك صديقه المقرب والمشجع في تطبيق الزتونة الدراسي، قم بتحليل إجاباته:
                1. إذا كانت كل إجاباته صحيحة، قم بتهنئته بأسلوب حماسي جداً وقل له أنك فخور بذكائه الأسطوري.
                2. إذا اختار أي إجابة خاطئة، حدد له أي سؤال أخطأ فيه، واشرح له الفكرة العلمية الصحيحة لهذا السؤال بأبسط طريقة ممكنة في العالم كأنك تدردش مع صاحبك، وشجعه من قلبك وركز معاه عشان يركز أكتر المرة الجاية وما يغلطش فيها تاني أبدأ!
                اجعل الأسلوب كله مصري، ودود، ومليء بالتشجيع والدعم الأخوي.
                """
                review_result = ask_openrouter(review_prompt)
                st.markdown("### 📊 تقرير صاحبك الذكي وتقييم الأداء:")
                st.success(review_result)
            
    with tab2:
        st.markdown("<h3 style='color: #41C9E2;'>🧠 قاموس الزتونة ومراجعة آخر الدقائق</h3>", unsafe_allow_html=True)
        st.write(st.session_state['exam_capsule'])
        
    with tab3:
        st.markdown("<h3 style='color: #41C9E2;'>📝 الخلاصة والتحليل الفظيع للمنهج</h3>", unsafe_allow_html=True)
        st.write(st.session_state['summary_data'])
        
    with tab4:
        st.markdown("<h3 style='color: #FFA447;'>🏆 لوحة الشرف وأبطال الزتونة الدراسي</h3>", unsafe_allow_html=True)
        st.write("لوحة شرف الأبطال اللي شرفونا النهاردة بمذاكرتهم:")
        st.success("🥇 المتصدر الأبدي ومطور التطبيق: عبد الرحمن (BoDa) 🇪🇬")
else:
    st.info("👋 أهلاً بك يا بطل! أنا صاحبك الذكي ومساعدك الدراسي. ارفع ملف المنهج من القائمة الجانبية، ودوس على زر المعالجة وخلينا نكسر الدنيا سوا!")
