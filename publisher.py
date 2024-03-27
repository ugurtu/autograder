# !/usr/bin/python
import argparse, sys, shutil, os, zipfile

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

## Contents
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import getpass
import pickle


COURSEPAGE = "https://adam.unibas.ch/goto_adam_crs_1688235.html" # TODO: specify ADAM coursesite
COURSE = "'Intro to Data Science'" # TODO: specify course name
SUBMISSION_TYPE = "Exam insurance" # TODO: specify exact submission type link name, e.g. "Exercises" or "Exam insurance"
HANDIN_PREFIX = "Insurance " # TODO: specify exact hand-in name link prefix (name of the hand-in without iterator, e.g. "Exercise sheet " or "Insurance ", be mindful of the extra space at the end)

TOTAL_POINTS = 1 # TODO: Total points of insurance exam or exercise

# This is more flexible than doing a final username!
uname = getpass.getuser()

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

    print("Starting auto-publish from browser...")
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
        print("1")
        success = wait_for(driver, "il_mhead_t_focus")
        print("2")
        # select_element = driver.find_element(By.ID, "ass_id")
        print("3")

        # select_object = Select(select_element)
        # select_object.select_by_visible_text(SUBMISSION_NAME)
        # button = driver.find_element(By.NAME, "cmd[selectAssignment]")
        # button.click()

        success = wait_for(driver, "il_mhead_t_focus")
        if not success:
            return False

    # set rows to 200 for a list of all submissions
    # Wait for the dropdown trigger button to be clickable and click it to open the dropdown menu
    dropdown_trigger = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ilAdvSelListAnchorText_sellst_rows_exc_mem"))
    )
    dropdown_trigger.click()

    # Now wait for the specific dropdown menu item ("200") to be clickable and click it
    menu_item_200 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "sellst_rows_exc_mem_200"))
    )
    menu_item_200.click()

    # iterate over all submissions
    emails = ['marcel.luethi@unibas.ch', 'e.kitzing@stud.unibas.ch', 'fabio.poletti@unibas.ch']
    points = [1, 0.667]
    feedbacks = ['All tests passed!', 'Question 1 results: All test cases passed!\nQuestion 2 results: All test cases passed!\nQuestion 3 results:\n    Question 3 - 1 result:\n        ❌ Test case failed\n        Error at line 11 in test Question 3:\n              q3 = env["Question3"]\n        KeyError: Question3']
    

    # Load the dictionary from the file
    with open('student_points.pkl', 'rb') as file:
        student_points = pickle.load(file)

    print("Retrieved dictionary:", student_points)

    # Use the dictionary as needed
    # Example: Print all keys and values
    for email, score in student_points.items():
        print(f"{email}: {score}")

    # Delete the temporary file
    # os.remove('student_points.pkl')
    # print("Temporary file deleted.")


    for student_mail in student_points:
        try:
            # Find the row with the matching email address
            email_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{student_mail}')]/.."))
            )
            # Select the "Bewertung" dropdown if condition A is true
            if student_points[student_mail]/TOTAL_POINTS >= 0.5:
                print(f"passed: {student_mail}" )
                select_element = Select(email_element.find_element(By.XPATH, ".//td/select[contains(@name, 'status')]"))
                select_element.select_by_value("passed")  # Set to "Bestanden"
            elif student_points[student_mail]/TOTAL_POINTS <= 0.33:
                print(f"failed: {student_mail}" )
                select_element = Select(email_element.find_element(By.XPATH, ".//td/select[contains(@name, 'status')]"))
                select_element.select_by_value("failed")  # Set to "Nicht Bestanden"

            

            # actions = ActionChains(driver)
            # actions.send_keys(Keys.PAGE_DOWN).perform()

            # Select the "Rückmeldung per Text" option from the "Aktionen" dropdown
            # actions_dropdown = email_element.find_element(By.XPATH, ".//td//div[@class='dropdown']//button")
            # actions_dropdown.click()
            
            

            # print("before")

            # feedback_option = email_element.find_element(By.XPATH, '//*[@id="il_ui_fw_65f13fd81a05c3_81537710"]')

            
            # After attempting to scroll, wait for the feedback option to be clickable.
            # feedback_option = WebDriverWait(driver, 10).until(
                # EC.element_to_be_clickable((By.XPATH, ".//button[contains(text(), 'Rückmeldung per Text')]"))
            # )
            # feedback_option.click()



            # print("before2")
            # # Wait for the feedback option to be clickable
            # feedback_option = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, ".//button[contains(text(), 'Rückmeldung per Datei')]"))
            # )
            # print("after")
            

            # Now click the feedback option
            # feedback_option.click()
            # print("test1")     
           
            # Now wait for the specific dropdown menu item "Rückmeldung per Text" to be clickable and click it
            # Since the menu item is identifiable by its text, we use an XPath expression that targets the button by its text.
            # menu_item_text = "Rückmeldung per Text"
            # menu_item_xpath = f"//button[contains(text(), '{menu_item_text}')]"
            # menu_item = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, menu_item_xpath))
            # )
            # menu_item.click()
            # print("test2")

            # clear text field and fill out grade report
            # text_field = driver.find_element_by_xpath('//*[@id="lcomment_9867_1867698"]')
            # text_field = driver.find_element(By.CLASS_NAME, "form-control")

            # text_field.sendKeys(Keys.TAB)
            
            # text_field.clear()
            # text_field.click()
            # text_field.send_keys("Some Sample Text Here")


            # Clear the text field
            # text_field.clear()

            # Split the input string by new lines and send each line, followed by pressing ENTER (except the last line)
            # lines = feedbacks[i].split('\n')
            # for line in lines[:-1]:
            #     text_field.send_keys(line)
            #     text_field.send_keys(Keys.ENTER)
            # text_field.send_keys(lines[-1])

            # # submit form
            # submit_button = driver.find_element_by_css_selector('input.btn.btn-default.btn-sm[type="submit"]')
            # submit_button.click()


        except Exception as e:
            print(f"Error processing {student_mail}: {e}") 
     
    
    
    
    
    
    
    # # dowload all submissions of chosen exercise_number
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