"""
基準物検出ロジック（モック実装）
後からYOLO実装に差し替え可能な構造にする
"""

from PIL import Image
from typing import Optional, Dict, Any


def mock_detect_reference_object(image: Image.Image) -> Optional[Dict[str, Any]]:
    """
    モック実装: 基準物を検出する関数
    
    実際の実装では、この関数内でYOLOモデルを実行して
    ポスト・ドアホン・ブロックを検出する。
    
    Args:
        image: PIL Image オブジェクト
        
    Returns:
        検出された場合は基準物情報の辞書、検出されない場合はNone
        辞書の形式:
        {
            "type": "postbox" | "intercom" | "block",
            "x": int,  # bounding boxの左上x座標（px）
            "y": int,  # bounding boxの左上y座標（px）
            "width": int,  # bounding boxの幅（px）
            "height": int,  # bounding boxの高さ（px）
            "confidence": float  # 信頼度（0.0-1.0）
        }
    """
    # モック実装: 画像の中央付近に固定のpostboxを返す
    img_width, img_height = image.size
    
    # 画像の中央付近に配置（画像サイズの20-40%の位置）
    bbox_x = int(img_width * 0.2)
    bbox_y = int(img_height * 0.3)
    bbox_width = int(img_width * 0.2)  # 画像幅の20%
    bbox_height = int(img_height * 0.15)  # 画像高さの15%
    
    return {
        "type": "postbox",
        "x": bbox_x,
        "y": bbox_y,
        "width": bbox_width,
        "height": bbox_height,
        "confidence": 0.94
    }


# 後からYOLO実装に差し替える場合は、この関数を実装して
# main.pyで import を変更するだけでOK
def detect_reference_object(image: Image.Image) -> Optional[Dict[str, Any]]:
    """
    実際のYOLO検出関数（将来実装用）
    
    現時点では mock_detect_reference_object を呼び出すだけ
    """
    return mock_detect_reference_object(image)

