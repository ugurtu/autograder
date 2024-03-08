# !/usr/bin/python
import argparse, sys, shutil, os, zipfile

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select


coursepage = "https://adam.unibas.ch/goto_adam_crs_1688235.html" # TODO: specify ADAM coursesite
download_path = "/home/josph/Downloads/" # TODO: adjust downloadpath of selenium firefox browser


def main(argv):

    # parse command line arguments
    try:
        username, pwd, mode, nr, url = parse_args()
        print(f"Username: {username}, Password: {pwd}, Mode: {mode}, Number: {nr}, Course URL: {url}")
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        sys.exit(1)

    url = coursepage
    target_id = url.replace("https://adam.unibas.ch/goto_adam_", "").replace(".html", "")

    # automate ADAM access
    driver = webdriver.Firefox()

    success = login(driver, username, pwd, target_id)
    if not success:
        driver.close()
        print("Login was not successful...")
        return
    
    success = wait_for(driver, "il_mhead_t_focus")
    if not success:
        return False
    # click exercises link
    exercise_link = driver.find_element(By.LINK_TEXT, "Exercises")
    exercise_link.click()

    success = wait_for(driver, "il_mhead_t_focus")
    if not success:
        return False

    exercise_link = driver.find_element(By.LINK_TEXT, "Abgaben und Noten")
    exercise_link.click()

    if nr > 1:
        # Find the select element by its name or ID
        select_element = driver.find_element(By.ID, "ass_id")
        # Create a Select object
        select_object = Select(select_element)
        # Select the option by visible text
        select_object.select_by_visible_text("Exercise sheet " + str(nr))
        # Find the button by its name attribute and click on it
        button = driver.find_element(By.NAME, "cmd[selectAssignment]")
        button.click()

        success = wait_for(driver, "il_mhead_t_focus")
        if not success:
            return False
    
    button = driver.find_element(By.NAME, "cmd[downloadSubmissions]")
    button.click()
    success = wait_for(driver, "il_mhead_t_focus")
    if not success:
        return False
    
    # Background tasks bell
    bell_icon = driver.find_element(By.CSS_SELECTOR, ".glyphicon.glyphicon-bell")
    bell_icon.click()

    # "Background tasks" button
    link = driver.find_element(By.LINK_TEXT, "Background Tasks")
    link.click()

    # "Exercise sheet <nr>" download button
    elem = "//button[contains(text(), 'Exercise sheet " + str(nr) + "')]"
    button = driver.find_element(By.XPATH, elem)
    button.click()

    # move downloaded zip file into current directory
    source_path = download_path + 'Exercise sheet ' + str(nr) + '.zip'
    destination_directory = os.getcwd()  # Get the current working directory
    destination_path = os.path.join(destination_directory, 'Exercise sheet ' + str(nr) + '.zip')
    shutil.move(source_path, destination_path)
    
    # unpack zip in current directory and delete zip
    # Specify the name of the ZIP file
    zip_file_name = 'Exercise sheet ' + str(nr) + '.zip'
    print(f"Extracted all contents of {zip_file_name} to the current directory.")

    # Ensure the ZIP file exists
    if os.path.exists(zip_file_name):
        # Open the ZIP file in read mode
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            # Extract all the contents into the current directory
            zip_ref.extractall('.')
            print(f"Extracted all contents of {zip_file_name} to the current directory.")
        
        # Remove the ZIP file after extraction
        os.remove(zip_file_name)
        print(f"Deleted the ZIP file: {zip_file_name}.")
    else:
        print(f"The file {zip_file_name} does not exist.")


    # close browser
    driver.close()

    

########################################################################################################################
    
########################################################################################################################

# parse command line arguments; -h or --help for info
def parse_args():
    parser = argparse.ArgumentParser(description='Parse command line arguments.')

    parser.add_argument('-u', '--username', type=str, required=True, help='Username')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password')
    parser.add_argument('-n', '--nr', type=int, required=True, help='Number')
    parser.add_argument('-m', '--mode', type=str, required=False, default='default_mode', help='Mode (optional)')
    parser.add_argument('-c', '--coursesite', type=str, required=False, default=coursepage, help='Course URL (optional)')

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
