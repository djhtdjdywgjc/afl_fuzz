import os
import sys
import subprocess
import multiprocessing
import time

# set parameters for fuzz automatically
CC_module = ""
fuzz_time = ""
file_name = ""
CXX_module = ""
install_path = ""
download_directory = ""
source_code = ""
compile_setting = ""
edit_params = [] # complie args
fuzzer_args = [] # afl-fuzz args
fuzz_targets = []

def output_info(info):
    print("[*] " + info)

def err(info):
    print("[!] " + info)
    sys.exit()

def check_path(addr):
    if os.path.isdir(addr): 
        return addr
    else:
        err("\"" + addr + "\"" + " is not a valid path")

def set_env():
    os.environ['LLVM_CONFIG'] = "llvm-config-11"
    os.environ['AFL_USE_ASAN'] = '1'

def compile_args_handle():
    global CC_module
    global CXX_module
    global edit_params
    global file_name
    global install_path
    global fuzzer_args
    global fuzz_targets
    global download_directory
    global fuzz_time
    global compile_setting
    global source_code

    i = 1
    while i < len(sys.argv):
        print(f"Argument {i}: {sys.argv[i]}")

        if sys.argv[i] == "-CC":
            if i + 1 >= len(sys.argv):
                err("It is necessary to specify the specific instrumentation module")
            if sys.argv[i+1].find("afl-clang-fast"):
                CC_module += sys.argv[i+1]
            elif sys.argv[i+1] == "afl-clang":
                CC_module += sys.argv[i+1]
            elif sys.argv[i+1] == "afl-cc":
                CC_module += sys.argv[i+1]
            else:
                err("invalid argument")
            i += 2
            continue

        elif sys.argv[i] == "-CXX":
            if i + 1 >= len(sys.argv):
                err("It is necessary to specify the specific instrumentation module")
            if sys.argv[i+1].find("afl-clang-fast++"):
                CXX_module += sys.argv[i+1]
            elif sys.argv[i+1] == "afl-clang++":
                CXX_module += sys.argv[i+1]
            elif sys.argv[i+1] == "afl-c++":
                CXX_module += sys.argv[i+1]
            else:
                err("invalid argument")
            i += 2
            continue
        
        elif sys.argv[i] == "-source_code":
            source_code += sys.argv[i+1]
            i+=1
            continue

        elif sys.argv[i] == "-fuzz_time":
            if i + 1 >= len(sys.argv):
                err("not find fuzz_time!")
            fuzz_time += sys.argv[i+1]
            i += 1
            continue

        elif sys.argv[i] == "-fuzz_target":
            if i + 1 >= len(sys.argv):
                err("not find fuzz_target!")
            while sys.argv[i+1][:1] != '-':
                fuzz_targets.append(sys.argv[i+1])
                print(fuzz_targets)
                i += 1
                if i+1 >= len(sys.argv):
                    break

        elif sys.argv[i] == "-compile_setting":
            if i + 1 >= len(sys.argv):
                err("not find compile_setting(configure or cmake)")
            compile_setting += sys.argv[i+1]
            i += 1
            continue

        elif sys.argv[i] == "-download_directory":
            if i + 1 >= len(sys.argv):
                err("not find download_directory")
            download_directory += sys.argv[i+1]
        
        elif sys.argv[i] == "-file":
            if i + 1 >= len(sys.argv):
                err("not find file_name")
            file_name += sys.argv[i+1]
        i += 1

    # check download directory
    if download_directory == "":
        err("It is necessary to specify download_directory!")
    check_path(download_directory)

    # entry download directory
    os.chdir(download_directory)
    install_path += download_directory + "/install/"

    # set default parameters
    if (CC_module == ""):
        output_info("try to use default setting CC=afl-clang-fast")
        CC_module += os.path.expanduser('~') + "/AFLplusplus/afl-clang-fast"
        # CC_module += "afl-clang-fast"
    
    if (CXX_module == ""):
        output_info("try to use default setting CXX=afl-clang-fast++")
        CXX_module += os.path.expanduser('~') + "/AFLplusplus/afl-clang-fast++"
        # CXX_module += "afl-clang-fast++"

    if compile_setting == "cmake":
        compile_cmake_handle()
    elif compile_setting == "configure":
        compile_configure_handle()
    else:
        err("It's necessary to specify compile_setting option(cmake or configure)")

