@echo off
if "%~1"=="" (
    echo [Loi] Vui long truyen duong dan file lua!
    echo Vi du: run_draw.bat scripts\chest.lua
    exit /b 1
)

:: Thay doi duong dan neu ban cai Aseprite o noi khac
set ASEPRITE="C:\Duongdandenfile\aseprite\aseprite.exe"

:: Dam bao cac thu muc output ton tai
if not exist "output\aseprite" mkdir "output\aseprite"
if not exist "output\gif" mkdir "output\gif"
if not exist "output\Sheet" mkdir "output\Sheet"

echo Dang ve bang Aseprite CLI...
%ASEPRITE% -b --script "%~1"
echo [Xong!] Kiem tra ket qua tai thu muc output\