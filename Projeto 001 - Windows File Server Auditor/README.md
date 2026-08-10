# Windows File Server Auditor

Ferramenta em Python para automação de auditoria de servidores de arquivos Windows, com foco em Infraestrutura, Segurança da Informação, Governança e análise inteligente de ambientes de armazenamento.

---

## Sobre o projeto

O Windows File Server Auditor (WFSA) é uma ferramenta desenvolvida em Python para auxiliar equipes de Infraestrutura e Segurança na análise de servidores de arquivos Windows.

O projeto nasceu de uma necessidade real de infraestrutura: automatizar tarefas que normalmente são executadas manualmente durante auditorias de File Servers.

Entre essas atividades estão:

- identificação de compartilhamentos;
- análise de permissões;
- análise de permissões NTFS;
- identificação de usuários e grupos;
- análise de utilização de armazenamento;
- identificação de arquivos antigos;
- geração de relatórios;
- identificação de possíveis riscos;
- geração de recomendações utilizando IA.

O objetivo é transformar atividades operacionais repetitivas em um processo automatizado, rastreável e orientado a dados.

---

## Problema

Administradores de infraestrutura e segurança frequentemente precisam verificar manualmente:

- compartilhamentos SMB;
- permissões de compartilhamento;
- permissões NTFS;
- usuários e grupos;
- herança de permissões;
- espaço utilizado;
- quantidade de arquivos;
- arquivos antigos;
- arquivos de grande tamanho;
- possíveis oportunidades de limpeza;
- possíveis problemas de segurança.

Esse processo pode consumir muitas horas de trabalho, principalmente em ambientes com grande quantidade de compartilhamentos e arquivos.

Além do tempo envolvido, processos manuais estão sujeitos a:

- erros humanos;
- informações incompletas;
- dificuldade de comparação entre servidores;
- dificuldade de geração de evidências;
- ausência de histórico;
- dificuldade de identificar tendências.

---

## Objetivo

Automatizar a auditoria de servidores de arquivos Windows e gerar informações estruturadas que possam apoiar:

- operações de infraestrutura;
- segurança da informação;
- governança;
- capacity planning;
- revisão de permissões;
- processos de limpeza;
- tomada de decisão.

---

## Visão do produto

O WFSA foi projetado para funcionar de forma **agentless**, sendo executado a partir de uma estação administrativa e realizando a coleta de informações remotamente.

Arquitetura conceitual:

```text
                    WFSA
                     |
          +----------+----------+
          |          |          |
         SMB       WinRM       AD
          |          |          |
          +----------+----------+
                     |
                  Collector
                     |
                  Analyzer
                     |
          +----------+----------+
          |          |          |
        JSON       Excel    Dashboard
                                |
                                v
                                IA