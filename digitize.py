import os
from shutil import move
from subprocess import Popen, CalledProcessError


# Optional capability to sort files by area of focus if multiple are present in one set of files
extra_layer = False

# Initialize list of accepted types from accompanying .txt file
with open('doctypes.txt') as file:
    accepted_types = file.readlines()

for i in range(0, len(accepted_types)):
    accepted_types[i] = accepted_types[i].strip()

# Any new types desired for next time
new_types = []

# Global Variables:
directories = []
remaining_files = 0
years = list(map(str, range(1950, 2051)))
months = list(map(lambda x: str(x).zfill(2), range(1, 13)))

# Implements UX and runs all primary functions
def main():
    print('Welcome to Digitize. Please locate the file you wish to process and drag it into this Terminal window to begin.')
    while True:
        dir = input('Current Working Directory Path: ').strip()
        if confirm(dir):
            break
        else:
            print('Usage: Drag & Drop file into the window of the Terminal app on Mac, resulting in a series of slash-separated values. You may need to increase the width of your Terminal window to fit the whole file path.')
            continue
    
    # Provides access to global variable "extra layer" within this function depending on outcome of prompt
    global extra_layer
    if (input('Multiple categories of files? y/n ')) in ['y', 'yes']:
        extra_layer = True
    else:
        extra_layer = False

    # Creates a list of existing directories in the current working directory
    global directories
    items = os.listdir('.')
    directories = [item for item in items if os.path.isdir(item)]
    global remaining_files
    remaining_files = len(items) - len(directories)

    for f in os.listdir('.'):
        filename, extension = os.path.splitext(f)
        if extension == '.pdf':
            category, year, month, contractor, doctype = metadata(f)
            if year == 'skip':
                remaining_files -= 1
                continue
            f = rename(f, month, contractor, doctype)
            move_file(f, year, category)
            remaining_files -= 1

    os.system('clear')
    print(os.listdir('.'))
    chain = input('Digitizaiton Complete. Would you like to digitize another file? y/n ').lower().strip()
    if chain in ['y', 'yes']:
        os.system('clear')
        main()

    with open('doctypes.txt', 'a') as file:
        for type in new_types:
            file.write(type + '\n')

    os.system('clear')
    print(os.listdir('.'))
    print('Digitization Complete.')
    
    return


# Function to open directory and confirm desired folder has been opened
def confirm(dir):
    if os.path.exists(dir):
            os.chdir(dir)
            print(os.listdir('.'))
            test = input('Process File? y/n ')
            if test.lower() in ['y', 'yes']:
                return True
            
    return False


# Function to prompt user for and return relevant data for titling
def metadata(file):
    os.system('clear')
    print(directories)
    print('Files Remaining: ' + str(remaining_files))
    # Open PDF file for viewing in its default application (i.e. Preview on Mac)
    try:
        Popen(['open', file])
    except CalledProcessError:
        print('An error occurred attempting to open file.')
    # User will be responsible for closing file after use

    # Prompt for category, if needed
    if extra_layer == True:
        while True:
            category = input('Category: ').strip()
            if category == '':
                test = input('Leave blank? y/n ')
                if test.lower() in ['y', 'yes']:
                    break
                else:
                    continue
            elif category.lower() == 'skip':
                return 'skip', 'skip', 'skip', 'skip', 'skip'
            break
            
        category = category.replace(' ', '-')

    else:
        category = ''

    # Prompt for year of document creation
    while True:
        year = input('Year: ').strip()
        # In all inputs, the following will test if lack of input means information will not be provided
        if year == '':
            test = input("Leave blank? y/n ")
            if test.lower() in ['y', 'yes']:
                break
            else:
                continue
        elif year.lower().strip() == 'skip':
            return 'skip', 'skip', 'skip', 'skip', 'skip'

        if year in years:
            break
        else:
            print('Usage: Please input a 4-digit year')

    # Prompt for month of document creation
    while True:
        month = input('Month: ').strip()
        if month == '':
            test = input("Leave blank? y/n ")
            if test.lower() in ['y', 'yes']:
                break
            else:
                continue
        elif month.lower() == 'skip':
            return 'skip', 'skip', 'skip', 'skip', 'skip'

        if month in months:
            break
        else:
            print('Usage: Please enter a valid 2-digit month')

    # Prompt for relevant contractor name
    while True:
        contractor = input('Contractor: ').strip()
        if contractor == '':
            test = input("Leave blank? y/n ")
            if test.lower() in ['y', 'yes']:
                break
            else:
                continue
        elif contractor.lower() == 'skip':
            return 'skip', 'skip', 'skip', 'skip', 'skip'
        
        contractor = contractor.replace(' ', '-')

        break
        
    # Prompt for type of document
    while True:
        doctype = input('Document Type: ').strip().title()
        if doctype == '':
            test = input("Leave blank? y/n ")
            if test.lower() in ['y', 'yes']:
                break
            else:
                print('Accepted Document Types: ' + ', '.join(accepted_types))
                continue
        elif doctype.lower() == 'skip':
            return 'skip', 'skip', 'skip', 'skip', 'skip'
        elif doctype.lower() == 'add':
            doctype = input('New Type: ').strip().title()
            accepted_types.append(doctype)
            new_types.append(doctype)

        doctype = doctype.replace(' ', '-')

        if doctype in accepted_types:
            break
        else:
            print('Accepted Document Types: ' + ', '.join(accepted_types) + "\nIf you would like to add a new type to this list, type 'add'.")
            continue

    return category, year, month, contractor, doctype
    

# Function to take user through files one by one and rename each
def rename(file, month, contractor, doctype):
    new_name = '.pdf'
    data_true = 0
    if doctype:
        new_name = doctype + new_name
        data_true += 1
        if contractor:
            new_name = contractor + '-' + new_name
            data_true += 1
            if month:
                new_name = month + '-' + new_name
        elif month:
            new_name = month + '-' + new_name
    elif contractor:
        new_name = contractor + new_name
        data_true += 1
        if month:
            new_name = month + '-' + new_name

    # Ensure there is enough identifying information, otherwise insert placeholder
    if data_true == 0:
        new_name = 'Miscellaneous' + new_name

    os.rename(file, new_name)
    return new_name


# Function to move newly renamed file (file) to new or existing directory (folder) by year or category if applicable
def move_file(file, year, category):
    # Case: Category is primary sorting method and year is secondary sorting method in non-homogeneous folder
    if bool(category):
        folder = os.path.join(category, year)
        if os.path.exists(folder):
            file = avoid_replacement(file, folder)
            move(file, folder)
        elif os.path.exists(category):
            os.mkdir(folder)
            move(file, folder)
        else:
            os.makedirs(folder)
            directories.append(category)
            move(file, folder)
    
    # Case: Year is primary sorting method as all documents are in homogeneous categories
    elif bool(year):
        if os.path.exists(year):
            file = avoid_replacement(file, year)
            move(file, year)
        else:
            os.mkdir(year)
            directories.append(year)
            move(file, year)

    return


# Helper function for move()
def avoid_replacement(file, path):
    i = 2
    while True:
        if os.path.exists(os.path.join(path, file)):
            filename, extension = os.path.splitext(file)
            new_name = filename + str(i) + extension
            if os.path.exists(os.path.join(path, new_name)):
                i += 1
                continue
            else:
                os.rename(file, new_name)
                file = new_name
                break
        else:
            break

    return file


main()