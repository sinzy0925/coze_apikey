@echo off
rem --- このバッチファイルは x_api_dify.py を100回実行します ---

echo 100回のループ処理を開始します...

for /L %%i in (1, 1, 100) do (
    echo.
    echo ---------------------------------
    echo %%i 回目の実行を開始します...
    echo ---------------------------------
    
    python x_api_dify.py
    
    echo %%i 回目の実行が完了しました。
)

echo.
echo 全ての処理が完了しました。
pause