# Roadmap

## Visão geral

O Windows File Server Auditor será desenvolvido de forma incremental, evoluindo de uma ferramenta de coleta de informações para uma solução de auditoria, análise e recomendação para ambientes de File Server Windows.

---

## Sprint 1 — Estrutura do projeto

Objetivo: criar a fundação do projeto.

- Estrutura do projeto
- Git/GitHub
- README
- Backlog
- Documentação inicial
- Definição da arquitetura
- Validação do ambiente de execução

---

## Sprint 2 — Compartilhamentos

Objetivo: automatizar a descoberta dos compartilhamentos SMB.

- Identificação dos compartilhamentos
- Nome
- Caminho
- Tipo
- Compartilhamentos administrativos
- Coleta remota
- Geração dos primeiros dados estruturados

---

## Sprint 3 — Permissões

Objetivo: automatizar a análise de permissões dos compartilhamentos e do sistema de arquivos.

- Share Permissions
- NTFS Permissions
- Permission Inheritance
- Explicit vs Inherited ACE
- Users and Groups
- SID Resolution
- Effective Access
- Security Findings

---

## Sprint 4 — Espaço e armazenamento

Objetivo: analisar utilização e capacidade do armazenamento.

- Volume utilization
- Share size
- Folder size
- Largest files
- Growth indicators
- Capacity findings

---

## Sprint 5 — Arquivos antigos

Objetivo: identificar arquivos sem alteração por longos períodos.

- Arquivos antigos
- Arquivos grandes
- Classificação por idade
- Tamanho acumulado
- Indicadores de limpeza
- Findings

---

## Sprint 6 — Relatórios Excel

Objetivo: transformar os resultados da auditoria em relatórios profissionais.

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

Objetivo: disponibilizar uma interface visual para análise dos resultados.

- Streamlit
- Dashboard
- Indicadores
- Gráficos
- Filtros
- Findings
- Exportação

---

## Sprint 8 — Inteligência Artificial

Objetivo: utilizar IA para interpretar os resultados da auditoria.

- Recomendações
- Resumo executivo
- Explicação de findings
- Identificação de padrões
- Priorização de riscos
- Plano de ação

---

## Sprint 9 — Productização

Objetivo: transformar o projeto em uma solução mais próxima de um produto.

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

Objetivo: preparar o projeto para publicação e apresentação profissional.

- Revisão do código
- Revisão da arquitetura
- Testes
- Documentação
- Exemplos
- Demonstração
- Release
- Publicação no GitHub

---

## Evolução futura

Após a primeira versão pública, poderão ser avaliadas:

- Auditoria de múltiplos servidores
- Histórico de auditorias
- Comparação entre auditorias
- Alertas
- API
- Banco de dados
- Integrações com ferramentas de segurança
- Integrações com ITSM
- Automação de remediação

### Segurança e execução em produção

- [ ] Definir conta de serviço para execução do auditor
- [ ] Definir permissões mínimas necessárias
- [ ] Validar execução remota via PowerShell/WinRM
- [ ] Evitar credenciais hardcoded
- [ ] Documentar requisitos de execução
- [ ] Testar execução com conta de serviço