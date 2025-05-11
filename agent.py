# agent.py

import asyncio
import yaml
import os
from core.loop import AgentLoop
from core.session import MultiMCP
from dotenv import load_dotenv
import sys
import io
import json

# Force UTF-8 encoding for standard output
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(stage: str, msg: str):
    """Simple timestamped console logger."""
    import datetime
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{stage}] {msg}")


async def main():
    print("🧫 Cortex-R Agent Ready")

    # Load .env credentials
    load_dotenv()

    # Load MCP server configs from profiles.yaml
    with open("config/profiles.yaml", "r") as f:
        profile = yaml.safe_load(f)
        mcp_servers = profile.get("mcp_servers", [])
    
    multi_mcp = MultiMCP(server_configs=mcp_servers)
    print("Agent before initialize")
    await multi_mcp.initialize()

    agent = AgentLoop(
        user_input="",  # placeholder for now
        dispatcher=multi_mcp  # now uses dynamic MultiMCP
    )

    try:
        # --- Telegram Triggered F1 Task ---
        try:
            print("Before Calling check_telegram_commands from tools")
            telegram_message = await asyncio.wait_for(
                multi_mcp.call_tool("check_telegram_commands", {}), timeout=5
            )
            #telegram_message = await multi_mcp.call_tool("check_telegram_commands", {})
            
            print("After Calling check_telegram_commands from tools", telegram_message)
        except asyncio.TimeoutError:
            print("⏰ Telegram check timed out.")
            telegram_message = ""

        if telegram_message and "f1" in str(telegram_message).lower() and "standing" in str(telegram_message).lower():
            print("🔍 Telegram Trigger: F1 Standings requested")

            f1_result = await multi_mcp.call_tool("fetch_f1_standings", {})
            f1_data = [row.text for row in f1_result.content] 
            print("f1_data : ",f1_data)
            recipient_email = os.getenv("GMAIL_ADDRESS")

            sheet_url = await multi_mcp.call_tool("post_to_google_sheets", {
                "data": f1_data,
                "email": recipient_email
            })

            await multi_mcp.call_tool("notify_via_email", {
                "email": recipient_email,
                "sheet_url": sheet_url
            })

            await multi_mcp.call_tool("send_telegram_message", {
                "text": f"Your F1 Standings Sheet is ready: {sheet_url}"
            })

            print("✅ Telegram-triggered F1 report sent via Gmail and Telegram.")
        else:
            print("ℹ️ No F1 request found in Telegram. Asking user manually...")
            user_input = input("🧑 What do you want to solve today? → ")
            agent.user_input = user_input
            final_response = await agent.run()
            print("\n💡 Final Answer:\n", final_response.replace("FINAL_ANSWER:", "").strip())

    except Exception as e:
        log("fatal", f"Agent failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())


# Find the ASCII values of characters in INDIA and then return sum of exponentials of those values.
# How much Anmol singh paid for his DLF apartment via Capbridge? 
# What do you know about Don Tapscott and Anthony Williams?
# What is the relationship between Gensol and Go-Auto?
# which course are we teaching on Canvas LMS?
# Summarize this page: https://theschoolof.ai/
# What is the log value of the amount that Anmol singh paid for his DLF apartment via Capbridge?
