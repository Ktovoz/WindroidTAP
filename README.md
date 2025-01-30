# 🤖 WindroidTAP

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Downloads](https://img.shields.io/github/downloads/ktovoz/WindroidTAP/total.svg)](https://github.com/ktovoz/WindroidTAP/releases)
[![Last Commit](https://img.shields.io/github/last-commit/ktovoz/WindroidTAP)](https://github.com/ktovoz/WindroidTAP/commits/main)

</div>

<div align="center">
  <h3>🌟 跨平台自动化测试框架</h3>
  <p>适用于 Windows 和 Android 应用程序的统一自动化测试解决方案</p>
</div>

<div align="center">
  <h3>📢 文档</h3>
  <p>
    <a href="README_en.md">English</a> | 
    <a href="README.md">中文</a>
  </p>
</div>

<div align="center">
  <h3>📌 重要提示</h3>
  <p>本项目仍在积极开发中，API 可能会有变动。请定期关注更新。</p>
</div>

---

<div align="center">
  <h3>👥 贡献者</h3>
  <p>感谢所有为项目做出贡献的开发者！</p>
  <a href="https://github.com/ktovoz/WindroidTAP/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=ktovoz/WindroidTAP" />
  </a>
</div>

---

<div align="center">
  <h3>🌟 支持项目</h3>
  <p>如果这个项目对你有帮助，请给它一个 Star ⭐️</p>
  <a href="https://github.com/ktovoz/WindroidTAP/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/ktovoz/WindroidTAP?style=social">
  </a>
</div>

WindroidTAP 是一个跨平台的自动化测试框架，适用于Windows和Android应用程序。它旨在简化测试流程，提高开发效率，并确保应用在不同操作系统上的稳定性和兼容性。

🌐 访问我的网站了解更多信息：[ktovoz.com](https://ktovoz.com)

## 📚 目录

- [主要特性](#主要特性)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [依赖说明](#依赖说明)
- [使用示例](#使用示例)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [联系我们](#联系我们)

## 🎯 主要特性

- **统一的操作接口**
  - 提供一致的API来处理不同平台的自动化操作
  - 支持鼠标点击、键盘输入、截图等基础功能

- **跨平台支持**
  - Windows桌面应用程序
  - Android移动应用程序

- **灵活的扩展性**
  - 模块化设计，易于扩展新功能
  - 支持自定义操作和测试场景

- **Android设备控制**
  - 通过自研 blecom APK 获取设备屏幕图像
  - 使用蓝牙HID设备进行精确操控
  - 支持多设备并行控制

## 🚀 快速开始

### 📥 安装

```bash
# 克隆项目
git clone https://github.com/ktovoz/WindroidTAP.git
cd WindroidTAP

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 🎮 基础用法

```python
from baseutil.platform_operator import PlatformOperator

# Windows应用程序示例
win_op = PlatformOperator('windows', window_title='记事本')
win_op.click(100, 100)  # 点击指定坐标
win_op.input_text('Hello, WindroidTAP!')  # 输入文本

# Android应用程序示例
app_op = PlatformOperator('app', ip='127.0.0.1', port=8080)
app_op.click(200, 300)  # 点击屏幕
app_op.swipe(100, 200, 100, 400)  # 滑动操作
```

## 📂 项目结构

```
WindroidTAP/
├── baseutil/                 # 核心工具库
│   ├── app/                 # Android平台相关
│   │   ├── app_OP.py       # Android操作实现
│   │   └── blecom.apk      # Android设备控制APK
│   └── win/                 # Windows平台相关
│       └── winOperate/     # Windows操作实现
├── docs/                    # 文档
├── examples/                # 示例代码
├── tests/                   # 测试用例
├── requirements.txt         # 项目依赖
└── README.md               # 项目说明
```

## 📦 依赖说明

### 环境准备

#### 更新解释器和pip

确保使用最新的pip版本：

```bash
python.exe -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 依赖库清单

#### 核心依赖

| 功能分类 | 库名称 | 描述 | 安装命令 |
|---------|--------|------|----------|
| **日志记录** | loguru | 提供简单且功能强大的日志记录功能 | `pip install loguru -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **图像处理** | pillow | 图像处理基础库 | `pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **Windows支持** | pywin32 | Windows系统API扩展 | `pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **键盘控制** | keyboard | 键盘事件监听与控制 | `pip install keyboard -i https://pypi.tuna.tsinghua.edu.cn/simple` |

#### 可选依赖

| 功能分类 | 库名称 | 描述 | 安装命令 |
|---------|--------|------|----------|
| **OCR识别** | paddleocr | 高精度OCR文字识别功能 | `pip install paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **OCR支持** | PaddlePaddle | 深度学习框架，支持OCR模型 | `pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **GUI开发** | pyside6 | Qt框架的Python绑定 | `pip install pyside6 -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **环境管理** | python-dotenv | 加载.env文件，管理环境变量 | `pip install python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple` |

### 注意事项

- 所有包均使用清华大学镜像源加速安装，确保网络连接正常
- 如果遇到安装问题，请检查防火墙设置或尝试更换镜像源
- 根据实际使用场景选择安装核心依赖或可选依赖

## 📖 使用示例

更多示例请查看 [examples](examples/) 目录。

### 🖥️ Windows应用测试

```python
from baseutil.platform_operator import PlatformOperator

def test_notepad():
    # 初始化Windows操作器
    op = PlatformOperator('windows', window_title='记事本')
    
    # 执行测试操作
    op.input_text('测试文本')
    op.hotkey('ctrl', 's')
```

### 📱 Android应用测试

```python
from baseutil.platform_operator import PlatformOperator

def test_android_app():
    # 初始化Android操作器
    op = PlatformOperator('app', ip='127.0.0.1')
    
    # 执行测试操作
    op.click(100, 200)
    op.swipe(100, 500, 100, 100)
```

## ❓ 常见问题

1. **Q: 如何处理元素定位问题？**
   - A: WindroidTAP 提供了多种元素定位方式，包括坐标定位和图像识别定位。

2. **Q: 支持哪些 Android 设备？**
   - A: 支持所有可安装 blecom APK 且可连接蓝牙HID设备的 Android 设备。

3. **Q: blecom APK 如何工作？**
   - A: blecom APK 在 Android 设备上运行，负责截取屏幕图像并通过网络传输，同时控制蓝牙HID设备执行具体的操作指令。

4. **Q: 如何连接 Android 设备？**
   - A: 
     1. 在 Android 设备上安装 blecom APK
     2. 确保设备已连接蓝牙HID设备
     3. 确保电脑与手机在同一网络
     4. 通过 IP 地址连接到运行 blecom 的设备
     5. 使用 PlatformOperator 进行操作

## 🤝 贡献指南

欢迎贡献代码！如果你有任何改进建议或功能需求，请通过 Issue 进行讨论。

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📮 联系我们

- 提交Issue: [GitHub Issues](https://github.com/ktovoz/WindroidTAP/issues)
- 邮件联系: 484202421@qq.com

<div align="center">
  <h3>🏷️ 标签</h3>
  <p>#AutomationTesting #Windows #Android #Python #CrossPlatform #Testing</p>
</div> 