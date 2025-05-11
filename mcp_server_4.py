from mcp.server.fastmcp import FastMCP, Context
#from mcp import tool, serve
import sys
from utils.gmail import send_gmail
from utils.gdrive import create_sheet_and_share
from utils.telegram import get_latest_telegram_message, send_telegram_message as send_telegram_api
import io
import os
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename="mcp_server_4.log", level=logging.DEBUG)

def debug_log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


mcp = FastMCP("ddg-search")

@mcp.tool()
def fetch_f1_standings() -> list:
    return [
        {"Driver": "Max Verstappen", "Points": 250},
        {"Driver": "Charles Leclerc", "Points": 200},
        {"Driver": "Lewis Hamilton", "Points": 180}
    ]

@mcp.tool()
def post_to_google_sheets(data: list, email: str) -> str:
    return create_sheet_and_share(data, email)

@mcp.tool()
def notify_via_email(email: str, sheet_url: str):
    subject = "Your F1 Standings Sheet"
    body = f"Hi,\n\nHere's the sheet with current F1 standings:\n\n{sheet_url}\n\n- Cortex-R Agent"
    send_gmail(to=email, subject=subject, body=body)

@mcp.tool()
async def check_telegram_commands() -> str:
    logging.debug("Inside check_telegram_commands() tool")
    message = await get_latest_telegram_message()
    logging.debug(f"Telegram command received: {message}")
    return str(message or "[empty]")

@mcp.tool()
def send_telegram_message(text: str) -> str:
    return send_telegram_api(text)

# Start the stdio MCP server
#serve()
if __name__ == "__main__":
    print("mcp_server_4.py starting")
    mcp.run(transport="stdio")
    #if len(sys.argv) > 1 and sys.argv[1] == "dev":
            #mcp.run()  # Run without transport for dev server
    #else:
        #mcp.run(transport="stdio")  # Run with stdio for direct execution
        #print("\nShutting down...")
