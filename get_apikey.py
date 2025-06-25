import requests
import re

def main() -> dict:
    """
    指定されたGitHubのRaw URLからファイルの内容を取得し、
    正規表現を使って '# apikey=...' のパターンからキーの値を抽出します。
    """
    
    # 取得対象は、ファイルの純粋なテキストが置かれている「Raw」URL
    raw_url = "https://raw.githubusercontent.com/sinzy0925/coze_apikey/main/README.md"
    
    # 正規表現パターン: '# apikey=' の後の文字列をキャプチャする
    pattern = re.compile(r"^\s*#\s*apikey\s*=\s*(.+)", re.MULTILINE)

    print(f"GitHub Raw URLからデータを取得します: {raw_url}")

    try:
        # 1. requests.get() でファイルの内容をテキストとして取得
        response = requests.get(raw_url, timeout=10)
        response.raise_for_status() # 404などのエラーをチェック
        
        # 2. ファイルの全内容を文字列として取得
        file_content = response.text

        print(file_content)
        # 3. 正規表現でパターンを検索
        match = pattern.search(file_content)
        
        if match:
            # パターンに一致した場合
            extracted_key = match.group(1).strip()
            
            print(f"成功！APIキーを抽出しました: {extracted_key}")
            
            # Difyの出力変数に合わせて結果を返す
            return {
                "status": "found",
                "api_key": extracted_key
            }
        else:
            # パターンが見つからなかった場合
            print("失敗。ファイル内に'# apikey=...'のパターンは見つかりませんでした。")
            return {
                "status": "not_found",
                "api_key": None
            }

    except requests.exceptions.RequestException as e:
        print(f"エラー: GitHubからファイルを取得できませんでした。詳細: {e}")
        return {
            "status": "request_error",
            "api_key": None,
            "error_message": str(e)
        }
    except Exception as e:
        import traceback
        print(f"予期せぬエラーが発生しました: {e}")
        return {
            "status": "unexpected_error",
            "api_key": None,
            "error_message": traceback.format_exc()
        }
main()