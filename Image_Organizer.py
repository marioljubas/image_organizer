import glob
import os
import shutil
import sys
from pathlib import Path
from time import localtime, strftime


def main():
    if len(sys.argv) < 3:
      print("Usage: python Image_Organizer.py <Input Directory> <Output Directory>")
      sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    filetypes = set()
    combined_mod_times = set()
    combined_subdirs = set()
    all_files = set()
    dng_input_glob = input_path + os.sep + "**" + os.sep +"*.DNG"
    jpg_input_glob = input_path + os.sep + "**" + os.sep +"*.JPG"

    print('#######################\n'
            '### Image Organizer ###\n'
            '#######################')
    print(f"Checking {input_path} for .DNG and .JPG files...")

    # Gather matching file(s).
    dng_files = glob.glob(dng_input_glob, recursive=True)
    jpg_files = glob.glob(jpg_input_glob, recursive=True)

    # Create discovery message(s).
    found_message_dng = f"{len(dng_files)} DNG file(s) in {len(get_subdirectory(dng_files))} folder(s)"
    found_message_jpg = f"{len(jpg_files)} JPG file(s) in {len(get_subdirectory(jpg_files))} folder(s)"

    # Print discovery messages and populate filetypes set with types seen.
    if len(dng_files) > 0 and len(jpg_files) > 0:
        print(f"Found {found_message_dng} and {found_message_jpg}")
        filetypes = {"DNG","JPG"}
    elif len(dng_files) > 0 and len(jpg_files) == 0:
        print(f"Found {found_message_dng}")
        filetypes = {"DNG"}
    elif len(dng_files) == 0 and len(jpg_files) > 0:
        print(f"Found {found_message_jpg}")
        filetypes = {"JPG"}
    else:
        print("No files found")
        sys.exit(1)

    # Iterate through list of discovered files and build set of mod times.
    dng_mod_times = get_file_mod_time(dng_files)
    jpg_mod_times = get_file_mod_time(jpg_files)
    combined_mod_times.update(dng_mod_times)
    combined_mod_times.update(jpg_mod_times)
    combined_mod_times = sorted(combined_mod_times)

    # Iterate through list of discovered files and pull subdirectory containing images.
    dng_subdirs = get_subdirectory(dng_files)
    jpg_subdirs = get_subdirectory(jpg_files)
    combined_subdirs.update(dng_subdirs)
    combined_subdirs.update(jpg_subdirs)
    combined_subdirs = sorted(combined_subdirs)

    # Create set of all input files.
    all_files.update(dng_files)
    all_files.update(jpg_files)
    all_files = sorted(all_files)

    # Captures list of created directories for later cleanup of empty dirs.
    created_directories = sorted(create_output_dirs(output_path, combined_subdirs, combined_mod_times, filetypes))

    # Copy all input files to correspodning folder in output_path.
    copy_files(all_files, filetypes, created_directories, output_path)

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
    print(f"Copied {len(moved_files)} {filetype} files")

def remove_empty_directories(created_directories):
    print("Cleaning up directories")
    for directory in created_directories:
        try:
            os.rmdir(directory)
        except OSError as error:
            continue
        try:
            os.rmdir(os.path.dirname(directory))
        except OSError as error:
            continue

if __name__ == "__main__":
    main()
