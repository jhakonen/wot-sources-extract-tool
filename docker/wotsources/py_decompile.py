import os
import traceback
import uncompyle6

def will_convert(path):
    return all([
    	# Is compiled py file
    	path.endswith(".pyc"),
    	# Is not Python std lib file
    	os.path.join("scripts", "common", "Lib") not in path,
    	# Is not problematic file
    	path != "scripts/client/gui/Scaleform/locale/RES_ICONS.pyc",
    ])

def convert(root_dir, src):
    print "Decompiling {}".format(src)
    dest_path = src[:-1] # .pyc --> .py
    dest_path = os.path.join("py", dest_path)
    full_dest_path = os.path.join(root_dir, dest_path)
    full_dest_dir_path = os.path.dirname(full_dest_path)
    full_src_path = os.path.join(root_dir, src)
    # Create destination directory
    if not os.path.exists(full_dest_dir_path):
        os.makedirs(full_dest_dir_path)
    # Decompile .pyc file to .py file
    with open(full_dest_path, "w+b") as dest_file:
        try:
            uncompyle6.uncompyle_file(full_src_path, dest_file)
        except:
            traceback.print_exc()

        # Replace uncompyle6 headers to avoid unnecessary changes in git history
        dest_file.seek(0)
        lines = dest_file.read().split("\n")
        assert all(line.startswith("#") for line in lines[:4]), \
            "File (%s) doesn't have uncompyle6 headers" % full_dest_path
        dest_file.seek(0)
        dest_file.truncate()
        dest_file.write("\r\n".join(lines[4:]))

    # Return decompiled .py file path
    return [dest_path]
