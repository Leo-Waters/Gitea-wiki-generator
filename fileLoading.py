
#will load an ignore list settings file
def load_ignore_list():
    pass

#should this directory be ignored
def should_ignore_directory(dir_path):
    return False

#should this file be ignored
def should_ignore_file(file_path):
    return False

#returns a list of files with the desired extension
def find_files_with_extension(directory, extension):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:

            file_path=os.path.join(root, file)

            #does the file have the desired extension and should the file be ignored
            if file.endswith(extension) and should_ignore_file(file_path)==False:
                matching_files.append(file_path)

    return matching_files