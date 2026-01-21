# MobileAutomationFramework 📱
项目还没开始,但是已经写好了vibe coding的相关操作手册,和函数规范

所以可以用这个项目试试vibe coding

用AI执行的话,在对话框@.vscode/memory-bank/ (让AI读取对应文档);再直接复制Prompt.md的内容发给AI即可

这条Prompt会让AI执行部分需求的vibe coding,之后的操作可以找AI问问,这里就不详细提供了

(还有操作手册,函数规范,已经本简介均有AI生成)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Appium](https://img.shields.io/badge/Appium-3.0%2B-green)](https://appium.io/)
[![Vibe Coding](https://img.shields.io/badge/Built%20with-Vibe%20Coding-purple)](https://github.com/your-profile)

一个基于 **Appium (W3C Standard)** + **Pytest** + **Allure** 的现代化移动端自动化测试框架。
采用严格的 **Pages - Workflows - TestCases** 三层架构设计，实现了业务逻辑、页面操作与测试数据的深度解耦。

---

## 📦 依赖清单 (Dependencies)

本项目依赖分为“核心必要”和“功能选配”，请根据需求安装。

### 🔴 核心必要依赖 (Core - 必须安装)
确保框架能正常运行的基础组件。

* **`Appium-Python-Client >= 3.1.0`**: **关键依赖**。强制使用 W3C 协议，摒弃过时的 `TouchAction`，支持最新版 Appium Server。
* **`pytest >= 7.0`**: 测试执行引擎。
* **`allure-pytest`**: 生成可视化的测试报告。
* **`loguru`**: 现代化的日志管理（自动切割/轮转）。
* **`PyYAML`**: 读取配置文件。
* **`openpyxl`**: 读取 Excel 测试数据。

### 🟡 功能选配依赖 (Optional - 按需安装)
如果你不需要相关功能，可以不装，并在 `utils/` 中禁用对应模块。

* **`opencv-python` & `numpy`**: 
    * *用途*: 用于 `utils/cv_helper.py`。
    * *场景*: 需要图像识别定位、图片相似度对比 (UI 视觉回归) 时安装。
* **`requests`**: 
    * *用途*: 用于 `utils/notify_helper.py`。
    * *场景*: 测试结束后需要发送 飞书/钉钉/企业微信 通知时安装。
* **`python-dotenv`**:
    * *用途*: 加载 `.env` 文件中的敏感信息（如密码）。

---

## 🚀 快速开始 (Usage)

### 1. 安装依赖
```bash
pip install -r requirements.txt

```

### 2. 配置环境

* 修改 `config/global_config.py` 或创建 `.env` 文件，配置 `APP_PACKAGE`, `APP_ACTIVITY` 和设备信息。
* 确保本地已安装 Appium Server 和 Android SDK/JDK。

### 3. 运行测试

支持通过命令行参数切换环境和平台：

```bash
# 默认运行 (Android + Test环境)
pytest

# 指定环境和平台
pytest --env=prod --platform=ios

# 生成并查看报告
pytest --alluredir=./reports/xml
allure serve ./reports/xml

```
## 📂 项目结构 (Project Structure)

```text
MobileAutomationFramework/
├── .github/                # [CI/CD] GitHub Actions 工作流
│   └── workflows/
│       └── ci.yml          # 配置代码提交时自动运行 pylint 检查或单元测试
├── .gitignore              # [Git配置] 忽略 logs/, reports/, __pycache__/, .env 等
├── .env.example            # [环境模板] 告诉使用者需要配置哪些环境变量 (如 USERNAME=xxx)
├── Dockerfile              # [容器化] (可选) 用于构建纯净的 Python 运行环境
├── LICENSE                 # [开源协议] MIT 或 Apache 2.0，声明版权
├── README.md               # [项目说明] 架构图、快速开始、贡献指南
├── requirements.txt        # [依赖列表] Appium-Python-Client, pytest, allure-pytest, loguru
├── pytest.ini              # [Pytest配置] addopts = -vs --alluredir=./reports/xml
└── run.py                  # [入口脚本] 统一执行入口，处理参数解析

配置与数据层
├── config/
│   ├── __init__.py
│   ├── global_config.py    # [全局配置] URL, BundleID, 等待超时时间
│   └── logging_config.py   # [日志设置] 格式化器、文件轮转配置
├── data/
│   ├── __init__.py
│   ├── test_accounts.yaml  # [账号池] 存放多角色测试账号
│   └── test_data.xlsx      # [测试数据] 参数化用例的数据源

驱动管理层
├── drivers/
│   ├── __init__.py
│   └── driver_factory.py   # [Driver工厂]
                            # 功能：封装 Android/iOS/H5 的 Desired Capabilities
                            # 职责：负责 Appium 连接建立与 quit 销毁

页面对象层 (Layer 1: Pages)
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # [核心基类]
                            # 功能：Find, Click, Input, Screenshot, SwitchContext(H5)
                            # 继承：ActionMixin
│   ├── mixins/             # [功能混入]
│   │   ├── __init__.py
│   │   └── action_mixin.py # [W3C动作] 封装 Swipe, LongPress, DragAndDrop, Pinch
│   ├── android/            # [Android页面]
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   └── webview_page.py # [H5专用] 处理内嵌 Webview 的特殊页面
│   └── ios/                # [iOS页面]
│       └── ...

业务流程层 (Layer 2: Workflows)
├── workflows/
│   ├── __init__.py
│   ├── base_workflow.py    # [Workflow基类]
                            # 功能：持有 driver，按需懒加载 Page 对象，避免重复实例化
│   ├── login_flow.py       # [登录业务] 组装：输入账号 -> 点击登录 -> 校验失败/成功
│   ├── post_flow.py        # [内容业务] 组装：进入发布页 -> 选图 -> 发送
│   └── h5_flow.py          # [混合业务] 原生入口 -> 切换H5 -> 操作网页 -> 切回原生

测试用例层 (Layer 3: TestCases)
├── testcases/
│   ├── __init__.py
│   ├── conftest.py         # [Pytest Fixture]
                            # Setup: 启动 Appium Driver
                            # Teardown: 关闭 Driver
                            # Hook: 失败自动截图并挂载到 Allure 报告
│   ├── test_login.py       # [功能测试] 验证登录模块
│   └── test_scenarios.py   # [场景测试] 跨账号、长链路的 E2E 测试

工具层 (Utils)
├── utils/
│   ├── __init__.py
│   ├── adb_helper.py       # [系统交互] 封装 ADB 命令 (清理缓存, 切换输入法)
│   ├── assert_helper.py    # [高级断言] 软断言、字典对比、列表排序校验
│   ├── cv_helper.py        # [图像识别] OpenCV 封装 (用于无法定位的控件)
│   ├── data_loader.py      # [数据读取] 解析 YAML/Excel/JSON
│   ├── file_helper.py      # [文件操作] 路径拼接、文件夹清理
│   ├── logger.py           # [日志封装] 二次封装 logging 或 loguru，提供简便调用接口
│   ├── notify_helper.py    # [消息通知] 飞书/钉钉 Webhook 封装
│   └── decorators.py       # [装饰器]
                            # @log_step: 记录步骤
                            # @handle_exception: 异常捕获

产出物 (Artifacts - 需在 .gitignore 中忽略)
├── reports/                # Allure XML/HTML 报告
├── logs/                   # 运行时产生的 .log 文件
└── screenshots/            # 失败截图或业务截图
```

---

## 🤖 关于 Vibe Coding

本项目采用 **Vibe Coding** 模式构建。

* **设计理念**: Design as Constraint (设计即约束)。
* **构建方式**: 人类负责架构设计与骨架定义 (Specs/Skeletons)，AI 负责具体逻辑填充与实现。
* **核心文档**: 所有的设计契约均存储于 `.vscode/memory-bank/` 中，确保了代码实现严格遵循架构规范。