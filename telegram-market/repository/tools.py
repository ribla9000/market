import datetime
import os
from aiogram import BaseMiddleware
from aiogram.types import Message
import aiohttp
from core.config import API_BASE_URL, STATIC_PICS
from typing import Callable, Dict, Any, Awaitable


class ErrorLoggingMiddleware(BaseMiddleware):
    def __init__(self, log_file_path = "logs.txt") -> None:
        self.log_file_path = log_file_path
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        try:
            return await handler(event, data)
        except Exception as e:
            error_message = f'Update {event} caused error {e}'
            print(error_message)

            if not os.path.exists(self.log_file_path):
                with open(self.log_file_path, 'w') as log_file:
                    pass

            with open(self.log_file_path, 'a') as log_file:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_file.write(f'{error_message}\n')
                log_file.write(f'DateError: {timestamp}\n\n')


def keyboard_cols(buttons, cols):
    menu = [buttons[i:i + cols] for i in range(0, len(buttons), cols)]
    return menu


def get_values(values):
    if values is None:
        return None
    return [dict(value) for value in values] if isinstance(values, list) else dict(values)


async def download_image(path):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_BASE_URL + f'download/{path}') as resp:
            if resp.status == 200:
                data = await resp.read()
                with open(STATIC_PICS + path, 'wb') as f:
                    f.write(data)

                return path
            else:
                return "unknown.jpg"
