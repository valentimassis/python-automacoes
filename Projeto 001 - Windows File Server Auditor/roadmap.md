# Roadmap

## Visão geral

O Windows File Server Auditor será desenvolvido de forma incremental, evoluindo de uma ferramenta de coleta de informações para uma solução de auditoria, análise e recomendação para ambientes de File Server Windows.

---

## Sprint 1 — Estrutura do projeto

Status: **Concluída**

- Estrutura do projeto
- Git/GitHub
- README
- Backlog
- Documentação inicial
- Definição da arquitetura
- Validação do ambiente de execução

---

## Sprint 2 — Compartilhamentos

Status: **Concluída**

- Identificação dos compartilhamentos
- Nome
- Caminho
- Tipo
- Compartilhamentos administrativos
- Coleta remota
- Geração dos primeiros dados estruturados

---

## Sprint 3 — Permissões

Status: **Em andamento**

### Implementado

- Share Permissions
- Coleta de permissões SMB
- Coleta de permissões NTFS
- Modelo estruturado de permissões
- Permission Inheritance
- Explicit vs Inherited ACE
- Normalização de direitos SMB e NTFS
- Cálculo de Effective Access
- Finding para `Everyone` com `Full` em compartilhamento SMB
- Finding para `Everyone` com `FullControl` em NTFS
- Finding para `Everyone` com `Modify` em NTFS
- Identificação de permissões herdadas
- Findings de segurança
- Integração da análise NTFS ao serviço de auditoria
- Testes automatizados

### Próximos passos

- Users and Groups
- SID Resolution
- Identificação de usuários vs grupos
- Ampliação dos Security Findings
- Análise de grupos privilegiados

---

## Sprint 4 — Espaço e armazenamento

Status: **Pendente**

- Volume utilization
- Share size
- Folder size
- Largest files
- Growth indicators
- Capacity findings

---

## Sprint 5 — Arquivos antigos

Status: **Em andamento**

### Implementado

- Coleta de metadados dos arquivos
- Nome
- Caminho
- Extensão
- Tamanho
- Data de criação
- Última alteração
- Último acesso
- Processamento em streaming
- Análise de arquivos antigos
- Identificação de arquivos sem alteração há mais de 2 anos
- Identificação de arquivos sem acesso há mais de 2 anos
- Findings de severidade `MEDIUM`
- Testes automatizados

### Validação real

A coleta e análise foram executadas contra:

- Servidor: `lst-fs01`
- Caminho: `E:\Shares\Financeiro`
- Data de referência: `18/08/2026`

Resultado:

- **536.417 findings**

---

## Sprint 6 — Relatórios Excel

Status: **Pendente**

- Relatório Excel
- Resumo executivo
- Compartilhamentos
- Permissões
- Armazenamento
- Arquivos antigos
- Findings
- Evidências

---

## Sprint 7 — Dashboard

Status: **Pendente**

- Streamlit
- Dashboard
- Indicadores
- Gráficos
- Filtros
- Findings
- Exportação

---

## Sprint 8 — Inteligência Artificial

Status: **Pendente**

- Recomendações
- Resumo executivo
- Explicação de findings
- Identificação de padrões
- Priorização de riscos
- Plano de ação

---

## Sprint 9 — Productização

Status: **Pendente**

- Docker
- Configuração
- Logging
- Segurança
- Tratamento de erros
- Documentação de instalação
- Documentação de operação
- Empacotamento

---

## Sprint 10 — Primeira versão pública

Status: **Pendente**

- Revisão do código
- Revisão da arquitetura
- Testes
- Documentação
- Exemplos
- Demonstração
- Release
- Publicação no GitHub

---

## Próximo foco

A próxima etapa será continuar a **Sprint 3 — Permissões**, com foco em identificação de usuários e grupos e resolução de SID, antes de avançar para armazenamento e relatórios.

### Segurança e execução em produção

- [ ] Definir conta de serviço para execução do auditor
- [ ] Definir permissões mínimas necessárias
- [ ] Validar execução remota via PowerShell/WinRM
- [ ] Evitar credenciais hardcoded
- [ ] Documentar requisitos de execução
- [ ] Testar execução com conta de serviço
