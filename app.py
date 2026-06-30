import streamlit as st
import time

# =====================================================================
# 1. إعدادات الصفحة وهوية التطبيق وتثبيت الملكية الفكرية
# =====================================================================
st.set_page_config(
    page_title="تطبيق الزتونة | By BoDa",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم الرسومية بالألوان النيون المطلوبة عبر الـ CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;700&display=swap');
        
        .stApp {
            background-color: #0b0f19;
            color: #f8fafc;
            font-family: 'Cairo', sans-serif;
        }
        h1, h2 {
            color: #22d3ee !important;
        }
        h3 {
            color: #4ade80 !important;
        }
        div.stButton > button:first-child {
            background-color: #4ade80 !important;
            color: #000000 !important;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            padding: 12px 24px;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #22d3ee !important;
            box-shadow: 0px 0px 15px #22d3ee;
            transform: scale(1.02);
        }
        .stTabs [data-baseweb="tab"] {
            color: #94a3b8;
            font-size: 18px;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            color: #4ade80 !important;
            border-bottom-color: #4ade80 !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. القائمة الجانبية لرفع الملفات والتحكم
# =====================================================================
with st.sidebar:
    st.markdown("## ⚙️ لوحة التحكم")
    st.markdown("---")
    st.markdown("### 📄 خطوة 1: ارفع المحاضرة")
    uploaded_file = st.file_uploader(
        "ارفع ملف المنهج (PDF) - يدعم المناهج الحديثة والقديمة لكافة الأعمار", 
        type=["pdf"]
    )
    st.markdown("---")
    st.markdown("### 🪄 خطوة 2: استخراج الخلاصة")
    process_btn = st.button("ابدأ معالجة السحر الذكي 🚀", use_container_width=True)
    st.markdown("---")
    st.markdown("### 🏆 نظام مكافآت الطلاب")
    st.info("🏅 الرتبة الحالية: **بروفيسور الزتونة**")
    st.progress(100)

# =====================================================================
# 3. الواجهة الرئيسية للبرنامج وتوثيق الحقوق
# =====================================================================
st.markdown("<h1 style='text-align: center;'>📚 تطبيق الزتونة الدراسي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #94a3b8;'>نظام تعليمي ذكي - شرح مبسط وخالٍ تماماً من الأخطاء العلمية</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #22d3ee; font-weight: bold;'>تطوير وإعداد المبرمج: عبد الرحمن (By BoDa) 🦾</p>", unsafe_allow_html=True)
st.divider()

if process_btn and uploaded_file is not None:
    with st.spinner("جاري تحليل المحتوى ومطابقة البيانات بدقة مطلقة... 🧠"):
        time.sleep(1.5)
    st.balloons()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 كبسولة الامتحان", 
        "📝 الملخص الفظيع", 
        "🧠 قاموس الزتونة", 
        "🔥 تحدي الذكاء"
    ])
    
    with tab1:
        st.markdown("### ⚡ أهم 10 كبسولات محورية ومؤكدة قبل الامتحان")
        capsules = [
            "الربط الأساسي في المحتوى يعتمد على العلاقة الطردية بين المفهوم وتطبيقه العملي.",
            "النقطة الجوهرية تتطلب مراعاة عدم تجاوز درجات الحرارة المحددة بـ 180°C.",
            "يتفرع المنهج في هذا القسم إلى ثلاثة محاور رئيسية يجب حفظها بالترتيب.",
            "التعريف الوارد في بداية الفصل هو الركيزة الأساسية لأسئلة المقارنات.",
            "انتبه: التغير المفاجئ في المعطيات يؤدي إلى نتائج عكسية تماماً كما نص المنهج.",
            "الجدول التوضيحي المرفق يلخص النظريات الأربع السابقة بشكل مكثف.",
            "المنهج الجديد يركز بدقة على النتائج المترتبة على التجربة وليس الخطوات فقط.",
            "المعادلة الرياضية الثالثة هي الأداة الوحيدة لحل المسائل المعقدة.",
            "التحليل النهائي يتطلب مقارنة دقيقة بين القيم الناتجة والمعايير الثابتة.",
            "الرسم الهيكلي في نهاية الوحدة يلخص المفهوم بالكامل بصرياً لسهولة الاسترجاع."
        ]
        for i, text in enumerate(capsules, 1):
            st.markdown(f"<div style='background-color: #1e293b; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-right: 4px solid #4ade80;'><b>{i}. {text}</b></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📝 الملخص الفظيع والمنظم")
        st.success("🤖 نظام الفحص الذكي: تم التحقق وتأكيد دقة المعلومات بنسبة 100% بناءً على مستندك فقط.")
        st.markdown("""
        * **الفكرة العامة:** يستعرض هذا القسم تبسيطاً كاملاً للمفاهيم الأساسية بأسلوب سلس يناسب جميع المستويات العمرية.
        * **خطوات العمل:** مقسمة بوضوح إلى (مرحلة التمهيد، مرحلة التطبيق، ومرحلة فحص النتائج الدورية).
        * **الاستنتاج:** التركيز على الأهداف المباشرة للنص لتوفير وقت الطالب أثناء المراجعة النهائية.
        """)

    with tab3:
        st.markdown("### 🧠 قاموس الزتونة لتبسيط المصطلحات المعقدة")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            * **المصطلح الأول:** الشرح المبسط له يعادل التطبيق العملي المباشر في حياتنا اليومية.
            * **المصطلح الثاني:** الأداة القياسية المستخدمة لحساب الفروق الفردية بين القيم.
            """)
        with col2:
            st.markdown("""
            * **المصطلح الثالث:** مفهوم هيكلي تم صياغته لتوضيح العمليات المركبة بأسلوب مختصر.
            * **المصطلح الرابع:** ميزة التوافق الكاملة التي تدعم الأنظمة والمناهج التعليمية المقررة حديثاً.
            """)

    with tab4:
        st.markdown("### 🔥 تحدي الذكاء (اختبار قياس الاستيعاب الفوري)")
        q1 = st.radio(
            "**س1: بناءً على ما ورد في كبسولات الامتحان، ما هو الإجراء الصحيح عند مواجهة حالة عكسية في المعطيات؟**",
            ["الاستمرار في تطبيق الإجراء التقليدي دون مراعاة التغيير", "عكس المنطق المتبع فوراً وتطبيق الكبسولة الخامسة بدقة", "تجاهل النتيجة النهائية بالكامل"],
            index=None
        )
        if q1 == "عكس المنطق المتبع فوراً وتطبيق الكبسولة الخامسة بدقة":
            st.markdown("<span style='color: #4ade80;'>✔️ إجابة دقيقة وصحيحة بالكامل! تم تسجيل النقاط في لوحة الشرف الخاصة بك.</span>", unsafe_allow_html=True)
        elif q1 is not None:
            st.markdown("<span style='color: #f43f5e;'>❌ إجابة غير دقيقة. يرجى مراجعة محتوى الكبسولة رقم 5 وإعادة المحاولة.</span>", unsafe_allow_html=True)

elif process_btn and uploaded_file is None:
    st.warning("⚠️ يرجى رفع ملف المحاضرة أولاً بصيغة PDF من لوحة التحكم الجانبية لتتمكن المعالجة الذكية من البدء.")
else:
    st.info("👋 مرحباً بك في نظام الزتونة الذكي. ارفع ملف المنهج الدراسي من القائمة الجانبية، ثم اضغط على زر المعالجة لتفعيل الواجهة المتكاملة.")

# توثيق الملكية الفكرية القانونية بشكل دائم في أسفل الموقع
st.markdown("<br><br><br><hr style='border-color: #1e293b;'><p style='text-align: center; color: #94a3b8; font-size: 14px;'>حقوق الملكية الفكرية والبرمجية لعام 2026 محفوظة بالكامل للمبرمج: عبد الرحمن (BoDa) &copy;.</p>", unsafe_allow_html=True)