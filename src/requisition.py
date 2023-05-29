import aiohttp
import asyncio

async def main():
    palavras = ['amor', 'moça', 'venda']

    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0'}) as get:
        tasks = [get.get(url=f'https://dicionario-solomon.onrender.com/{palavra}?format=json') for palavra in palavras]
        responses = await asyncio.gather(*tasks)
        meanings = [await response.json() for response in responses]
        for meaning in meanings:
            print(meaning['results'][0]['examples'][0]['sentence'])

asyncio.run(main())