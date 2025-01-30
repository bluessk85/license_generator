import streamlit as st
from datetime import datetime, timedelta, date
from license_manager import LicenseManager
import json

class WebLicenseGenerator:
    def __init__(self):
        self.license_manager = LicenseManager()
        
    def generate_license(self, user_id, duration):
        today = date.today()
        expiration_date = today + timedelta(days=duration)
        license_key = self.license_manager.create_license(user_id, expiration_date)
        
        is_valid, message = self.license_manager.verify_license(license_key, user_id)
        
        result = {
            "user_id": user_id,
            "license_key": license_key,
            "expiration_date": expiration_date.strftime('%Y-%m-%d'),
            "is_valid": is_valid,
            "message": message
        }
        
        return result

def main():
    st.set_page_config(
        page_title="블로그 꿀댕이 라이센스 생성기",
        page_icon="🔑",
        layout="centered"
    )
    
    st.title("블로그 꿀댕이 라이센스 생성기")
    
    # 입력 필드
    user_id = st.text_input("사용자 ID", placeholder="네이버 아이디를 입력하세요")
    duration = st.number_input("라이센스 유효 기간(일)", 
                             min_value=1, 
                             max_value=3650, 
                             value=365)
    
    # 라이센스 생성 버튼
    if st.button("라이센스 생성", type="primary"):
        if not user_id:
            st.error("사용자 ID를 입력해주세요.")
            return
            
        try:
            generator = WebLicenseGenerator()
            result = generator.generate_license(user_id, duration)
            
            # 결과 표시
            st.success("라이센스가 생성되었습니다!")
            
            # 라이센스 정보를 깔끔한 카드 형태로 표시
            with st.container():
                st.markdown("### 라이센스 정보")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**사용자 ID**")
                    st.code(result["user_id"])
                    
                    st.markdown("**만료일**")
                    st.code(result["expiration_date"])
                
                with col2:
                    st.markdown("**라이센스 상태**")
                    if result["is_valid"]:
                        st.success("유효함")
                    else:
                        st.error("유효하지 않음")
                    
                    st.markdown("**메시지**")
                    st.info(result["message"])
                
                st.markdown("**라이센스 키**")
                st.code(result["license_key"], language="text")
                
                # 라이센스 정보 다운로드 버튼
                license_info = f"""사용자 ID: {result['user_id']}
라이센스 키: {result['license_key']}
만료일: {result['expiration_date']}
라이센스 상태: {'유효함' if result['is_valid'] else '유효하지 않음'}
메시지: {result['message']}"""
                
                st.download_button(
                    label="라이센스 정보 다운로드",
                    data=license_info,
                    file_name=f"license_{user_id}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"라이센스 생성 중 오류가 발생했습니다: {str(e)}")
    
    # 푸터 추가
    st.markdown("---")
    st.markdown("© 2024 블로그 꿀댕이. All rights reserved.")

if __name__ == "__main__":
    main() 