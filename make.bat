@echo off
title MAKE
set args=0
for %%x in (%*) do set /A args+=1
if %args%==0 goto eof
if %args%==1 if "%1"=="check" goto check
if %args%==1 if "%1"=="clean" (
    echo cleaning
    for %%f in ("*.pyc" "*.pyo" "*.log" "*.db") do (
            echo "%%~f%"
	    del "%%~f"
    ))
goto eof
:check
echo checking syntax
flake8 checker.py
:eof
echo done
