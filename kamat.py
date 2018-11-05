from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as sel_ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options 

import string_handler
import my_trello, my_todoist
import settings
import codecs

CONTAINER_CLASS = 'event-list-item'

LOGIN_URL = "https://moodle2.cs.huji.ac.il/nu" + str(settings.year) + "/login/index.php"
TASKS_URL = "https://moodle2.cs.huji.ac.il/nu" + str(settings.year) + "/my/"
READ = "r"
FIREFOX_BROWSER_PATH = r'geckodriver\geckodriver.exe'
CHROME_BROWSER_PATH = r'chromedriver\chromedriver.exe'



def run():
    print("------------- STARTED RUNNIN -----------------")
    print("Opening 'downloaded' - list of already uploaded tasks...")
    global downloaded_file, downloaded
    downloaded_file = codecs.open('downloaded', 'r', encoding='utf-8')
    downloaded = downloaded_file.read()
    downloaded_file.close()
    downloaded_file = codecs.open('downloaded', 'a', encoding='utf-8')

    tasks = get_tasks()
    print("Connecting to todoist/trello...")
    todolist = None
    if settings.todolist == 'todoist':
        todolist = my_todoist.Todoist(settings.list_name)
    elif settings.todolist == 'trello':
        todolist = my_trello.Trello(settings.list_name, settings.trello_board_id)
    print("Sending tasks to todoist/trello:")
    todolist.send_tasks(tasks)

    downloaded_file.close()
    print("----------------- DONE ---------------------")


def get_tasks():
    print("Getting tasks from Moodle:")
    soup = get_soup()
    containers = soup.find_all('li', {'class': CONTAINER_CLASS})
    err_task = None
    tasks = []
    print("Going through tasks:")
    for container in containers:
        task_dict = dict()

        # ***** add all elements *****
        task_dict['name'] = get_tag(container, 'a', {'class': 'event-name'})
        task_dict['course_num'] = get_tag(container, 'small', {}).split()[0]
        task_dict['course'] = get_tag(container, 'small', {}).split()[1]
        task_dict['date_txt'] = get_tag(container, 'div', {'class': 'span5'}, '\n')
        try:
            task_dict['date'] = string_handler.heb_to_date(task_dict['date_txt'])
        except NameError:
            task_dict['date'] = None

            err_task = dict()
            err_task['name'] = 'Error in KAMAT with parsing month ' + task_dict['date_txt']
            err_task['course_num'] = 0
            err_task['course'] = 'send to Ofri'
            err_task['date'] = None

        task_dict['id'] = (task_dict['name'] + task_dict['course_num'])
        # if not exist in the file:
        if task_dict['id'] in downloaded:
            print("\tTask already uploaded: "+task_dict['name'])
        else:
            tasks.append(task_dict)
            downloaded_file.write(task_dict['id'] + '\n')
    if err_task is not None:
        tasks.append(err_task)
    return tasks


def get_tag(parent, tag, opt, start='>', end='</'):
    tag = parent.find(tag, opt)
    tag_str = str(tag).split(start)[1]
    tag_str = tag_str.split(end)[0]
    tag_str = tag_str.decode('utf-8', 'ignore')
    return tag_str


def get_soup():
    # TODO: use chrome
    print('\tOpenning chrome...')
    # driver = webdriver.Firefox(executable_path=FIREFOX_BROWSER_PATH)
    chrome_options = Options()  
    chrome_options.add_argument('log-level=3')  
    driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH, chrome_options=chrome_options)
    #driver.options.add_argument('log-level=3')
    print('\tConnecting to Moodle...')
    driver.get(LOGIN_URL)
    print('\tInserting username and password...')

    # ***** login *****
    username_input = driver.find_element_by_id("username")
    password_input = driver.find_element_by_id("password")

    '''
    login_file = open(INIT_FILE, READ)
    file_str = login_file.readlines()
    login_file.close()
    user = init.bat.get_data(file_str[1])
    password = init.bat.get_data(file_str[2])
    '''
    username_input.send_keys(settings.moodle_username)
    password_input.send_keys(settings.moodle_password)
    driver.find_element_by_id("loginbtn").click()

    # ***** get tasks *****
    print('\tOpenning tasks list in Moodle...')
    driver.get(TASKS_URL)
    try:
        WebDriverWait(driver, 20).until(sel_ec.presence_of_element_located((By.CLASS_NAME, 'event-name')))
        # TODO: check if it renders all links or just the first one
        print("\tGot HTML or tasks list!")
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
    except TimeoutException:
        print("ERROR: Loading (of tasks list in Moodle) took too much time!")

    driver.close()
    return soup  # TODO: handle exception


def test():
    t = my_trello.Trello()
    pass


run()
# TODO - prerealese: check if script is working on someone else computer
# TODO: Noa - auto run
# TODO - beta: check if task already exist
# TODO - optional: print status (how many tasks downloaded etc.)
# TODO - beta: download files
# TODO - beta: better description to cards

# test()
