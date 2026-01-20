# MobileAutomationFramework 📱
还没开始

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

---

## 🤖 关于 Vibe Coding

本项目采用 **Vibe Coding** 模式构建。

* **设计理念**: Design as Constraint (设计即约束)。
* **构建方式**: 人类负责架构设计与骨架定义 (Specs/Skeletons)，AI 负责具体逻辑填充与实现。
* **核心文档**: 所有的设计契约均存储于 `.vscode/memory-bank/` 中，确保了代码实现严格遵循架构规范。