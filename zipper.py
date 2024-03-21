import re
import zipfile
import os
import shutil
import pickle

TYPE = "Exercise"
NR = "3"

student_points = {}

# Extracts exactly one zip file, the one that contains the folder structure for ADAM multi-feedback
def find_and_unzip(zip_folder_path, extract_path):
    # List all files in the given directory
    files = os.listdir(zip_folder_path)
    
    # Filter the list to find the ZIP file
    zip_files = [f for f in files if f.endswith('.zip')]
    
    if len(zip_files) == 1:
        zip_file_name = zip_files[0]  # Store the name of the zip file
        zip_path = os.path.join(zip_folder_path, zip_file_name)
        
        # Unzip the found ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"Extracted {zip_path} to {extract_path}")
        
        # Return the name of the zip file for further use
        return zip_file_name
    elif len(zip_files) > 1:
        print("Error: More than one ZIP file found.")
        return None
    else:
        print("Error: No ZIP files found.")
        return None
    
# def zip_folder(folder_path, output_path):
#     with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         len_dir_path = len(folder_path)
#         for root, _, files in os.walk(folder_path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 zipf.write(file_path, file_path[len_dir_path:])
    
def zip_folder(folder_path, output_path):
    # Get the absolute path of the folder
    abs_folder_path = os.path.abspath(folder_path)
    # Extract the folder name to include in the zip
    folder_name = os.path.basename(abs_folder_path)
    # Calculate parent directory to construct correct paths within the zip
    parent_dir = os.path.dirname(abs_folder_path)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(abs_folder_path):
            # Construct the correct path for files in the zip
            for file in files:
                file_path = os.path.join(root, file)
                # Construct the archive path, including the folder name
                archive_path = os.path.relpath(file_path, parent_dir)
                zipf.write(file_path, archive_path)
                
    print(f"Folder '{folder_name}' has been zipped as '{output_path}'")

    
def extract_insurance_points(filename):
    # open feedback file and take 2nd to last line
    with open(filename, 'r') as file:
        lines = file.readlines()

    # second_to_last_line = lines[-2] # insurance
    second_to_last_line = lines[31:-2] # exercise

    # pattern looks for any sequence of digits (\d+) possibly followed by a decimal point
    # and more digits. ? makes the decimal point and the following digits optional to
    # allow for whole numbers as well.
    # match = re.search(r"(\d+\.\d+)", second_to_last_line) # insurance
    match = re.search(r"(\d+(?:\.\d+)?)", second_to_last_line) # exercise
    if match:
        return float(match.group(1))
    else:
        return 0

def match_and_copy_files(path1, path2):
    # Iterate over all folders in PATH1
    for folder_name in os.listdir(path1):
        folder_path = os.path.join(path1, folder_name)
        # Ensure it's a directory and not a file
        if os.path.isdir(folder_path):
            # Extract mail address from the folder name
            try:
                print(folder_name)
                _, _, mail_address, _ = folder_name.split('_')
            except ValueError:
                print(f"Folder {folder_name} does not match the expected naming convention.")
                continue
            
            # Construct the expected text file name based on the mail address
            expected_text_file_name = f"{mail_address}_feedback.txt"
            expected_text_file_path = os.path.join(path2, expected_text_file_name)
            
            # Check if the text file exists in PATH2
            if os.path.isfile(expected_text_file_path):
                points = extract_insurance_points(expected_text_file_path)
                student_points[mail_address] = points

                # Copy the text file into the corresponding folder in PATH1
                # destination_path = os.path.join(folder_path, expected_text_file_name)
                destination_path = os.path.join(folder_path, f"{TYPE}-{NR}-feedback-{points}pts.txt")
                # destination_path = os.path.join(folder_path, "feedback.txt")
                shutil.copyfile(expected_text_file_path, destination_path)
                print(f"Copied {expected_text_file_name} to {folder_path}")
            else:
                print(f"No matching file found for {mail_address}")



zip_folder_path = '../autograder'
extract_path = '../autograder'
zip_file_name = find_and_unzip(zip_folder_path, extract_path)

if zip_file_name:
    print(f"The extracted ZIP file's name is: {zip_file_name}")

unzipped_folder_structure_path = f'../autograder/{zip_file_name[:-4]}'  # Replace PATH1 with the actual path
feedback_folder_path = f'../autograder/analysis/{TYPE}_Analysis_{NR}/Feedback_{TYPE} 2'  # Replace PATH2 with the actual path
match_and_copy_files(unzipped_folder_structure_path, feedback_folder_path)

# folder_path = 'path/to/your/folder'
# output_path = 'your_archive.zip'
zip_folder(unzipped_folder_structure_path, f"{unzipped_folder_structure_path}2.zip")


# Serialize and save the dictionary to a file
with open('student_points.pkl', 'wb') as file:
    pickle.dump(student_points, file)

print("Dictionary with student points has been saved.")
