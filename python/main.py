from conexao import Conexao


class Main:

    def __init__(self):
        texto = "Teste de string"
        print(f"Teste gravando string {Conexao().set_string('teste1', texto)}")
        print(f"Texto recuperado: {Conexao().get_string('teste1')}")
        print(f"Teste de lista: {Conexao().set_list('minha_lista', ['cesar','ozzy','jimi','tina'])}")
        print(f"Recuperando um item da lista: {Conexao().get_item_list('minha_lista')}")
        print(f"Recuperando mais um item da lista: {Conexao().get_item_list('minha_lista')}")
        print(f"Teste de lista exclusiva {Conexao().set_set('lista',['um','dois','tres','tres','tres'])}")
        print(f"Recupera a lista exclusiva: {Conexao().get_set('lista')}")
        print(f"Gravando registros: {Conexao().set_hset('animal',1,'nome','Ozzy')}")
        print(f"Gravando registros: {Conexao().set_hset('animal',2,'nome','Tina')}")
        print(f"Gravando registros: {Conexao().set_hset('animal',3,'nome','Jimi')}")
        print(f"Recuperando registro: {Conexao().get_hset('animal', 2)}")

if __name__ == '__main__':
    Main()