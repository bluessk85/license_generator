import requests
from datetime import datetime, date, timedelta
from cryptography.fernet import Fernet
import json
from config import ENCRYPTED_MASTER_KEY, ENCRYPTION_KEY
import platform
import os

class LicenseManager:
    def __init__(self):
        f = Fernet(ENCRYPTION_KEY)
        self.master_key = f.decrypt(ENCRYPTED_MASTER_KEY).decode()
        self.fernet = Fernet(self.master_key.encode())

    def get_current_date(self):
        try:
            # 시간 서버에서 현재 시간 가져오기 시도
            response = requests.get("http://worldtimeapi.org/api/ip")
            data = response.json()
            return date.fromisoformat(data['datetime'].split('T')[0])
        except:
            # 실패시 로컬 시간 사용 (1일 유예기간 부여)
            return date.today() - timedelta(days=1)

    def create_license(self, user_id, expiration_date):
        """라이센스 생성 함수"""
        license_data = {
            'u': user_id,
            'e': expiration_date.isoformat(),  # 날짜만 저장
            'os': platform.system(),  # OS 정보 추가
            'created': date.today().isoformat()  # 생성일 추가
        }
        encrypted_license = self.fernet.encrypt(json.dumps(license_data).encode())
        return encrypted_license.decode()

    def verify_license(self, license_key, user_id):
        """라이센스 검증 함수"""
        try:
            decrypted_data = self.fernet.decrypt(license_key.encode())
            license_data = json.loads(decrypted_data.decode())

            # 사용자 ID 검증
            if license_data['u'] != user_id:
                return False, "라이센스가 현재 사용자 ID와 일치하지 않습니다."

            # 만료일 검증
            expiration_date = date.fromisoformat(license_data['e'])
            current_date = self.get_current_date()

            if current_date > expiration_date:
                days_expired = (current_date - expiration_date).days
                return False, f"라이센스가 {days_expired}일 전에 만료되었습니다."

            # 남은 기간 계산
            days_remaining = (expiration_date - current_date).days
            
            return True, f"유효한 라이센스입니다. 만료까지 {days_remaining}일 남았습니다."

        except Exception as e:
            return False, f"라이센스 확인 중 오류 발생: {str(e)}"

    def save_license_info(self, user_id, license_key):
        """라이센스 정보 저장"""
        try:
            filename = f"license_{user_id}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"사용자 ID: {user_id}\n")
                f.write(f"라이센스 키: {license_key}\n")
                f.write(f"저장 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            return True
        except Exception:
            return False