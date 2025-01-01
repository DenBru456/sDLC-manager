import os
import glob
import win32api
import shutil
import re

# Components dictionary
components = {
    'Steam': ['steam_api.dll', 'wotblitz.exe'],
    'WGC': ['wgc_api.dll', 'wgc_api.exe', 'wotblitz.exe'],
    'LGC': ['tanksblitz.exe']
}

steam_and_wgc_packs = os.path.join(os.getenv('LOCALAPPDATA'), 'wotblitz', 'packs')
lgc_packs = os.path.join(os.getenv('USERPROFILE'), 'Documents', 'TanksBlitz', 'packs')

list_ignore_folders = ["locales", "3d", "Configs", "Fonts", "Gfx", "HtmlDocuments", "Materials", "Materials.custom", "MessageFilters", "replays", "Stories", "Strings", "UI", "WwiseSound", "XML"]
list_of_found_folders_and_path_to_them = []

game_type = None

game_packs = None

game_path = None

game_version = None

selected_mod = None










# First: game info


# Prompt user to choose client
print("Choose client:\n1. Steam\n2. WGC\n3. LGC")
choice = input("Input[1-3]: ")

# Determine game type based on user input
if choice == '1':
    game_type = 'Steam'
elif choice == '2':
    game_type = 'WGC'
elif choice == '3':
    game_type = 'LGC'
else:
    print("Invalid choice")
    exit()

# Search and display folders with the selected client components
def search_folders(component_list):
    folders = []
    for root, dirs, files in os.walk('/'):
        if all(comp in files for comp in component_list):
            folders.append(root)
    return folders

folders = search_folders(components[game_type])
print(f"{game_type}:")
for idx, folder in enumerate(folders):
    print(f"{idx + 1}. {folder}")

# Prompt user to select a folder
selected_number = int(input("Input: "))
game_path = os.path.abspath(folders[selected_number - 1])

