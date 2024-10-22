import os
import sys
import shutil
import subprocess
import signal
import json
import time

# 检查是否提供了fuzz的二进制文件路径作为参数
if len(sys.argv) < 3:
    print("Usage: python script.py <path_to_fuzz_binary> <No set time> [task_id]")
    sys.exit(1)

afl = "afl-fuzz"
input_dir = "../input"
fuzz_binary = sys.argv[1]
binary_name = os.path.basename(fuzz_binary)  # 提取二进制文件名，不包括路径
run_time = sys.argv[2]
source_code = sys.argv[4]
task_id = sys.argv[3] if len(sys.argv) > 3 else ""
output_dir = f"../{task_id}output_{binary_name}"  # 根据二进制文件名生成输出目录名

# 删除旧的输出目录并创建新的输出目录
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# 运行 afl-fuzz
def run_afl_fuzz():
    global afl_process
    if source_code == "":
        afl_process = subprocess.Popen(
            ["timeout", run_time, afl, "-i", input_dir, "-o", output_dir, "-s", "123", "-m", "none", "--", fuzz_binary, "@@"],
            preexec_fn=os.setsid
        )
    else:
        print(source_code)
        source_code_list = source_code.split()
        afl_process = subprocess.Popen(
            ["timeout", run_time, afl, "-i", input_dir, "-o", output_dir, "-s", "123", "-m", "none", "--",fuzz_binary] +  source_code_list + ["@@"],
            preexec_fn=os.setsid
        )


def signal_handler(signum, frame):
    print("Stopping afl-fuzz...")
    if afl_process:
        os.killpg(os.getpgid(afl_process.pid), signal.SIGTERM)  # 发送 SIGTERM 到 afl-fuzz 进程组
        afl_process.wait()
    print("afl-fuzz stopped")

signal.signal(signal.SIGINT, signal_handler)  # 捕获 Ctrl+C 信号

# 开始运行 afl-fuzz
run_afl_fuzz()

# 等待 afl-fuzz 进程结束
try:
    while afl_process.poll() is None:
        time.sleep(1)
except KeyboardInterrupt:
    # 在捕获到 KeyboardInterrupt 时仅停止 afl-fuzz，而不是退出程序
    signal_handler(signal.SIGINT, None)

stats_file = os.path.join(output_dir, "default", "fuzzer_stats")

# 后续代码继续执行

# 提取 fuzzer stats 数据
def extract_fuzzer_stats(stats_file):
    stats_data = {}
    with open(stats_file, "r") as f:
        for line in f:
            if line.startswith("bitmap_cvg"):
                key, value = line.strip().split(": ")
                stats_data[key.strip()] = value.strip()
                return stats_data
    return None

fuzzer_stats = extract_fuzzer_stats(stats_file)

# 路径配置
crash_dir = os.path.join(output_dir, "default", "crashes")
output_analysis_dir = os.path.dirname(os.getcwd())+f"/crash_analysis_{binary_name}"
heap_overflow_dir = os.path.join(output_analysis_dir, "heap_overflow")
stack_overflow_dir = os.path.join(output_analysis_dir, "stack_overflow")
uaf_dir = os.path.join(output_analysis_dir, "use_after_free")
segv_dir = os.path.join(output_analysis_dir, "segmentation_fault")
oom_dir = os.path.join(output_analysis_dir, "out_of_memory")
double_free_dir = os.path.join(output_analysis_dir, "double_free")
memory_leak_dir = os.path.join(output_analysis_dir, "memory_leak")
integer_overflow_dir = os.path.join(output_analysis_dir, "integer_overflow")
format_string_dir = os.path.join(output_analysis_dir, "format_string_bug")
null_dereference_dir = os.path.join(output_analysis_dir, "null_dereference")
out_of_bounds_dir = os.path.join(output_analysis_dir, "out_of_bounds")
type_confusion_dir = os.path.join(output_analysis_dir, "type_confusion")
recursive_call_dir = os.path.join(output_analysis_dir, "recursive_call")
other_dir = os.path.join(output_analysis_dir, "other")


os.makedirs(heap_overflow_dir, exist_ok=True)
os.makedirs(stack_overflow_dir, exist_ok=True)
os.makedirs(uaf_dir, exist_ok=True)
os.makedirs(segv_dir, exist_ok=True)
os.makedirs(oom_dir, exist_ok=True)
os.makedirs(double_free_dir, exist_ok=True)
os.makedirs(memory_leak_dir, exist_ok=True)
os.makedirs(integer_overflow_dir, exist_ok=True)
os.makedirs(format_string_dir, exist_ok=True)
os.makedirs(null_dereference_dir, exist_ok=True)
os.makedirs(out_of_bounds_dir, exist_ok=True)
os.makedirs(type_confusion_dir, exist_ok=True)
os.makedirs(recursive_call_dir, exist_ok=True)
os.makedirs(other_dir, exist_ok=True)

