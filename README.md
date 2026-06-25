# Markov Weather Station

> 2次マルコフ連鎖と画像認識（TensorFlow Lite）を組み合わせた、天気記録・予報アプリケーション

---

## 概要

毎日の天気（晴れ・曇り・雨・雪）を手動またはAI画像認識で記録し、2次マルコフ連鎖を用いて最大5日先の天気を確率的に予報するデスクトップアプリです。GUIとCUIの両方で動作します。

---

## ディレクトリ構成

```
Markov Weather Station/
├── index/                          # アプリ本体
│   ├── weathernews_GUI.py          # GUIアプリ（メイン）
│   ├── weathernews_CUI.py          # CUI版（コマンドライン）
│   ├── weather_config.py           # 表示・フォント設定
│   ├── weather_model.tflite        # 画像認識用TFLiteモデル
│   ├── weather_data_save.csv  # 天気記録データ
├── .gitignore
└── README.md
```

---

## 機能一覧

### 記録

* **手動記録** ：ボタンまたはキー入力で晴れ・曇り・雨・雪を記録
* **画像認識記録** ：空の写真をアップロードすると TFLite モデル（MobileNetV2ベース）が天気を自動判定してCSVに書き込む

### 確認

* 天気の集計（晴れ・曇り・雨・雪の日数）をバーグラフで表示
* 日付×天気の推移を折れ線グラフで表示
* CSVの内容をテーブルで表示

### 予報

* **2次マルコフ連鎖**を使い、直前2日間の天気から遷移確率行列を計算
* 翌日の最有力天気を表示、さらに2〜5日後の各天気の発生確率も出力
* 開発者モード：遷移行列の内部（最大値・最小値・平均・中央値・分散・標準偏差）を確認可能

### その他

* **削除** ：最新の記録を1件削除
* **リセット** ：全記録を削除
* **ファイル検索** ：Python・CSV・TFLite・設定ファイルのパスを自動検索・表示

---

## 動作環境・インストール

**Python 3.10 以上を推奨**

```bash
pip install customtkinter tensorflow pandas numpy matplotlib tqdm psutil
```

or

```bash
pip install -r requirements.txt
```

| パッケージ    | 用途                                         |
| ------------- | -------------------------------------------- |
| customtkinter | GUIフレームワーク（ライト/ダークモード対応） |
| tensorflow    | TFLite推論（画像認識）                       |
| pandas        | CSVの読み書き・データ集計                    |
| numpy         | 遷移行列の計算                               |
| matplotlib    | グラフ表示                                   |
| tqdm          | 起動時プログレスバー                         |
| psutil        | CPU使用率モニタリング                        |

---

## 使い方

### GUIアプリ（推奨）

```bash
cd index
python weathernews_GUI.py
```

起動すると自動的にホームディレクトリから必要ファイルを検索します。

| メニュー                | 操作                                            |
| ----------------------- | ----------------------------------------------- |
| 操作 > 記録             | 天気ボタン（晴れ/曇り/雨/雪）で今日の天気を記録 |
| 操作 > 記録（画像認識） | 空の写真を選択してAIが天気を判定・記録          |
| 操作 > 確認             | 統計グラフとデータ一覧を表示                    |
| 操作 > 予報             | マルコフ連鎖で5日先まで予報                     |
| 操作 > 削除             | 最新レコードを1件削除                           |
| 設定                    | ライトモード / ダークモード / システムに従う    |
| ヘルプ > 使い方         | アプリの使い方を表示                            |
| ファイル > リセット     | 全データ削除                                    |

### CUIアプリ

```bash
cd index
python weathernews_CUI.py
```

```
1: 記録　2: 確認　3: 予報　4: 終了　5: リセット　6: ファイル検索
```

---

## データフォーマット

`index/weather_data_save.csv`

```csv
Date,Weather
2025-01-01 12:00:00,snow
2025-01-02 12:00:00,rain
...
```

| カラム  | 型       | 値                                  |
| ------- | -------- | ----------------------------------- |
| Date    | datetime | 記録日時                            |
| Weather | str      | `sun`/`cloud`/`rain`/`snow` |

---

## 設定

`index/weather_config.py` を編集することで外観をカスタマイズできます。

```python
DEBUG_MODE = True or False          # 開発者モードの有効・無効化
VER_INFO = "1.0 BETA"

DISPLAY_SIZE = "425x425"   # ウィンドウ初期サイズ
FONT_FAMILY = "Meiryo"     # フォントファミリー
FONT_SIZE_MAIN = 24        # 本文フォントサイズ
FONT_SIZE_BTN = 20         # ボタンフォントサイズ
FONT_SIZE_TITLE = 28       # タイトルフォントサイズ
FONT_COLOR = ("black", "white")  # (ライトモード, ダークモード)
FG_COLOR = ("lightgray", "gray") # ボタン背景色
```

---

## 予報アルゴリズム

1. CSVから読み込んだ天気データを前処理し、**直前2日間の天気（State）** を作成
2. `pd.crosstab` で State → 翌日天気の遷移確率表を生成
3. 16×16の遷移行列 `p_1` を構築し、行列積で `p_2`〜`p_5`（2〜5日後）を計算
4. 最新2日間の天気から対応する行を参照し、最大確率の天気を予報として出力

---

