WFSA-001  Criar estrutura do projeto
WFSA-002  Validar ambiente Windows

WFSA-003  Validar acesso remoto WinRM
Prioridade: P0
Status: 🟢 Done

Descrição:
Validar a capacidade de executar comandos remotamente no File Server utilizando PowerShell Remoting/WinRM.
Critérios de aceite:
 Test-WSMan executado
 WinRM validado
 Identificada diferença de privilégio entre usuários
 Conta administrativa validada
 Invoke-Command executado com sucesso
 Execução remota validada
Evidência:
Test-WSMan lst-fs01

Invoke-Command -ComputerName "hostname" -ScriptBlock {
    hostname
    whoami
}
Resultado esperado:
host-servidor
LST-DOMAIN\(usuario adm)

WFSA-004  Definir arquitetura de coleta
Prioridade: P0
Status: 🟢 Done

Descrição:
Definir a arquitetura inicial do WFSA.
Decisão:
O WFSA utilizará inicialmente uma arquitetura agentless.
A execução ocorrerá a partir de uma estação administrativa.
Workstation
     |
     | WinRM / PowerShell
     v
hostname(servidor de arquivo)
     |
     v
Collectors
     |
     v
Structured Data
Critérios de aceite:
 Arquitetura agentless definida
 Execução remota definida
 Collector separado conceitualmente da análise
 Dados estruturados definidos como objetivo
 Nenhum agente necessário no File Server na primeira versão

WFSA-005  Definir modelo Share

WFSA-006  Implementar SMB Collector
WFSA-007  Serializar Shares para JSON
WFSA-008  Criar testes do SMB Collector
WFSA-009  Implementar Storage Collector
WFSA-010  Criar documentação da coletao

# Backlog — Windows File Server Auditor

Este documento contém as tarefas planejadas para desenvolvimento do Windows File Server Auditor.

---

# Status

- 🔴 To Do
- 🟡 In Progress
- 🟢 Done
- ⚪ Blocked

---

# Prioridade

- P0 — Crítica
- P1 — Alta
- P2 — Média
- P3 — Baixa

---

# Sprint 1 — Foundation

## WFSA-001 — Estruturar projeto

**Prioridade:** P0  
**Status:** 🟢 Done

### Descrição

Criar a estrutura inicial do projeto e os diretórios necessários para desenvolvimento, testes, documentação e geração de resultados.

### Critérios de aceite

- [x] Diretório `src/`
- [x] Diretório `tests/`
- [x] Diretório `docs/`
- [x] Diretório `examples/`
- [x] Diretório `output/`
- [x] `.gitignore`
- [x] `README.md`
- [x] `roadmap.md`
- [x] `learning.md`
- [x] `changelog.md`
- [x] `requirements.txt`

---

## WFSA-002 — Documentar ambiente de laboratório

**Prioridade:** P0  
**Status:** 🟢 Done

### Descrição

Documentar as características do File Server utilizado como ambiente real de desenvolvimento e validação.

### Ambiente

```text
Hostname: LST-FS01
Sistema: Windows Server 2016 Standard
Build: 14393
IP: 192.168.25.7
Domínio: LST-DOMAIN.LOCAL