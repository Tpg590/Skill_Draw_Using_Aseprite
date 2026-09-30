@echo off
if "%~1"=="" (
    echo [Loi] Vui long truyen duong dan file lua!
    echo Vi du: run_draw.bat scripts\chest.lua
    exit /b 1
)

:: ============================================================================
:: DUONG DAN UNG DUNG (ASEPRITE / LIBRESPRITE)
:: Neu cai dat o thu muc khac hoac dung LibreSprite, vui long sua duong dan duoi day.
:: Xem huong dan chi tiet tai file: Instruction.md
:: ============================================================================
set ASEPRITE="C:\Program Files\Aseprite\aseprite.exe"

:: Kiem tra su ton tai cua file executable, neu khong thay thi tim trong PATH
if not exist %ASEPRITE% (
    where aseprite >nul 2>nul
    if %errorlevel% equ 0 (
        set ASEPRITE=aseprite
    ) else (
        where libresprite >nul 2>nul
        if %errorlevel% equ 0 (
            set ASEPRITE=libresprite
        ) else (
            echo [CANH BAO] Khong tim thay Aseprite tai: %ASEPRITE%
            echo Vui long mo file run_draw.bat de sua duong dan hoac xem huong dan tai Instruction.md!
            exit /b 1
        )
    )
)

:: Dam bao cac thu muc output ton tai
if not exist "output\aseprite" mkdir "output\aseprite"
if not exist "output\gif" mkdir "output\gif"
if not exist "output\Sheet" mkdir "output\Sheet"

echo Dang ve bang Aseprite CLI (%ASEPRITE%)...
%ASEPRITE% -b --script "%~1"
echo [Xong!] Kiem tra ket qua tai thu muc output\