TIMEOUT = 10
stack_traces = []
bug_occurrences = {}

# def classify_bug_type(asan_output_file):
#     with open(asan_output_file, 'r') as f:
#         asan_output = f.read()
    
#     summary_line = next((line for line in asan_output.splitlines() if "SUMMARY:" in line), None)
#     if summary_line:
#         bug_type = summary_line.split()[1]
#         return bug_type
#     return "other"

def classify_crash(crash_file):
    asan_output_file = os.path.join(output_analysis_dir, f"asan_output_{os.path.basename(crash_file)}.txt")
    
    with open(asan_output_file, "rb") as f:
        asan_output = f.read()

    asan_output = asan_output.decode(errors='ignore')
    
    if "heap-buffer-overflow" in asan_output:
        shutil.copy(crash_file, os.path.join(heap_overflow_dir, os.path.basename(crash_file)))
        return "heap-buffer-overflow"
    elif "stack-buffer-overflow" in asan_output:
        shutil.copy(crash_file, os.path.join(stack_overflow_dir, os.path.basename(crash_file)))
        return "stack-buffer-overflow"
    elif "use-after-free" in asan_output:
        shutil.copy(crash_file, os.path.join(uaf_dir, os.path.basename(crash_file)))
        return "use-after-free"
    elif "SEGV" in asan_output or "invalid memory access" in asan_output:
        shutil.copy(crash_file, os.path.join(segv_dir, os.path.basename(crash_file)))
        return "segmentation_fault"
    elif "out-of-memory" in asan_output:
        shutil.copy(crash_file, os.path.join(oom_dir, os.path.basename(crash_file)))
        return "out-of-memory"
    elif "double-free" in asan_output:
        shutil.copy(crash_file, os.path.join(double_free_dir, os.path.basename(crash_file)))
        return "double-free"
    elif "memory-leaks" in asan_output:
        shutil.copy(crash_file, os.path.join(memory_leak_dir, os.path.basename(crash_file)))
        return "memory-leak"
    elif "integer-overflow" in asan_output:
        shutil.copy(crash_file, os.path.join(integer_overflow_dir, os.path.basename(crash_file)))
        return "integer-overflow"
    elif "format-string" in asan_output:
        shutil.copy(crash_file, os.path.join(format_string_dir, os.path.basename(crash_file)))
        return "format-string-bug"
    elif "null dereference" in asan_output:
        shutil.copy(crash_file, os.path.join(null_dereference_dir, os.path.basename(crash_file)))
        return "null-dereference"
    elif "out-of-bounds" in asan_output:
        shutil.copy(crash_file, os.path.join(out_of_bounds_dir, os.path.basename(crash_file)))
        return "out-of-bounds"
    elif "type-confusion" in asan_output:
        shutil.copy(crash_file, os.path.join(type_confusion_dir, os.path.basename(crash_file)))
        return "type-confusion"
    elif "stack-overflow" in asan_output:
        shutil.copy(crash_file, os.path.join(stack_overflow_dir, os.path.basename(crash_file)))
        return "stack-overflow"
    else:
        # 其他未知的bug类型处理
        # bug_type = classify_bug_type(asan_output_file)
        # shutil.copy(crash_file, os.path.join(other_dir, os.path.basename(crash_file)))
        # return bug_type
        return "other"

