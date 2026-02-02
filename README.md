# Discord Template Copier (GUI)

A powerful, user-friendly, and open-source tool designed to clone Discord server structures (channels, roles, categories, and permissions) from one server to another using a graphical user interface (GUI).

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Library](https://img.shields.io/badge/Library-discord.py--self-red)

## 🚀 Features

- **Graphical User Interface:** No more command-line confusion. Select servers from a dropdown list.
- **Full Structure Cloning:** Copies Categories, Text Channels, and Voice Channels.
- **Role Replication:** Clones roles with their exact permissions, colors, and hierarchy.
- **Permission Sync:** Transfers channel-specific permissions (overwrites) for roles.
- **Server Metadata:** Copies the server Icon and Name.
- **Auto-Wipe:** Automatically clears the target server before cloning to ensure a clean slate.
- **Log System:** Real-time log viewer within the app to track the progress.

## ⚠️ Disclaimer

**This tool automates user accounts (Self-Botting).**
Automating user accounts is against Discord's Terms of Service. This project is intended for **educational purposes only**. The developer is not responsible for any account bans or suspensions resulting from the use of this tool. Use it at your own risk.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/codedByCan/Discord_Template_Copyier.git
   cd Discord_Template_Copyier
   ```

2. **Install the required dependencies:**
*Note: This tool uses `discord.py-self` to function with user tokens.*
```bash
pip install discord.py-self
```



## 💻 Usage

1. Run the script:
```bash
python main.py

```


2. **Authentication:**
* Enter your Discord **User Token** in the input field.
* Click **Login**.


3. **Selection:**
* **Source Server:** Select the server you want to copy FROM.
* **Target Server:** Select the empty server you want to copy TO.


*(Note: The Target Server will be completely wiped before copying starts.)*
4. **Start:**
* Click **START CLONING**.
* Monitor the logs for progress.



## 📸 Preview


## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE)
