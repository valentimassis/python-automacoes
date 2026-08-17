# Fase 01 — SMB Collector

## Windows File Server Auditor

**Status:** Concluída

**Commit:** `507cc6a` — `implementando SMB collector com PowerShell`

---

## 1. Objetivo

Construir a primeira parte funcional do Windows File Server Auditor:

- conectar a um servidor Windows;
- autenticar com uma conta administrativa quando necessário;
- executar comandos remotamente via PowerShell/WinRM;
- coletar os compartilhamentos SMB;
- transformar o resultado em objetos Python;
- criar testes automatizados.

Servidor utilizado nos testes:

2. Arquitetura

Durante a implementação foi decidido separar as responsabilidades entre Python e PowerShell.

Python

Responsável por:

estrutura da aplicação;
modelos de dados;
collectors;
tratamento dos dados;
testes;
futura análise;
geração de relatórios.
PowerShell

Responsável por:

interação com recursos nativos do Windows;
autenticação;
execução remota;
coleta de informações SMB.

Arquitetura atual:
Python
   │
   ▼
SMB Collector
   │
   ▼
PowerShell
   │
   ├── Get-Credential
   │
   └── Invoke-Command
          │
          ▼
       lst-fs01
          │
          ▼
     Get-SmbShare
          │
          ▼
         JSON
          │
          ▼
        Python
          │
          ▼
      list[Share]

      3. Estrutura do projeto

A estrutura adotada ficou:
src/
└── wfsa/
    ├── __init__.py
    │
    ├── collectors/
    │   ├── __init__.py
    │   └── smb.py
    │
    ├── models/
    │   ├── __init__.py
    │   └── share.py
    │
    └── powershell/
        ├── __init__.py
        └── smb_shares.ps1
        tests/
├── test_share.py
└── test_smb.py

4. Ambiente Python

Foi criado um ambiente virtual:

.venv

Python utilizado:

Python 3.14.7

pytest:

pytest 9.1.1

O projeto utiliza:

pyproject.toml

e foi instalado em modo editable:

pip install -e .

Isso permitiu importar os módulos utilizando:

from wfsa.models.share import Share
5. Modelo Share

O modelo representa um compartilhamento SMB.

Arquivo:

src/wfsa/models/share.py

Implementação:

from dataclasses import dataclass




@dataclass
class Share:
    """Representa um compartilhamento SMB de um servidor Windows."""


    name: str
    path: str
    description: str
    share_type: str

Exemplo:

Share(
    name="Financeiro$",
    path=r"E:\Shares\Financeiro",
    description="Financeiro",
    share_type="FileSystemDirectory",
)
6. Validação da conexão

Antes de executar a coleta, foram realizados testes progressivos.

Identificar usuário
whoami

Resultado utilizado nos testes:

LST-DOMAIN\valentim.assis
Verificar domínio
$env:USERDOMAIN

Resultado:

LST-DOMAIN
Verificar usuário
$env:USERNAME

Resultado:

valentim.assis
Testar WinRM
Test-WSMan lst-fs01

O teste funcionou.

7. Conectividade x autorização

Foi testado:

Invoke-Command -ComputerName lst-fs01 -ScriptBlock {
    Get-SmbShare
}

Com o usuário normal, o servidor retornou:

Access is denied

Isso mostrou uma diferença importante:

Conectividade não significa autorização.

O Test-WSMan funcionar significa que a comunicação com o WinRM está disponível.

Isso não significa que o usuário tenha permissão para executar o comando remotamente.

Com uma conta administrativa/DA, o Invoke-Command funcionou.

8. Autenticação com Get-Credential

Para não colocar senha diretamente no código, foi utilizado:

$Credential = Get-Credential

A execução remota utiliza:

