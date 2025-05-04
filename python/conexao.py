from redis.sentinel import Sentinel
from typing import List
import json

class Conexao:


    def __init__(self):
        self.host = '192.168.123.201'
        self.port = 6379
        self.password = 'J51QEot4fiXS1Ow'
        self.user = 'default'
        self.conexao = None


    def __get_conexao(self) -> Sentinel.master_for:
        """
        Obtém uma conexão com o master do Redis Sentinel.
        Este método cria uma instância de Sentinel, conecta-se ao master identificado
        pelo nome 'mymaster' e retorna a conexão configurada. Caso ocorra algum erro
        durante o processo, o método captura a exceção, exibe uma mensagem de erro
        e retorna None.
        Returns:
            redis.client.Redis: Objeto de conexão com o master do Redis Sentinel,
            ou None em caso de falha.
        """
        try:
            sentinel = Sentinel(
                [(self.host, self.port)],
                socket_timeout=0.1,
            )
            self.conexao = sentinel.master_for('mymaster', db=0, password=self.password, decode_responses=True)
            return self.conexao
        except Exception as e:
            print(f'get_conexao', e)
            return None
        
        
    def __close(self) -> bool:
        """
        Fecha a conexão com o banco de dados Redis.
        Returns:
            bool: Retorna True se a conexão foi fechada com sucesso, 
            caso contrário, retorna False.
        """
        try:
            self.conexao.close()
            return True
        except Exception as e:
            print(f'close', e)
            return False
        
        
    def set_string(self, chave: str, valor: str, expira: int = None) -> bool:
        """
        Define uma chave e um valor no banco de dados Redis.
        Este método armazena uma string no Redis associada a uma chave específica.
        Caso a conexão com o Redis ainda não esteja estabelecida, ela será criada
        automaticamente. Em caso de falha, uma mensagem de erro será exibida e o
        método retornará False.
        Params:
            chave (str): A chave que será usada para armazenar o valor no Redis.
            valor (str): O valor que será armazenado no Redis.
            expira (int): valor em segundos para expirar o conteúdo no Redis.
        Returns:
            bool: Retorna True se a operação for bem-sucedida, caso contrário, False.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            return self.conexao.set(chave, valor) if expira is None else self.conexao.set(chave, valor, ex=expira)
        except Exception as e:
            print('set_string', e)
            return False
        finally:
            self.__close()


    def get_string(self, chave: str) -> str:
        """
        Recupera uma string armazenada no Redis a partir de uma chave fornecida.
        Este método tenta obter uma conexão com o Redis, recupera o valor associado
        à chave fornecida e o decodifica para o formato UTF-8. Caso ocorra algum erro
        durante o processo, ele captura a exceção, exibe uma mensagem de erro e retorna None.
        Params:
            chave (str): A chave para buscar o valor armazenado no Redis.
        Returns:
            str: O valor associado à chave, decodificado como uma string UTF-8.
            None: Retorna None caso ocorra algum erro ou a chave não exista.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            return self.conexao.get(chave)
        except Exception as e:
            print('get_string',e)
            return None
        finally: 
            self.__close()


    def set_list(self, chave: str, lista: List[str]) -> bool:
        """
        Adiciona uma lista de strings a uma chave no Redis.
        Permite itens duplicados.
        Params:
            chave (str): A chave no Redis onde a lista será armazenada.
            lista (List[str]): A lista de strings a ser adicionada à chave.
        Returns:
            bool: Retorna `True` se a operação for bem-sucedida, ou `False` em caso
            de falha.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            self.conexao.rpush(chave, *lista)
            return True
        except Exception as e:
            print('set_list', e)
            return False
        finally:
            self.__close()

    
    def get_item_list(self, chave: str) -> str:
        """
        Recupera e remove o primeiro item de uma lista armazenada no Redis.
        Caso ocorra algum erro, ele imprime o erro e
        retorna None.
        Params:
            chave (str): A chave associada à lista no Redis.
        Returns:
            str: O primeiro item da lista como uma string, ou None se ocorrer um erro.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            return self.conexao.lpop(chave)
        except Exception as e:
            print('get_item_list', e)
            return None
        finally:
            self.__close()


    def set_set(self, chave: str, lista: List[str]) -> bool:
        """
        Adiciona múltiplos valores a um conjunto no Redis.
        Este método grava somente valores exclusivos na lista.
        Params:
            chave (str): A chave do conjunto no Redis.
            lista (List[str]): Uma lista de strings contendo os valores a serem adicionados ao conjunto.
        Returns:
            bool: Retorna `True` se os valores forem adicionados com sucesso ao conjunto,
                  ou `False` em caso de falha.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            self.conexao.sadd(chave, *lista)
            return True
        except Exception as e:
            print('set_set', e)
            return False
        finally:
            self.__close()

    
    def get_set(self, chave: str) -> list:
        """
        Recupera todos os membros de um conjunto (set) armazenado no Redis.
        Params:
            chave (str): A chave do conjunto no Redis.
        Returns:
            list: Uma lista contendo os membros do conjunto, ou None em caso de erro.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            return self.conexao.smembers(chave)
        except Exception as e:
            print('get_set', e)
            return []
        finally:
            self.__close()


    def set_hset(self, chave: str, id: int, atributo: str, valor: str) -> bool:
        """
        Define um valor em um hash no Redis, que é uma coleção de atributos
        para um registro identificado pela chave (coleção) e seu id.
        Params:
            chave (str): A chave base do hash no Redis.
            id (int): O identificador único que será concatenado à chave base.
            atributo (str): O campo do hash onde o valor será armazenado.
            valor (str): O valor a ser armazenado no campo especificado.
        Returns:
            bool: Retorna True se a operação for bem-sucedida, caso contrário, False.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            chave = str(chave) + ':' + str(id)
            self.conexao.hset(chave, atributo, valor)
            return True
        except Exception as e:
            print('set_hset', e)
            return False
        finally:
            self.__close()


    def get_hset(self, chave: str, id: int) -> dict:
        """
        Recupera todos os campos e valores de um hash armazenado no Redis
        associados a uma chave específica no formato "chave:id".
        Params:
            chave (str): A chave base do hash no Redis.
            id (int): O identificador único que será concatenado à chave base.
        Returns:
            dict: Um dicionário contendo os campos e valores do hash no Redis.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            chave = str(chave) + ':' + str(id)
            return self.conexao.hgetall(chave)
        except Exception as e:
            print('get_hset', e)
            return {}
        finally:
            self.__close()


    def delete(self, chave: str, id: int=None) -> bool:
        """
        Remove uma chave do Redis.
        Este método exclui uma chave específica do Redis. Caso um `id` seja fornecido, 
        ele será concatenado à chave antes da exclusão.
        Params:
            chave (str): A chave a ser removida do Redis.
            id (int, opcional): Um identificador adicional que será concatenado à chave. 
                Padrão é None.
        Returns:
            bool: Retorna True se a chave foi removida com sucesso, caso contrário, False.
        """
        try:
            if self.conexao is None:
                self.conexao = self.__get_conexao()
            if id is not None:
                chave = str(chave) + ':' + str(id)
            self.conexao.delete(chave)
            return True
        except Exception as e:
            print('delete', e)
            return False
        finally:
            self.__close()