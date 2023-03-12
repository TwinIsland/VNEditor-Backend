@echo off
set /p "commit_msg=Commit Message: "
echo run linter script, please wait...
timeout 1  > nul
black ./
echo generating linter report
>linter_result.txt (
  echo Generated In: %date% %time%
  echo:
  echo check ./engine
  pylint ./engine
  echo check ./module
  pylint ./module
  echo check ./utils
  pylint ./utils
)
echo linter result been pushed into 'linter_result.txt'
echo start committing
timeout 1  > nul
git add ./
git commit -m %commit_msg%
git push
echo OK!
pause