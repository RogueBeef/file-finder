import os
import tkinter as tk
from tkinter import scrolledtext, Toplevel, Label, Button
from io import open


def on_button_click():
    '''Main grab, search, check & report gen '''
    #grab:
    files_entered = entry1.get("1.0",tk.END)
    search_dir = entry2.get()
    report_dir = entry3.get()
    #print(search_dir)
    #print(report_dir)

    files_to_find = files_entered.splitlines()
    #print(files_to_find)

    #search:
    try:
        file_names = search_folder(search_dir) # files in the search directory without extension
        files_found = check_files(files_to_find, file_names)
        create_report(report_dir, files_to_find, file_names, files_found)
    except FileNotFoundError:
        popup = Toplevel(root)
        popup.title("Error")
        label = Label(popup, text="\nError - Check directory location\n")
        label.pack()
        # Add a close button to the pop-up window
        close_button = Button(popup, text="Close", command=popup.destroy)
        close_button.pack()
        popup.mainloop()



def search_folder(search_dir):
    files_list = os.listdir(search_dir)
    # Create a new list to store the names without the file extensions
    files_no_ext = [os.path.splitext(file)[0] for file in files_list]
    #print(f'End of search folder func, output is: {files_no_ext}')
    return files_no_ext

def check_files(files_to_find, file_names):
    files_found = [] # list to be populated with tuples (file, found) - file is the name, found is a boolean, true is in folder, false if not.
    #print(f'files to find var: {files_to_find}')
    #print(f'file names var: {file_names}')
    #print(range(len(files_to_find)))
    for i in range(len(files_to_find)):
        if files_to_find[i] in file_names:
            exists = True
        else:
            exists = False
        temp_toup = (files_to_find[i], exists)
        files_found.append (temp_toup)
    #print('End of check files func')
    return files_found

def other_files(file_match_list, file_names):
    '''Take files in folder, delete files found'''
    others = file_names.copy()
    #print(f'others = {others}')
    for i in others:
        #print(i)
        #print(file_match_list)
        if i in file_match_list:
            #print('i ({i}) in files_found, removing')
            others.remove(i)
    return others

def create_report(report_dir, files_to_find, file_names, files_found):
    #print()
    #text_file = str(report_dir + '\\report.txt')
    text_file = os.path.join(report_dir, 'report.txt')
    #print(text_file)
    file_match_list = []
    with open(text_file, "w", encoding='utf-8') as file:
        file.write(f'Looking for {len(files_to_find)} files in folder containing {len(file_names)} files: \n')
        file.write('\n')
        file.write('Files found: \n')
        for i in files_found:
            if i[1] == True:
                file_match_list.append(i[0])
                #print(i[0])
                file.write(i[0]+ '\n')
        
        file.write('\n')
        file.write('Files NOT found: \n')
        for i in files_found:
            if i[1] == False:
                #print(i[0])
                file.write(i[0]+ '\n')

        file.write('\n')
        file.write('Other files in folder not matching: \n')
        others = other_files(file_match_list, file_names)
        for i in others:
            file.write(i + '\n')

        file.write('\n')
        file.write('End of report. \n')


root = tk.Tk()
root.title("File-finder - Version 0.1.0")
root.geometry("400x350")

text0 = tk.Label(root, text="")
text0.pack()
text1 = tk.Label(root, text="Find these files:")
text1.pack()
entry1 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=20, height=10)
entry1.pack()

text2 = tk.Label(root, text="In this folder:")
text2.pack()
entry2 = tk.Entry(root, width = 50)
entry2.pack()

text3 = tk.Label(root, text="And save the report here:")
text3.pack()
entry3 = tk.Entry(root, width = 50)
entry3.pack()

button = tk.Button(root, text="Submit", command=on_button_click)
button.pack()

text4 = tk.Label(root, text="")
text4.pack()

text5 = tk.Label(root, text="Send bugs to James Proctor")
text5.pack()

root.mainloop()
