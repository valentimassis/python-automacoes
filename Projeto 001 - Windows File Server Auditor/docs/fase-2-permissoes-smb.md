# Fase 2 — Auditoria de Permissões SMB

## 1. Objetivo

A Fase 2 tem como objetivo adicionar ao Windows File Server Auditor a capacidade de coletar as permissões configuradas nos compartilhamentos SMB de um servidor Windows.

Na Fase 1, o projeto passou a coletar informações dos compartilhamentos.

Nesta fase, passamos a coletar também as permissões associadas a cada compartilhamento.

---

## 2. Resultado da Fase 2

Ao final desta fase, o projeto consegue:

- conectar remotamente ao servidor Windows;
- autenticar utilizando uma conta administrativa;
- executar `Get-SmbShareAccess`;
- coletar as permissões de um compartilhamento;
- converter os valores dos enums do PowerShell para texto;
- retornar os dados em JSON;
- consumir o JSON através do Python;
- transformar os dados em objetos `Permission`;
- executar testes automatizados.

Exemplo real coletado:

```text
Permission(
    account_name='Everyone',
    access_control_type='Allow',
    access_right='Full',
    scope_name='*'
)
3. Arquitetura

A arquitetura adotada mantém a responsabilidade de comunicação com o Windows no PowerShell e a responsabilidade de processamento/modelagem no Python.

Python
   │
   │ subprocess
   ▼
PowerShell
   │
   │ Invoke-Command
   ▼
Windows File Server
   │
   │ Get-SmbShareAccess
   ▼
JSON
   │
   ▼
Python
   │
   ▼
Permission

Essa separação evita colocar toda a lógica específica do Windows dentro do código Python.
steriores.

17. Aprendizados técnicos

Durante esta fase foram praticados:

dataclass;
criação de modelos Python;
subprocess;
execução de PowerShell através do Python;
JSON;
conversão JSON → Python;
listas de objetos;
Get-SmbShareAccess;
Invoke-Command;
WinRM;
Get-Credential;
enums do PowerShell;
testes com pytest;
integração Python + PowerShell;
organização de responsabilidades entre linguagens.
18. Decisão arquitetural

Foi adotada a seguinte divisão:

Python

Responsável por:

modelos;
processamento;
integração;
regras de negócio;
testes;
futura análise;
relatórios;
CLI.
PowerShell

Responsável por:

comunicação com Windows;
PowerShell Remoting;
WinRM;
cmdlets específicos do Windows Server;
coleta de informações SMB/NTFS.

Essa divisão permite aproveitar as capacidades nativas do Windows sem transformar o projeto Python em uma coleção de comandos PowerShell embutidos.

19. Estado da Fase 2
Modelo Permission             ✅
Teste do modelo               ✅
Script PowerShell             ✅
Get-SmbShareAccess             ✅
Autenticação via Get-Credential ✅
Conversão de enums             ✅
JSON                           ✅
Collector Python               ✅
Teste do collector             ✅
Teste real no lst-fs01         ✅
UTF-8                          ✅
Git commit                     ✅
Git push                       ✅
20. Próxima fase

A próxima etapa será a Fase 3 — Estrutura e permissões NTFS.

Objetivos previstos:

Coletar caminho físico do Share
        ↓
Coletar permissões NTFS
        ↓
Criar modelo NTFS
        ↓
Relacionar Share + SMB Permission + NTFS Permission
        ↓
Preparar os dados para análise de risco

A partir dessa etapa o projeto começará a deixar de ser apenas um coletor e passará a funcionar como uma ferramenta de auditoria.

21. Marco da Fase 2

A Fase 2 representa a conclusão da segunda camada de coleta do projeto:

Fase 1
Shares SMB
     +
Fase 2
Permissões SMB
     ↓
Base inicial para auditoria