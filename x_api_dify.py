import requests
import json

def run_dify_workflow():
    """
    Difyのワークフローをブロッキングモードで実行し、結果を出力する関数
    """
    # curlコマンドの各要素をPythonの変数に置き換える
    api_url = "https://api.dify.ai/v1/workflows/run"
    
    # ヘッダー情報
    headers = {
        "Authorization": "Bearer app-Ne5lNNpRvmHjE46TYapSO1wh",
        "Content-Type": "application/json"
    }
    
    # 送信するデータ（リクエストボディ）
    # --data-raw の中身をPythonの辞書として表現
    payload = {
        "inputs": {
            "query": "ai",
            "count": "1",
            "type": "Top",
            "user": ""
        },
        "response_mode": "blocking",
        "user": "Dify_Mizuho"
    }

    print("Difyワークフローを実行します...")

    try:
        # requests.post() を使ってAPIにリクエストを送信
        # json=payload とすることで、自動的に辞書がJSON文字列に変換され、
        # ヘッダーのContent-Typeも適切に処理される
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)

        # ステータスコードをチェックし、エラーがあれば例外を発生させる
        # (例: 401 Unauthorized, 404 Not Found, 500 Internal Server Error など)
        response.raise_for_status()

        print("APIからのレスポンスを正常に受信しました。")
        
        # レスポンスのJSONデータをPythonの辞書に変換
        result_data = response.json()
        
        # 辞書データを、インデント付きで見やすく、日本語が文字化けしない形式のJSON文字列に変換して出力
        # ensure_ascii=False が日本語を正しく表示するためのキーポイント
        formatted_json_string = json.dumps(result_data, indent=2, ensure_ascii=False)
        
        print("\n--- 実行結果 ---")
        print(formatted_json_string)

    except requests.exceptions.RequestException as e:
        # ネットワークエラーやHTTPエラーなど、リクエストに関するエラー
        print(f"\nエラー: APIへのリクエストに失敗しました。")
        print(f"詳細: {e}")
        # エラーレスポンスの内容も表示してみる
        if 'response' in locals() and response.text:
            print(f"サーバーからの応答: {response.text}")
    except json.JSONDecodeError:
        # レスポンスがJSON形式でなかった場合のエラー
        print("\nエラー: APIからのレスポンスをJSONとして解析できませんでした。")
        print(f"受信した生データ: {response.text}")
    except Exception as e:
        # その他の予期せぬエラー
        print(f"\n予期せぬエラーが発生しました: {e}")

# このスクリプトが直接実行された場合に、上記の関数を呼び出す
if __name__ == "__main__":
    run_dify_workflow()