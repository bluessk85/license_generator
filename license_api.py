from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
from license_manager import LicenseManager
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="블로그 꿀댕이 라이센스 API",
    description="블로그 꿀댕이 라이센스 생성 및 검증 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LicenseRequest(BaseModel):
    user_id: str
    duration: int

    class Config:
        schema_extra = {
            "example": {
                "user_id": "test_user",
                "duration": 365
            }
        }

class LicenseResponse(BaseModel):
    user_id: str
    license_key: str
    expiration_date: str
    is_valid: bool
    message: str

@app.post("/generate-license", 
         response_model=LicenseResponse,
         summary="라이센스 생성",
         description="사용자 ID와 기간을 입력받아 라이센스를 생성합니다.")
async def generate_license(request: LicenseRequest):
    """
    라이센스 생성 API
    
    - **user_id**: 네이버 아이디
    - **duration**: 라이센스 유효 기간(일)
    """
    try:
        license_manager = LicenseManager()
        expiration_date = date.today() + timedelta(days=request.duration)
        
        license_key = license_manager.create_license(request.user_id, expiration_date)
        is_valid, message = license_manager.verify_license(license_key, request.user_id)
        
        return {
            "user_id": request.user_id,
            "license_key": license_key,
            "expiration_date": expiration_date.strftime('%Y-%m-%d'),
            "is_valid": is_valid,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", 
        summary="헬스 체크",
        description="API 서버의 상태를 확인합니다.")
async def health_check():
    """
    서버 상태 확인 API
    """
    return {"status": "healthy"} 