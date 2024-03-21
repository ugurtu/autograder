import os

def replace_chars_in_files(folder_path):
    # Iterate over all files in the given folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip directories, only process files
        if os.path.isfile(file_path):
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Only proceed if there's at least one line in the file
            if lines:
                # Work on the last line
                last_line = lines[-1]
                
                # Ensure the line has at least 43 characters
                if len(last_line) >= 43:
                    # Replace characters at positions 41 and 42 (0-based index)
                    modified_last_line = last_line[:41] + "32" + last_line[43:]
                    # Update the last line
                    lines[-1] = modified_last_line
                    
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(lines)

# Specify the path to the folder containing the text files
folder_path = 'Feedback_Exercise 3'
replace_chars_in_files(folder_path)
