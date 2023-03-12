## YuiEngine

![icon](res/ok.webp)

start server by running `start_server.bat`, you can find API document on the engine website

code format by [black](https://github.com/psf/black), linter by [pylint](https://pypi.org/project/pylint/), run `linter_script.bat` to check code format every time before pull request; the most current linter report can be found in [linter_result.txt](./linter_result.txt)

unit test included in `./test` folder, power by [unittest framework](https://docs.python.org/3/library/unittest.html)

**dependence:**

+ fastapi
+ uvicorn
+ python-multipart
