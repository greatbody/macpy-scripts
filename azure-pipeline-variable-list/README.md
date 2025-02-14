# Azure Pipeline Variable List

[![Test](https://github.com/greatbody/macpy-scripts/actions/workflows/test.yml/badge.svg)](https://github.com/greatbody/macpy-scripts/actions/workflows/test.yml)

A tool to analyze and list variables used in Azure Pipeline YAML files.

[English](#features) | [中文](#chinese)

## Chinese

一个用于分析和列出 Azure Pipeline YAML 文件中使用的变量的工具。

### 功能特点

- 检测 `$(VARIABLE)` 格式的变量
- 识别变量组中定义的变量
- 支持嵌套目录结构
- 支持 `.yml` 和 `.yaml` 文件扩展名

例如，如果你有一个 `demo.yml` 流水线文件，内容如下：

```yaml
...
variables:
  group: infra
  ## - var1
  ## - var2
  ## - var3

stages:
  - stage: Build
    jobs:
      - job: Build
        steps:
          - script: echo $(var1)
...
```

azpipvar 将输出：

```
demo.yml:
  - var1 (by variable group)
```

使用说明：

```
## - var3
```

这是一个注释，告诉工具 `var3` 是在变量组中定义的，或者是在 Azure DevOps 流水线的变量中定义的（未存储在代码仓库中）。

该工具将列出流水线文件中使用的所有变量，并显示它们是否在变量组中定义。

这个工具可以帮助你找到流水线文件中所有未预定义的变量。

---

## Features

- Detects variables in `$(VARIABLE)` format
- Identifies variables defined in variable groups
- Supports nested directory structures
- Handles both `.yml` and `.yaml` file extensions

For example, if you have a pipeline file `demo.yml` like this:

```yaml
...
variables:
  group: infra
  ## - var1
  ## - var2
  ## - var3

stages:
  - stage: Build
    jobs:
      - job: Build
        steps:
          - script: echo $(var1)
...
```

azpipvar will output:

```
demo.yml:
  - var1 (by variable group)
```

Let me explain the usage:

```
## - var3
```

This is a comment, that tells the tool that `var3` is defined in a variable group or just defined in the variables of the azure devops pipeline(which is not stored in repository).

It will list all variables used in the pipeline files and show whether they are defined in variable groups or not.

This tool can help you find all variables used in the pipeline files that is not predefined.

## Requirements

- Python 3.8 or higher
- PyYAML 6.0.1 or higher

## Installation

You can install the package using pip:

```bash
pip install azpipvar
```

For development installation from source:

```bash
git clone https://github.com/greatbody/macpy-scripts.git
cd macpy-scripts
pip install -e .
```

## Usage

Navigate to your Azure Pipelines directory and run:

```bash
azpipvar
```

This will scan all YAML files in the current directory and subdirectories, listing all variables used in the pipeline files.

## License

This project is licensed under the MIT License.

## Author

- greatbody (sunruicode@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.