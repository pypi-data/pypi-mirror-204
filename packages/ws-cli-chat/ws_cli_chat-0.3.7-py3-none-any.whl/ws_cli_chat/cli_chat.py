import threading
import websockets
import asyncio
import typer
import PySimpleGUI as sg
from pysimpleevent import EventSimpleGUI
from typing import Optional
from ws_cli_chat.myconsole import MyConsole


app = typer.Typer()
MESSAGES: list[str] = []


def rederizar_menssagens(lista_menssagens: list) -> None:
    MyConsole.clear()
    [print(menssagen) for menssagen in lista_menssagens]
    MyConsole.br(30)


async def recive_message(socket) -> None:
    try:
        while True:
            msg: str = await socket.recv()
            if msg:
                MyConsole.clear()
                MESSAGES.append(msg)
                rederizar_menssagens(MESSAGES)
    except KeyboardInterrupt:
        return None


def send_message(socket) -> None:
    while True:
        try:
            msg: str = input()
            if msg and msg != '':
                asyncio.run(socket.send(msg))
        except KeyboardInterrupt:
            return None


def winded_send_message(socket) -> None:
    loop = EventSimpleGUI()
    sg.theme(
        sg.theme_list()[32]
    )

    win = sg.Window(
        'Escreva sua menssagem !',
        layout=[
            [sg.Button("fechar", expand_x=True)],
            [sg.Text("Sua menssagen >"),sg.Input(expand_x=True, key='message'), sg.Button("enviar", bind_return_key=True)]
        ],
        resizable=True,
        scaling=2.0,
        grab_anywhere_using_control=True,
        titlebar_background_color='black'
    )

    @loop.event("enviar")
    def send_message(event: str, values: dict, win: sg.Window):
        if values.get('message', '') != '':
            input = win.FindElement('message')
            asyncio.run(socket.send(values['message']))
            input.update('')
    try:
        loop.run_window(win, close_event='fechar')
    except KeyboardInterrupt:
        return None


async def main(
    *,
    name: str | None = None,
    url: str | None = None,
    window: bool = False
) -> None:

    MyConsole.clear()

    if not name:
        name: str = input("""Escolha um username! \n>"""
        )
    if not url:
        url: str = f'wss://webchat-production-8f8d.up.railway.app/?username={name}'
    else:
        url += f'/?username={name}'

    MyConsole.clear()

    if not window:
        try:
            async with websockets.connect(url) as socket:
                threading.Thread(target=send_message, args=(socket,)).start()
                await recive_message(socket)
        except KeyboardInterrupt:
            return None
    else:
        try:
            async with websockets.connect(url) as socket:
                threading.Thread(target=winded_send_message, args=(socket,)).start()
                threading.Thread(target=send_message, args=(socket,)).start()
                await recive_message(socket)
        except KeyboardInterrupt:
            return None


@app.command()
def connect(
        *,
        name: Optional[str] = typer.Argument(None),
        url: Optional[str] = typer.Argument(None),
        window: bool = typer.Option(False, '--window', '-w')
) -> None:
    asyncio.run(main(name=name, url=url, window=window))


if __name__ == '__main__':
    typer.run(connect)

