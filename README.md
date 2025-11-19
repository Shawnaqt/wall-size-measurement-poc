# 寸法測定PoC - 門柱画像解析システム

門柱の写真から基準物（ポスト・ドアホン・ブロック）を検出し、ユーザーが指定した矩形の実寸を測定するPoC（Proof of Concept）です。

## 機能概要

1. **画像アップロード**: 門柱の写真を選択
2. **基準物検出**: AI（YOLO）で基準物を自動検出（現時点ではモック実装）
3. **基準寸法入力**: 検出された基準物の実寸を入力
4. **矩形選択**: 画像上でドラッグして貼り付け位置を指定
5. **実寸表示**: 選択した矩形の実寸（幅・高さ・アスペクト比）を表示

## プロジェクト構成

```
project_root/
├── backend/
│   ├── main.py           # FastAPI エントリポイント
│   ├── detection.py      # YOLO or モック検出ロジック
│   └── requirements.txt  # Python依存パッケージ
├── frontend/
│   ├── index.html        # メインHTML
│   ├── style.css         # スタイルシート
│   └── main.js           # メインJavaScript
└── README.md             # このファイル
```

## セットアップ手順

### バックエンドのセットアップ

1. **Python環境の準備**
   - Python 3.8以上が必要です
   - 仮想環境の作成（推奨）:
     ```bash
     cd backend
     python -m venv venv
     ```

2. **仮想環境の有効化**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **依存パッケージのインストール**
   ```bash
   pip install -r requirements.txt
   ```

4. **サーバーの起動**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   
   サーバーが起動すると、以下のURLでアクセスできます:
   - API: http://127.0.0.1:8000
   - APIドキュメント: http://127.0.0.1:8000/docs

### フロントエンドのセットアップ

1. **簡易HTTPサーバーの起動**
   
   VSCodeを使用している場合:
   - `frontend`フォルダを右クリック
   - 「Open with Live Server」を選択
   - または、拡張機能「Live Server」をインストールして使用
   
   その他の方法:
   - Pythonの簡易サーバーを使用:
     ```bash
     cd frontend
     python -m http.server 5500
     ```
   - Node.jsのhttp-serverを使用:
     ```bash
     npx http-server frontend -p 5500
     ```

2. **ブラウザでアクセス**
   - http://127.0.0.1:5500 にアクセス

## 使用方法

1. **画像の選択**
   - 「画像ファイルを選択」ボタンをクリックして、門柱の写真を選択

2. **基準物の解析**
   - 「基準物を解析する」ボタンをクリック
   - サーバーが画像を解析し、基準物（ポストなど）の位置を検出
   - 画像上に赤い枠が表示されます

3. **基準物の確認**
   - 検出された枠が正しいか確認
   - 「はい（正しい）」をクリック

4. **基準物の実寸入力**
   - 基準物の種別（ポスト/ドアホン/ブロック）が表示されます
   - 幅と高さ（mm）を入力（デフォルト値が設定されています）
   - 「基準寸法を確定」をクリック

5. **貼り付け位置の指定**
   - 画像上でマウスをドラッグして矩形を描画
   - 貼り付けたい位置の範囲を指定

6. **結果の確認**
   - 選択した矩形の実寸が表示されます:
     - 幅（mm）
     - 高さ（mm）
     - アスペクト比

## API仕様

### POST /api/v1/pillar/analyze

門柱画像を解析して基準物を検出するエンドポイント。

**リクエスト:**
- メソッド: POST
- Content-Type: multipart/form-data
- パラメータ:
  - `pillar_image`: 画像ファイル

**レスポンス（成功時）:**
```json
{
  "reference_object": {
    "type": "postbox",
    "x": 120,
    "y": 300,
    "width": 200,
    "height": 150,
    "confidence": 0.94
  },
  "pillar_image_width": 1080,
  "pillar_image_height": 1920
}
```

**レスポンス（検出失敗時）:**
```json
{
  "reference_object": null,
  "pillar_image_width": 1080,
  "pillar_image_height": 1920
}
```

## 技術スタック

- **フロントエンド**: HTML5, CSS3, JavaScript (Vanilla JS), Canvas API
- **バックエンド**: Python 3.8+, FastAPI, Pillow
- **AI検出**: 現時点ではモック実装（将来YOLOに差し替え予定）

## 注意事項

- このPoCはローカル開発環境を想定しています
- 現時点では基準物検出はモック実装です（固定のダミーbounding boxを返します）
- 将来的にYOLO実装に差し替える場合は、`backend/detection.py`の`detect_reference_object`関数を実装してください
- CORS設定は開発用に全オリジンを許可しています。本番環境では適切に設定してください

## トラブルシューティング

### バックエンドが起動しない
- Pythonのバージョンを確認（3.8以上が必要）
- 仮想環境が有効化されているか確認
- 依存パッケージが正しくインストールされているか確認

### フロントエンドからAPIに接続できない
- バックエンドが起動しているか確認（http://127.0.0.1:8000/docs にアクセスして確認）
- ブラウザのコンソールでエラーメッセージを確認
- CORSエラーの場合は、バックエンドのCORS設定を確認

### 画像が表示されない
- 画像ファイルの形式を確認（JPEG, PNGなど）
- ブラウザのコンソールでエラーメッセージを確認

## 今後の拡張予定

- [ ] YOLOモデルによる実際の基準物検出
- [ ] 基準物の枠を手動で修正する機能
- [ ] カメラからの直接撮影機能
- [ ] 複数の基準物に対応
- [ ] 測定結果の保存・エクスポート機能

## ライセンス

このプロジェクトはPoC（概念実証）用のコードです。

