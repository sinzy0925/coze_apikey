@echo off
rem --- ���̃o�b�`�t�@�C���� x_api_dify.py ��100����s���܂� ---

echo 100��̃��[�v�������J�n���܂�...

for /L %%i in (1, 1, 100) do (
    echo.
    echo ---------------------------------
    echo %%i ��ڂ̎��s���J�n���܂�...
    echo ---------------------------------
    
    python x_api_dify.py
    
    echo %%i ��ڂ̎��s���������܂����B
)

echo.
echo �S�Ă̏������������܂����B
pause