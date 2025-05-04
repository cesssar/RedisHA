# Redis modo master/slave

Este repositório é um projeto para utilizar o Redis em modo réplica via Docker utilizando servidores separados e um proxy (HAProxy). Está organizado para cada nós redis executar em um servidor com Docker, bem como o HAProxy em outro. Também executa o Redis Sentinel, que monitora os nós Redis e elege um novo master se o atual cair.

É possível adaptar para rodar em menos servidores ou até mesmo em um somente, porém as portas do Redis e do HAProxy precisam ser ajustadas.

Com a estrutura proposta o cluster pode perder um servidor de três e continuará operando. Assim que este servidor voltar a responder os dados são replicados novamente mantendo todos os nós com dados replicados.

## ✅ Vantagens

1. Alta Disponibilidade com Sentinel
Os Sentinels monitoram o nó master e iniciam a eleição de um novo master automaticamente em caso de falha, garantindo failover automático.

Redis Sentinel também atualiza os clientes com a nova topologia após um failover indicando qual é o master atual. Desta forma os nós Redis são automaticamente reconfigurados sem necessidade de reiniciar.

2. Isolamento via Docker
Cada componente (Redis, HAProxy, Sentinel) roda isoladamente, facilitando manutenção, upgrades e implantações.

Docker facilita a portabilidade entre ambientes e o uso de ferramentas de orquestração como Docker Compose ou Kubernetes.

3. Tolerância a Falhas
Mesmo se um dos nós Redis ou servidores físicos cair, o cluster pode continuar operando com os outros nós e redistribuir o papel de master se necessário.

4. Gerenciamento Centralizado de Acesso
O HAProxy atua como um ponto único de entrada, simplificando a configuração de clientes e roteamento de requisições.

## ❌ Desvantagens

1. HAProxy como Ponto Único de Falha (SPOF)
A menos que você use mais de uma instância de HAProxy com alta disponibilidade (por exemplo, com Keepalived ou um LoadBalancer externo), ele se torna um ponto único de falha.

2. Latência e Complexidade com Docker
A sobrecarga de rede e I/O do Docker (especialmente sem configuração adequada de volumes persistentes e rede bridge) pode impactar o desempenho.
Problemas como "split brain" podem ocorrer se os Sentinels perderem conectividade entre si ou com os Redis por problemas de rede interna nos containers.

3. Replicação Assíncrona
Redis utiliza replicação assíncrona, o que significa que em caso de falha do master, alguns dados podem ser perdidos se ainda não foram replicados para os slaves.

## Estrutura do projeto

O projeto está organizado nos diretórios abaixo para facilitar a separação dos arquivos necessários para execução. Abaixo a estrutura e comentários do que é necessário ajustar para o ambiente onde será executado.

```
Projeto
|
├── haproxy/
|   ├── docker-compose.yaml     # aplicar no servidor que será o proxy
|   ├── haproxy.cfg             # ajustar com os IP dos servidores Redis e a senha
├── nodes/
|   ├── master/
|   |   ├── redis.conf          # ajustar a senha
|   ├── nodes/
|   |   ├── redis.conf          # ajustar a senha e também o IP do master
|   ├── sentinel-data/
|   |   ├── sentinel.conf       # ajustar com o IP do master
|   ├── docker-compose.yaml     # aplicar em todos os servidores que irão executar o Redis
├── redisweb/
|   ├── docker-compose.yaml     # aplicar no servidor ou máquina local para interface web
```

## Requisitos

Mínimo de quatro servidores Linux executando a engine do Docker. Sendo:
- 1 servidor para o proxy
- 1 servidor para o master inicial
- 2 servidores para os nós

Este projeto foi testado utilizando quatro máquinas virtuais iguais com as seguintes configurações:

- Ubuntu Server 22.04.5 LTS (instalação completa padrão)
- 4GB de RAM
- 2 vCPU
- placa de rede em modo NAT
- IP fixado no arquivo de configuração netplan
- engine Docker versão 28.1.1

