
import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide", page_title="نظام البحث عن معلومات الموظف")
st.image("Unknown.jpeg", width=100)
st.title("🔍 نظام البحث عن معلومات الموظف")

@st.cache_data
def load_data():
    df = pd.read_excel("Book2.xlsx")
    df.fillna("", inplace=True)
    return df

df = load_data()

WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU"]
WEEKEND = ["FRI", "SAT"]

query = st.text_input("🔎 أدخل اسم الموظف أو الهوية أو أي معلومة أخرى")

if query.strip():
    results = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False, na=False)).any(axis=1)]
    if not results.empty:
        st.success(f"تم العثور على {len(results)} نتيجة مطابقة ✅")
        st.dataframe(results, use_container_width=True)
        towrite = io.BytesIO()
        results.to_excel(towrite, index=False)
        st.download_button("💾 تحميل Excel", data=towrite.getvalue(), file_name="search_results.xlsx")
    else:
        st.warning("⚠️ لا توجد نتائج مطابقة")

st.divider()
st.header("📋 تقارير الحضور الذكية")

full_attendance = df[df[WEEKDAYS].apply(lambda x: all(str(val).strip() == '1' for val in x), axis=1)]
partial_attendance = df[df[WEEKDAYS].apply(lambda x: 1 <= sum(str(val).strip() == '1' for val in x) < 5, axis=1)]
absent_all_weekdays = df[df[WEEKDAYS].apply(lambda x: all(str(val).strip() != '1' for val in x), axis=1)]
weekend_only = df[df[WEEKEND].apply(lambda x: any(str(val).strip() == '1' for val in x), axis=1) &
                  df[WEEKDAYS].apply(lambda x: all(str(val).strip() != '1' for val in x), axis=1)]

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ حضر كامل أيام الأحد إلى الخميس"):
        st.subheader("الموظفون الذين حضروا كامل الأسبوع")
        st.dataframe(full_attendance)
        buffer = io.BytesIO()
        full_attendance.to_excel(buffer, index=False)
        st.download_button("تحميل التقرير", buffer.getvalue(), file_name="full_attendance.xlsx")

with col2:
    if st.button("📅 حضر الجمعة/السبت فقط"):
        st.subheader("الموظفون الذين حضروا فقط في عطلة نهاية الأسبوع")
        st.dataframe(weekend_only)
        buffer = io.BytesIO()
        weekend_only.to_excel(buffer, index=False)
        st.download_button("تحميل التقرير", buffer.getvalue(), file_name="weekend_attendance.xlsx")

with col3:
    if st.button("🟨 غاب يوم أو أكثر من الأحد إلى الخميس"):
        st.subheader("الموظفون الذين غابوا يوم واحد أو أكثر")
        st.dataframe(partial_attendance)
        buffer = io.BytesIO()
        partial_attendance.to_excel(buffer, index=False)
        st.download_button("تحميل تقرير الغياب", buffer.getvalue(), file_name="partial_attendance.xlsx")

st.divider()
if st.button("🚫 الموظفون الغائبون تمامًا من الأحد إلى الخميس"):
    st.subheader("الموظفون الذين لم يحضروا نهائيًا من الأحد إلى الخميس")
    st.dataframe(absent_all_weekdays)
    buffer = io.BytesIO()
    absent_all_weekdays.to_excel(buffer, index=False)
    st.download_button("تحميل تقرير الغياب الكلي", buffer.getvalue(), file_name="absent_all_week.xlsx")

with st.sidebar:
    st.subheader("📘 دليل الاستخدام")
    st.markdown("""
    ابحث باسم الموظف، رقم الموظف، أو استخدم التقارير الذكية.

    **التقارير المتوفرة:**
    - حضور كامل أيام الأسبوع.
    - حضور فقط في عطلة نهاية الأسبوع.
    - غياب يوم أو أكثر.
    - غياب كامل.

    **الشعار أعلاه تابع لوزارة الحرس الوطني - الشؤون الصحية.**
    """)
    st.caption("© 2025 فريق التقنية")
