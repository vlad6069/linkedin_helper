import tkinter
import tkinter.ttk
import webbrowser
import datetime
import pathlib
import json
import functools
from sys import platform

#This list will be appended with profiles and allow navigating among them
tablist = []

def write(content):
    with open(log_file_path(),'w') as file:
        #Store profile data in JSON format.
        json.dump(content, file)

def read():
    try:
        with open(log_file_path(),'r') as file: 
            file_content = file.read()
            #Load saved profiles from JSON format into Python data structures
            content = json.loads(file_content)
            return(content)
    except:
        # Missing file or first use
        print("file not found")

def log_file_path():
    # Select an OS-appropriate application data directory
    if platform == "linux":
        file_directory = pathlib.Path.home() / '.local/share/linkedin_helper/'
    elif platform == "darwin":
        file_directory = pathlib.Path.home() / 'Library/Application Support/vlad6069/linkedin_helper/'
    elif platform == "win32":
        file_directory = pathlib.Path.home() / 'AppData/Roaming/linkedin_helper'
    else:
        file_directory = pathlib.Path.home() / 'linkedin_helper'
    file_path = file_directory / f'user_input.json'
    if (file_directory.is_dir() == False):
        file_directory.mkdir()
        print('log_file_path() - directory created')
    return file_path

def exit_script():
    raise SystemExit()

def process_user_input(user_input):
    content = read()
    if content is None:
        content = []
    content.append(user_input)
    write(content)
    #Return index of the newly added profile
    return len(content)-1
        

def timestamp(led):
    # Handle new profile creation
    if (led == None):
        # 604800 seconds correspond to 7 days, it's entirely arbitrary.
        return'604800'
    else:
        raw_delta = datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.strptime(led, "%Y-%m-%d %H:%M:%S.%f%z")
        return round(raw_delta.total_seconds())

def search():
    content = read()
    for counter, profile in enumerate(content):
        if 'to_delete' not in profile:
            # Profile has never been executed before
            if 'last_execution_time' not in content[counter]:
                content[counter]['last_execution_time'] = None
            if (profile['posting_date'] == ''):
                time = timestamp(profile['last_execution_time'])
            else:
                time = profile['posting_date']
            keywords = ''
            for character in profile['keywords']:
                if (character == ' '):
                    keywords += '%20'
                else:
                    keywords += character
            # See README for details concerning search parameters
            url = f'https://www.linkedin.com/jobs/search/?keywords={profile['keywords']}&geoId={profile['geoId']}&distance={profile['distance']}&f_TPR=r{time}&sortBy={profile['sorting_filter']}'
            webbrowser.open_new_tab(url)
            content[counter]['last_execution_time'] = str(datetime.datetime.now(datetime.timezone.utc))
    write(content)

