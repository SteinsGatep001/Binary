@echo off
setlocal
:PROMPT
SET /P AREYOUSURE=Are you sure? This driver modifies kernel and may trigger patchguard protection ! you may just use IDA ! (Y/[N])
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END
sc delete debug
sc create debug type=kernel binpath=%CD%\pgdemo.sys
sc start debug
echo You should see the flag in DbgPrint after 10 seconds
pause
:END
endlocal