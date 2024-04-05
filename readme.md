# API de Produtos e Promoções

## Descrição
Esta é uma API para gerenciar produtos e promoções, desenvolvida para a aplicação web sharedPromo. Ela oferece funcionalidades para adicionar, visualizar e remover produtos e promoções. 

## Como rodar o projeto?
Execute o comando para ativar o ambiente virtual em python  env\Scripts\activate
execute o pip install -r requirements.txt
E por final, execute localmente a api  
flask run --host 0.0.0.0 --port 5000


## Documentação
A documentação da API pode ser encontrada nas seguintes ferramentas:
- [Swagger](http://192.168.0.107:5000/openapi/swagger) - Interface interativa para explorar e testar a API.

## Endpoints

### Produtos

#### Listar Produtos
- **URL:** `GET /produtos`
- **Descrição:** Busca todos os produtos cadastrados no banco de dados.
- **Respostas:**
  - 200 OK: Retorna uma lista de produtos encontrados.
  - 404 Not Found: Retorna uma mensagem de que nenhum produto foi encontrado.

#### Buscar Produto por Nome
- **URL:** `POST /produtos/busca-por-nome`
- **Descrição:** Busca um produto pelo nome fornecido no corpo da requisição.
- **Parâmetros:**
  - `nome` (string): Nome do produto a ser buscado.
- **Respostas:**
  - 200 OK: Retorna o produto encontrado.
  - 404 Not Found: Retorna uma mensagem de que o produto não foi encontrado.

#### Cadastrar Produto
- **URL:** `POST /cadastrar-produto`
- **Descrição:** Cadastra um novo produto no banco de dados.
- **Parâmetros:**
  - `nome` (string): Nome do produto.
  - `valor` (float): Valor do produto.
  - `categoria` (string): Categoria do produto.
  - `promocao_id` (integer): ID da promoção associada ao produto.
- **Respostas:**
  - 201 Created: Retorna os dados do produto cadastrado.
  - 400 Bad Request: Retorna uma mensagem de erro se os campos obrigatórios não forem fornecidos.

#### Remover Produto
- **URL:** `DELETE /remover-produto`
- **Descrição:** Remove um produto com base no ID fornecido.
- **Parâmetros:**
  - `produto_id` (integer): ID do produto a ser removido.
- **Respostas:**
  - 200 OK: Retorna uma mensagem de confirmação de que o produto foi removido com sucesso.

### Promoções

#### Listar Promoções
- **URL:** `GET /promocoes`
- **Descrição:** Busca todas as promoções cadastradas no banco de dados.
- **Respostas:**
  - 200 OK: Retorna uma lista de promoções encontradas.
  - 404 Not Found: Retorna uma mensagem de que nenhuma promoção foi encontrada.

#### Buscar Promoção por Nome
- **URL:** `POST /promocoes/busca-por-nome`
- **Descrição:** Busca uma promoção pelo nome fornecido no corpo da requisição.
- **Parâmetros:**
  - `nome` (string): Nome da promoção a ser buscada.
- **Respostas:**
  - 200 OK: Retorna a promoção encontrada.
  - 404 Not Found: Retorna uma mensagem de que a promoção não foi encontrada.

#### Cadastrar Promoção
- **URL:** `POST /cadastrar-promocao`
- **Descrição:** Cadastra uma nova promoção no banco de dados.
- **Parâmetros:**
  - `nome` (string): Nome da promoção.
  - `divulgador` (string): Divulgador da promoção.
  - `url` (string): URL da promoção.
  - `produto_id` (lista): Id do produto associado à promoção.
- **Respostas:**
  - 201 Created: Retorna uma mensagem de confirmação de que a promoção foi cadastrada com sucesso.
  - 400 Bad Request: Retorna uma mensagem de erro se os campos obrigatórios não forem fornecidos.

#### Remover Promoção
- **URL:** `DELETE /remover-promocao`
- **Descrição:** Remove uma promoção com base no ID fornecido.
- **Parâmetros:**
  - `id` (integer): ID da promoção a ser removida.
- **Respostas:**
  - 200 OK: Retorna uma mensagem de confirmação de que a promoção foi removida com sucesso.

## Autor
Maria Isabela dos Santos Silva
Email: isa2014mgspn@gmail.com