def create_tab(tab_manager, tablist, mode, content = None): 

    search_parameters = {'posting_date' : '', 'keywords' : '', 'geoId' : '', 'distance' : '', 'sorting_filter' : ''}
    helper = {'posting_date' : 'Maximum age of offers in seconds; empty = since last execution', 'geoId' : 'Location identifier used to filter offers (see README)', 'distance' : 'Expand search area by X km', 'sorting_filter' : 'Sort by date (DD) or relevance (R)'}
    tab_details ={'root' : tkinter.ttk.Frame(tab_manager), 'search_parameters' : search_parameters}
    tablist.append(tab_details)
    
    def generate_profile_content(tab, mode, content = None, new_profile_index = None):
        tab_manager.add(tablist[tab]['root'], text= tab)
        for counter, parameter in enumerate(tab_details['search_parameters']):
            if(parameter != 'last_execution_time'):
                parameter_content = {}
                parameter_content['name'] = parameter
                parameter_content['label'] = tkinter.ttk.Label(tablist[tab]['root'], text= parameter)
                parameter_content['label'].grid(column=0, row=counter)
                if (mode == 'edit'):
                    parameter_content['user_input'] = tkinter.StringVar()
                    parameter_content['Input'] = tkinter.ttk.Entry(tablist[tab]['root'], textvariable= parameter_content['user_input'])
                    parameter_content['Input'].grid(column=1, row=counter)
                    if parameter in helper:
                        parameter_content['helper'] = tkinter.ttk.Label(tablist[tab]['root'], text = helper[parameter])
                        parameter_content['helper'].grid(column=2, row=counter)
                    if content is None:
                        None
                    else:
                        parameter_content['Input'].insert(0, content[parameter])
                if (mode == 'save'):
                    parameter_content['Input'] = tkinter.ttk.Label(tablist[tab]['root'], text = content[parameter])
                    parameter_content['Input'].grid(column=1, row=counter)
                tab_details['search_parameters'][parameter] = parameter_content
        manual_widget = {} 
        if (mode == 'edit'):
            if content is None:
                manual_widget['save_button'] = tkinter.ttk.Button(tablist[tab]['root'], text='Save', command = functools.partial(save, tab, 'save'))
                manual_widget['save_button'].grid(column=1, row=len(tab_details['search_parameters']))
            else:
                manual_widget['update_button'] = tkinter.ttk.Button(tablist[tab]['root'], text='Update', command = functools.partial(update, tab, 'save', new_profile_index))
                manual_widget['update_button'].grid(column=1, row=len(tab_details['search_parameters']))
        if (mode == 'save'):
            manual_widget['Edit_button'] = tkinter.ttk.Button(tablist[tab]['root'], text='Edit', command = functools.partial(edit, tab, 'edit', content, new_profile_index))
            manual_widget['Edit_button'].grid(column=1, row=len(tab_details['search_parameters']))
        # For tabs with stored data
        if (new_profile_index is not None) or (content is not None):
            manual_widget['Delete_button'] = tkinter.ttk.Button(tablist[tab]['root'], text='Delete', command = functools.partial(delete, tab, new_profile_index))
            manual_widget['Delete_button'].grid(column=2, row=len(tab_details['search_parameters']))              
        tab_details['manual_widget'] = manual_widget 
    
    def delete(tab, new_profile_index = None):
        file_content = read()
        # Handle index differently for new vs loaded profiles
        if (new_profile_index != None):
            file_content[new_profile_index]['to_delete'] = None
        else:
            file_content[tab-1]['to_delete'] = None
        write(file_content)
        tab_manager.tab(tab, state="disabled")
    
    def save(tab, mode):
        user_input = {}
        for parameter in tablist[tab]['search_parameters']:
            user_input[parameter] = tablist[tab]['search_parameters'][parameter]['user_input'].get()
        new_profile_index = process_user_input(user_input)
        for parameter in tablist[tab]['search_parameters']:
            # Remove UI widgets before rebuilding the tab content
            tablist[tab]['search_parameters'][parameter]['Input'].destroy()
            if 'helper' in tablist[tab]['search_parameters'][parameter]:
                tablist[tab]['search_parameters'][parameter]['helper'].destroy()
        generate_profile_content(tab, mode, user_input, new_profile_index)

    def update(tab, mode, new_profile_index = None):
        user_input = {}
        file_content = read()
        for parameter in tablist[tab]['search_parameters']:
                user_input[parameter] = tablist[tab]['search_parameters'][parameter]['user_input'].get()
                if 'helper' in tablist[tab]['search_parameters'][parameter]:
                    tablist[tab]['search_parameters'][parameter]['helper'].destroy()
        if (new_profile_index != None):
            relevant_counter = new_profile_index
        else:
            relevant_counter = tab - 1
        if 'last_execution_time' in file_content[relevant_counter]:
            user_input['last_execution_time'] = file_content[relevant_counter]['last_execution_time']
        file_content[relevant_counter] = user_input
        write(file_content)
        for parameter in tablist[tab]['search_parameters']:
            tablist[tab]['search_parameters'][parameter]['Input'].destroy()
        generate_profile_content(tab, mode, user_input, new_profile_index)
    
    def edit(tab, mode, content, new_profile_index = None):
        for parameter in tablist[tab]['search_parameters']:
            tablist[tab]['search_parameters'][parameter]['Input'].destroy()
        generate_profile_content(tab, mode, content, new_profile_index)
    
    # Static Main Menu tab (not part of dynamic profile tabs)
    if (len(tablist) == 1):
        tab_manager.add(tablist[len(tablist)-1]['root'], text= f'Main Menu')
    else:
        generate_profile_content(len(tablist)-1, mode, content)
    tab_manager.pack(expand = 1, fill ="both")
     
main_window_root = tkinter.Tk()
tab_manager = tkinter.ttk.Notebook(main_window_root)

create_tab(tab_manager, tablist, '')
cleared_content = []
try:
    for profile in read():
        # Remove profiles marked for deletion while preserving active ones
        if 'to_delete' not in profile:
            cleared_content.append(profile)
    write(cleared_content)
    for profile in read():
        if 'to_delete' not in profile:
            create_tab(tab_manager, tablist, 'save', profile)
except:
    print('First execution : no existing data file.')
        
new_profile = tkinter.ttk.Button(tablist[0]['root'], text= 'New profile', command = lambda: create_tab(tab_manager, tablist, 'edit'))
new_profile.grid(column= 0, row= 0)
search_button = tkinter.ttk.Button(tablist[0]['root'], text="Open tab(s)", command = search)
search_button.grid(column=0, row=1)
exit_button = tkinter.ttk.Button(tablist[0]['root'], text="Exit", command = exit_script)
exit_button.grid(column=0, row=2)
main_window_root.mainloop()
                                                                        