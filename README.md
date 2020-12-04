<a href="https://www.linkedin.com/in/fabiocamposgp/" target="blank"><img src="https://img.shields.io/badge/Author-Fabio%20Campos-green" /></a> <img src="https://img.shields.io/badge/python-3.7%2B-blue" />
<br>
## Problema

Imagine que você ficou responsável por construir um sistema que seja capaz de receber milhares de eventos por segundo de sensores espalhados pelo Brasil, nas regiões norte, nordeste, sudeste e sul. Seu cliente também deseja que na solução ele possa visualizar esses eventos de forma clara.

Um evento é defino por um JSON com o seguinte formato:

```json
{
   "timestamp": <Unix Timestamp ex: 1539112021301>,
   "tag": "<string separada por '.' ex: brasil.sudeste.sensor01 >",
   "valor" : "<string>"
}
```

Descrição:
 * O campo timestamp é quando o evento ocorreu em UNIX Timestamp.
 * Tag é o identificador do evento, sendo composto de pais.região.nome_sensor.
 * Valor é o dado coletado de um determinado sensor (podendo ser numérico ou string).

## Requisitos

* Sua solução deverá ser capaz de armazenar os eventos recebidos.

* Considere um número de inserções de 1000 eventos/sec. Cada sensor envia um evento a cada segundo independente se seu valor foi alterado, então um sensor pode enviar um evento com o mesmo valor do segundo anterior.

* Cada evento poderá ter o estado processado ou erro, caso o campo valor chegue vazio, o status do evento será erro caso contrário processado.

* Para visualização desses dados, sua solução deve possuir:
    * Uma tabela que mostre todos os eventos recebidos. Essa tabela deve ser atualizada automaticamente.
    * Um gráfico apenas para eventos com valor numérico.

* Para seu cliente, é muito importante que ele saiba o número de eventos que aconteceram por região e por sensor. Como no exemplo abaixo:
    * Região sudeste e sul ambas com dois sensores (sensor01 e sensor02):
        * brasil.sudeste - 1000
        * brasil.sudeste.sensor01 - 700
        * brasil.sudeste.sensor02 - 300
        * brasil.sul - 1500
        * brasil.sul.sensor01 - 1250
        * brasil.sul.sensor02 - 250

## Solução

* Tecnologia utilizada: Python
* Serviços: API para gerar os eventos, API para retornar os valores e montar a visualização e Banco de dados MySql
* Ambiente: Imagens dos serviços em container (docker-compose)

## Instalação

* Baixar ou clonar esse repositório
* Instalar o Docker
* Instalar o powershell, caso esteja utlizando o windows e não tenha o software instalado
* Não se preocupe com as dependências (pacotes Python). Todas serão devidamente instaladas ao construir as imagens com o docker-compose

## Execução

* Iniciar o Docker
* Abrir o terminal ou o powershell e navegar até a pasta onde o repositório foi criado ou clonado
* Construir as imagens com o comando: <pre>docker-compose build</pre>
* Subir as imagens com o comando: <pre>docker-compose up -d</pre>
* Certifique-se que todos os serviços estão "up" com o comando: <pre>docker-compose ps</pre>

Com o ambiente devidamente instalado e rodando, segue o passo a passo para simular os eventos.

# Disparo de eventos

A API localizada em http://localhost:3000 é a responsável por simular os disparos de eventos dos sensores. Ela trabalha com pool de processos para paralelizar as requests.

Caso queira simular um disparo de 100 eventos, por exemplo, basta utilizar a URL abaixo no seu nagevador ou no Insomnia. Ao fazer isso, a API cria um JSON randomico com os dados pré-formatados para um ou mais eventos, e dispara uma chamada POST para a API http://api-sensor:5000/get_sensor, que está na mesma network do container, e envia o JSON.

<pre>http://localhost:3000/generate/100</pre>

# Recebimento de eventos e visualização

A API localizada em http://localhost:5000 é responsável por receber o POST dos eventos, processar os JSONs, inserir os arquivos nas suas respectivas pastas, gravar os registros no banco de dados, retonar os dados através de JSON e exibir em HTML.

**A rota para receber o JSON via POST é:**
<pre>http://localhost:5000/get_sensor</pre>
**O que ela faz?** Recebe e valida o JSON, verifica se o campo valor é nulo (se for nulo, salva o arquivo na pasta files/error, caso tenha valor, salva o arquivo na pasta files/processed) e insere o registro na tabela sensores (base sensor) do banco de dados MySql.

A base, tabela, e o banco MySql já estão devidamente configurados no Docker. Caso aconteça algum problema na tabela, segue abaixo o seu esquema:
<pre>
CREATE TABLE `sensores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `regiao` varchar(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tag` varchar(45) NOT NULL,
  `valor` varchar(10) NOT NULL,
  `status` enum('Processado','Erro') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
</pre>

**A rota para visualizar os dados via GET é:**
<pre>http://localhost:5000/get_data</pre>
**O que ela faz?** Retorna um JSON com todos os eventos.

**A rota para exibir uma HTML com os dados dos eventos é:**
<pre>http://localhost:5000/view_sensor</pre>
**O que ela faz?** Retorna uma HTML com: Tabela com todos os eventos, tabela com os sensores por região e gráfico com os totalizadores de eventos por região.

Após o final da avaliação, execute o comando abaixo para paralizar a execução do docker e excluir as imagens criadas.
<pre>docker-compose down</pre>
