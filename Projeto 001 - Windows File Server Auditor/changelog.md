# Changelog

Todas as mudanças relevantes do projeto serão registradas neste arquivo.

---

## [Unreleased]

### Em desenvolvimento

- Evolução da análise de permissões SMB e NTFS.
- Consolidação do fluxo de auditoria.
- Estruturação de findings.
- Preparação para relatórios e armazenamento dos resultados.

### Próximos passos

- Permission Inheritance.
- Explicit vs Inherited ACE.
- Users and Groups.
- SID Resolution.
- Effective Access.
- Novas regras de análise de segurança.
- Análise de armazenamento.
- Consolidação dos resultados da auditoria.
- Relatórios Excel.
- Dashboard.
- Inteligência Artificial.
- Productização.

---

## [0.1.0] — 2026-08-19

### Implementado

- Estrutura inicial do projeto Python.
- Descoberta de compartilhamentos SMB.
- Coleta de permissões SMB.
- Coleta de permissões NTFS.
- Modelo de Findings.
- Análise inicial de permissões.
- Detecção de `Everyone` com acesso `Full`.
- Coleta de metadados de arquivos.
- Processamento dos metadados em streaming.
- Análise de arquivos antigos.
- Findings de arquivos antigos.
- Tratamento de datetime naive/aware.
- Testes automatizados.

### Validação

- Suite automatizada: **13 testes passando**.
- Servidor validado: `lst-fs01`.
- Caminho validado: `E:\Shares\Financeiro`.
- Data de referência: `18/08/2026`.
- Resultado da execução real: **536.417 findings**.

### Problemas tratados

- Encoding PowerShell/Python.
- Caminhos Windows.
- Caracteres especiais.
- Formato delimitado de saída.
- Codificação Base64.
- Diferenças entre dados de teste e dados reais.
- Execução remota com solicitação de credenciais.

---

## Estado atual

Arquitetura:

```text
PowerShell / Windows
        ↓
    Collectors
        ↓
      Models
        ↓
     Analyzers
        ↓
     Findings
Evolução das permissões SMB/NTFS
        ↓
Análise de armazenamento
        ↓
Consolidação da auditoria
        ↓
Relatórios Excel
        ↓
Dashboard
        ↓
IA
        ↓
Productização
