import os
import subprocess
import sys
import yaml
from termcolor import colored
import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 配置
API_ENDPOINT = "https://api.siliconflow.cn/v1"  # 替换为您的 API 端点
API_KEY = os.getenv("OPENAI_API_KEY")  # Load API key from environment variable
if not API_KEY:
    print(colored("[ERROR] OPENAI_API_KEY not found in .env file", "red"))
    sys.exit(1)

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
ARRANGE_STYLE_FILE = os.path.expanduser("~/.arrangestyle")

# 文件类型映射
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.csv'],
    'Archives': ['.zip', '.tar.gz', '.tar', '.rar', '.7z', '.bz2', '.dmg', '.iso'],
    'Installers': ['.exe', '.msi', '.pkg', '.deb', '.rpm'],
    'Development': ['.py', '.js', '.java', '.cpp', '.h', '.json', '.tfstate', '.xml'],
    'Media': ['.mp4', '.mkv', '.avi', '.mov', '.mp3', '.wav'],
    'Config': ['.pem', '.crt', '.key', '.keystore', '.rdp', '.ovpn'],
    'Android': ['.apk'],
}

# 初始化OpenAI客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=API_ENDPOINT
)

# 初始化样式文件
def initialize_style_file():
    """如果样式文件不存在，则创建默认样式文件"""
    if not os.path.exists(ARRANGE_STYLE_FILE):
        default_style = {
            "LLM Style": [
                "Images: .jpg, .png, .gif",
                "Documents: .pdf, .docx, .txt"
            ],
            "User Style": [
                "Projects: project_*",
                "Videos: .mp4, .avi"
            ]
        }
        with open(ARRANGE_STYLE_FILE, 'w') as f:
            yaml.dump(default_style, f)

# 读取样式文件
def read_style_file():
    """读取并返回样式文件内容"""
    with open(ARRANGE_STYLE_FILE, 'r') as f:
        return yaml.safe_load(f)

# 更新 LLM 样式
def update_llm_style(new_llm_style):
    """更新 LLM 样式部分并保存"""
    style = read_style_file()
    style["LLM Style"] = new_llm_style
    with open(ARRANGE_STYLE_FILE, 'w') as f:
        yaml.dump(style, f)

# 获取 Downloads 目录内容
def get_downloads_contents():
    """获取 Downloads 目录中的文件和目录列表，排除隐藏文件"""
    try:
        contents = os.listdir(DOWNLOADS_DIR)
        return [item for item in contents if not item.startswith('.')]
    except Exception as e:
        print(colored(f"[ERROR] 无法读取Downloads目录: {e}", "red"))
        sys.exit(1)

