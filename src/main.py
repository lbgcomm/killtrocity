import sys
import os

import config
import killfrenzy
import kilimanjaro

import asyncio

async def main():
    # Run each program as a new thread to allow for blocking, etc.
    await asyncio.gather(asyncio.to_thread(kilimanjaro.init), asyncio.to_thread(killfrenzy.init))

if __name__ == "__main__":
    asyncio.run(main())