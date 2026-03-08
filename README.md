# BillMind

Um bot simples que notifica por WhatsApp o valor estimado das faturas e o progresso em relação a metas semanais.

## 📦 Requisitos

- Python 3.10+ instalado
- PostgreSQL disponível e acessível
- Chrome ou Firefox e o respectivo WebDriver (ex: chromedriver) no PATH

## ⚙️ Instalação

1. Copie `.env.example` para `.env` e ajuste variáveis de ambiente.
2. Crie e ative um virtualenv:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
3. Instale dependências:
   ```powershell
   pip install -r requirements.txt
   ```
4. Inicialize o banco de dados:
   ```powershell
   python -m billmind.main initdb
   ```

## 🚀 Uso

Antes de disparar o relatório você precisa ter pelo menos* uma meta semanal e
uma mensal, além de algumas faturas cadastradas. Você pode inserir dados
diretamente via SQL ou usar sessões do SQLAlchemy no REPL. Exemplo rápido:

```python
from billmind import db, models
from billmind.config import settings
from datetime import date, timedelta

session = db.SessionLocal()
# meta semanal
week_start = date.today()
week_end = week_start + timedelta(days=6)
session.add(models.MetaSemanal(valor_meta=5000, semana_inicio=week_start, semana_fim=week_end))
# meta mensal (mês e ano atuais)
session.add(models.MetaMensal(valor_meta=20000, ano=week_start.year, mes=week_start.month))
# adicionar um banco e fatura fictícia
banco = models.Banco(nome="Banco Exemplo")
cartao = models.Cartao(banco=banco, numero="1234 5678 9012 3456")
session.add(cartao)
session.add(models.Fatura(cartao=cartao, valor_estimado=123.45, data_obtencao=week_start))
session.commit()
session.close()
```
- Enviar relatório imediato:
  ```powershell
  python -m billmind.main send
  ```
- Iniciar o agendador (08:00 e 20:00 locais):
  ```powershell
  python -m billmind.main run
  ```
  *(mantém-se rodando até Ctrl+C)*

## 🛠️ Desenvolvimento

- Scripts devem ser adicionados em `billmind/`.
- Testes em `tests/` e executados via `pytest`.

### 📡 Integração com Banco do Brasil

Você pode usar a API oficial do Banco do Brasil para obter o valor da fatura
automaticamente em vez de fazer scraping ou inserir manualmente. Para isso:

1. Registre um aplicativo no portal de desenvolvedores do BB e obtenha as
   credenciais (``client_id`` e ``client_secret``).
2. Faça download do certificado de cliente (MTLS) e coloque o caminho em
   ``BB_CERT_PATH`` no seu `.env`.
3. Adicione as variáveis ao `.env`:

    ```ini
    BB_CLIENT_ID=seu_id
    BB_CLIENT_SECRET=sua_chave
    BB_CERT_PATH=C:\caminho\para\certificado.pem
    ```

4. Use o módulo `billmind.bb_api` para buscar e gravar o valor da fatura:

    ```powershell
    python -m billmind.bb_api <account_id>
    # ou acionar programaticamente:
    from billmind import bb_api, db, models
    session = db.SessionLocal()
    cartao = session.query(models.Cartao).first()
    bb_api.update_invoice_in_db("<account_id>", cartao)
    ```

   O ``account_id`` é fornecido pelo BB quando você consulta as contas do
   cliente via a própria API.

5. Agende essa chamada junto com o agendador principal ou como tarefa
   separada; por exemplo, adicione import e execução em
   ``billmind/scheduler.py``.

> **Segurança:** guarde suas credenciais em variáveis de ambiente e nunca poste
> o certificado em código público.

> **Observação:** os endpoints e payloads exatos podem mudar; adapte o código
> do módulo ``bb_api.py`` de acordo com a documentação oficial.

> **Nota:** o Selenium abrirá o navegador na primeira execução para você escanear o QR
> do WhatsApp Web. Use um perfil de usuário persistente para não precisar repetir isso.
BillMind é um aplicativo para monitoramento de gastos mensais, para nunca sair da planilha, mesmo para quem não tem o hábito de olhar o banco todos os dias. O nome é bem intuitivo, Bill = Conta e Mind = Mente, para o valor devido nunca sair da sua cabeça!