# 发送请求到 LLM
def send_to_llm(contents, style):
    """将目录内容和样式发送到 LLM，获取整理命令"""
    system_prompt = (
        "你是一位专业的文件整理专家，擅长从多个维度分析和组织文件。在整理文件时，你会："
        "\n1. 分析文件名规律：寻找文件名中的共同模式、日期、项目名等信息"
        "\n2. 识别项目关联：判断文件是否属于同一个项目或主题"
        "\n3. 理解使用场景：推测文件的使用场景（如学习资料、工作项目、娱乐内容等）"
        "\n4. 考虑文件类型：不仅按扩展名分类，更注重文件的实际用途"
        "\n5. 使用合理的中文目录名：选择清晰、具体且符合中文使用习惯的目录名"
        "\n\n在创建目录时，优先考虑以下命名方式："
        "\n- 项目类：'项目-项目名称'，如 '项目-网站设计'"
        "\n- 学习类：'学习-主题'，如 '学习-Python'"
        "\n- 工作类：'工作-类别'，如 '工作-会议记录'"
        "\n- 娱乐类：'娱乐-类别'，如 '娱乐-电影'"
        "\n- 临时文件：'临时文件-日期'"
        "\n\n你只能使用以下命令格式："
        "\n1. mkdir命令格式：mkdir -p '目录名'"
        "\n2. mv命令格式：mv '源文件' '目标目录'"
        "\n\n请参考以下用户定义的整理风格：\n"
        f"{style}"
    )

    user_prompt = (
        "这是当前下载文件夹中的文件列表，请帮我整理：\n\n" +
        "\n".join([f"- {item}" for item in contents]) +
        "\n\n请按照以下步骤整理文件："
        "\n1. 先仔细分析文件名，找出可能的关联性"
        "\n2. 创建合适的中文目录（使用 mkdir 命令）"
        "\n3. 将文件移动到对应目录（使用 mv 命令）"
        "\n\n要求："
        "\n1. 每行输出一条命令"
        "\n2. 优先创建所有需要的目录，再移动文件"
        "\n3. 相关文件应该放在同一个目录中"
        "\n4. 目录名要用中文，清晰表达内容类型"
        "\n5. 所有路径都要用单引号包围"
        "\n6. 如果发现文件可能属于同一个项目或主题，请放在同一个目录下"
        "\n7. 如果文件名包含日期，可以考虑按时间组织"
    )

    print(colored("\n[LLM REQUEST] 发送到LLM的请求:", "blue"))
    print(colored("系统提示词:", "blue"))
    print(system_prompt)
    print(colored("\n用户提示词:", "blue"))
    print(user_prompt)
    print(colored("\nAPI端点:", "blue"))
    print(API_ENDPOINT)

    try:
        print(colored("\n[LLM] 正在发送请求...", "blue"))

        # Initialize virtual filesystem for simulation
        fs = build_virtual_fs(DOWNLOADS_DIR)
        print(colored("\n[初始状态] 当前文件结构:", "green"))
        print_tree(fs)

        # Initialize streaming response
        response_stream = client.chat.completions.create(
            model="Pro/deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            timeout=600,  # 10 minutes timeout
            stream=True  # Enable streaming
        )

        print(colored("\n[LLM RESPONSE] LLM返回的响应和实时模拟:", "blue"))

        # Process the streaming response
        full_response = []
        current_line = []
        command_buffer = ""

        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)  # Print content in real-time

                # Process content character by character
                for char in content:
                    if char == '\n':
                        # When we hit a newline, process the completed line
                        if current_line:
                            completed_line = ''.join(current_line)
                            command_buffer = completed_line.strip()

                            # Process the command if it's valid
                            if command_buffer:
                                if validate_command(command_buffer):
                                    print(colored(f"\n[模拟] 执行命令: {command_buffer}", "yellow"))

                                    # Simulate the command
                                    if command_buffer.startswith('mkdir'):
                                        dirname = command_buffer.split("'")[1]
                                        simulate_mkdir(fs, dirname)
                                    elif command_buffer.startswith('mv'):
                                        parts = command_buffer.split("'")
                                        src = parts[1]
                                        dst = parts[3]
                                        simulate_mv(fs, src, dst)

                                    # Show the updated structure
                                    print(colored("\n当前文件结构:", "green"))
                                    print_tree(fs)
                                    print()  # Add a blank line for readability
                                else:
                                    print(colored(f"\n[警告] 跳过无效命令: {command_buffer}", "red"))

                            full_response.append(completed_line)
                            current_line = []
                            command_buffer = ""
                    else:
                        current_line.append(char)

        # Handle any remaining content in the last line
        if current_line:
            completed_line = ''.join(current_line)
            if completed_line.strip():
                full_response.append(completed_line)
                if validate_command(completed_line.strip()):
                    print(colored(f"\n[模拟] 执行最后的命令: {completed_line.strip()}", "yellow"))
                    if completed_line.startswith('mkdir'):
                        dirname = completed_line.split("'")[1]
                        simulate_mkdir(fs, dirname)
                    elif completed_line.startswith('mv'):
                        parts = completed_line.split("'")
                        src = parts[1]
                        dst = parts[3]
                        simulate_mv(fs, src, dst)
                    print(colored("\n最终文件结构:", "green"))
                    print_tree(fs)

        print(colored("\n[完成] 所有命令模拟完成", "green"))
        return '\n'.join(full_response)

    except Exception as e:
        print(colored(f"[错误] API请求失败: {e}", "red"))
        print(colored("错误详情:", "red"))
        print(str(e))
        sys.exit(1)

