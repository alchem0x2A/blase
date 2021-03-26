# Handles commandline call of blender
import subprocess
import os
import tempfile
import warnings
from pathlib import Path


def handle_site_packages():
    """
    Find the current setting of site-packages and set PYTHONPATH
    the returned env will only be used for subprocess calls
    """
    try:
        import ase
    except ImportError:
        warnings.warn("Cannot import ase library, blender export may fail")
    import site
    import os
    # Import both user and system site packages
    site_packages = site.getsitepackages()
    env = os.environ.copy()
    # Add to $PYTHONPATH
    try:
        python_path = env["PYTHONPATH"]
    except KeyError:
        python_path = ""
    # Add all python site-packages as low-level pythonpath
    python_path_list = python_path.split(":") + site_packages
    env["PYTHONPATH"] = ":".join(site_packages)
    return env

def make_py_script(fileobj,
                   input_file="blase.inp",
                   blender_file="blase.blend"):
    """Write a main python script to be executed
       saves the blend file by default
    """
    #TODO: expanduers expandvars
    input_file = Path(input_file)
    blender_file = Path(blender_file)
    
    content = ["from blase.bio import Blase",
               "import pickle",
               "import bpy",
               f"inputfile='{input_file}'",
               "with open(inputfile, 'rb') as f:",
               "    images, kwargs = pickle.load(f)",
               "bobj = Blase(images, **kwargs)",
               "bobj.draw()",
               f"bpy.ops.wm.save_as_mainfile(filepath='{blender_file.as_posix()}')"]

    
    fileobj.writelines(map(lambda s: s+"\n", content))
    fileobj.seek(0)
    return


def save_blender_cli(input_file="blase.inp",
                     blender_file="blase.blend"):
    """Draw the blender scene using intermediate input file
       save to blender_file
    """
    subproc_env = handle_site_packages()
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py") as fpy:
        make_py_script(fpy, input_file=input_file, blender_file=blender_file)
        # blender command
        command = ["blender", "-b", "-noaudio",
                   "--python-use-system-env",
                   "-P", f"{fpy.name}"]
        # command = ["blender", "-b", "-noaudio", "-P", "./test_env.py"]
        proc = subprocess.run(command, env=subproc_env)
        return proc.returncode
