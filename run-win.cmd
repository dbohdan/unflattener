@echo off
rem set OUTPUTFN=res-%RANDOM%%RANDOM%
set OUTPUTFN=result.png
set TESTDIR=test-images
set PYTHON=c:\python27\python.exe
echo on
%PYTHON% unflatten.py --top %TESTDIR%\zombie-top.png --bottom %TESTDIR%\zombie-bottom.png --left %TESTDIR%\zombie-left.png --right %TESTDIR%\zombie-right.png -o %OUTPUTFN% -d 0.5
pause