# 解析命令
def parse_commands(response):
    """从 LLM 响应中解析出命令列表"""
    print(colored("\n[PARSE] 解析LLM响应为命令列表:", "blue"))
    commands = response.strip().split("\n")
    parsed_commands = [cmd.strip() for cmd in commands if cmd.strip()]
    print("\n".join(parsed_commands))
    return parsed_commands

# 验证命令
def validate_command(cmd):
    """验证命令是否有效且安全"""
    if not (cmd.startswith("mkdir -p") or cmd.startswith("mv ")):
        return False

    # Extract the actual paths from the command
    parts = cmd.split("'")
    if cmd.startswith("mkdir -p"):
        if len(parts) != 3:  # Format: mkdir -p 'dir'
            return False
        path = parts[1]
    else:  # mv command
        if len(parts) != 5:  # Format: mv 'source' 'target'
            return False
        path = parts[1]
        target = parts[3]

    # Validate paths
    base_path = DOWNLOADS_DIR + "/"
    for p in [path, target] if cmd.startswith("mv ") else [path]:
        full_path = os.path.realpath(os.path.join(DOWNLOADS_DIR, p))
        if not full_path.startswith(base_path):
            return False
    return True

# 构建虚拟文件系统
def build_virtual_fs(root_dir):
    """根据实际目录构建虚拟文件系统"""
    fs = {}
    try:
        for item in os.listdir(root_dir):
            if not item.startswith('.'):  # Skip hidden files
                if os.path.isdir(os.path.join(root_dir, item)):
                    fs[item] = {}
                else:
                    fs[item] = None
    except Exception as e:
        print(colored(f"[ERROR] 读取目录失败: {e}", "red"))
    return fs

# 模拟 mkdir
def simulate_mkdir(fs, dirname):
    """模拟创建目录"""
    if dirname not in fs:
        fs[dirname] = {}
        print(colored(f"[SIMULATE] 创建目录: {dirname}", "green"))

# 模拟 mv
def simulate_mv(fs, src, dst):
    """模拟移动文件"""
    # Handle paths with spaces and special characters
    src = src.strip()
    dst = dst.strip()

    # Split destination into directory and filename if necessary
    if '/' in dst:
        dst_dir, dst_file = dst.split('/', 1)
    else:
        dst_dir, dst_file = dst, src

    if src not in fs:
        print(colored(f"[ERROR] 源文件 '{src}' 不存在", "red"))
        return

    if dst_dir not in fs:
        print(colored(f"[ERROR] 目标目录 '{dst_dir}' 不存在", "red"))
        return

    # Move the file
    item = fs.pop(src)
    if dst_file in fs[dst_dir]:
        print(colored(f"[WARNING] 目标文件 '{dst_file}' 已存在，将重命名", "yellow"))
        base, ext = os.path.splitext(dst_file)
        counter = 1
        while f"{base}_{counter}{ext}" in fs[dst_dir]:
            counter += 1
        dst_file = f"{base}_{counter}{ext}"

    fs[dst_dir][dst_file] = item
    print(colored(f"[SIMULATE] 移动 '{src}' 到 '{dst_dir}/{dst_file}'", "green"))

# 打印文件树
def print_tree(fs, prefix=''):
    """以树形结构打印虚拟文件系统"""
    items = sorted(fs.items())
    for i, (name, subtree) in enumerate(items):
        is_last = i == len(items) - 1
        print(prefix + ('└── ' if is_last else '├── ') + name)
        if isinstance(subtree, dict):  # If it's a directory
            new_prefix = prefix + ('    ' if is_last else '│   ')
            print_tree(subtree, new_prefix)

