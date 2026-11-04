import glob
import os
import shutil
import sys
from pathlib import Path
from time import localtime, strftime


def main():
    if len(sys.argv) < 3:
      print("Usage: python Image_Organizer.py <Input Directory> <Output Directory> <File Types>")
      sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print('#######################\n'
            '### Image Organizer ###\n'
            '#######################')
    print(f"Checking {input_path}")

    file_types = []
    file_extensions = []

    for type in sys.argv[3].split(","):
        file_types.append(type)

    print(file_types)

    for type in file_types:
        file_extensions.append("*." + type)

    file_lists = {}
    input_globs = {}
    found_messages = {}
    file_mod_times = {}
    file_subdirs = {}

    discovered_filetypes = set()
    combined_mod_times = set()
    combined_subdirs = set()
    all_files = set()

    for i, file_type in enumerate(file_types):
        input_globs[i] = input_path + os.sep + "**" + os.sep + file_extensions[i]
        file_lists[i] = glob.glob(input_globs[i], recursive=True)

        if len(file_lists[i]) > 0:
            discovered_filetypes.add(file_type)
            found_messages[i] = f"{len(file_lists[i])} {file_type} file(s) in {len(get_subdirectory(file_lists[i]))} folder(s)"
            file_mod_times[i] = get_file_mod_time(file_lists[i])
            file_subdirs[i] = get_subdirectory(file_lists[i])

    # Exit if no files of expected type(s) have been discovered.
    if len(discovered_filetypes) == 0:
        print("No files found")
        sys.exit(1)
    else:
        for v in found_messages.values():
            print(v)

    for v in file_mod_times.values():
        combined_mod_times.update(v)
    combined_mod_times = sorted(combined_mod_times)

    for v in file_subdirs.values():
        combined_subdirs.update(v)
    combined_subdirs = sorted(combined_subdirs)

    for v in file_lists.values():
        all_files.update(v)
    all_files = sorted(all_files
    )

    # Captures list of created directories for later cleanup of empty dirs.
    created_directories = sorted(create_output_dirs(output_path, combined_subdirs, combined_mod_times, discovered_filetypes))

    # Copy all input files to correspodning folder in output_path.
    copy_files(all_files, discovered_filetypes, created_directories, output_path)

    # Remove any directory that was created but not used.
    remove_empty_directories(created_directories)

    # Done!
    print("Done!")

def get_file_mod_time(files):
    unique_dates = set()
    for file in files:
        file_date = os.path.getmtime(file)
        unique_dates.add(strftime('%Y-%m-%d', localtime(file_date)))
    return unique_dates

def get_subdirectory(files):
    unique_subdirectories = set()
    for file in files:
        subdirectory = os.path.basename(os.path.dirname(file))
        unique_subdirectories.add(subdirectory)
    return unique_subdirectories

def create_output_dirs(output, subdirectories, dates, filetypes):
    created_dirs = set()
    for type in filetypes:
        for subdir in subdirectories:
            for date in dates:
                create_path = output + os.sep + subdir + os.sep + type + os.sep + date
                Path(create_path).mkdir(parents=True, exist_ok=True)
                created_dirs.add(create_path)
    return created_dirs

def copy_files(files, filetype, created_directories, output_path):
    moved_files = set()
    num_moved_files = 1
    num_of_files = len(files)
    for f_type in filetype:
        for file in files:
            f_mod_time = strftime('%Y-%m-%d', localtime(os.path.getmtime(file)))
            f_sub_dir = os.path.basename(os.path.dirname(file))
            f_name = os.path.basename(file)
            expected_path = output_path + os.sep + f_sub_dir + os.sep + f_type + os.sep + f_mod_time
            if f_name not in moved_files and f_type in f_name:
                for dir in created_directories:
                    target_path = dir + os.sep + f_name
                    if dir == expected_path and target_path not in moved_files and not os.path.exists(target_path):
                        shutil.copyfile(file, target_path)
                        print(f"Copying {num_moved_files}/{num_of_files} files")
                        moved_files.add(target_path)
                        num_moved_files += 1
            else:
                continue

def remove_empty_directories(created_directories):
    print("Cleaning up directories")
    for directory in created_directories:
        try:
            os.rmdir(directory)
        except OSError:
            continue
        try:
            os.rmdir(os.path.dirname(directory))
        except OSError:
            continue

if __name__ == "__main__":
    main()
