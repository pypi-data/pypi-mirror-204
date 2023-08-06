import os
import sys


class Console:
    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def clear():
        """Limpa o console"""
        os.system('clear' if os.name == 'posix' else 'cls')

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