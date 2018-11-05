python -m pip install todoist-python
python -m pip install py-trello
python -m pip install selenium
python -m pip install BeautifulSoup
python -m pip install bs4

schtasks /Create ^
/SC DAILY ^
/TR %cd%\run.bat ^
/ST 03:50:00 ^
/ED 02/20/2020 ^
/TN kamat

PAUSE