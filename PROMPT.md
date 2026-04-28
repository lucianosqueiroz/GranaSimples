Trabalhe diretamente neste repositório. Antes de alterar, leia a estrutura atual do projeto. Preserve o que já existir funcionando. Faça mudanças incrementais, organizadas e testáveis. Ao final, informe arquivos alterados, comandos para rodar e checklist de testes.

Crie um aplicativo completo de controle financeiro pessoal e familiar chamado GranaSimples, com foco em simplicidade, rapidez de uso no dia a dia e viabilidade comercial.



IMPORTANTE:



\- O sistema NÃO deve ser complexo como um ERP.

\- Deve ser simples, intuitivo e rápido.

\- Deve ser projetado como produto comercial.

\- Deve rodar inicialmente como aplicativo Android.

\- Deve ser preparado para futura versão web (frontend web no futuro).

\- Evitar decisões abertas. Implementar exatamente o que está descrito.



---



IDENTIDADE DO PRODUTO



Nome: GranaSimples



Slogan:

"Controle financeiro simples, rápido e sem complicação."



Público-alvo:



\- pessoas comuns

\- famílias

\- usuários que não gostam de planilhas

\- pessoas que precisam de praticidade no dia a dia



Design:



\- moderno e minimalista

\- cores principais:

&nbsp; - azul (#2563EB)

&nbsp; - verde (#16A34A)

&nbsp; - fundo cinza claro

\- layout limpo

\- poucos campos

\- botões grandes

\- foco total em rapidez de uso



---



TECNOLOGIA



\- Backend: Python



\- Interface: Flet (obrigatório)



\- Banco de dados: SQLite



\- Arquitetura:

&nbsp; 

&nbsp; - Models

&nbsp; - Repository

&nbsp; - Service

&nbsp; - UI (Pages)



\- Estrutura pronta para:

&nbsp; 

&nbsp; - futura API

&nbsp; - futura versão web (frontend separado)



---



OBJETIVO DO SISTEMA



Criar um aplicativo que permita:



\- controle financeiro diário simples

\- cadastro rápido de receitas e despesas

\- controle de cartões de crédito

\- visão clara do mês atual

\- base para monetização futura (freemium)



---



MÓDULOS OBRIGATÓRIOS



1\. PESSOAS / CENTRO DE CUSTO



\- id

\- nome

\- tipo (Pessoa ou Centro de Custo)

\- ativo



Funções:



\- criar

\- editar

\- inativar



---



2\. CONTAS



\- id

\- nome

\- tipo (banco, carteira, etc)

\- saldo\_atual

\- ativo



---



3\. CARTÕES DE CRÉDITO



\- id

\- nome

\- 4 últimos dígitos

\- dia\_vencimento

\- dia\_fechamento (menor que vencimento)

\- limite\_total

\- limite\_usado (não editável)

\- ativo



---



4\. CATEGORIAS



\- id

\- nome

\- tipo (receita ou despesa)

\- ativo



---



5\. SUBCATEGORIAS



\- id

\- categoria\_id

\- nome

\- ativo



Regra:



\- NÃO obrigatória



---



6\. LANÇAMENTOS (PRINCIPAL)



Campos:



\- id

\- tipo (receita ou despesa)

\- meio\_financeiro (conta ou cartao)

\- data

\- valor

\- descricao (opcional)

\- categoria\_id (obrigatório)

\- subcategoria\_id (opcional)

\- pessoa\_id (opcional)

\- conta\_id (se conta)

\- cartao\_id (se cartão)

\- observacoes (opcional)

\- ativo



---



REGRAS DE NEGÓCIO



\- Receita → só conta

\- Despesa → conta ou cartão



Fluxo UI:



1\. escolher tipo

2\. escolher meio financeiro

3\. exibir campos



\- Subcategoria opcional

\- Descrição opcional

\- Sistema deve priorizar rapidez



---



7\. DASHBOARD



\- total receitas mês

\- total despesas mês

\- saldo



---



8\. ORÇAMENTO (PREPARADO)



\- valor previsto por categoria

\- percentual de alerta (ex: 80%)



---



9\. ALERTAS (PREPARADO)



\- estrutura pronta



---



10\. UX



\- navegação lateral

\- cards

\- formulários simples

\- campos dinâmicos

\- sem poluição visual



---



11\. REGRAS DE EXCLUSÃO



\- sem vínculo → excluir

\- com vínculo → inativar



---



12\. OBJETIVO FINAL



---



Aplicativo deve estar:



\- funcional

\- simples

\- rápido

\- pronto para uso real

\- preparado para virar produto comercial Android

\- preparado para futura versão web



---



NÃO FAZER:



\- Open Finance

\- IA

\- integrações externas

\- excesso de complexidade



---



ENTREGAR:



\- código completo

\- estrutura de pastas

\- arquivos separados

\- sistema rodando com python app.py



---

