import os
import sys

# 프로젝트 루트 디렉토리를 파이썬 모듈 검색 경로에 추가합니다.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from license_api import app

# Vercel이 이 파일을 통해 FastAPI(app)를 실행하게 됩니다.
