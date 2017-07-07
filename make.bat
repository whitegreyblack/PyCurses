@echo off
title MAKE
set args=0
for %%x in (%*) do set /A args+=1
if %args%==0 goto badarg
if %args%==1 if "%1"=="check" goto check
if %args%==1 if "%1"=="clean" (
    echo cleaning
    for %%f in ("*.pyc" "*.pyo" "*.log" "*.db") do (
            echo "%%~f%"
	    del "%%~f"
    ))
goto eof
if %args%==3 if "%1"=="test" (
    set "folder=testfolder"
    goto recieptsetup
)
if %args%==3 if "%1"=="real" (
    set "folder=reciepts"
    goto recieptsetup
)
:recieptsetup
set "file=%folder%%~1%.yaml"
echo %file%
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
echo checking syntax
flake8 checker.py
:badarg
echo incorrect args
echo USAGE: make [check]
echo             [clean]
echo             [reciept] [real/test] [filename]
echo        make [test]
:eof
echo done
