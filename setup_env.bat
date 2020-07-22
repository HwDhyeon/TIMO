@ECHO OFF

IF NOT DEFINED PYTHONPATH (
    SETX PYTHONPATH %cd%/timo -m
)

IF NOT DEFINED TIMO_HOME (
    SETX TIMO_HOME %PYTHONPATH% -m
    SETX PATH %TIMO_HOME%;%PATH% -m
)

IF NOT EXIST %cd%/data (
    MKDIR %cd%/data
)

IF NOT EXIST %cd%/data/conf.json (
    COPY %TIMO_HOME%/data/conf_template.json %cd%/data/conf.json
)

PAUSE