def deduplicate_crash(crash_file):
    asan_output_file = os.path.join(output_analysis_dir, f"asan_output_{os.path.basename(crash_file)}.txt")
    try:
        asan_output = subprocess.check_output([fuzz_binary, crash_file], stderr=subprocess.STDOUT, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        asan_output = b'Timeout'
    except subprocess.CalledProcessError as e:
        asan_output = e.output

    with open(asan_output_file, "wb") as f:
        f.write(asan_output)

    asan_output = asan_output.decode(errors='ignore')

    stack_trace = tuple([line.strip() for line in asan_output.splitlines() if line.strip().startswith("SUMMARY: ")])
    stack_trace_str = "\n".join(stack_trace)

    if stack_trace_str in stack_traces:
        if crash_file not in bug_occurrences:
            bug_occurrences[crash_file] = {}
        bug_occurrences[crash_file][stack_trace_str] = bug_occurrences[crash_file].get(stack_trace_str, 0) + 1
        return False
    else:
        stack_traces.append(stack_trace_str)
        if crash_file not in bug_occurrences:
            bug_occurrences[crash_file] = {}
        bug_occurrences[crash_file][stack_trace_str] = 1

    return True


classification_summary = {
    "heap_overflow": 0,
    "stack_overflow": 0,
    "use_after_free": 0,
    "segmentation_fault": 0,
    "out_of_memory": 0,
    "double_free": 0,
    "memory_leak": 0,
    "integer_overflow": 0,
    "format_string_bug": 0,
    "null_dereference": 0,
    "out_of_bounds": 0,
    "type_confusion": 0,
    "other": 0,
    "recursive_call": 0
}

bugs_found = []

if len(os.listdir(crash_dir)) == 0:
    fuzzing_task_count = 0
else:
    fuzzing_task_count = len(os.listdir(crash_dir)) - 1

for crash_file in os.listdir(crash_dir):
    if crash_file.rsplit('.', 1)[0] == "README":
        continue
    total_discovery_count = 0
    risk_level = ""
    bug_description = ""
    fix_recommendation = ""  # 修复建议
    crash_file_path = os.path.join(crash_dir, crash_file)
    if os.path.isfile(crash_file_path):
        if deduplicate_crash(crash_file_path):
            category = classify_crash(crash_file_path)
            if category == "heap-buffer-overflow":
                classification_summary["heap_overflow"] += 1
            elif category == "stack-buffer-overflow":
                classification_summary["stack_overflow"] += 1
            elif category == "use-after-free":
                classification_summary["use_after_free"] += 1
            elif category == "segmentation_fault":
                classification_summary["segmentation_fault"] += 1
            elif category == "out-of-memory":
                classification_summary["out_of_memory"] += 1
            elif category == "double-free":
                classification_summary["double_free"] += 1
            elif category == "memory-leak":
                classification_summary["memory_leak"] += 1
            elif category == "integer-overflow":
                classification_summary["integer_overflow"] += 1
            elif category == "format-string-bug":
                classification_summary["format_string_bug"] += 1
            elif category == "null-dereference":
                classification_summary["null_dereference"] += 1
            elif category == "out-of-bounds":
                classification_summary["out_of_bounds"] += 1
            elif category == "type-confusion":
                classification_summary["type_confusion"] += 1
            else:
                classification_summary["other"] += 1

            # 根据漏洞分类设置风险等级、描述和修复建议
            if category == "heap-buffer-overflow" or category == "stack-buffer-overflow":
                risk_level = "高"
                bug_description = "向预期输入缓冲区的边界之外读入或写入数据"
                fix_recommendation = "确保对缓冲区的访问操作不会超过其边界，建议使用安全的库函数如 `strncpy`, `memcpy_s` 或者增加边界检查。"
            elif category == "use-after-free" or category == "UAF":
                risk_level = "中"
                bug_description = "程序尝试使用已经释放后的堆块"
                fix_recommendation = "避免在释放内存后继续访问，确保释放后指针被置为 `NULL`，并在重新分配内存时正确更新指针。"
            elif category == "SEGV on unknown address" or category == "invalid memory access":
                risk_level = "中"
                bug_description = "程序访问了无效或未分配的内存地址，导致段错误"
                fix_recommendation = "检查指针是否为 `NULL` 或是否指向有效的内存地址，确保所有指针在使用前都被正确初始化。"
            elif category == "out-of-memory" or category == "failed to allocate":
                risk_level = "中"
                bug_description = "程序无法分配足够的内存，导致崩溃"
                fix_recommendation = "优化内存使用，避免大规模内存分配；同时检查系统内存资源，并处理分配失败的情况。"
            elif category == "double-free":
                risk_level = "高"
                bug_description = "程序对同一内存块进行了两次释放，导致未定义行为"
                fix_recommendation = "确保每个内存块只被释放一次，使用智能指针或增加标志位来避免重复释放。"
            elif category == "memory-leaks" or category == "leaked memory":
                risk_level = "中"
                bug_description = "程序在使用后没有释放动态分配的内存，导致内存泄漏"
                fix_recommendation = "使用内存泄漏检测工具如 `valgrind` 或 `ASAN` 来检查并确保所有动态分配的内存都能被正确释放。"
            elif category == "integer-overflow" or category == "signed-integer-overflow":
                risk_level = "中"
                bug_description = "整数操作超出其表示范围，可能导致未定义行为"
                fix_recommendation = "检查所有整数运算是否超出范围，使用库函数进行边界检查并避免未定义行为。"
            elif category == "format-string-bug" or category == "format overflow":
                risk_level = "高"
                bug_description = "格式化字符串漏洞可能导致任意代码执行"
                fix_recommendation = "避免使用不受控的格式字符串，确保输入的格式化字符串安全且经过校验，推荐使用 `snprintf` 等安全函数。"
            elif category == "null-dereference" or category == "null-pointer-access":
                risk_level = "中"
                bug_description = "程序试图解引用空指针，导致崩溃"
                fix_recommendation = "在使用指针之前检查其是否为 `NULL`，确保在解引用之前指针指向有效内存。"
            elif category == "out-of-bounds" or category == "oob-read" or category == "oob-write":
                risk_level = "高"
                bug_description = "程序尝试访问数组或缓冲区边界之外的内存"
                fix_recommendation = "确保对数组和缓冲区的访问在有效范围内，使用边界检查或安全的数组访问函数。"
            elif category == "type-confusion" or category == "bad-cast":
                risk_level = "中"
                bug_description = "类型混淆可能导致未定义行为或内存损坏"
                fix_recommendation = "在进行类型转换时，确保目标类型与原类型兼容，避免强制转换，使用 `dynamic_cast` 等安全的类型转换方法。"
            else:
                risk_level = "中"
                bug_description = "未知"
                fix_recommendation = "请查看 ASAN 输出或进行进一步分析。"

            # 读取 ASAN 输出文件
            asan_output_file = os.path.join(output_analysis_dir, f"asan_output_{os.path.basename(crash_file)}.txt")
            with open(asan_output_file, "r") as f:
                asn_output = f.read()

            # 从 ASAN 报告中提取 summary 行信息
            summary_line = next((line for line in asn_output.splitlines() if "SUMMARY:" in line), None)
            path = summary_line.rsplit(' ', 3)[1]
            code_path = path.rsplit(":", 2)[0]
            code_line = path.rsplit(":", 2)[1]

            f.close()

            # 提取代码片段
            code_all = ""
            if code_path[0] == "/":
                with open(code_path, 'r') as f:
                    for i in range(int(code_line) + 6):
                        code = str(i+1) + '  ' + f.readline()
                        if i > int(code_line) - 5:
                            code_all += code
            else:
                code_all = "未知，请自行打开 ASAN 文件查看"

            if category == "heap-buffer-overflow":
                category = "heap_overflow"
            elif category == "stack-buffer-overflow":
                category = "stack_overflow"

            # 将漏洞信息记录到 bug 列表中
            bug = {
                "bug_id": f"{category[:3]}_{classification_summary[category]:03}",
                "bug_type": category,
                "risk_level": risk_level,
                "bug_description": bug_description,
                "fix_recommendation": fix_recommendation,  # 添加修复建议
                "first_discovery_time": time.ctime(os.path.getctime(crash_file_path)),
                "total_discovery_count": 0,  # 使用 bug_occurrences 记录次数
                "risk_code_display_file": code_all,
                "asan_report_file": asn_output,
                "crash_file_path": crash_file_path,
                "high_light" : code_line
            }
            bugs_found.append(bug)


# 重新遍历分类好的文件夹并更新 `total_discovery_count`
for category, dir_path in {
    "heap_overflow": heap_overflow_dir,
    "stack_overflow": stack_overflow_dir,
    "recursive_call": recursive_call_dir,
    "other": other_dir
}.items():
    for crash_file in os.listdir(dir_path):
        crash_file_path = os.path.join(dir_path, crash_file)
        if crash_file_path in bug_occurrences:
            for bug in bugs_found:
                if bug["crash_file_path"] == crash_file_path:
                    bug["total_discovery_count"] = bug_occurrences[crash_file_path]

for i in bugs_found:
    crash_file_path = i['crash_file_path']
    total_discovery_count = 0

    for j in bug_occurrences.values():
        if bug_occurrences[crash_file_path].keys() == j.keys():
            total_discovery_count += 1
    i['total_discovery_count'] = total_discovery_count

for i in bugs_found:
    i['crash_file_path'] = os.path.dirname(os.getcwd())+'/'+(i['crash_file_path']).rsplit('../',1)[1]

# 生成 JSON 报告
report = {
    "code_path": os.getcwd(),
    "code_coverage": fuzzer_stats,
    "fuzzing_task_count": len(os.listdir(os.path.dirname(fuzz_binary))),
    "total_bugs_found": fuzzing_task_count,
    "bugs_found": bugs_found
}

report_file = os.path.join(os.path.dirname(os.getcwd()), binary_name+"_report.json")
with open(report_file, "w") as f:
    json.dump(report, f, indent=4, ensure_ascii=False)