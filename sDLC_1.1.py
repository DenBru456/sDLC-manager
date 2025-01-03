import os
import glob
import shutil
import win32api

game_type = None
game_packs = None
game_path = None
game_version = None

list_of_found_folders_and_path_to_them = []

components = {
    'Steam': ['steam_api.dll', 'wotblitz.exe'],
    'WGC': ['wgc_api.dll', 'wotblitz.exe'],
    'LGC': ['tanksblitz.exe']
}

steam_and_wgc_packs = os.path.expandvars(r'%LOCALAPPDATA%\wotblitz\packs')
lgc_packs = os.path.expandvars(r'%USERPROFILE%\Documents\TanksBlitz\packs')

typical_paths = {
    'Steam': os.path.expandvars(r'%PROGRAMFILES(X86)%\Steam\steamapps\common\World of Tanks Blitz'),
    'WGC': os.path.expandvars(r'C:\Games\World_of_Tanks_Blitz'),
    'LGC': os.path.expandvars(r'%USERPROFILE%\Documents\TanksBlitz')
}


  



def typical_info():

    typ_choice = input( "Choose client: \n 1.Steam \n 2.WGC \n 3.LGC \n\n Input[1-3]: ") 
            
    if typ_choice == '1':
            game_type = 'Steam'

            game_path = typical_paths['Steam']


    if  typ_choice == '2':
            game_type = 'WGC'

            game_path = typical_paths['WGC']


    if  typ_choice == '3':
            game_type = 'LGC'

            game_path = typical_paths['LGC']

    return game_type, game_path    








def search_info():
    sea_info = input("Choose client: \n 1.Steam \n 2.WGC \n 3.LGC \n Input[1-3]")

    if sea_info == '1':
        game_type = 'Steam'
    elif sea_info == '2':
        game_type = 'WGC'
    elif sea_info == '3':
        game_type = 'LGC'
    else:
        print("Invalid input")
        return



    return game_type 
            
def custom_info():
    own_choice = input("Enter game type: 1.Steam 2.WGC 3.LGC      ")

    if own_choice == '1':
        game_type = 'Steam'

    if own_choice == '2':
        game_type = 'WGC'

    if own_choice == '3':
        game_type = 'LGC'

    return game_type    





