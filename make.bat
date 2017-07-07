@echo off
title MAKE
set args=0
for %%x in (%*) do set /A args+=1
if %args%==0 goto badarg
if %args%==1 if "%1"=="check" goto checkall
if %args%==2 if "%1"=="check" goto check
if %args%==1 if "%1"=="clean" (
    echo cleaning
    for %%f in ("*.pyc" "*.pyo" "*.log" "*.db") do (
            echo "%%~f%"
	    del "%%~f"
    ))
    echo done cleaning
    if exist "__pycache__/" del /Q "__pycache__"
    if exist "__pycache__/" rmdir "__pycache__"

    goto :eof
if %args%==3 if "%1"=="reciept" if "%2"=="test" (
    set "folder=testfolder/"
    goto recieptsetup
)
if %args%==3 if "%1"=="reciept" if "%2"=="real" (
    set "folder=reciepts/"
    goto recieptsetup
)
goto eof
:recieptsetup
set "file=%folder%%~3%.yaml"
echo --- Creating Yaml File: %file% ---
echo --- !Reciept > %file%
echo store: >> %file%
echo date: >> %file%
echo type: >> %file%
echo prod: >> %file%
echo   { >> %file%
echo   } >> %file%
echo sub: >> %file%
echo tax: >> %file%
echo tot: >> %file%
goto eof
:check
if "%2"=="parser" flake8 checker.py
goto eof
if "%2"=="db" flake8 populate.py
goto eof
:checkall
echo checking syntax
flake8 checker.py
flake8 populate.py
goto eof
:badarg
echo incorrect args
echo USAGE: make [check]
echo             [clean]
echo             [reciept] [real/test] [filename]
echo        make [test]
:eof
echo done
