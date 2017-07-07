title TEMPLATE

if "%~1"=="" (
	echo Incorrect Args
	goto eof)
set "folder=testfolder/"
set "file=%folder%%~1.yaml"
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
:eof
echo Done
