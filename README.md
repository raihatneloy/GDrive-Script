# Setup (First time only)

Clone the scripts to your local directory:
`git clone git@github.com:raihatneloy/GDrive-Script.git`

Go to the cloned directory using `cd`. 
`cd <path to clonned scripts>`

Install the requirements
`pip install -r requirements.txt`

If you face any issues installing requirements, please run: `sudo pip install -r requirements.txt`

# Usage

For using the script you will have to go to the script's directory.
`cd <path to scripts>`

## List command

List files from the root folder
`./gdrive.py list`

List files in a directory using folder id:
`./gdrive.py list --id <directory_id>`

List filest in a directory using directory url (original/share url):
`./gdrive.py list --url <directory_url>`

Output the list in a file
`./gdrive.py list -o <output_file_path>`

## Download command

Default download directory will be: `<stript dir>/output/`

Download a directory or file using their id:
`./gdrive.py download --id <directory/file id>`

Download file from a file which was previously exported using the script
`./gdrive.py download -f <file path>`

Download file in a specific directory:
`./gdrive.py download -f <file_path> -o <output_directory_path>`