## Executando o projeto

Para o servidor que será o Redis master, copiar o arquivo redis.conf da pasta master e o docker-compose.yaml da pasta nodes. 
Executar o docker-compose:

```
docker-compose up -d
```

Para os servidores que serão os nós do Redis, copiar o arquivo redis.conf da pasta nodes e o docker-compose.yaml da pasta nodes.
Executar o docker-compose:

```
docker-compose up -d
```

Para o servidor que será o proxy, copiar a pasta haproxy com seu conteúdo e executar o docker-compose:

```
docker-compose up -d
```

E executar o docker-compose da pasta redisweb para iniciar o cliente web que manipula o banco de dados Redis.


## Redis Insight

Para visualizar e manipular o banco de dados é possível utilizar o Redis Insight com interface web conectando o mesmo no proxy.

Acesse o Redis Insight:

http://IP do servidor ou localhost:5540

No primeiro acesso aceite os termos.
Depois clique em + Add Redis database e em seguida no botão Connection Settings

![add redis database](https://github.com/cesssar/RedisHA/blob/main/screenshots/redis1.png)

![connection settings](https://github.com/cesssar/RedisHA/blob/main/screenshots/redis2.png)

Preencha os campos:
- Database Alias: qualquer nome para a conexão
- Host: IP do servidor onde está sendo executado o proxy
- Port: 6379 ou outra se o arquivo haproxy.cfg foi alterado
- Password: senha do Redis gravado no arquivo redis.conf

Clique no botão Test Connection para validar as informações.

![test connection](https://github.com/cesssar/RedisHA/blob/main/screenshots/redis3.png)

Se houve algum erro, revise as informações preenchidas. Se sucesso clique em Add Redis Database.


A interface irá localizar o Redis Sentinel e a configuração do master atual. Configure o campo Username para default e o campo Password para a senha do Redis. Selecione a configuração e clique em Add Primary Group.

![add primary group](https://github.com/cesssar/RedisHA/blob/main/screenshots/redis4.png)

Voltando para a tela inicial a conexão com o Redis estará disponível, basta clicar sobre al para ver os dados existentes no Rdis e também para inserir novos.

![add primary group](https://github.com/cesssar/RedisHA/blob/main/screenshots/redis5.png)

![add primary group](https://github.com/cesssar/RedisHA/blob/main/screenshots/redis6.png)

## Avaliando o cluster

Para avaliar o desempenho de um cluster Redis por meio de um HAProxy usando a ferramenta redis-benchmark, você pode seguir os passos abaixo. O redis-benchmark é uma ferramenta nativa do Redis para testes de carga e desempenho.

O redis-benchmark é instalado juntamente com o Redis Clinet ou com o Redis Server.

Comando para testar o cluster (pode-se alter o número de conexões e requisições para avaliar capacidade e/ou avaliar desempenho para uma realidade aproximada de um ambiente de produção):

```
redis-benchmark -h 192.168.123.201 -p 6379 -a J51QEot4fiXS1Ow -c 100 -n 100000 -d 256 -t set,get

```

-h 192.168.1.100: IP do HAProxy

-p 6379: Porta do HAProxy

-a J51QEot4fiXS1Ow: Senha do Redis

-c 100: Número de conexões simultâneas

-n 100000: Total de requisições

-d 256: Tamanho dos dados em bytes por operação

-t set,get: Tipos de comandos testados


Na saída do comando procure pelo resumo das escritas (SET) e leituras (GET):

====== SET ======
  100000 requests completed in 3.09 seconds
  100 parallel clients
  256 bytes payload
  keep alive: 1
  multi-thread: no

====== GET ======
  100000 requests completed in 3.22 seconds
  100 parallel clients
  256 bytes payload
  keep alive: 1
  multi-thread: no

Ele também exibe quantas requisições foram realizadas por segundo.
Por exemplo na leitura (GET) foram processadas 30165.91 requisições por segundo com a instação informada.

## Referências

https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/
https://redis.io/
https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-linux/
https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-windows/
