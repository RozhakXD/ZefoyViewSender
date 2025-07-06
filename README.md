# ZefoyViewSender — Automate TikTok View Boosting with Selenium 🚀
![ZefoyViewSender Logo](https://github.com/user-attachments/assets/ff22dd86-8740-4c90-af9e-453ea136abfd)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**ZefoyViewSender** is a lightweight automation tool built with Python and Selenium to interact with the [Zefoy.com](https://zefoy.com) platform.
It automates the process of sending free TikTok views without requiring any login or TikTok credentials.

Using Zefoy’s built-in services, this tool can deliver **500+ views** per submission, with a typical cooldown of **every 5 minutes**. All CAPTCHA handling is done manually at the start, and the rest is fully automated.

## 🎯 Key Features
* ✅ **Auto Submit Views** — Automatically sends \~500+ views every 5 minutes
* ✅ **Timer Intelligence** — Smart delay detection with precision waiting
* ✅ **Robust Error Handling** — Auto retry system for failed attempts
* ✅ **Professional CLI Interface** — Console output with progress feedback
* ✅ **Multi-Config Support** — Easily configurable via `config.json`
* ✅ **Ad Management System** — Detects and closes ads/popups seamlessly

## 🖥️ System Requirements
* ChromeDriver (must match Chrome version)
* Google Chrome (latest stable version)
* Python 3.8 or higher
* Stable internet connection

## 📥 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/RozhakXD/ZefoyViewSender.git
    cd ZefoyViewSender
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download the ChromeDriver matching your Chrome version:
   👉 [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

## 🚀 Usage
1. Copy the config template:
    ```bash
    cp config.example.json config.json
    ```

2. Edit `config.json`:
    ```json
    {
        "video_url": "YOUR_TIKTOK_VIDEO_URL_HERE",
        "max_retries": 5,
        "wait_times": {
            "element_timeout": 10,
            "retry_delay": 15,
            "error_delay": 300
        }
    }
    ```

3. Run the program:
    ```bash
    python main.py
    ```

4. Follow the console instructions:
   * Solve CAPTCHA manually when prompted
   * Let the script run in the background automatically

## 📸 Screenshot
![Image](https://github.com/user-attachments/assets/4f81f9c3-0f65-48c5-b4a2-3b03132309ab)

## ⚠️ Important Notes
1. **Manual CAPTCHA** solving is required at the beginning
2. Keep **ChromeDriver updated** to match your Chrome version
3. Recommended usage: **max 5x per hour** to avoid rate-limits
4. **Monitor system usage** (CPU/RAM) during operation
5. Zefoy's UI may change unexpectedly — scripts may need adjustments

## 🔒 Disclaimer

> This tool is intended for educational and research purposes only.
> Use at your own risk. The developer is **not responsible** for:
>
> * TikTok account bans or suspensions
> * System failures or damages
> * Abuse or malicious use
> * Any legal consequences
>
> ⚠️ Use responsibly and avoid abuse. We strongly encourage users to:
>
> * Avoid sending spam traffic
> * Respect TikTok's [Community Guidelines](https://www.tiktok.com/community-guidelines)

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.
