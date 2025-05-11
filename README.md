
# 🧠 Cortex-R Agent: Multi-Tool AI Automation

This project implements a multi-capability AI agent using the **Cortex-R** architecture, integrating services like Telegram, Gmail, and Google Sheets via a modular tool system (`MultiMCP`). It can autonomously respond to Telegram messages and trigger cross-service actions like creating spreadsheets and sending notifications.

---

## 📦 Features

- ✅ **Telegram Command Listener** (e.g., responds to "F1 Standings")
- 📊 **Fetches F1 Driver Standings** via a mock data tool
- 📄 **Creates a Google Sheet** and shares it with a Gmail account
- 📧 **Sends Email Notifications** with the generated sheet
- 💬 **Sends Telegram Messages** back with confirmation

---

## 🗂 Directory Structure

```
S8_Assignment/
├── agent.py                    # Main orchestrator agent
├── config/
│   └── profiles.yaml           # MCP tool server configurations
├── utils/
│   ├── gmail.py                # Gmail notification logic
│   ├── gdrive.py               # Google Sheets creation logic
│   └── telegram.py             # Telegram polling and messaging
├── mcp_server_3.py            # First MCP toolset (e.g., search)
├── mcp_server_4.py            # Extended tools (F1, sheets, email, Telegram)
├── credentials.json           # Google service account creds (not committed)
├── .env                       # Environment vars (e.g., Gmail creds, tokens)
```

---

## 🚀 Setup Instructions

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

> You’ll need:
> - `openai`
> - `gspread`
> - `oauth2client`
> - `python-dotenv`
> - `pyTelegramBotAPI` (or similar)

2. **Configure `.env`**

```dotenv
GMAIL_ADDRESS=youremail@example.com
GMAIL_PASSWORD=your_app_password
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_CREDS_JSON=credentials.json
```

3. **Add Google Service Account Credentials**

Download your `credentials.json` from Google Cloud and place it in the root directory.

4. **Run the Agent**

```bash
python agent.py
```

---

## 🧪 Example Flow

1. You send a Telegram message: **"F1 Standings"**
2. Agent fetches F1 mock data
3. It creates a sheet in Google Drive and shares it with you
4. Sends confirmation via Gmail and Telegram

---

## 🛠 Tool Servers (MCP)

Ensure both tool servers are configured in `config/profiles.yaml` and registered with `MultiMCP`.

Example:

```yaml
mcp_servers:
  - name: mcp_server_3
    path: mcp_server_3.py
  - name: mcp_server_4
    path: mcp_server_4.py
```

---

## ✅ Status

- [x] Telegram to Sheets trigger working
- [x] Email notification sent
- [x] Modular MCP tool system in place
