import os
import sys
import json
import subprocess

program_name = ""
url = ""
source_code_path = ""
compress_file_name = ""

def err(message):
    print(f"Error: {message}")
    sys.exit(1) 

def output_info(info):
    print("[*] " + info)

def parse_json_and_execute(file_path):
    global program_name
    global url
    global source_code_path
    # 读取并解析 JSON 文件
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            
            # 提取 JSON 数据到变量
            program_name = data.get("program_name", "")
            url = data.get("url", "")
            source_code_path = data.get("source_code_path", "")
            
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the JSON format.")
        return
    
    # 调用其他 Python 文件
    # try:
    #     subprocess.run(["python3", "other_script.py"], check=True)
    # except subprocess.CalledProcessError as e:
    #     print(f"Error executing other_script.py: {e}")
    
# 运行函数并指定 JSON 文件路径

def down_code():
    global compress_file_name

    if program_name == "":
        print("Don't have project name!!!")
        sys.exit(1)

    if os.path.isdir(os.path.join(os.getcwd(),program_name)):
        os.chdir(program_name)
    else:
        os.mkdir(program_name)
        os.chdir(program_name)


    compress_file_name = url.rsplit('/', 1)[-1]

    path = os.getcwd()

    if os.path.isfile(os.path.join(path,compress_file_name)):
        os.chdir('..')
        return 
   

    if url != "":
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
            
        except subprocess.CalledProcessError as e:
            print('Return code:', e.returncode)
            print('Mistake reason:', e.stderr)
            err("Failed to download file from url")

    elif source_code_path != "":
        try:
            git_command = ["mv", source_code_path, "./"]
            result = subprocess.run(git_command, capture_output=True, text=True, check=True)
            print("file mv successfully...")
            
        except subprocess.CalledProcessError as e:
            print('Return code:', e.returncode)
            print('Mistake reason:', e.stderr)
            err("Failed to download file from url")

    else:
        print("Please input your url or code!!!")
        sys.exit(1)

    os.chdir('..')

# def run_weggli():

def main():
    if len(sys.argv) < 2:
        print("[*] The agent requires a parameter that specifies the path to the JSON file.")
        print(f"[*] Usage: {sys.argv[0]} data.json")
        sys.exit(1)

    a = sys.argv[1]

    parse_json_and_execute(a)

        # 打印变量内容以确认
    print(f"Program Name: {program_name}")
    print(f"URL: {url}")
    print(f"Source Code Path: {source_code_path}")

    down_code()

    code = ['python3','weggli.py']
    code.append(program_name)
    subprocess.run(code,check=True)


if __name__ == '__main__':
    main()