def set_C_CXX_env():
    global edit_params
    global CXX_module
    global CC_module
    # edit_params.append("CC=" + CC_module)
    # edit_params.append("CXX=" + CXX_module)
    os.environ['CC'] = CC_module
    os.environ['CXX'] = CXX_module

def compile_configure_handle():
    global edit_params
    global install_path
    # setting edit_params
    edit_params.append('bash')
    edit_params.append('./configure')
    set_C_CXX_env()
    edit_params.append("--prefix=" + install_path + "" )   

def compile_cmake_handle():
    global edit_params
    global install_path
    global download_directory
    global file_name
    set_C_CXX_env()
    edit_params.append('cmake')
    edit_params.append('-D')
    edit_params.append('CMAKE_BUILD_TYPE=Debug')
    edit_params.append(download_directory + '/' + file_name)
    edit_params.append('-DCMAKE_INSTALL_PREFIX=' + install_path)
    edit_params.append("-DCMAKE_C_FLAGS=-fsanitize=address -g")
    edit_params.append("-DCMAKE_CXX_FLAGS=-fsanitize=address -g")
    edit_params.append("-DCMAKE_C_COMPILER=afl-clang-fast")
    edit_params.append("-DCMAKE_CXX_COMPILER=afl-clang-fast++")


def compile_target_with_afl():
    global file_name
    global edit_params
    # switch working dir
    print(os.getcwd())
    os.chdir(os.getcwd() + "/" + file_name)
    # perform instrution automatically
    try:
        if os.path.isdir("install"):
            return 0;
        result = subprocess.run(edit_params, capture_output=True, text=True, check=True)
        output_info("configure success!")
        # result = subprocess.run(['make'], capture_output=True, text=True, check=True)
        subprocess.run(['make'], check=True)
        output_info("make success!")
        subprocess.run(['make', 'install'], capture_output=True, text=True, check=True)
        output_info("make install success!")
        current_directory = os.getcwd() 
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        os.chdir(parent_directory)

    except subprocess.CalledProcessError as e:
        print('return code:', e.returncode)
        print('mistake reason', e.stderr)
        err("fail to make, please check reason")

def construct_fuzzer_args(fuzzing_elf_target_path, task_id):
    global install_path
    fuzzer_args = []
    fuzzer_args.append('python3')
    fuzzer_args.append('../start_fuzz.py')
    fuzzer_args.append(fuzzing_elf_target_path)
    fuzzer_args.append(fuzz_time)
    fuzzer_args.append(task_id)
    fuzzer_args.append(source_code)
    return fuzzer_args

def process_fuzz(fuzzer_args):
    fuzz_target_name = fuzzer_args[1].rsplit('/', 1)[-1]
    """child process tast"""
    print(f'Fuzzing worker {fuzz_target_name} started...')
    try:
        result = subprocess.run(fuzzer_args)
    except subprocess.CalledProcessError as e:
        err("Fail to open mulprocess to fuzz")
        err(f"Fail to open multiprocess to fuzz: {e}")
        err(f"Command: {e.cmd}")
        err(f"Return code: {e.returncode}")
        err(f"Error output: {e.stderr}")
    print(f'Fuzzing worker {fuzz_target_name} finished...')

def run_mul_fuzz():
    global fuzz_targets
    # handle mul_fuzz_args args
    mul_fuzz_args = []
    i = 0
    while i < len(fuzz_targets):
        fuzzing_elf_target_path = install_path + "bin/" + fuzz_targets[i]
        mul_fuzz_args.append(construct_fuzzer_args(fuzzing_elf_target_path, str(i)))
        i += 1

    # fuzz targets with multiple process
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(process_fuzz, mul_fuzz_args)
    print(f'Results: {results}')

def main():
    global CC_module
    global CXX_module
    global edit_params
    global install_path
    global fuzzer_args
    global fuzz_targets
    global download_directory
    global file_name
    set_env()

    # print all args
    print("All arguments:", sys.argv)
    
    # print script name
    script_name = sys.argv[0]
    print("Script name:", script_name)
    
    # handle compiler args
    compile_args_handle()

    # compile source code with afl
    output_info("default intall path is:" + install_path)
    compile_target_with_afl()

    # create multiple process begin to fuzz
    run_mul_fuzz()

if __name__ == "__main__":
    main()
