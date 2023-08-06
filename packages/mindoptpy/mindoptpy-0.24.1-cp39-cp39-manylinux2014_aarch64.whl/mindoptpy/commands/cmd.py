import argparse
import os
import platform
import shutil
import subprocess
import sys

version_info = "0.24.1"
os.environ['MDO_LICENSE_VERBOSE_LV'] = "2"


def get_home_dir():
    if sys.platform == "win32":
        home_dir = os.environ["USERPROFILE"]
    elif sys.platform == "linux" or sys.platform == "darwin":
        home_dir = os.environ["HOME"]
    else:
        raise NotImplemented(f"Error! Not this system. {sys.platform}")
    return home_dir


os_arch = "linux64-x86"

if platform.system() == "Windows":
    os_arch = "win64-x86"
elif platform.system() == "Linux":
    if platform.machine() == "arm64":
        os_arch = "linux64-aarch"
    else:
        os_arch = "linux64-x86"
elif platform.system() == "Darwin":
    if platform.machine() == "arm64":
        os_arch = "osx64-aarch"
    else:
        os_arch = "osx64-x86"

sdk_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sdk_docs_dir = os.path.join(sdk_root_dir, "doc")
sdk_exam_dir = os.path.join(sdk_root_dir, "examples")
sdk_arch_dir = os.path.join(sdk_root_dir, os_arch)
sdk_bin_dir = os.path.join(sdk_arch_dir, "bin")


def install_full():
    print("mindopt examples, c/c++ sdk(include headers, libraries) will be installed into this location:")
    print("===> {0}".format(get_home_dir()))
    print("  - Press ENTER to confirm the location")
    print("  - Press CTRL-C to abort the installation")
    print("  - Or specify a different location below")
    print("===> ", end="")

    path = input()
    if len(path) == 0:
        path = get_home_dir()
    print("===> Installing to {}".format(path))
    path = os.path.join(path, "mindopt")
    target_path = os.path.abspath(os.path.join(path, version_info))

    shutil.copytree(sdk_docs_dir, os.path.join(target_path, "doc"))
    shutil.copytree(sdk_exam_dir, os.path.join(target_path, "examples"))
    shutil.copytree(sdk_arch_dir, os.path.join(target_path, os_arch))

    if platform.system() == "Windows":
        import winreg
        user_env = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(user_env, "MINDOPT_HOME", 0, winreg.REG_EXPAND_SZ, target_path)
        winreg.CloseKey(user_env)

        user_env = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)

        path_value, path_type = winreg.QueryValueEx(user_env, "PATH")
        winreg.CloseKey(user_env)

        mindopt_lib_path = os.path.join(target_path, "win64-x86", "lib")
        mindopt_bin_path = os.path.join(target_path, "win64-x86", "bin")
        if mindopt_lib_path not in path_value:
            path_value = mindopt_lib_path + os.pathsep + path_value
        if mindopt_bin_path not in path_value:
            path_value = mindopt_bin_path + os.pathsep + path_value
        # update
        user_env = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(user_env, "PATH", 0, path_type, path_value)
        winreg.CloseKey(user_env)

        print("")
        print("Installation has been completed.")
        print("Need to restart your computer for the environment to take effect.")
        print("And then type 'mindopt --help' for more information.")
    else:
        os.system("bash {} {}".format(os.path.join(target_path, os_arch, ".export.sh"), target_path))


def run_check():
    import mindoptpy
    from mindoptpy import MdoError

    case_path = os.path.join(sdk_exam_dir, "data", "afiro.mps")

    model = mindoptpy.MdoModel()

    try:
        model.read_prob(case_path)
        model.solve_prob()
        model.display_results()

    except MdoError as e:
        print("Received MindOpt exception.")
        print(" - Code          : {}".format(e.code))
        print(" - Reason        : {}".format(e.message))
    except Exception as e:
        print("Received exception.")
        print(" - Reason        : {}".format(e))
    finally:
        model.free_mdl()

    return ""


def run_mindoptpy():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--check",
        action="store_true",
        help="run a simple example to test the solver.",
    )
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="print mindopt solver version.",
    )

    args = parser.parse_args()
    if not sys.argv[1:]:
        parser.print_help()
    if args.check:
        print(run_check())
    if args.version:
        print("MindOpt Solver Version:", version_info)
