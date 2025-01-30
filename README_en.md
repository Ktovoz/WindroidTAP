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
  <h3>🌟 Cross-Platform Test Automation Framework</h3>
  <p>A unified automation testing solution for Windows and Android applications</p>
</div>

<div align="center">
  <h3>📢 Documentation</h3>
  <p>
    <a href="README_en.md">English</a> | 
    <a href="README.md">中文</a>
  </p>
</div>

<div align="center">
  <h3>📌 Important Note</h3>
  <p>This project is under active development. APIs may change. Please stay tuned for updates.</p>
</div>

---

<div align="center">
  <h3>👥 Contributors</h3>
  <p>Thanks to all the developers who contributed to this project!</p>
  <a href="https://github.com/ktovoz/WindroidTAP/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=ktovoz/WindroidTAP" />
  </a>
</div>

---

<div align="center">
  <h3>🌟 Support the Project</h3>
  <p>If you find this project helpful, please give it a star ⭐️</p>
  <a href="https://github.com/ktovoz/WindroidTAP/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/ktovoz/WindroidTAP?style=social">
  </a>
</div>

WindroidTAP is a cross-platform test automation framework for Windows and Android applications. It aims to simplify the testing process, improve development efficiency, and ensure application stability and compatibility across different operating systems.

🌐 Visit my website for more information: [ktovoz.com](https://ktovoz.com)

## 📚 Table of Contents

- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Dependencies](#-dependencies)
- [Usage Examples](#-usage-examples)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Future Development](#-future-development)

## 🎯 Key Features

- **Unified Operation Interface**
  - Provides consistent APIs for automation operations across platforms
  - Supports basic functions like mouse clicks, keyboard inputs, screenshots

- **Cross-Platform Support**
  - Windows Desktop Applications
  - Android Mobile Applications

- **Flexible Extensibility**
  - Modular design for easy feature extension
  - Supports custom operations and test scenarios

- **Android Device Control**
  - Capture device screen through custom blecom APK
  - Precise control via Bluetooth HID device
  - Support parallel control of multiple devices

## 🚀 Quick Start

### 📥 Installation

```bash
# Clone the repository
git clone https://github.com/ktovoz/WindroidTAP.git
cd WindroidTAP

# Install dependencies
pip install -r requirements.txt
```

### 🎮 Basic Usage

```python
from baseutil.platform_operator import PlatformOperator

# Windows application example
win_op = PlatformOperator('windows', window_title='Notepad')
win_op.click(100, 100)  # Click specific coordinates
win_op.input_text('Hello, WindroidTAP!')  # Input text

# Android application example
app_op = PlatformOperator('app', ip='127.0.0.1', port=8080)
app_op.click(200, 300)  # Click screen
app_op.swipe(100, 200, 100, 400)  # Swipe operation
```

## 📂 Project Structure

```
WindroidTAP/
├── baseutil/                 # Core utilities
│   ├── app/                 # Android platform related
│   │   ├── app_OP.py       # Android operations
│   │   └── blecom.apk      # Android device control APK
│   └── win/                 # Windows platform related
│       └── winOperate/     # Windows operations
├── docs/                    # Documentation
├── examples/                # Example code
├── tests/                   # Test cases
├── requirements.txt         # Dependencies
└── README.md               # Project description
```

## 📦 Dependencies

### Environment Setup

#### Update Python and pip

Ensure you have the latest pip version:

```bash
python.exe -m pip install --upgrade pip
```

### Dependencies List

#### Core Dependencies

| Category | Library | Description | Install Command |
|----------|---------|-------------|-----------------|
| **Logging** | loguru | Simple yet powerful logging functionality | `pip install loguru` |
| **Image Processing** | pillow | Basic image processing library | `pip install pillow` |
| **Windows Support** | pywin32 | Windows system API extension | `pip install pywin32` |
| **Keyboard Control** | keyboard | Keyboard event monitoring and control | `pip install keyboard` |

#### Optional Dependencies

| Category | Library | Description | Install Command |
|----------|---------|-------------|-----------------|
| **OCR** | paddleocr | High-precision OCR text recognition | `pip install paddleocr` |
| **OCR Support** | PaddlePaddle | Deep learning framework for OCR | `pip install paddlepaddle` |
| **GUI Development** | pyside6 | Python bindings for Qt framework | `pip install pyside6` |
| **Environment** | python-dotenv | Load .env files, manage environment variables | `pip install python-dotenv` |

### Notes

- If you encounter installation issues, please check your network connection and firewall settings
- Choose to install core or optional dependencies based on your actual usage scenario

## 📖 Usage Examples

More examples can be found in the [examples](examples/) directory.

### 🖥️ Windows Application Testing

```python
from baseutil.platform_operator import PlatformOperator

def test_notepad():
    # Initialize Windows operator
    op = PlatformOperator('windows', window_title='Notepad')
    
    # Perform test operations
    op.input_text('Test Text')
    op.hotkey('ctrl', 's')
```

### 📱 Android Application Testing

```python
from baseutil.platform_operator import PlatformOperator

def test_android_app():
    # Initialize Android operator
    op = PlatformOperator('app', ip='127.0.0.1')
    
    # Perform test operations
    op.click(100, 200)
    op.swipe(100, 500, 100, 100)
```

## ❓ FAQ

1. **Q: How to handle element location?**
   - A: WindroidTAP provides multiple element location methods, including coordinate positioning and image recognition positioning.

2. **Q: Which Android devices are supported?**
   - A: All Android devices that can install blecom APK and connect to Bluetooth HID devices are supported.

3. **Q: How does blecom APK work?**
   - A: blecom APK runs on Android devices, responsible for capturing screen images and transmitting them over the network, while controlling Bluetooth HID devices to execute specific operation commands.

4. **Q: How to connect Android devices?**
   - A: 
     1. Install blecom APK on Android device
     2. Ensure device is connected to Bluetooth HID device
     3. Ensure computer and phone are on the same network
     4. Connect to the device running blecom via IP address
     5. Use PlatformOperator for operations

## 🤝 Contributing

We welcome contributions! If you have any suggestions for improvements or feature requests, please discuss them through Issues.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📮 Contact

- Submit Issues: [GitHub Issues](https://github.com/ktovoz/WindroidTAP/issues)
- Email: 484202421@qq.com

<div align="center">
  <h3>🏷️ Tags</h3>
  <p>#AutomationTesting #Windows #Android #Python #CrossPlatform #Testing</p>
</div>

## 🔮 Future Development

### 🌐 Web Service Transformation
- Encapsulate existing functionalities into RESTful APIs using FastAPI
- Provide comprehensive API documentation and Swagger UI interface
- Support asynchronous operations and concurrent task processing

### 🎨 Visual Operation Interface
- Develop modern HTML5-based web interface
- Intuitive test case orchestration
- Real-time operation preview and result feedback
- Support record and playback functionality

### 📊 Test Management Platform
- Test case management and version control
- Test result data visualization
- Automated test report generation
- Multi-user collaboration support

### 🔄 CI Integration
- Provide CI/CD integration interfaces
- Support platforms like Jenkins, GitHub Actions
- Automated test result feedback 