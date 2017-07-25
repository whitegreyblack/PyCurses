@echo off
title MAKE
set args=0
for %%x in (%*) do set /A args+=1

rem start of argument parsing and matching
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
    if exist "src/debug.log" del "src/debug.log"
    if exist "src/food.db" del "src/food.db"
    if exist "src/__pycache__/" del /Q "src/__pycache__"
    if exist "src/__pycache__/" rmdir "src/__pycache__"
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

rem Start of goto branching and argument cases
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
if "%2"=="parser" (
	:parse
	echo linting checker
	flake8 checker.py
	if "%~2"=="" goto db
	goto eof)
if "%2"=="db" (
	:db
	echo linting populate
	flake8 populate.py
	if "%~2"=="" goto gui
	goto eof)
if "%2"=="gui" (
	:gui
	echo linting gui
	flake8 revert.py
	if "%~2"=="" goto pop
	goto eof)
goto eof
:checkall
echo linting all files
goto parse
:badarg
echo incorrect args
echo USAGE: make [check]
echo             [clean]
echo             [reciept] [real/test] [filename]
echo        make [test]
:eof
echo done