# Find game version
def find_game_version(path, exe_name):
    exe_path = glob.glob(os.path.join(path, exe_name))
    if exe_path:
        info = win32api.GetFileVersionInfo(exe_path[0], '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        game_version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
        return game_version
    return "Version not found"

if game_type in ['Steam', 'WGC']:
    game_version = find_game_version(game_path, 'wotblitz.exe')
else:
    game_version = find_game_version(game_path, 'tanksblitz.exe')


if game_type in ['Steam', 'WGC']:
    game_packs = steam_and_wgc_packs
else:
    game_packs = lgc_packs

# Print the results
print(f"""
{game_type} {game_version}

{game_path}

{game_packs}
""")










# Second: file sync actions 
disable_check = input("Disable online sDLC check? (Y/n/r): ")

if disable_check.lower() == 'y':

    # Create backup folder in game_packs path
    backup_folder = os.path.join(game_packs, f"Backup {game_version}")
    os.makedirs(backup_folder, exist_ok=True)

    # Move need_sync_cache_and_files to backup folder
    file_to_move = os.path.join(game_packs, 'need_sync_cache_and_files')
    if os.path.exists(file_to_move):
        shutil.move(file_to_move, backup_folder)
        print(f"Moved {file_to_move} to {backup_folder}")
    else:
        print(f"{file_to_move} does not exist.")

elif disable_check.lower() == 'n':
    print("Online sDLC check not disabled.")


elif disable_check.lower() == 'r':
    # List all backup folders
    backup_dirs = [d for d in os.listdir(game_packs) if d.startswith("Backup")]
    if not backup_dirs:
        print("No backup folders found.")
    else:
        print("Available backup folders:")
        for idx, folder in enumerate(backup_dirs):
            print(f"{idx + 1}. {folder}")

        choice = int(input(f"Select a folder to restore [1-{len(backup_dirs)}]: "))
        if 1 <= choice <= len(backup_dirs):
            selected_backup_folder = backup_dirs[choice - 1]
            src_file = os.path.join(game_packs, selected_backup_folder, 'need_sync_cache_and_files')

            if os.path.exists(src_file):
                dest_file = os.path.join(game_packs, 'need_sync_cache_and_files')
                shutil.move(src_file, dest_file)
                print(f"Restored {src_file} to {dest_file}")

                # Delete the selected backup folder after restoring the file
                shutil.rmtree(os.path.join(game_packs, selected_backup_folder))
                print(f"Deleted backup folder: {selected_backup_folder}")
            else:
                print(f"{src_file} does not exist in the selected backup folder.")
        else:
            print("Invalid selection.")
else:
    print(f"Your choice was {disable_check.lower()}")   














# Third: find and adjust configs



for root, dirs, files in os.walk(game_path):
    dirs[:] = [d for d in dirs if d not in list_ignore_folders]
    if "Bfile.ini" in files and "unmod.ini" in files:
        folder_name = os.path.basename(root)
        folder_path_to_their_Bfile = os.path.join(root, "Bfile.ini")
        folder_path_to_their_unmod = os.path.join(root, "unmod.ini")
        list_of_found_folders_and_path_to_them.append((folder_name, folder_path_to_their_Bfile, folder_path_to_their_unmod))

# Create folders in configs and copy Bfile.ini
configs_path = os.path.join(os.path.dirname(__file__), "configs")
os.makedirs(configs_path, exist_ok=True)

for folder_name, bfile_path, unmod_path in list_of_found_folders_and_path_to_them:
    dest_folder = os.path.join(configs_path, folder_name)
    os.makedirs(dest_folder, exist_ok=True)
    shutil.copy(bfile_path, dest_folder)
    shutil.copy(unmod_path, dest_folder)

# Modify Bfile.ini in each folder
for folder_name, bfile_path, unmod_path in list_of_found_folders_and_path_to_them:
    folder_path = os.path.join(configs_path, folder_name)
    bfile_path = os.path.join(folder_path, "Bfile.ini")
    ufile_path = os.path.join(folder_path, "Ufile.ini")
    unmod_path = os.path.join(folder_path, "unmod.ini")

    with open(bfile_path, 'r') as file:
        content = file.read()

    # Modify Bfile.ini content
    modified_content = content.replace(game_path + r"\Data", game_packs).replace(".dvpljmp3", ".dvpl")

    with open(bfile_path, 'w') as file:
        file.write(modified_content)

    # Create Ufile.ini with different modifications
    ufile_content = content.replace(game_path + r"\Data", game_packs)

    with open(ufile_path, 'w') as file:
        file.write(ufile_content)

    # Modify unmod.ini content
    with open(unmod_path, 'r') as file:
        content = file.read()

    # Replace the part between 1= and 2=
    content = re.sub(r'1=.*?2=', f'game={game_type}\n2=', content, flags=re.DOTALL)
    # Replace "3" with "version" while keeping its original value
    content = re.sub(r'3=(.*)', r'version=\1', content)

    # Write the modified content back to the ini file
    with open(unmod_path, 'w') as file:
        file.write(content)









# Fourth: select config


def list_configs_folders(mod_path):
    folders = []
    for f in os.listdir(mod_path):
        folder_path = os.path.join(mod_path, f)
        if os.path.isdir(folder_path):
            version, game = get_version_from_unmod(folder_path)
            folders.append((f, version, game))
    return folders

def get_version_from_unmod(folder_path):
    version = "Unknown"
    game = "Unknown"
    unmod_file = os.path.join(folder_path, "unmod.ini")
    if os.path.exists(unmod_file):
        with open(unmod_file, 'r') as file:
            for line in file:
                if line.startswith("version"):
                    version = line.strip().split('=')[1]
                elif line.startswith("game"):
                    game = line.strip().split('=')[1]
    return version, game

def select_folder(mod_path):
    folders = list_configs_folders(mod_path)
    if not folders:
        print("No folders found in configs.")
        return None

    print("\nSelect a folder:")
    for idx, (folder, version, game) in enumerate(folders, start=1):
        print(f"{idx}. {folder} (version: {version} game: {game})")

    choice = int(input("Input the number of the folder: "))
    if 1 <= choice <= len(folders):
        selected_folder, selected_version, selected_game = folders[choice - 1]
        print(f"Selected folder: {selected_folder} (version: {selected_version} game: {selected_game})")
        return os.path.join(mod_path, selected_folder)
    else:
        print("Invalid choice.")
        return None









# Fifth: Freeze/Unfreeze

def modify_files(file_list_path, old_ext, new_ext):
    with open(file_list_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        mod_path = line.strip()
        if mod_path.endswith(old_ext):
            new_file_path = mod_path.replace(old_ext, new_ext)
            print(f"Attempting to rename: {mod_path} to {new_file_path}")
            if os.path.exists(mod_path):
                os.rename(mod_path, new_file_path)
                print(f"Renamed: {mod_path} to {new_file_path}")
            else:
                print(f"File not found: {mod_path}")
        else:
            print(f"File does not end with {old_ext}: {mod_path}")

mod_path = os.path.join(os.path.dirname(__file__), "configs")
selected_folder = select_folder(mod_path)

if not selected_folder:
    print("No folder was selected.")

print(f"Selected folder: {selected_folder}")
bfile_path = os.path.join(selected_folder, "Bfile.ini")
ufile_path = os.path.join(selected_folder, "Ufile.ini")

action = input("\nSelect action:\n1. Freeze\n2. Unfreeze\nInput:(1,2): ")
if action == '1':
    if os.path.exists(bfile_path):
        modify_files(bfile_path, ".dvpl", ".dvpljmp3")
        print("Freeze action completed.")
    else:
        print(f"Bfile.ini not found in {selected_folder}")
elif action == '2':
    if os.path.exists(ufile_path):
        modify_files(ufile_path, ".dvpljmp3", ".dvpl")
        print("Unfreeze action completed.")
    else:
        print(f"Ufile.ini not found in {selected_folder}")
else:
    print("Invalid action.")


# Sixth: Cleanup and exit
shutil.rmtree(configs_path)


