import os

def make_dir(name):
    try:
        os.mkdir(name)
        return True, None
    except FileNotFoundError as e:
        return False, "Direcoty already exists"
    except Exception as e:
        return False, str(e)

def change_dir(name):
    try:
        os.chdir(name)
        return True, None
    except FileNotFoundError as e:
        return False, "Directory not found"
    except Exception as e:
        return False, str(e)
    
def write_file(filename):
    try:
        with open(filename, "w") as text_file:
            text_file.write("aaaa")
            text_file.write("bbbb")
        print("File created and written successfully.")
    except Exception as e:
        print("Failed to write to file..", e)

def rename_file(name):
    try:
        os.rename(name, "rename.txt")
        print("File renamed to ok")
    except FileNotFoundError:
        print("File not found..")
    except FileExistsError:
        print("File already exist..")
    except Exception as e:
        print("rename failed..", e)
        


success, error = make_dir("folder")
if not success:
    print("mkdir failed:", error)

success, error = change_dir("folder2")
if not success:
    print("chdir failed:", error)

write_file("text.txt")
rename_file("text1.txt")
rename_file("text.txt")