# 执行命令
def execute_command(cmd):
    """执行实际的 shell 命令"""
    print(colored(f"[INFO] 执行命令: {cmd}", "green"))
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=DOWNLOADS_DIR)
    except subprocess.CalledProcessError as e:
        print(colored(f"[ERROR] 命令执行失败: {cmd}\n错误: {e}", "red"))

def categorize_file(filename):
    """根据文件名确定其类别"""
    ext = os.path.splitext(filename.lower())[1]
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'Others'

def get_safe_filename(filename, target_dir):
    """生成安全的文件名，避免冲突"""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(target_dir, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

def organize_downloads():
    """智能组织下载文件夹"""
    contents = get_downloads_contents()
    if not contents:
        return []

    commands = []
    categories = set()

    # 首先创建所需的目录
    for file in contents:
        if os.path.isfile(os.path.join(DOWNLOADS_DIR, file)):
            category = categorize_file(file)
            if category not in categories:
                categories.add(category)
                commands.append(f"mkdir -p '{category}'")

    # 然后移动文件
    for file in contents:
        file_path = os.path.join(DOWNLOADS_DIR, file)
        if os.path.isfile(file_path) and not file.startswith('.'):
            category = categorize_file(file)
            safe_filename = get_safe_filename(file, os.path.join(DOWNLOADS_DIR, category))
            if safe_filename != file:
                commands.append(f"mv '{file}' '{category}/{safe_filename}'")
            else:
                commands.append(f"mv '{file}' '{category}'")

    return commands

def simulate_execution(commands):
    """模拟执行命令并返回虚拟文件系统"""
    fs = build_virtual_fs(DOWNLOADS_DIR)

    # First, create all directories
    for cmd in commands:
        if cmd.startswith('mkdir'):
            dirname = cmd.split("'")[1]  # Extract directory name from 'mkdir -p <dirname>'
            simulate_mkdir(fs, dirname)

    # Then, move all files
    for cmd in commands:
        if cmd.startswith('mv'):
            parts = cmd.split("'")
            if len(parts) >= 5:
                src = parts[1]
                dst = parts[3]
                simulate_mv(fs, src, dst)

    return fs

# 主函数
def main():
    """脚本主入口"""
    print(colored("[INFO] 开始整理Downloads文件夹...", "green"))
    print(colored(f"[INFO] 当前时间: {datetime.datetime.now()}", "green"))
    print(colored(f"[INFO] 工作目录: {DOWNLOADS_DIR}", "green"))

    # 初始化样式文件
    initialize_style_file()
    style = read_style_file()
    style_text = yaml.dump(style, default_flow_style=False)

    # 获取目录内容
    contents = get_downloads_contents()
    if not contents:
        print(colored("[INFO] Downloads目录为空，无需整理。", "green"))
        return

    print(colored("\n[INFO] 当前目录内容:", "green"))
    for item in contents:
        print(f"- {item}")

    # 使用LLM整理
    print(colored("[INFO] 正在使用AI分析文件并生成整理方案...", "green"))
    response = send_to_llm(contents, style_text)
    commands = parse_commands(response)

    if not commands:
        print(colored("[INFO] 没有需要整理的文件。", "green"))
        return

    print(colored("\n[INFO] AI生成的整理命令:", "green"))
    for cmd in commands:
        print(f"- {cmd}")

    # 模拟执行
    print(colored("[INFO] 模拟执行开始...", "green"))
    simulated_fs = simulate_execution(commands)
    print(colored("\n模拟执行后的文件结构：", "green"))
    print_tree(simulated_fs)

    # 用户确认
    confirm = input("\n是否执行整理操作？(yes/no): ").strip().lower()
    if confirm == 'yes':
        print(colored("\n开始执行整理...", "green"))
        for cmd in commands:
            if validate_command(cmd):
                execute_command(cmd)
            else:
                print(colored(f"[错误] 无效或不安全的命令，已跳过: {cmd}", "red"))
        print(colored("[INFO] 文件整理完成！", "green"))
    else:
        print(colored("[INFO] 用户取消操作", "green"))

if __name__ == "__main__":
    main()