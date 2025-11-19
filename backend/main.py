"""
FastAPI エントリポイント
門柱画像解析APIを提供する
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from typing import Optional, Dict, Any
from pydantic import BaseModel

from detection import detect_reference_object

app = FastAPI(title="門柱画像解析API", version="1.0.0")

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReferenceObject(BaseModel):
    """基準物情報のレスポンスモデル"""
    type: str  # "postbox" | "intercom" | "block"
    x: int
    y: int
    width: int
    height: int
    confidence: float


class AnalyzeResponse(BaseModel):
    """解析APIのレスポンスモデル"""
    reference_object: Optional[ReferenceObject]
    pillar_image_width: int
    pillar_image_height: int


@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {
        "message": "門柱画像解析API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/",
            "analyze": "/api/v1/pillar/analyze"
        }
    }


@app.post("/api/v1/pillar/analyze", response_model=AnalyzeResponse)
async def analyze_pillar_image(pillar_image: UploadFile = File(...)):
    """
    門柱画像を解析して基準物を検出する
    
    Args:
        pillar_image: multipart/form-dataで送信された画像ファイル
        
    Returns:
        AnalyzeResponse: 検出結果と画像サイズ情報
    """
    try:
        # 画像ファイルを読み込む
        image_bytes = await pillar_image.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # 画像サイズを取得
        img_width, img_height = image.size
        
        # 基準物を検出（現時点ではモック実装）
        reference_obj = detect_reference_object(image)
        
        # レスポンスを構築
        response_data = {
            "reference_object": reference_obj,
            "pillar_image_width": img_width,
            "pillar_image_height": img_height
        }
        
        return AnalyzeResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"画像解析エラー: {str(e)}")

