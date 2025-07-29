import asyncio
import json
import os
import requests
from telegram import Bot
from solana.rpc.websocket_api import connect

# Lees gegevens uit environment variables
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
WATCHED_WALLET = os.getenv("WATCHED_WALLET")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def listen():
    url = f"wss://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
    async with connect(url) as websocket:
        await websocket.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [{
                "mentions": [WATCHED_WALLET]
            }, {
                "commitment": "confirmed"
            }]
        }))
        await send_telegram("👀 Sniperbot is live en luistert naar wallet: " + WATCHED_WALLET)
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if "method" in data and data["method"] == "logsNotification":
                logs = data["params"]["result"]["value"]["logs"]
                for log in logs:
                    if "Program log: Instruction: Buy" in log:
                        await send_telegram(f"💰 Buy gedetecteerd van {WATCHED_WALLET}!\n\nLogs:\n{logs}")
                        # Hier kun je zelf nog je koop-logica uitbreiden

if __name__ == "__main__":
    asyncio.run(listen())
