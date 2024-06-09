@echo off
:: 获得管理员权限
Net session >nul 2>&1 || mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0","","runas",1)(window.close)&&exit
:: 进入conda环境
CALL conda activate facefusion
cd E:/soft/se/facefusion/facefusion/
E:
echo "python run.py"
python run.py
pause