import multiprocessing
import os
import subprocess
import re

IGNORED_SWFS = [
    "battleDirectionIndicatorApp.swf", # Gives error: Premature end of the stream reached
    "lobby.swf" # Too big to fit in memory, enable once docker LCOW allows giving container more memory
]

def will_convert(path):
    return path.endswith(".swf") and os.path.basename(path) not in IGNORED_SWFS

def convert(root_dir, src):
    swf_filepath = os.path.join(root_dir, src)
    destination_dirpath = os.path.join(root_dir, "as")
    print "Exporting ActionScript sources from {}...".format(src)
    try:
        _call_ffdec(destination_dirpath, swf_filepath, parallel=True)
    except RuntimeError:
        print "FAILED, retrying without parallel decompiling..."
        _call_ffdec(destination_dirpath, swf_filepath, parallel=False)
    output_paths = []
    for root, dirs, files in os.walk(destination_dirpath):
        for file in files:
            filepath = os.path.join(root, file)
            output_paths.append(os.path.relpath(_to_safe_file(filepath), root_dir))
    return output_paths

def _call_ffdec(dst, swf_file, parallel):
    config = ""
    if parallel:
        config += "parallelSpeedUp=1,parallelSpeedUpThreadCount={}".format(multiprocessing.cpu_count())
    else:
        config += "parallelSpeedUp=0,parallelSpeedUpThreadCount=1"
    with open(os.devnull, 'w') as devnull:
        result = subprocess.call([
            "ffdec",
            "-exportTimeout", "3600",
            "-config", config,
            "-export",
            "script",
            dst,
            swf_file
        ], stdout=devnull)
        if result != 0:
            raise RuntimeError('ffdec failed with exit code: %s' % result)

def _to_safe_file(src):
    # Some extracted files have question marks in file names, this function
    # renames those files to Windows FS compliant files
    dirname, filename = os.path.split(src)
    safe_filename = re.sub('[^-a-zA-Z0-9$.]', '_', filename)
    safe_src = os.path.join(dirname, safe_filename)
    if src != safe_src:
        os.rename(src, safe_src)
    return safe_src
