# Agentic Discord Bot ~ developed by Harvey Coombs ~ 2021-2026
import asyncio
from discord.gateway import Gateway

async def main():
    while True:
        try:
            await Gateway.connect()
        except Exception as ex:
            print(ex)

        await asyncio.sleep(4)

asyncio.run(main())