import threading
import websockets
import asyncio
import typer
from ws_cli_chat.console import Console

app = typer.Typer()
MESSAGES: list[str] = []


async def recive_message(socket) -> None:
    try:
        while True:
            msg: str = await socket.recv()
            if msg:
                Console.clear()
                MESSAGES.append(msg)
                [print(message) for message in MESSAGES]
                Console.br(100)
    except KeyboardInterrupt:
        return None


def send_message(socket) -> None:
    while True:
        try:
            msg: str = input()
            asyncio.run(socket.send(msg))
        except KeyboardInterrupt:
            return None


async def main():
    try:
        name: str = input("Escolha um username!\n>")
        url: str = f'wss://webchat-production-8f8d.up.railway.app/?username={name}'
        async with websockets.connect(url) as socket:
            threading.Thread(target=send_message, args=(socket,)).start()
            await recive_message(socket)
    except KeyboardInterrupt:
        return None


@app.command()
def run_main():
    asyncio.run(main())


if __name__ == '__main__':
    run_main()