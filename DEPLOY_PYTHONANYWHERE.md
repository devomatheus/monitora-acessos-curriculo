# Instruções de Deploy no PythonAnywhere

Este guia descreve como colocar a aplicação Flask (`main.py`) em produção no PythonAnywhere, considerando o estado atual do projeto: uso de `pathlib`, variáveis de ambiente via `python-dotenv`, logs em arquivo com `loguru` e CORS configurável.

## 1. Enviar os arquivos para o PythonAnywhere

Com sua conta já criada, acesse a aba **Files** do painel do PythonAnywhere e envie (ou clone via Git) os seguintes arquivos do projeto para uma pasta, por exemplo `/home/seu_usuario/visualizando`:

- `main.py`
- `requirements.txt`

Não é necessário enviar a pasta `venv` nem o arquivo `.env` local — eles serão recriados diretamente no servidor (veja os passos 3 e 5).

Se preferir usar Git, abra um **Bash console** no PythonAnywhere e rode:

```bash
git clone <url-do-seu-repositorio> visualizando
```

## 2. Criar um virtualenv no servidor

Ainda no **Bash console** do PythonAnywhere:

```bash
cd ~/visualizando
mkvirtualenv --python=/usr/bin/python3.11 visualizando-venv
```

> Ajuste a versão do Python conforme a disponível na sua conta (verifique em **Account > Language**).

## 3. Instalar as dependências

Com o virtualenv ativo (o `mkvirtualenv` já ativa automaticamente):

```bash
pip install -r requirements.txt
```

## 4. Criar a Web App

1. Vá até a aba **Web** e clique em **Add a new web app**.
2. Escolha **Manual configuration** (não use o assistente automático do Flask, pois o projeto já está estruturado manualmente).
3. Selecione a mesma versão de Python usada no virtualenv.

## 5. Configurar variáveis de ambiente

Ainda na aba **Web**, na seção **Environment variables**, adicione:

| Nome                 | Valor                          |
|----------------------|---------------------------------|
| `FLASK_DEBUG`        | `false`                         |
| `ORIGENS_PERMITIDAS` | domínio(s) real(is) do front-end, separados por vírgula (ex: `https://meusite.com`) — evite deixar `*` em produção |

Como o `main.py` já chama `load_dotenv()`, essas variáveis também podem ser definidas em um arquivo `.env` dentro de `/home/seu_usuario/visualizando`, mas o método acima (Environment variables do painel) é o recomendado pelo PythonAnywhere para produção.

## 6. Apontar o virtualenv

Na aba **Web**, seção **Virtualenv**, informe o caminho:

```
/home/seu_usuario/.virtualenvs/visualizando-venv
```

## 7. Configurar o arquivo WSGI

Ainda na aba **Web**, clique no link do arquivo WSGI (algo como `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`) e substitua o conteúdo por:

```python
import sys

path = '/home/seu_usuario/visualizando'
if path not in sys.path:
    sys.path.append(path)

from main import app as application
```

> Isso funciona porque `main.py` expõe o objeto Flask na variável `app`, e o WSGI do PythonAnywhere espera uma variável chamada `application`.

## 8. Verificar a pasta de logs

A aplicação grava logs em `logs/app.log`, dentro da própria pasta do projeto (`BASE_DIR / "logs" / "app.log"`, calculado via `pathlib`). Essa pasta é criada automaticamente pelo `loguru` na primeira execução — não é necessário criá-la manualmente.

## 9. Recarregar a aplicação

De volta à aba **Web**, clique no botão verde **Reload seu_usuario.pythonanywhere.com**.

## 10. Testar

- `POST https://seu_usuario.pythonanywhere.com/visualizado` com os parâmetros `nome` e `texto` (form-data ou query string).
- `GET https://seu_usuario.pythonanywhere.com/logs` para conferir os logs registrados.

## Checklist rápido de produção

- [ ] `FLASK_DEBUG=false` configurado (nunca deixar `true` em produção).
- [ ] `ORIGENS_PERMITIDAS` restrito ao(s) domínio(s) real(is), sem usar `*`.
- [ ] Virtualenv apontado corretamente na aba **Web**.
- [ ] Arquivo WSGI configurado com `from main import app as application`.
- [ ] Aplicação recarregada após qualquer alteração de código ou variável de ambiente.
