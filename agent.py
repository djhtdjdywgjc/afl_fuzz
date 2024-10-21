# -*- coding:utf-8 -*-
import os
import sys
import json
import subprocess
import zipfile

download_url = ""
source_code_path = ""
program_name = ""

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

def read_json(file_path):
    # open & read json file
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    return data

def print_json(data, indent=0):
    # print json data recursively
    for key, value in data.items():
        print(' ' * indent + str(key) + ':', end=' ')
        if isinstance(value, dict):
            print()
            print_json(value, indent + 2)
        elif isinstance(value, list):
            print()
            for item in value:
                if isinstance(item, dict):
                    print_json(item, indent + 2)
                else:
                    print(' ' * (indent + 2) + str(item))
        else:
            print(str(value))

def get_json_value(data, key_info):
    for key, value in data.items():
        if key == key_info:
            return value

def load_code_from_url(url, download_directory):
    # create a download_dir
    compress_file_name = url.rsplit('/', 1)[-1]
    filename = compress_file_name.rsplit('.', 2)[0]

    if os.path.isdir(download_directory):
        return filename

    print("-----------")
    os.makedirs(download_directory)
    
    # entry download_directory
    os.chdir(download_directory)

    try:
        # Determine if URL is for Git or wget
        if url.endswith('.git'):
            # Clone git repository
            git_command = ["git", "clone", url]
            result = subprocess.run(git_command, capture_output=True, text=True, check=True)
            output_info("Cloned git repository successfully...")
        else:
            # wget file
            wget_command = ["wget", url, "-O", compress_file_name]
            result = subprocess.run(wget_command, capture_output=True, text=True, check=True)
            output_info("wget code successfully...")

            # uncompress file if it's a tar.gz file
            if compress_file_name.endswith('.tar.gz') or compress_file_name.endswith('.tgz'):
                extract_command = ["tar", "-xvzf", compress_file_name]
                result = subprocess.run(extract_command, capture_output=True, text=True, check=True)
                output_info("uncompressed " + compress_file_name + " successfully...")
            # Add more checks if necessary for other file types
        
    except subprocess.CalledProcessError as e:
        print('Return code:', e.returncode)
        print('Mistake reason:', e.stderr)
        err("Failed to download file from url")

    os.chdir('..')

    return filename

def unzip_file(zip_path, extract_to):
    os.makedirs(extract_to)
    print("zip_path: " + zip_path)
    print("extract_to: " + extract_to)
    # split url to get name info 
    compress_file_name = zip_path.rsplit('/', 1)[-1]
    filename = compress_file_name.rsplit('.', 1)[0]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    output_info(f"File has been extracted to {extract_to}")
    print("ddddd -> ",extract_to)
    print("aaaaa -> ",filename)
    return filename

def afl_args_handle():
    global json_data
    afl_fuzz_args = get_json_value(json_data, "afl_fuzz_args")
    task_id = get_json_value(afl_fuzz_args, "task_id")
    default_compiler = get_json_value(afl_fuzz_args, "Default_compiler")
    fuzzer = get_json_value(afl_fuzz_args, "fuzzer")
    fuzz_time = get_json_value(afl_fuzz_args, "fuzz_time")
    fuzz_target = get_json_value(afl_fuzz_args, "fuzz_target")
    CC_module = get_json_value(afl_fuzz_args, "CC_module")
    CXX_module = get_json_value(afl_fuzz_args, "CXX_module")
    compile_setting = get_json_value(default_compiler, "compile_setting")
    for key, value in afl_fuzz_args.items():
        print(str(key) + ":" + str(value))
    json_args = []
    json_args.append( "-fuzz_time")
    json_args.append(str(fuzz_time))
    json_args.append( "-fuzz_target")
    for value in fuzz_target:
        json_args.append(str(value))
    json_args.append("-source_code")
    json_args.append(source_code)
    json_args.append( "-compile_setting")
    json_args.append(compile_setting)
    return json_args


def main():
    global download_url
    global source_code_path
    global program_name
    global json_data
    global source_code
    # get url info from json
    if len(sys.argv) < 2:
        print("[*] The agent requires a parameter that specifies the path to the JSON file.")
        print("[*] Usage: agent.py data.json")
        err("exit")
    
    # check json format 
    try:
        json_data = read_json(sys.argv[1])
    except FileNotFoundError:
        err("Fail to find json file, plz check path")
    print("="*20 + sys.argv[1] + "="*20)
    print_json(json_data)
    print("="*(40 + len(sys.argv[1])))

    # traverse json_data to get key & value pairs
    download_url = get_json_value(json_data, "url")
    source_code_path = get_json_value(json_data, "source_code_path")
    source_code = get_json_value(json_data,"source_code")

    if download_url == "" and source_code_path == "":
        err("The agent require source code url or file")

    # create a dir for fuzzing program
    program_name = get_json_value(json_data, "program_name")
    if program_name == "":
        err("The agent requires a program name to store source code")
    download_directory = os.getcwd() + "/" + program_name

    # download source code from url
    file_name = ""
    if download_url != "":
        file_name += load_code_from_url(download_url, download_directory)

    # unzip source.zip if url not exist
    if source_code_path != "":
        print(download_directory)
        file_name += unzip_file(source_code_path, download_directory)

    # extract fuzz settings from data.json and transfer to demo.py
    json_args = afl_args_handle()

    # call demop.py
    demo_args = ['python3', 'demo.py']
    demo_args.extend(json_args)
    demo_args.append('-download_directory')
    demo_args.append(download_directory)
    demo_args.append('-file')
    demo_args.append(file_name)
    # print(demo_args)
    subprocess.run(demo_args, check=True)

if __name__ == '__main__':
    main()



