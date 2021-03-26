import subprocess
import os
import tempfile
try:
    import ase
except ImportError:
    raise ImportError("ASE cannot be imported. ")

def handle_site_packages():
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

def main():
    # Use a temp .py file as the container for execution
    subproc_env = handle_site_packages()
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py") as fpy:
        fpy.writelines("\n".join(["import ase", "print(ase)"]))
        fpy.seek(0)
        command = ["blender", "-b", "-noaudio",
                   "--python-use-system-env",
                   "-P", f"{fpy.name}"]
        # command = ["blender", "-b", "-noaudio", "-P", "./test_env.py"]
        subprocess.run(command, env=subproc_env)

if __name__ == "__main__":
    main()
