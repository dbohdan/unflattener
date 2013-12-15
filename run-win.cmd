@echo off
rem set OUTPUTFN=res-%RANDOM%%RANDOM%
set TESTDIR=test-images
set PYTHON=c:\python27\python.exe
set IMAGE=robot
set OUTPUTFN=result-%IMAGE%.png
echo on
%PYTHON% unflatten.py --top %TESTDIR%\%IMAGE%-top.png --bottom %TESTDIR%\%IMAGE%-bottom.png --left %TESTDIR%\%IMAGE%-left.png --right %TESTDIR%\%IMAGE%-right.png -o %OUTPUTFN% -d 0.5
@pause
