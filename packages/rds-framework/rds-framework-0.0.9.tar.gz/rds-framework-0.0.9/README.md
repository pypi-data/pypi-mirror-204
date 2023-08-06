# rds-framework

É uma biblioteca Python privada que condensa um conjunto de boas práticas para o desenvolvimento das aplicações que
compõem ou comporão a **RDS**  do LAIS e dos parceiros que contratarem o LAIS para fazer suas próprias RDS, a exemplo 
REDS-RN e RDS-ES. disponível apenas para usuários com com permissão no projeto 
https://github.com/lais-huol/rds-framework/ através do repositório pypi no GitHub do LAIS. 

> **RDS** é acrônimo para **Rede de Dados em Saúde**. 


## Usando em seu projeto

Entenda que, como uma biblioteca em repositório privado é necessária a autorização para usá-la, assim sendo, sempre 
que for instalar via `pip` você precisará autenticar-se no repositório do LAIS hospedado pelo GitHub.

> Aproveite e confira as 
> [versões da biblioteca](https://pypi.org/project/rds-framework/).

### Autorizando e configurando
1. A **autorização** é feita em https://git.lais.huol.ufrn.br/-/profile/personal_access_tokens , veja como criar o 
[token de acesso pessoal](https://git.lais.huol.ufrn.br/help/user/profile/personal_access_tokens) na a documentação 
oficial do GitHub. Lembre de que deve ter ao menos o escopo api, este token pode ser usado para pacotes Python 
(libraries) ou Docker (imagens). Nome sugerido: `pacotes`.
2. Assumindo que o token gerado seja `ACCESS-TOKEN`, crie o arquivo `.pip/pip.conf` na pasta home do seu usuário, 
conforme exemplo abaixo:

> Atenção para o `909` nesta URL, isso é o que identifica de qual projeto no GitHub o arquivo será baixado, ou seja, 
> serve para esta biblioteca apenas, assim sendo, caso você queira usar outra bibliteca dos nossos repostitório será 
> necessário configurar para o ID do projeto correto.

Feito isso o teu ambiente estará configurado e autorizado no repositório deste projeto no GitHub do LAIS.

### Usando no seu projeto 

Agora vamos ver como configurar isso no seu projeto, supondo que você use um arquivo `requirements.txt` em Linux, tente
o comando abaixo

```
echo 'rds-framework==0.1.2' >> requirements.txt
```

Agora é só instalar normalmente usando `pip install -r requirements.txt`, como sempre.

## Contribuíndo com o desenvolvimento do framework

> Aqui entende-se que o ambiente já esteja configurado para fazer acesso usando SSH ao repositório git do GitHub.

> Daqui para frente entende-se o uso do Linux ou Mac. Fique à vontade para documentar para Windows. 

1. Clone o projeto **rds-search** `git@github.com:lais-huol/rds-framework.git` para ter uma
instância de desenvolvimento do OpenSearch, do OpenSearch Dashboards e do Redis (mais instruções no próprio projeto)
2. Deixe o **rds-search** com o OpenSearch e o Redis em execução: `cd rds-search; _/restart;cd ..`
3. Clone o projeto `git clone git@github.com:lais-huol/rds-framework.git`
4. Entre na página do código `cd rds-framework`
5. Crie um ambiente virtual usando `mkvirtualenv rds-framework` ou uma das formas que você está aconstumado a usar 
6. Instale os pacotes `pip install -r requirements` neste ambiente virtual
7. Crie um branch para a issue de trabalho, no exemplo de ser a issue 4: `git checkout -b issue4`  
8. Codifique como de costume
9. Antes de fazer um push para o GitHub confira a qualidade do código (todos serão gerados e salvos no servidor):
   1. Confira se o código está bem formatado: `flake8`. A meta não haver mensagem alguma
   2. Confira se a tipagem do código está boa: `mypy rds_framework`. A meta não haver mensagem alguma
   3. Confira se todos os testes passam: `python -m pytest`. A meta é cobertura superior a 92% e sucesso nos testes de 100%
10. Crie um Merge Request para a branch `main` e atribua a `kelson.medeiros`

## Dicas

1. Para saber se a documentação pydocs `pdoc --html -o artifacts/pydocs --config show_source_code=False --force rds/`
2. Ao subir o código a documentação está pública em .
3. A versão pública da documentação fica disponível em http://barramento.pages.lais.huol.ufrn.br/rds-framework/

## Tipo de commits

- `feat:` novas funcionalidades.
- `fix:` correção de bugs.
- `refactor:` refatoração ou performances (sem impacto em lógica).
- `style:` estilo ou formatação de código (sem impacto em lógica).
- `test:` testes.
- `doc:` documentação no código ou do repositório.
- `env:` CI/CD ou settings.
- `build:` build ou dependências.