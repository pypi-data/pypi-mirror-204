import io
import sys

# Codigo legado


class SequestraConsole:
    def __init__(self):
        self.ultima_linha: list = []

    def sequestar_console(self):
        def decorator(func):
            def enpacotador(*args, **kwargs):
                out = io.StringIO()
                sys.stdout = out
                func(*args, **kwargs)
                sys.stdout = sys.__stdout__
                output = out.getvalue()
                print(output)
                self.ultima_linha = self._out_para_lista(output)
            return enpacotador
        return decorator

    def _out_para_lista(self, out) -> list[str]:
        return list(
            filter(
                bool,
                out.split('\n')
            )
        )
