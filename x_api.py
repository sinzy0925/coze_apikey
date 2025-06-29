import requests
import json,time

raw_url = "https://raw.githubusercontent.com/sinzy0925/coze_apikey/main/README1.md"


def main(query: str, count: str, types: str, user: str) -> dict:
    
    # --- ★★★ キャッシュバスティングの処理 ★★★ ---
    # URLの末尾に、現在のUNIXタイムスタンプをダミーパラメータとして付与
    cache_buster = int(time.time())
    url_with_buster = f"{raw_url}?v={cache_buster}"
    # --- ★★★ ここまで ★★★ ---
    try:
        response = requests.get(url_with_buster, timeout=20)
        response.raise_for_status() # 404などのエラーをチェック
        app_id       = response.text.split('\r\n')[0]
        workflow_id  = response.text.split('\r\n')[1]
        access_token = response.text.split('\r\n')[2]
        print(f"app_id: {app_id}")
        print(f"workflow_id: {workflow_id}")
        print(f"access_token: {access_token}")
    except Exception as e:
        # どの行でどんなエラーが起きたか分かるように、より詳細なエラー情報を返す
        import traceback
        return {"result": {"error": f"An unexpected error occurred: {e}", "traceback": traceback.format_exc()}}




    url = "https://api.coze.com/v1/workflow/run"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": app_id,
        "workflow_id": workflow_id,
        "parameters": {
            "user": user,
            "query": query,
            "count": count,
            "type_latest_top": types
        }
    }


    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result_from_api = response.json()
        
        if result_from_api.get('code') != 0:
            return {"result": result_from_api}
            
        if isinstance(result_from_api.get('data'), str):
            try:
                result_from_api['data'] = json.loads(result_from_api['data'])
            except json.JSONDecodeError:
                pass
        
        # --- ここからがデータ整形処理 ---
        
        simplified_tweets = []
        # .get()を繋げて、深い階層のデータも安全に取得
        posts = result_from_api.get('data', {}).get('output', {}).get('freeBusy', {}).get('post', [])

        # APIから返ってきた各ツイート(post)をループで処理
        for post in posts:
            # postが辞書でない、または空の場合はスキップ
            if not isinstance(post, dict) or not post:
                continue

            # userオブジェクトを安全に取得
            user_info = post.get('user')
            
            # 必要な情報だけを抜き出したシンプルな辞書を作成
            tweet_data = {
                "text": post.get('full_text', ''),
                # user_infoがNoneでないことを確認してから、中の情報を取得
                "author_name": user_info.get('name', 'N/A') if user_info else 'N/A',
                "author_id": user_info.get('screen_name', 'N/A') if user_info else 'N/A',
                "followers_count": user_info.get('followers_count', 0) if user_info else 0,
                "created_at": post.get('created_at', ''),
                "favorite_count": post.get('favorite_count', 0),
                "retweet_count": post.get('retweet_count', 0),
                "image_url": None,
                "video_url": None
            }
            
            # mediaリストが存在し、かつ空でないことを確認
            media_list = post.get('media', [])
            if media_list and len(media_list) > 0:
                # media_listの最初の要素が辞書であることを確認
                first_media = media_list[0]
                if isinstance(first_media, dict):
                    if first_media.get('type') == 'photo':
                        tweet_data['image_url'] = first_media.get('media_url_https')
                    elif first_media.get('type') == 'video':
                        tweet_data['video_url'] = first_media.get('expanded_url')

            simplified_tweets.append(tweet_data)


        # 整形した、浅い階層のリスト、元の詳細データのリストを出力
        return {"result": {"result":simplified_tweets,"raw_result":posts}}

    except requests.exceptions.RequestException as e:
        return {"result": {"error": f"API request failed: {e}"}}
    except Exception as e:
        # どの行でどんなエラーが起きたか分かるように、より詳細なエラー情報を返す
        import traceback
        return {"result": {"error": f"An unexpected error occurred: {e}", "traceback": traceback.format_exc()}}


if __name__ == "__main__":
    apikey={
    "app_id": "7519396627493306376",
    "workflow_id": "7519743309867352071"
    }
    apikey=json.dumps(apikey)
    query="ai"
    count="1"
    types="Top"
    user=""
    res = main(query, count, types, user)
    print(res)