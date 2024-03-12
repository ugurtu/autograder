# !/usr/bin/python
import argparse, sys, shutil, os, zipfile

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

## Contents
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import getpass


COURSEPAGE = "https://adam.unibas.ch/goto_adam_crs_1688235.html" # TODO: specify ADAM coursesite
COURSE = "'Intro to Data Science'" # TODO: specify course name
SUBMISSION_TYPE = "Exam insurance" # TODO: specify exact submission type link name, e.g. "Exercises" or "Exam insurance"
HANDIN_PREFIX = "Insurance " # TODO: specify exact hand-in name link prefix (name of the hand-in without iterator, e.g. "Exercise sheet " or "Insurance ", be mindful of the extra space at the end)

# This is more flexible than doing a final username!
uname = getpass.getuser()

DOWNLOAD_PATH = f"/home/{uname}/Downloads/" # TODO: adjust downloadpath of selenium firefox browser
DOWNLOAD_PATH = f"/home/{uname}/Downloads/" # TODO: adjust downloadpath of selenium firefox browser


def main(argv):

    # parse command line arguments
    try:
        USERNAME, PWD, MODE, NR, URL = parse_args()
        print(f"Username: {USERNAME}, Password: HIDDEN, Mode: {MODE}, Number: {NR}, Course URL: {URL}")
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        sys.exit(1)

    
    SUBMISSION_NAME = HANDIN_PREFIX + str(NR) 

    target_id = URL.replace("https://adam.unibas.ch/goto_adam_", "").replace(".html", "")

    print("Starting auto-download from browser...")
    # automate ADAM access
    driver = webdriver.Firefox()

    # login procedure
    success = login(driver, USERNAME, PWD, target_id)
    if not success:
        driver.close()
        print("Login was not successful...")
        return
    success = wait_for(driver, "il_mhead_t_focus")
    if not success:
        return False
    
    # click exercises link on the ADAM course page
    exercise_link = driver.find_element(By.LINK_TEXT, SUBMISSION_TYPE)
    exercise_link.click()

    success = wait_for(driver, "il_mhead_t_focus")
    if not success:
        return False

    # "Abgaben und Noten" Button
    exercise_link = driver.find_element(By.LINK_TEXT, "Abgaben und Noten")
    exercise_link.click()

    # select Exercise sheet in dropdown menu based on <nr> argument
    if NR > 1:
        select_element = driver.find_element(By.ID, "ass_id")
        select_object = Select(select_element)
        select_object.select_by_visible_text(SUBMISSION_NAME)
        button = driver.find_element(By.NAME, "cmd[selectAssignment]")
        button.click()

        success = wait_for(driver, "il_mhead_t_focus")
        if not success:
            return False

    # set rows to 200 for a list of all submissions


    # iterate over all submissions
    
     
    
    
    
    
    
    
    # # dowload all submissions of chosen exercise
    # button = driver.find_element(By.NAME, "cmd[downloadSubmissions]")
    # button.click()
    # success = wait_for(driver, "il_mhead_t_focus")
    # if not success:
    #     return False
    
    # # "Background tasks" bell
    # # bell_icon = driver.find_element(By.CSS_SELECTOR, ".glyphicon.glyphicon-bell")
    # bell_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".glyphicon.glyphicon-bell")))
    # bell_icon.click()

    # # "Background tasks" button
    # link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Background Tasks")))
    # link.click()

    # # "Exercise sheet <nr>" download button
    # elem = f"//button[contains(text(), '{SUBMISSION_NAME}')]"
    # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, elem)))
    # button.click()

    # # move downloaded ZIP file into current directory
    # source_path = DOWNLOAD_PATH + SUBMISSION_NAME + '.zip'
    # destination_directory = os.getcwd()  # Get the current working directory
    # destination_path = os.path.join(destination_directory, SUBMISSION_NAME + '.zip')
    # shutil.move(source_path, destination_path)
    
    # # unpack zip in current directory and delete zip
    # # Specify the name of the ZIP file
    # zip_file_name = SUBMISSION_NAME + '.zip'

    # # ensure the ZIP file exists, open and extract
    # if os.path.exists(zip_file_name):
    #     with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
    #         zip_ref.extractall('.')
    #         print(f"Extracted all contents of '{zip_file_name}' to the current directory.")
        
    #     # remove the ZIP file after extraction
    #     os.remove(zip_file_name)
    #     print(f"Deleted the ZIP file: '{zip_file_name}'")
    # else:
    #     print(f"The file '{zip_file_name}' does not exist.")

    # print(f"\n==========================================================================")
    # print(f"'{SUBMISSION_NAME}' from the course {COURSE} and hand-in type '{SUBMISSION_TYPE}' \nhas been downloaded into the current directory.")
    # print(f"==========================================================================\n")

    # # close browser
    # driver.close()

    

########################################################################################################################
    
########################################################################################################################

# parse command line arguments; -h or --help for info
def parse_args():
    parser = argparse.ArgumentParser(description='Parse command line arguments.')

    parser.add_argument('-u', '--username', type=str, required=True, help='Username')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password')
    parser.add_argument('-n', '--nr', type=int, required=True, help='Number')
    parser.add_argument('-m', '--mode', type=str, required=False, default='default_mode', help='Mode (optional)')
    parser.add_argument('-c', '--coursesite', type=str, required=False, default=COURSEPAGE, help='Course URL (optional)')

    args = parser.parse_args()

    return args.username, args.password, args.mode, args.nr, args.coursesite


# login to ADAM via switch edu-id
def login(driver: webdriver, user, pwd, target_id):
    login_target = "https://adam.unibas.ch/shib_login.php?target="
    driver.get(login_target + target_id)
    success = wait_for(driver, "userIdPSelection_iddicon")
    if not success:
        return False
    unibas_selector = driver.find_element("xpath", "//*[@id='userIdPSelection_iddicon']")
    unibas_selector.click()
    unibas = driver.find_element("xpath", "//div[@title='Universities: Universität Basel']")
    unibas.click()
    actualTitle = driver.title
    if not actualTitle.startswith('SWITCH edu-ID Login'):
        return False
    success = wait_for(driver, "username")
    if not success:
        return False
    driver.find_element("name", "j_username").send_keys(user)
    driver.find_element("xpath", '//*[@id="login-button"]').click()
    success = wait_for(driver, "username")
    if not success:
        return False
    driver.find_element("name", "j_password").send_keys(pwd)
    driver.find_element("xpath", '//*[@id="login-button"]').click()

    # return wait_for(driver, "userlog")
    return True


def wait_for(driver, elem_id):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, elem_id)))
        return True
    except TimeoutException:
        return False


if __name__ == '__main__':
    main(sys.argv[1:])