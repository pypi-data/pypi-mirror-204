import os
import sys
import subprocess
from rich.console import Console


console = Console(record=True)


class MyConsole:
    
    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def clear():
        """ Gerado pelo chat gpt"""
        os.system('cls' if os.name == 'nt' else 'clear')


    @staticmethod
    def clear_line():
        """Limpa a linha atual do console"""
        sys.stdout.write("\033[K")

    @staticmethod
    def move_cursor(row, col):
        """Move o cursor do console para a posição especificada"""
        sys.stdout.write(f"\033[{row};{col}H")

    @staticmethod
    def color(fg=None, bg=None):
        """Muda a cor do texto e do fundo do console"""
        codes = []
        if fg:
            codes.append(f"\033[38;5;{fg}m")
        if bg:
            codes.append(f"\033[48;5;{bg}m")
        sys.stdout.write("".join(codes))

    @staticmethod
    def tab(n=1):
        """Imprime n tabulações na saída padrão"""
        for _ in range(n):
            print('\t', end='')

    @staticmethod
    def br(n: int):
        print('-' * n)

    @staticmethod
    def split_screen():
        """Divide a tela em duas seções"""
        # Obtém o tamanho da tela em linhas e colunas
        rows, columns = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        columns = int(columns)
        # Calcula a posição da divisória
        divider = columns // 2
        # Imprime a divisória
        for row in range(rows):
            if row == 0 or row == rows - 1:
                print('-' * columns)
            else:
                print('|' + ' ' * (divider - 1) + '|' + ' ' * (columns - divider - 1) + '|')

    @staticmethod
    def open_terminal_and_get_message():
        # Determinar o comando do sistema operacional para abrir o terminal
        if 'win' in sys.platform:
            command = ['cmd', '/c', 'set /p msg=Enter message: && echo !msg!']
        elif 'darwin' in sys.platform:
            command = ['osascript', '-e',
                       'tell application "Terminal" to do script "read -p \\"Enter message: \\" msg && echo $msg"']
        else:  # Linux ou outros sistemas operacionais similares ao Unix
            command = ['xterm', '-e', 'read -p "Enter message: " msg && echo $msg']

        # Executar o comando do sistema operacional para abrir o terminal e obter a mensagem
        process = subprocess.Popen( command, stdin=subprocess.PIPE, stdout=subprocess.PIPE )
        input_str = '\n'  # Enviar uma quebra de linha para iniciar a entrada do usuário
        output_str, _ = process.communicate( input=input_str.encode() )

        # Retornar a mensagem digitada pelo usuário
        message = output_str.decode().strip()
        return message