def detect_game_version(game_path):
    exe_path = os.path.join(game_path, 'wotblitz.exe')
    if os.path.exists(exe_path):
        info = win32api.GetFileVersionInfo(exe_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
    return None

def find_game_packs(game_type):
    if game_type in ['Steam', 'WGC']:
        game_packs = steam_and_wgc_packs
    elif game_type == 'LGC':
        game_packs = lgc_packs
    else:
        return []
    
    return game_packs
    








first_info = input("Choose info type: \n 1.Typical \n 2.Search \n 3.Custom Input[1-3]")
if first_info == '1':
    game_type, game_path = typical_info()

    
elif first_info == '2':
    game_type = search_info()
    component_list = components[game_type]
    folders = []
    list_ignore_folders = ["locales", "3d", "Configs", "Fonts", "Gfx", "HtmlDocuments", "Materials", "Materials.custom", "MessageFilters", "replays", "Stories", "Strings", "UI", "WwiseSound", "XML", "Users", "Windows", "ProgramData", "PerfLogs", "Imagination Technologies", "OneDriveTemp", "Internet Explorer", "MediaTek"]

    for root, dirs, files in os.walk('/'):
        # Remove ignored folders from dirs to prevent os.walk from traversing them
        dirs[:] = [d for d in dirs if d not in list_ignore_folders]
        if all(comp in files for comp in component_list):
            folders.append(root)

    print(f"{game_type}:")
    for idx, folder in enumerate(folders):
        print(f"{idx + 1}. {folder}")

    selected_number = int(input("Input: "))
    game_path = os.path.abspath(folders[selected_number - 1])


elif first_info == '3':
    game_type = custom_info()
    cus_path = input("Enter path to game folder: ")
    game_path = os.path.normpath(cus_path)

game_version = detect_game_version(game_path)
game_packs = find_game_packs(game_type)



if os.path.exists(game_path):
    print(f"\n {game_type} {game_version} \n Game: {game_path} \n sDLC: {game_packs}")
else:
    print(f"\n The path {game_path} does not exist.")










# Second: file sync actions 



disable_check = input("Disable online sDLC check? (Y/n/r): ")

if disable_check.lower() == 'y':
    # Check if need_sync_cache_and_files exists before proceeding
    file_to_move = os.path.join(game_packs, 'need_sync_cache_and_files')
    if os.path.exists(file_to_move):
        # Create backup folder in game_packs path
        backup_folder = os.path.join(game_packs, f"Backup {game_version}")
        os.makedirs(backup_folder, exist_ok=True)

        # Move need_sync_cache_and_files to backup folder
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

list_ignore_folders = ["locales", "3d", "Configs", "Fonts", "Gfx", "HtmlDocuments", "Materials", "Materials.custom", "MessageFilters", "replays", "Stories", "Strings", "UI", "WwiseSound", "XML", "Users", "Windows", "ProgramData", "PerfLogs", "Imagination Technologies", "OneDriveTemp", "Internet Explorer", "MediaTek"]
list_of_found_folders_and_path_to_them = []

for root, dirs, files in os.walk(game_path):
    dirs[:] = [d for d in dirs if d not in list_ignore_folders]
    if "Bfile.ini" in files and "Dfile.ini" in files and "unmod.ini" in files:
        folder_name = os.path.basename(root)
        folder_path_to_their_Bfile = os.path.join(root, "Bfile.ini")
        folder_path_to_their_Dfile = os.path.join(root, "Dfile.ini")
        
        list_of_found_folders_and_path_to_them.append((folder_name, folder_path_to_their_Bfile, folder_path_to_their_Dfile))   

# Prompt user to select a folder
print("Select a folder from the list:")
for idx, (folder_name, _, dfile_path) in enumerate(list_of_found_folders_and_path_to_them):
    unmod_path = os.path.join(os.path.dirname(dfile_path), 'unmod.ini')
    with open(unmod_path, 'r') as unmod_file:
        unmod_content = unmod_file.read()
        version_line = [line for line in unmod_content.splitlines() if line.startswith('3=')][0]
        version = version_line.split('=')[1]
    print(f"{idx + 1}. {folder_name} (Version: {version})")

selected_number = int(input("Input: "))
selected_folder = list_of_found_folders_and_path_to_them[selected_number - 1]

# Create Fze.ini and Ufze.ini with modified content
folder_path = os.path.dirname(selected_folder[1])
bfile_path = selected_folder[1]
dfile_path = selected_folder[2]

with open(bfile_path, 'r') as bfile:
    bfile_content = bfile.read()

with open(dfile_path, 'r') as dfile:
    dfile_content = dfile.read()

# Modify content for Fze.ini
fze_content = bfile_content.replace('.dvpljmp3', '.dvpl') + "\n" + dfile_content
fze_content = fze_content.replace(game_path + '\\Data', game_packs)

# Modify content for Ufze.ini
ufze_content = bfile_content + "\n" + dfile_content.replace('.dvpl', '.dvpljmp3')
ufze_content = ufze_content.replace(game_path + '\\Data', game_packs)

fze_path = os.path.join(folder_path, 'Fze.ini')
ufze_path = os.path.join(folder_path, 'Ufze.ini')

with open(fze_path, 'w') as fze_file:
    fze_file.write(fze_content)

with open(ufze_path, 'w') as ufze_file:
    ufze_file.write(ufze_content)





# Freeze and Unfreeze actions
option = input("Option:\n\n1. Freeze\n2. Unfreeze\n3. Critical Restore\n\nInput: ")

if option == '1':
    # Freeze
    with open(fze_path, 'r') as fze_file:
        fze_content = fze_file.read().splitlines()

    for file_path in fze_content:
        print(f"Checking file: {file_path}")
        if os.path.exists(file_path):
            new_file_path = file_path.replace('.dvpl', '.dvpljmp3')
            os.rename(file_path, new_file_path)
            print(f"Renamed {file_path} to {new_file_path}")
        else:
            print(f"File {file_path} does not exist")

elif option == '2':
    # Unfreeze
    with open(ufze_path, 'r') as ufze_file:
        ufze_content = ufze_file.read().splitlines()

    for file_path in ufze_content:
        print(f"Checking file: {file_path}")
        if os.path.exists(file_path):
            new_file_path = file_path.replace('.dvpljmp3', '.dvpl')
            os.rename(file_path, new_file_path)
            print(f"Renamed {file_path} to {new_file_path}")
        else:
            print(f"File {file_path} does not exist")

elif option == '3':
    # Critical Restore
    for root, dirs, files in os.walk(game_packs):
        for file in files:
            if file.endswith('.dvpljmp3'):
                file_path = os.path.join(root, file)
                new_file_path = file_path.replace('.dvpljmp3', '.dvpl')
                os.rename(file_path, new_file_path)
                print(f"Renamed {file_path} to {new_file_path}")            

else:
    print("Invalid option selected.")


# Final

try:
    os.remove(fze_path)
    print(f"Removed {fze_path}")
except OSError as e:
    print(f"Error removing {fze_path}: {e}")

try:
    os.remove(ufze_path)
    print(f"Removed {ufze_path}")
except OSError as e:
    print(f"Error removing {ufze_path}: {e}")


input("Press Enter to close")    
