# LinkedIn_helper
#### Video Demo: 

https://youtu.be/KFHqTmRORk4

#### Description:

This program helps users filter job listings on the LinkedIn job board to only show offers posted since their last visit. It supports multiple saved search profiles, each defining a different set of search parameters.

## Installation:

### Requirements:

Developed and tested with Python 3.13. Earlier Python 3 versions are untested.

The default web browser must already be logged into LinkedIn before using the program.

### Repository setup:

```
git clone https://github.com/vlad6069/linkedin_helper.git
```

### Data storage:

On first launch, the program creates a JSON storage file in the appropriate OS-specific user data location.

### Execution:

```
cd <project_folder> 
python linkedin_helper.py
```

## Usage:

### Create/Edit a profile:

Once the program is executed, a UI appears containing 3 buttons labelled "New profile" "Open tab(s)" and "Exit".
For the first use or any time you wish to create a new profile, click on the New profile button and select the numbered tab that opened at the top right of the UI to edit its parameters.

#### Search Parameters:

Only a selection of search parameters is accessible while editing a profile, those are as follows:

- posting_date : Leave this field empty to display offers posted since the last execution of the program. You can also enter an integer to display offers posted during the last X seconds (e.g. 86400 for the last 24 hours). New profiles default to 604800 seconds (7 days) when no custom posting date is specified.


- keywords : This is the content of your query, if multiple words long, separated with a space.

- geoId : This is the value associated with the location of job offers. To obtain the geoId value, use the tool available on [this website](https://www.ghostgenius.fr/tools/search-sales-navigator-locations-id) to look for the desired location, copy the corresponding value, and then paste it into the field. It can also be retrieved directly from LinkedIn job search URLs.

- distance : This is the increase of value in kilometers of the initial area designated by the geoId.

- sorting filter : This is the sorting filter. Only two inputs are valid, "R" to sort by relevance and "DD" to sort in antechronological order. Any other input or lack thereof defaults to relevance as the sorting filter.

### Save/Update a profile:

Click on the "Save"/"Update" button once you're done editing search parameters, so your changes are taken into account and saved.


### Search:

Click on the "Main Menu" tab at the top left and select Open tab(s) to open a tab for each saved profile.

### Delete a profile:

To delete a profile, click on the button labeled Delete at the bottom right of one of the profile tabs that was saved.

## Convenience:

For frequent personal use, I recommend packaging the program into an executable using PyInstaller to avoid launching it through the Python interpreter each time.

## Implementation Notes:

### Programming language:

Python was chosen for its ease of use and large panel of built-in libraries to solve frequent problems.

### Main limitations and potential for improvement:

- Dependence on the LinkedIn job board : The program is tied to the structure and relevance of the LinkedIn job board, and as such, it might break at some point or become irrelevant. 

- Absence of user input check : User inputs are not validated, as they only affect locally stored configuration data and generated URLs.

- Retrieval of Geoid value : Integration of a built-in geoId lookup system was out of scope for this project. Users must retrieve the value externally.

- Polish the User Interface : While serviceable, the UI could use improvements. The first one being proper scaling for elements.

- Implement Profile Naming : While extremely easy to implement, profile naming would require improvement of the UI first as the increase in tab label width could hinder access to newer tabs.

### Design decisions:

- Data Storage Location: Storing user data in the program directory was avoided because it becomes unreliable when the application is packaged as an executable. The program instead uses an OS-dependent user data directory to ensure persistence across installations and execution contexts.

- Soft deletion of user profile: Direct deletion of profile data during runtime would disrupt the UI state and tab indexing logic. To avoid restructuring the overall architecture, a soft deletion strategy is used. When a user chooses to delete a profile, it is marked as inactive and its corresponding UI tab is disabled, preventing further interaction while preserving tab ordering. The profile is also flagged in the stored data to exclude it from execution. Cleanup of deleted profiles is performed at program startup.


## License:

This project is licensed under the MIT License — see the LICENSE file.








