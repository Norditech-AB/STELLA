@echo off
setlocal enabledelayedexpansion

:: Define the file that contains the list of files and folders to remove
set "CLEAR_FILES=.clear_files"

:: Check if the .clear_files exists
if not exist "%CLEAR_FILES%" (
    echo The file %CLEAR_FILES% does not exist.
    exit /b 1
)

:: Read the .clear_files and remove each entry
for /f "usebackq tokens=*" %%A in ("%CLEAR_FILES%") do (
    set "line=%%A"
    if not "!line!"=="" (
        if exist "!line!\\" (
            rmdir /s /q "!line!"
        ) else (
            del /q "!line!"
        )
        if !errorlevel! equ 0 (
            echo Removed !line!
        ) else (
            echo Failed to remove !line!
        )
    )
)

echo Cleanup completed.
endlocal