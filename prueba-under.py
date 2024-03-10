# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 15:19:12 2024

@author: enado
"""

import json
from understat import Understat
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        table = await understat.get_league_table("Bundesliga", "2022")
        print(json.dumps(table))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
