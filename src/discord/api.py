import os
import aiohttp

from exception import BotException

class DiscordAPI:
    BASE_URL = "https://discord.com/api/"

    @staticmethod
    async def get(endpoint, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        })
        
        if additional_headers is not None:
            headers.update(additional_headers)        

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                match response.status:
                    case 429:
                        raise BotException(":warning: You are being rate limited. Please try again later.")
                    case 403:
                        raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                    case 400 | 404:
                        raise BotException(await response.text())
                    case 500 | 503:
                        raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                    case 200 | 201:
                        try:
                            return await response.json()
                        except:
                            return await response.text()

    @staticmethod
    async def post(endpoint, payload, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)
        
        async with aiohttp.ClientSession() as session:
            if payload is not None: 
                async with session.post(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                    match response.status:
                        case 429:
                            raise BotException(":warning: You are being rate limited. Please try again later.")
                        case 403:
                            raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                        case 400 | 404:
                            raise BotException(await response.text())
                        case 500 | 503:
                            raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                        case 200 | 201:
                            try:
                                return await response.json()
                            except:
                                return await response.text()
            else:
                async with session.post(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                    match response.status:
                        case 429:
                            raise BotException(":warning: You are being rate limited. Please try again later.")
                        case 403:
                            raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                        case 400 | 404:
                            raise BotException(await response.text())
                        case 500 | 503:
                            raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                        case 200 | 201:
                            try:
                                return await response.json()
                            except:
                                return await response.text()

    @staticmethod
    async def patch(endpoint, payload, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)

        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                match response.status:
                    case 429:
                        raise BotException(":warning: You are being rate limited. Please try again later.")
                    case 403:
                        raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                    case 400 | 404:
                        raise BotException(await response.text())
                    case 500 | 503:
                        raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                    case 200 | 201:
                        try:
                            return await response.json()
                        except:
                            return await response.text()

    @staticmethod
    async def put(endpoint, payload, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)

        async with aiohttp.ClientSession() as session:
            if payload is not None:
                async with session.put(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                    match response.status:
                        case 429:
                            raise BotException(":warning: You are being rate limited. Please try again later.")
                        case 403:
                            raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                        case 400 | 404:
                            raise BotException(await response.text())
                        case 500 | 503:
                            raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                        case 200 | 201:
                            try:
                                return await response.json()
                            except:
                                return await response.text()
            else:
                async with session.put(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                    match response.status:
                        case 429:
                            raise BotException(":warning: You are being rate limited. Please try again later.")
                        case 403:
                            raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                        case 400 | 404:
                            raise BotException(await response.text())
                        case 500 | 503:
                            raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                        case 200 | 201:
                            try:
                                return await response.json()
                            except:
                                return await response.text()

    @staticmethod
    async def delete(endpoint, payload=None, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)     

        async with aiohttp.ClientSession() as session:
            if payload is not None:
                async with session.delete(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                    match response.status:
                        case 429:
                            raise BotException(":warning: You are being rate limited. Please try again later.")
                        case 403:
                            raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                        case 400 | 404:
                            raise BotException(await response.text())
                        case 500 | 503:
                            raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                        case 200 | 201:
                            try:
                                return await response.json()
                            except:
                                return await response.text()
            else:
                async with session.delete(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                    match response.status:
                        case 429:
                            raise BotException(":warning: You are being rate limited. Please try again later.")
                        case 403:
                            raise BotException(":no_entry_sign: I do not have permission to perform this action.")
                        case 400 | 404:
                            raise BotException(await response.text())
                        case 500 | 503:
                            raise BotException(":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.agenti.bot/contact) for further assistance.")
                        case 200 | 201:
                            try:
                                return await response.json()
                            except:
                                return await response.text()