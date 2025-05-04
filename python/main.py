from conexao import Conexao


class Main:

    def __init__(self):
        Conexao().delete('nome')
        Conexao().delete('pessoa',2)
        Conexao().delete('pessoa',3)

if __name__ == '__main__':
    Main()