# Digitize
A short program used for bulk digitization of files

For my final project in CS50, I tackled a real-world problem I have been dealing with. This fall, I began the process of digitizing a few thousand files for a local church in my community. I am tasked with creating a file organization system, deciding on naming conventions, and digitizing the backlog of files which are necessary to keep for business purposes from the 80s and 90s up until 2023. I quickly tired of manually naming, sorting, and creating folders for files while I worked. I had been planning to use code to simplify and potentially automate the process and thought I could kill two birds with one stone and make my program for the final project of my CS50 course.

digitize.py is a simple program which allows the user to navigate to a folder on their computer and cycle through PDF files, renaming them according to conventions I created for the church's files. The final product of a successful session results in however many files sorted into folders by year, named according to the convention "{2-digit month}-{contractor/vendor name}-{document type}.pdf". 

For Example: "2016/01-CVS-Receipt.pdf". 

If the digitizer's current folder has documents of more than one category in it (for example: if a folder has both meeting minutes and invoices from a painting company) there is a y/n prompt which adds another level of organization to the folder creation process. The result creates files along these lines:

"Minutes/2016/08-Leadership-Team-Minutes.pdf"


The program relies on the os module and the move function from shutil in Python. The user is initially prompted for the directory they want to operate on. The program checks whether that directory exists and then changes to it, or else prints usage instructions. At this point, the function confirm() is called to give the user the opportunity to make sure they picked the right file. After the confirmation is accepted, the processing begins in full by looping through the files in the folder and running the various functions involved in document processing.

Here is a step-by-step runthrough of a typical use of this system:

    Current Working Directory Path:     # User copy pastes path of working directory, or is otherwise given instructions on how to do that
    Multiple categories of files? y/n   # User may stipulate whether multiple categories exist in their present directory
    [Contents of working directory printed to console]
    Process File? y/n                   # User is prompted on whether to begin processing the documents

    # Console is cleared, and the first file is opened in default document viewer for system
    [List of existing files]    # List of files remaining & folders created always displayed above prompts
    Category:       # User types category of file; this prompt does not appear if user answered in the negative above
    Year:           # User types year of file creation (if 4-digit year not used, reprompted with instructions)
    Month:          # User types month of file creation (if 2-digit month formulation not used, reprompted with instructions)
    Contractor:     # User types contractor who resulted in creation of document for file organization purposes, will be autoconverted to title case
    Document Type:  # User types type of document, whether Invoice or Contract, etc. Alternatively, User may type "add" to add a document type to the system for the duration of this folder's processing, though it will not remain in the list after the folder is fully processed
    
    # The above prompts are cleared and repeated in sequence until no documents remain. User may skip any document at any time by typing "skip", leaving the document untouched for the user to do with it as they will
    [List of existing files]
    Digitization Complete.  # Prints this message when all files have been processed or skipped

    # Final result leaves user with list of folders corresponding to categories and/or years with files neatly renamed and sorted inside
    
Major Functions:

The **first** and most complex function for file processing is metadata(), so named because the naming convention requires a decent amount of data from within the document in order to be effective. The user is prompted for each of these datapoints in succession, with checks to ensure the data matches with convention (i.e. years are four-digit numbers, months match a list of two-digit numbers from 1-12, and the right capitalization methods are followed with regard to the contractor name and document type). The fourth piece of data, the document type, is taken from a list, as follows below this paragrah.

Accepted Document Types: Auth, Certificate, Communication, Contract, Data, Insurance, Invoice, Notes, Notification, Order, Policy, Proposal, Receipt, Warranty

This list can be updated, and contains all of the types of files I have encountered in my digitization efforts up until this point. metadata() returns its data, which is then assigned to corresponding variables for year, month, contractor, and document type.

_Future development of this project would allow the PDF (which is naturally searchable) to be searched by the function to suggest possible document types, but parsing the required libraries to navigate an Adobe-standard searchable PDF and implementing in the program would both increase the relative size of the program and appeared outside the scope of this assignment to me._


The **second** function for file processing is rename(), which takes file, month, contractor, and doctype as inputs. It then implements the naming convention and reassigns the f variable (which has been representing the file) to the new name of the file to be passed into the final function, move().


The **final** function is short and two the point. It takes the file and the year, creates a folder for the year if one doesn't exist already, and moves the file to the year. It also runs a check to see if the folder already contains a document of the same title and concatenates an integer from 2-10 prior to the .pdf extension of the file name.