Invoke-Command `
    -ComputerName lst-fs01 `
    -Credential $Credential `
    -ScriptBlock {
        Get-SmbShare
    }

A senha não fica armazenada no código-fonte.

Requisito para produção

Ainda deverá ser definido um mecanismo seguro para execução automatizada.

Possibilidades futuras:

conta de serviço;
permissões mínimas;
Windows Credential Manager;
Secret Store;
execução agendada;
outro mecanismo seguro de armazenamento de credenciais.

Não utilizar senhas hardcoded.

9. PowerShell

O script foi separado do código Python.

Arquivo:

src/wfsa/powershell/smb_shares.ps1

Responsabilidade:

Coletar os compartilhamentos SMB do servidor Windows e retornar os dados em JSON.

A coleta utiliza:

Get-SmbShare

e:

ConvertTo-Json
10. ShareType

Foi identificado um comportamento importante durante a serialização.

Diretamente no PowerShell:

Get-SmbShare

pode apresentar:

ShareType : FileSystemDirectory

Porém, ao converter diretamente para JSON, o enum poderia aparecer como:

"ShareType": 0

Para preservar o valor legível foi utilizado:

$_.ShareType.ToString()

Assim o Python recebe:

"ShareType": "FileSystemDirectory"
11. Collector Python

Arquivo:

src/wfsa/collectors/smb.py

O collector utiliza Python para executar o PowerShell e processar o JSON.

Fluxo:

PowerShell
    ↓
JSON
    ↓
json.loads()
    ↓
Share(...)

O objetivo é manter a integração com Windows no PowerShell e a lógica da aplicação no Python.

12. Encoding UTF-8

Durante os testes foi identificado um problema com caracteres acentuados.

Exemplo esperado:

formalização
operações

Inicialmente o Python recebia valores corrompidos semelhantes a:

formaliza€Ço
opera€åes

Foi investigado o fluxo de bytes entre PowerShell e Python.

Foi validada a utilização de UTF-8 explícito:

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Também foi validada a leitura em Python utilizando UTF-8.

Resultado:

formalização
operações

passaram a ser recebidos corretamente.

Aprendizado

Em integrações entre Windows, PowerShell e Python, encoding precisa ser tratado explicitamente quando houver caracteres fora de ASCII.

13. Testes automatizados

Foram criados dois testes.

Teste do modelo

Arquivo:

tests/test_share.py

Valida a criação e os atributos do objeto Share.

Teste do collector

Arquivo:

tests/test_smb.py

Valida o comportamento do collector.

Execução:

python -m pytest

Resultado:

collected 2 items


tests\test_share.py .   [ 50%]
tests\test_smb.py .     [100%]


2 passed
14. Teste real contra o servidor

Após validar os testes automatizados, foi realizada uma coleta real no servidor:

python -c "from wfsa.collectors.smb import get_shares; shares = get_shares('lst-fs01'); print(f'Total: {len(shares)}'); print(*shares[:3], sep='\n')"

Resultado:

Total: 74

Exemplos coletados:

Share(
    name='002 - fornecedor$',
    path='E:\\shares\\scd\\formalização - checagem\\operações\\002 - fornecedor',
    description='',
    share_type='FileSystemDirectory'
)
Share(
    name='1. risk assessment$',
    path='E:\\shares\\listo ip\\1. risk assessment',
    description='',
    share_type='FileSystemDirectory'
)
Share(
    name='14. contabil$',
    path='E:\\shares\\listo ip\\99. financeiro\\14. contabil',
    description='',
    share_type='FileSystemDirectory'
)

Resultado final:

74 compartilhamentos SMB coletados com sucesso.

15. Git

A Fase 1 foi versionada no Git.

Commit:

507cc6a

Mensagem:

implementando SMB collector com PowerShell

Branch:

main

Estado:

HEAD -> main
origin/main

O repositório local ficou sincronizado com o remoto.

O arquivo:

../backlog.md

permaneceu fora do commit.

16. Problemas encontrados

Durante a implementação foram encontrados diversos problemas.

Estrutura duplicada

Existiam duas arquiteturas:

src/collectors/
src/models/

e:

src/wfsa/

Foi decidido padronizar o projeto em:

src/wfsa/
Importações

Foram encontrados erros como:

ModuleNotFoundError

e:

ImportError

Esses problemas foram resolvidos reorganizando os módulos e garantindo a existência dos arquivos necessários.

Permissões

O usuário normal conseguia:

Test-WSMan lst-fs01

mas não conseguia executar:

Invoke-Command

Resultado:

Access is denied

A utilização de uma conta administrativa resolveu o problema.

CalledProcessError

O Python inicialmente apresentou:

subprocess.CalledProcessError

Isso levou à investigação da execução do PowerShell através do subprocess.

Encoding

Caracteres acentuados chegaram corrompidos ao Python.

A solução foi padronizar a comunicação em UTF-8.

Arquitetura

Foi decidido não tentar implementar toda a interação com Windows diretamente em Python.

A solução adotada foi:

Python + PowerShell

Cada tecnologia fica responsável pela parte em que é mais adequada.

17. Resultado da Fase 1
Concluído
 Ambiente Python configurado
 .venv criado
 pyproject.toml configurado
 Estrutura src/wfsa
 Modelo Share
 SMB Collector
 Script PowerShell
 Get-Credential
 Invoke-Command
 WinRM
 Get-SmbShare
 JSON
 Integração Python + PowerShell
 UTF-8
 Testes automatizados
 Teste real contra lst-fs01
 74 compartilhamentos coletados
 Estrutura antiga removida
 Commit criado
 Push para origin/main
18. Principais aprendizados

Esta fase ensinou conceitos além de Python.

Python
ambiente virtual;
pyproject.toml;
estrutura src;
packages;
dataclasses;
subprocess;
JSON;
testes;
pytest.
PowerShell
Get-Credential;
Invoke-Command;
Get-SmbShare;
ConvertTo-Json;
enums;
encoding.
Windows
WinRM;
execução remota;
autenticação;
autorização;
compartilhamentos SMB.
Git
git status;
git add;
git diff;
git commit;
git push;
organização de commits.
19. Principal aprendizado arquitetural

Um dos principais aprendizados da fase foi:

Não é necessário fazer tudo em Python.

O objetivo é utilizar a tecnologia mais adequada para cada responsabilidade.

Neste projeto:

Python
    ↓
Aplicação
    ↓
Modelos
    ↓
Collectors
    ↓
Tratamento dos dados
    ↓
Testes

Enquanto:

PowerShell
    ↓
Windows
    ↓
WinRM
    ↓
SMB

Essa separação torna o projeto mais adequado ao ambiente Windows e facilita a evolução futura.

20. Próxima fase
Fase 2 — Auditoria de permissões SMB

A primeira fase respondeu:

Quais compartilhamentos existem no servidor?

Agora queremos responder:

Quem tem acesso a cada compartilhamento?

O primeiro comando a investigar será:

Get-SmbShareAccess

A arquitetura deverá evoluir de:

Servidor
   ↓
Get-SmbShare
   ↓
Share

para:

Servidor
   ↓
Get-SmbShare
   ↓
Share
   │
   └── Permissions
          ↓
     Get-SmbShareAccess
          ↓
       Permission

Possíveis informações:

Share
 ├── Name
 ├── Path
 ├── Description
 └── Permissions
       ├── AccountName
       ├── AccessControlType
       ├── AccessRight
       └── ScopeName
Objetivo da Fase 2

Criar o modelo de permissões e o collector correspondente.

Nesta fase ainda não serão implementados:

análise de risco;
classificação de permissões;
geração de relatórios;
remediação.

Primeiro vamos garantir que conseguimos coletar e modelar os dados corretamente.

Marco da Fase 1
FASE 01 — SMB COLLECTOR
════════════════════════════════════


Python
   │
   ▼
SMB Collector
   │
   ▼
PowerShell
   │
   ▼
Get-Credential
   │
   ▼
Invoke-Command / WinRM
   │
   ▼
lst-fs01
   │
   ▼
Get-SmbShare
   │
   ▼
JSON UTF-8
   │
   ▼
Python
   │
   ▼
Share objects
   │
   ▼
74 compartilhamentos


Status: CONCLUÍDA