# Phantom Maze: Write-up

Таск представляет собой лабиринт из последовательно идущих страниц с некоторыми усложнениями. 
Одно из усложнений — ссылки на следующие страницы подгружаются через JavaScript. 
Таким образом, стандартными средствами таск не решается.

Для загрузки JS из кода существует несколько средств, мы воспользуемся модулем [Selenium](https://github.com/SeleniumHQ/selenium/tree/master/py) 
для Python, а также драйвером [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads).  
Примем во внимание, что флаг находится не в конце лабиринта, а где-то на одной из страниц, и напишем
скрипт:
```
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

current_url = 'https://maze.ctf.upml.tech/maze/2648lGMiwyGujegVjzeHYV2Opa2OfYEX'

while 1:
    driver.get(current_url)
    time.sleep(1)
    if 'uctf' in driver.page_source:
        print(driver.page_source)
        break
    current_url = driver.find_element_by_xpath('html/body/p/a').get_attribute('href')
``` 

Существует также второе решение, короче и проще, так как сам флаг не загружается через JS. Исследуем скрипт и
видим, что для получения ссылки на следующую страницу он делает запрос на `/next`. Воспользуемся этим и
напишем скрипт, который сделает работу немного быстрее:
```
import requests

url = 'https://maze.ctf.upml.tech/maze/'
current_id = '2648lGMiwyGujegVjzeHYV2Opa2OfYEX'

while 1:
    current_id = requests.post('https://maze.ctf.upml.tech/next', data={ 'id': current_id }).text
    r = requests.get(url + current_id)
    if 'uctf' in r.text:
        print(r.text)
        break
```
На одной из страниц находим флаг.

Флаг: **uctf_h1dd3n_1n_th3_m4z3**