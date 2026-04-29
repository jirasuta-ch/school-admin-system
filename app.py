import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบงานสารบรรณโรงเรียน", page_icon="📝")
# --- ปรับแต่ง UI ให้ดู Modern & Minimal ---
st.markdown("""
    <style>
    /* 1. ปรับแต่งปุ่มกดหลัก */
    div.stButton > button {
        width: 100%;
        height: 110px;               /* สูงกำลังดีสำหรับนิ้วจิ้ม */
        border-radius: 20px;          /* โค้งมนแบบแอปสมัยใหม่ */
        border: 1px solid #E0E0E0;    /* ขอบบางๆ สีเทาอ่อน */
        background-color: #FFFFFF;    /* พื้นหลังสีขาวสะอาด */
        color: #1E3A8A;               /* ตัวอักษรสีน้ำเงินเข้ม (Modern Navy) */
        font-size: 22px !important;   /* ขนาดตัวอักษรใหญ่ชัดเจน */
        font-weight: 700;             /* ตัวหนาพิเศษ */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* เงาบางๆ แบบนุ่มนวล */
        transition: all 0.3s ease;    /* เวลาเปลี่ยนสีให้ดูสมูท */
    }

    /* 2. เอฟเฟกต์เวลาเอาเมาส์ชี้ หรือกด (Hover) */
    div.stButton > button:hover {
        border: 1px solid #1E3A8A;    /* ขอบเปลี่ยนเป็นสีเข้ม */
        background-color: #F8FAFC;    /* เปลี่ยนสีพื้นหลังนิดเดียวพอ */
        color: #2563EB;               /* ตัวอักษรสีฟ้าสว่างขึ้น */
        transform: translateY(-3px);  /* ปุ่มลอยขึ้นนิดนึงเวลาชี้ */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); /* เงาเข้มขึ้นตอนลอย */
    }

    /* 3. ปรับแต่งกล่อง Info (เลขล่าสุด) ให้เข้ากัน */
    div.stAlert {
        border-radius: 15px;
        border: none;
        background-color: #EFF6FF;    /* สีฟ้าอ่อนแบบพาสเทล */
        color: #1E3A8A;
    }
    
    /* 4. ปรับหัวข้อ (Title) */
    h1 {
        color: #0F172A;
        font-family: 'Sarabun', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

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
        st.title("🏫 ระบบออกเลขสารบรรณออนไลน์")
        st.write("โรงเรียนบ้านพรหมมาสามัคคี | สพป.กำแพงเพชร เขต 2")
       

        # --- ส่วนที่เพิ่มใหม่: แสดงข้อมูลล่าสุด ---
        try:
            # ใช้ฟังก์ชัน get_data() ที่คุณครูสร้างไว้ในบรรทัดที่ 14
            df_last = get_data() 
            
            if df_last is not None and not df_last.empty:
                last_row = df_last.iloc[-1]
                
                # ดึงค่ามาโชว์ (เช็คชื่อหัวตารางใน Sheets ให้ตรงกันนะครับ)
                l_no = last_row.get('เลขที่', 'ไม่มีข้อมูล')
                l_sub = last_row.get('เรื่อง', 'ไม่มีข้อมูล')
                l_date_raw = str(last_row.get('วันที่', 'ไม่มีข้อมูล'))
                l_date = l_date_raw.split(' ')[0]
                
                st.info(f"📢 **เลขล่าสุด:** {l_no} | **เรื่อง:** {l_sub} | **เมื่อ:** {l_date}")
            else:
                st.caption("🔍 ยังไม่มีข้อมูลการออกเลขในฐานข้อมูล")
        except Exception as e:
            st.caption(f"⚠️ ไม่สามารถดึงเลขล่าสุดได้: {str(e)}")

        st.divider() # ขีดเส้นคั่นเพื่อความสวยงาม
        st.write("กรุณาเลือกประเภทเอกสารที่ต้องการออกเลข")
        # --- ปุ่มกด 3 ปุ่มเดิมของคุณครู ---
        col1, col2, col3 = st.columns(3)
        # ... โค้ดปุ่มกดของคุณครู ...
    
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

        st.divider()
        st.subheader("📊 ตรวจสอบเลขล่าสุดรายประเภท")
        
        # สร้าง 3 คอลัมน์สำหรับโชว์ 3 ประเภทเอกสาร
        sum_col1, sum_col2, sum_col3 = st.columns(3)
        
        types = ["บันทึกข้อความ", "เลขคำสั่ง", "เลขหนังสือส่ง"]
        cols = [sum_col1, sum_col2, sum_col3]
        
        for doc_type, col in zip(types, cols):
            with col:
                st.markdown(f"**📍 {doc_type}**")
                # กรองข้อมูลเฉพาะประเภทนั้นๆ และหยิบ 2 แถวล่าสุด
                filtered_df = df_last[df_last['ประเภท'] == doc_type].tail(2)
                
                if not filtered_df.empty:
                    # วนลูปโชว์เลข 2 ลำดับล่าสุด
                    for _, row in filtered_df.iloc[::-1].iterrows():
                        st.caption(f"🔹 เลขที่: {row['เลขที่']}\n\n_{row['เรื่อง']}_")
                else:
                    st.caption("ยังไม่มีข้อมูล")

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
