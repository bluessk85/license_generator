import uvicorn
import os
import sys

# API 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

if __name__ == "__main__":
    uvicorn.run("api.license_api:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True,
                reload_dirs=[os.path.join(os.path.dirname(__file__), 'api')]) 