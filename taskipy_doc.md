# Taskipy — Comandos configurados

Este arquivo descreve os comandos definidos na seção `[tool.taskipy.tasks]` do `pyproject.toml` e mostra como executá-los localmente usando `task`.

Nota: Todos os comandos do Taskipy que apresentam prefixos `pre_` ou `post_` não precisam ser executados diretamente. Por exemplo, ao executar `task test`, o Taskipy executará automaticamente `pre_test` antes de `test` e, se tudo ocorrer sem erros, executará `post_test` depois.

## Comandos disponíveis

As tarefas listadas abaixo são as definidas no `pyproject.toml` deste projeto.

- lint
  - Comando: `ruff check`
  - Descrição: Executa o linter/cheque estático de código (`ruff`) para identificar problemas de estilo, erros simples e avisos.

- pre_format
  - Comando: `ruff check --fix`
  - Descrição: Roda o `ruff` em modo de correção automática para aplicar correções que o `ruff` consegue fazer. Geralmente usado como etapa prévia antes de formatar.

- format
  - Comando: `ruff format`
  - Descrição: Formata o código conforme as regras do `ruff.format` configuradas no `pyproject.toml`.

- run
  - Comando: `fastapi dev src/app.py`
  - Descrição: Executa a aplicação FastAPI em modo de desenvolvimento.
  - Observação: Este comando presume que o utilitário `fastapi` (provavelmente `uvicorn` ou `fastapi[standard]`) está disponível no ambiente. Pode também ser substituído por `uvicorn src.app:app --reload` se preferir executar explicitamente o servidor.

- pre_test
  - Comando: `task lint`
  - Descrição: Tarefa que roda `lint` antes de `test`. Note que aqui a pre-tarefa usa o `task` para invocar outra tarefa do Taskipy.

- test
  - Comando: `pytest -s -x --cov=src -vv`
  - Descrição: Executa os testes com `pytest`, mostrando saída detalhada, saindo no primeiro erro, e medindo cobertura para a pasta `src`.

- post_test
  - Comando: `coverage html`
  - Descrição: Gera um relatório HTML de cobertura após a execução dos testes (chamado automaticamente se os testes tiverem sucesso).

## Como executar os comandos

Instale as dependências do projeto usando o gerenciador `uv`.

Observação: existem variações de comandos dependendo da versão do `uv` e de como o projeto está configurado. Abaixo seguem duas abordagens comuns; use a que corresponde ao seu fluxo de trabalho com `uv`.

Opção A — usar um ambiente gerenciado pelo `uv` e instalar dependências de desenvolvimento:

```bash
# criar/ativar o ambiente (comandos dependem da instalação do uv)
uv sync
source .venv/bin/activate # Ou abra um novo terminal integrado no vscode.
```

Se o seu `uv` não suportar exatamente os flags acima, use o `pip` diretamente como fallback:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev]
```

Executar uma tarefa do Taskipy (exemplo):

```bash
# rodar o linter
task lint

# formatar o código
task format

# rodar a aplicação em desenvolvimento
task run

# executar testes (executará pre_test -> test -> post_test)
task test
```

## Sugestões e observações

- Se `task` não estiver instalado, instale com `pip install taskipy` ou via `pip install -e .[dev]` (se o `pyproject.toml` estiver configurado com extras).
- O comando `run` pode variar conforme preferência. Se usar `uvicorn`, um equivalente é:

```bash
uvicorn src.app:app --reload
```

- O `pre_format` foi configurado como `ruff check --fix`, que tenta corrigir automaticamente problemas detectáveis. Depois dele, você pode rodar `task format` para aplicar o formatador do `ruff`.

## Links úteis

- Ruff: https://github.com/charliermarsh/ruff
- Taskipy: https://github.com/arthurdejong/taskipy
- Pytest: https://docs.pytest.org/

---

Arquivo gerado automaticamente para documentar os comandos do Taskipy definidos em `pyproject.toml`.
