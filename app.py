import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบงานสารบรรณโรงเรียน", page_icon="📝")

# เชื่อมต่อกับ Google Sheets
# หมายเหตุ: คุณครูต้องนำ URL ของ Google Sheets มาใส่ในส่วน secrets หรือตอนใช้งานจริง
conn = st.connection("gsheets", type=GSheetsConnection)

# ฟังก์ชันดึงข้อมูลล่าสุด
def get_data():
    return conn.read(worksheet="Data", ttl="0")

# ฟังก์ชันคำนวณเลขถัดไป
def get_next_number(df, doc_type):
    current_year = datetime.now().year + 543
    if df.empty:
        return f"1/{current_year}"
    
    # กรองเฉพาะประเภทที่เลือก
    filtered_df = df[df['ประเภท'] == doc_type]
    next_num = len(filtered_df) + 1
    return f"{next_num}/{current_year}"

# --- หน้าแรก (Main Menu) ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_type' not in st.session_state:
    st.session_state.selected_type = None

if st.session_state.page == 'main':
    st.title("🏛️ ระบบออกเลขสารบรรณออนไลน์")
    st.write("กรุณาเลือกประเภทเอกสารที่ต้องการออกเลข")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 บันทึกข้อความ", use_container_width=True):
            st.session_state.selected_type = "บันทึกข้อความ"
            st.session_state.page = 'form'
            st.rerun()
            
    with col2:
        if st.button("📜 เลขคำสั่ง", use_container_width=True):
            st.session_state.selected_type = "คำสั่ง"
            st.session_state.page = 'form'
            st.rerun()
            
    with col3:
        if st.button("📩 เลขหนังสือส่ง", use_container_width=True):
            st.session_state.selected_type = "หนังสือส่ง"
            st.session_state.page = 'form'
            st.rerun()

# --- หน้ากรอกข้อมูล (Form Page) ---
elif st.session_state.page == 'form':
    st.button("⬅️ กลับหน้าหลัก", on_click=lambda: setattr(st.session_state, 'page', 'main'))
    
    doc_type = st.session_state.selected_type
    st.header(f"ออกเลข: {doc_type}")
    
    # ดึงข้อมูลมาเพื่อแสดงเลขล่าสุด
    df = get_data()
    next_no = get_next_number(df, doc_type)
    
    with st.container(border=True):
        st.subheader(f"เลขที่คุณจะได้รับคือ: :blue[{next_no}]")
        
        with st.form("my_form", clear_on_submit=True):
            subject = st.text_input("ชื่อเรื่องเอกสาร")
            name = st.text_input("ชื่อผู้ขอออกเลข (ชื่อ-นามสกุล)")
            submit = st.form_submit_button("✅ ยืนยันออกเลข", use_container_width=True)
            
            if submit:
                if subject and name:
                    # เตรียมข้อมูลบันทึก
                    new_row = pd.DataFrame([{
                        "ลำดับ": len(df) + 1,
                        "วันที่": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "ประเภท": doc_type,
                        "เลขที่เอกสาร": next_no,
                        "เรื่อง": subject,
                        "เจ้าของเรื่อง": name
                    }])
                    
                    # บันทึกลง Google Sheets
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(worksheet="Data", data=updated_df)
                    
                    # เก็บค่าไปโชว์หน้าสำเร็จ
                    st.session_state.final_no = next_no
                    st.session_state.final_subject = subject
                    st.session_state.page = 'success'
                    st.rerun()
                else:
                    st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# --- หน้าสำเร็จ (Success Page) ---
elif st.session_state.page == 'success':
    st.balloons()
    st.success(f"ออกเลข{st.session_state.selected_type} สำเร็จ!")
    
    st.markdown(f"""
    ### เลขที่ได้รับ: **{st.session_state.final_no}**
    **เรื่อง:** {st.session_state.final_subject}
    """)
    
    if st.button("กลับหน้าหลัก"):
        st.session_state.page = 'main'
        st.rerun()
