---
type: RFC
id: rfc-0002-sinos-verifiable-experience
title: Sinos como framework de resolução verificável e geração de Experiences raw
status: draft
issue: 24
---

# RFC 0002 — Sinos como framework de resolução verificável e geração de Experiences raw

## Resumo

Esta RFC propõe integrar WikiSkill e Sinos por uma fronteira simples: o Sinos conduz uma resolução de problema como uma trajetória verificável de um estado RED até um estado GREEN e, ao final, fornece a estrutura e a evidência para que o agente produza uma `Experience` padronizada em `raw/`.

A unidade fundamental deixa de ser exclusivamente um teste de software. Passa a ser uma obrigação de resolução verificável, aplicável a qualquer domínio no qual seja possível representar um estado, declarar critérios de sucesso, preservar invariantes e verificar transições.

O WikiSkill continua responsável por persistência e aprendizado: `raw/` contém Experiences ainda não consolidadas; `wiki/` contém conhecimento consolidado entre múltiplas Experiences; `skills/` contém procedimentos reutilizáveis derivados desse conhecimento. O Sinos não se torna fonte de verdade concorrente do WikiSkill. Ele fornece protocolo, witnesses e evidência para tornar os relatos de Experience mais estruturados, comparáveis e resistentes a reconstrução pós-hoc.

## Motivação

O WikiSkill depende de Experiences de qualidade. Um relatório livre escrito pelo agente depois da tarefa pode omitir estados intermediários, confundir intenção com resultado, reconstruir causalidade incorretamente ou afirmar que uma condição foi verificada quando ela apenas pareceu plausível.

O Sinos já modela disciplina causal RED → GREEN para TDD. Essa estrutura pode ser generalizada: muitos problemas de agentes, inclusive fora de programação, podem ser expressos como um estado inicial que não satisfaz uma condição desejada, seguido por uma sequência de ações verificáveis que preserva invariantes até um estado final que satisfaz a condição GREEN.

Exemplos incluem:

- corrigir uma implementação até uma suíte de testes passar;
- levar uma pull request de conflitos/checks quebrados até elegibilidade para merge;
- produzir uma matéria jornalística até todos os requisitos de proveniência estarem satisfeitos;
- preparar um documento até todos os requisitos formais estarem presentes;
- reconciliar um conjunto de dados até satisfazer invariantes de cobertura e consistência;
- executar um fluxo operacional até atingir um estado verificável de conclusão.

O objetivo desta RFC não é afirmar que todo problema é formalizável de modo completo. É estabelecer um protocolo comum para problemas com algum grau de verificabilidade.

## Tese

A integração proposta é:

```text
Sinos
execução + estados + obligations + witnesses + evidence
        ↓
WikiSkill raw/Experience
relatório estruturado da trajetória do agente
        ↓
WikiSkill wiki/
conhecimento consolidado de múltiplas trajetórias
        ↓
WikiSkill skills/
procedimentos reutilizáveis derivados do conhecimento
```

O Sinos estrutura a experiência; o WikiSkill aprende com ela.

## Terminologia

### Experience

Relato primário do agente sobre uma execução concreta. `raw/` significa não consolidado, e não não interpretado. Uma Experience pode conter interpretação, decisões e aprendizados do agente, desde que distinga claramente fatos observados, inferências e incertezas.

### Obligation

Unidade de trabalho verificável. Uma obligation descreve pelo menos:

- problema em linguagem natural;
- estado inicial;
- condição GREEN;
- invariantes;
- ações ou transformações admissíveis quando conhecidas;
- requisitos de evidência;
- nível de verificação usado.

### RED

Estado inicial que verificavelmente não satisfaz a condição GREEN.

RED não significa simplesmente que uma prova de GREEN ainda não foi encontrada. Quando possível, RED deve ser sustentado por um predicado decidível que avalia como falso ou por uma prova explícita de `¬ Green(initial_state)`.

### GREEN

Estado observado que satisfaz a condição GREEN segundo o mecanismo de verificação declarado.

### Witness

Artefato ou prova que sustenta uma afirmação sobre RED, GREEN ou uma transição intermediária.

### Trajectory

Sequência de estados, decisões, ações, observações e witnesses entre o estado inicial e o estado final.

## Modelo conceitual

Uma obligation pode ser vista abstratamente como:

```text
Problem
  ├── natural_language_description
  ├── initial_state
  ├── green_predicate
  ├── invariants
  ├── allowed_actions
  ├── evidence_requirements
  └── verification_level
```

O ciclo geral é:

```text
OBSERVE
   ↓
FORMALIZE
   ↓
RED
   ↓
PLAN / PROVE NEXT STEP
   ↓
ACT
   ↓
OBSERVE
   ↓
VERIFY TRANSITION
   ↓
... repetir ...
   ↓
GREEN
   ↓
GENERATE EXPERIENCE
```

Nem toda execução precisa usar todas as fases como comandos explícitos. O contrato importante é que o relatório final consiga reconstruir a trajetória e distinguir o que foi observado, inferido, executado e verificado.

## Níveis de verificação

O protocolo não deve tornar Lean obrigatório para todos os problemas. São propostos três níveis iniciais.

### `simple`

Condição verificada diretamente por um mecanismo determinístico externo.

Exemplos:

- exit code de uma suíte;
- validação de schema;
- presença de arquivos obrigatórios;
- resposta de uma API;
- check de CI.

### `predicate`

Estado modelado por predicados compostos sobre observações estruturadas.

Exemplo:

```text
mergeable(pr)
AND required_checks_green(pr)
AND blocking_reviews(pr) = 0
```

### `formal`

Estado, invariantes e/ou transições formalizados em um sistema como Lean. O agente pode construir lemas e witnesses que demonstram que determinadas transformações preservam invariantes e levam ao GREEN.

Lean é uma capacidade de verificação do Sinos, não a definição do Sinos.

## Lean como mecanismo de formalização

Para problemas adequados, o Sinos pode transformar uma descrição natural em um modelo formal semelhante a:

```lean
structure State where
  -- variáveis relevantes

def Green (s : State) : Prop :=
  -- condição de sucesso

inductive Action
  | ...

def Step (before : State) (action : Action) (after : State) : Prop :=
  -- transições legítimas
```

O estado inicial `s₀` deve possuir um RED verificável. A resolução busca uma trajetória que termine em um estado que satisfaça `Green`.

Quando a formalização é construtiva, uma prova de existência pode carregar um witness da trajetória ou de partes dela. Isso permite usar Lean não apenas para provar propriedades finais, mas para restringir o espaço de transformações aceitáveis.

## Linguagem natural → contrato → RED

O Sinos pode oferecer um fluxo de formalização assistida:

```text
natural-language requirement
        ↓
formal contract
        ↓
semantic examples / counterexamples
        ↓
validation of formalization
        ↓
RED witness
```

O sistema deve evitar a falácia de considerar uma formalização válida como automaticamente fiel à intenção humana. O kernel pode verificar uma proposição formal sem saber se essa proposição representa corretamente o requisito original.

Por isso o relatório deve preservar lado a lado:

- requisito original em linguagem natural;
- contrato formal;
- exemplos positivos;
- contraexemplos;
- assumptions;
- ambiguidades residuais.

## Fronteira entre mundo e modelo

Nenhum provador formal elimina o problema de conectar modelo e mundo real.

A arquitetura deve tornar essa fronteira explícita:

```text
WORLD
  ↓ observation
observer / tool / sensor
  ↓ certificate
FORMAL OR STRUCTURED STATE
  ↓ reasoning / proof
ACTION
  ↓
WORLD
  ↓ new observation
```

Uma propriedade pode ser provada perfeitamente a partir de uma premissa falsa. Portanto toda entrada que represente fato externo deve indicar sua proveniência e o mecanismo que a observou.

## Experience gerada pelo Sinos

Ao concluir ou interromper uma obligation, o Sinos deve fornecer ao agente uma estrutura padronizada para gerar uma Experience WikiSkill.

O relatório deve ser escrito como relato do agente, não como dump de máquina. Ele pode incorporar automaticamente fatos e witnesses coletados pelo Sinos, mas deve preservar a voz e interpretação da execução.

Estrutura mínima proposta:

```text
# Objective
O que precisava ser alcançado.

# Initial state
Estado observado antes da atuação.

# Green condition
Como a conclusão seria verificada.

# Invariants
O que não poderia ser quebrado durante a resolução.

# Red witness
Por que o estado inicial era RED.

# Trajectory
Para cada passo relevante:
- observação;
- decisão;
- ação;
- justificativa;
- resultado;
- witness quando aplicável.

# Proof obligations
Obrigações formais ou verificáveis encontradas durante o trabalho.

# Evidence
Evidências que sustentam afirmações relevantes.

# Final state
Estado observado ao terminar.

# Green witness
Por que o estado final pode ser chamado GREEN.

# Learnings
O que a execução ensinou.

# Residual uncertainty
O que não foi provado, permanece ambíguo ou ficou fora do modelo.
```

## Localização em WikiSkill

A Experience final pertence ao namespace semântico de experiências não consolidadas do WikiSkill, por exemplo:

```text
raw/
  <experience-id>.md
```

ou, caso o projeto adote diretórios por run:

```text
raw/
  <run-id>/
    experience.md
```

Esta RFC não obriga um layout físico definitivo. O ponto normativo é que o artefato final é uma `Experience`, e não um segundo ledger histórico independente.

## Evidência interna do Sinos

O Sinos pode precisar de artefatos internos para verificar causalidade, hashes, estados, diffs, resultados de comandos ou provas formais. Esses artefatos não são automaticamente Experiences WikiSkill.

A relação correta é:

```text
Sinos internal evidence
        ↓ constrains/supports
WikiSkill Experience
```

A Experience pode referenciar ou incorporar witnesses relevantes. O Sinos não deve criar uma segunda memória semântica concorrente à `raw/` do WikiSkill.

## Imutabilidade e causalidade

Depois que uma fase relevante é testemunhada, os elementos que definem sua obrigação não devem ser silenciosamente alteráveis.

Em uma obligation formalizada, o witness RED pode congelar, conforme aplicável:

- digest do requisito em linguagem natural;
- digest do contrato formal;
- digest dos testes derivados;
- digest de invariantes;
- estado observado;
- mecanismo de verificação.

Mudanças posteriores que alterem semanticamente a obrigação devem abrir uma nova revisão ou uma nova obligation, e não reescrever retrospectivamente o RED.

## Compatibilidade com TDD tradicional

TDD é um caso particular do modelo geral.

```text
State          = checkout + implementação + testes
Green          = suite passes
RED witness    = novos testes falham antes da implementação
Action         = alteração de produção
Invariants     = testes RED congelados + invariantes do repositório
Green witness  = mesma obrigação agora satisfeita
```

O comportamento atual do Sinos deve continuar possível como um perfil especializado de obligation.

## Exemplos não matemáticos

### Pull request

```text
Initial state:
- conflito presente
- check obrigatório falhando

Green:
- mergeable
- todos os checks obrigatórios verdes
- nenhuma review bloqueante

Trajectory:
- observar conflito
- aplicar resolução
- verificar preservação do diff desejado
- corrigir check
- observar estado remoto novamente
```

### Jornalismo verificável

```text
Initial state:
- matéria possui afirmação sem proveniência suficiente

Green:
- toda afirmação factual relevante possui fonte admissível
- todos os gates editoriais passam

Trajectory:
- localizar lacuna
- adquirir fonte
- comparar afirmação com fonte
- corrigir texto se necessário
- reexecutar gates
```

### Documento operacional

```text
Initial state:
- faltam requisitos obrigatórios

Green:
- todos os requisitos presentes
- nenhuma inconsistência detectada

Trajectory:
- identificar requisito ausente
- adquirir dado necessário
- inserir informação
- validar documento completo
```

## Consolidação no WikiSkill

Experiences padronizadas tornam mais fácil identificar estruturas recorrentes entre domínios distintos.

Duas tarefas aparentemente diferentes podem compartilhar a mesma trajetória abstrata:

```text
missing required evidence
→ acquire evidence
→ validate evidence
→ re-evaluate obligation
→ GREEN
```

O WikiSkill pode consolidar esse padrão em `wiki/` e, quando apropriado, evoluí-lo para uma skill reutilizável.

A padronização não deve apagar detalhes específicos da execução. Ela fornece uma espinha dorsal comum sobre a qual o conteúdo particular é preservado.

## Não objetivos

Esta RFC não propõe:

- tornar Lean obrigatório para todas as Experiences;
- formalizar completamente o mundo externo;
- substituir observadores e ferramentas reais por modelos formais;
- transformar toda narrativa do agente em prova matemática;
- fazer o WikiSkill depender do Sinos para conseguir registrar qualquer Experience;
- fundir os armazenamentos internos dos dois projetos;
- considerar ausência de prova como prova de RED;
- permitir que um relatório pós-hoc fabrique causalidade ausente.

## Contrato de integração

O contrato mínimo entre os projetos deve permanecer pequeno.

O Sinos deve ser capaz de fornecer uma representação estruturada de uma execução contendo, quando disponível:

```text
obligation_id
objective
initial_state
red_witness
green_condition
invariants
trajectory[]
proof_obligations[]
evidence[]
final_state
green_witness
learnings
residual_uncertainty
verification_level
```

O WikiSkill deve ser capaz de transformar ou persistir essa representação como `Experience` válida segundo seu próprio schema.

Não é necessário que o WikiSkill importe o runtime do Sinos. Integrações por CLI, MCP, arquivo OKF ou outra superfície estável são aceitáveis.

## Proveniência das afirmações

Cada afirmação relevante no relatório deve poder ser classificada, explicitamente ou por estrutura, como uma destas categorias:

- `observed`: obtida diretamente de ferramenta, execução ou fonte;
- `verified`: satisfeita por mecanismo determinístico ou formal;
- `inferred`: conclusão do agente a partir de evidências;
- `reported`: informação recebida de fonte externa sem verificação independente;
- `uncertain`: hipótese ou interpretação ainda não resolvida.

Essa distinção reduz o risco de uma inferência narrativa ser posteriormente tratada pelo WikiSkill como fato consolidado.

## Falhas e execuções incompletas

Uma Experience não exige GREEN.

Falhas, impasses e obligations abandonadas são material valioso para o WikiSkill. O Sinos deve poder gerar relatório parcial contendo:

- RED confirmado;
- trajetória percorrida;
- tentativas que não funcionaram;
- último estado observado;
- obrigação ainda aberta;
- razão da interrupção;
- incerteza residual.

O status da Experience deve refletir isso sem mascarar ausência de GREEN.

## Segurança contra narrativa pós-hoc

O relatório final pode ser produzido no fim da execução, mas seus fatos causais fortes devem estar ancorados em witnesses registrados durante a trajetória.

Exemplos de afirmações que não devem ser aceitas apenas porque o agente as escreveu ao final:

- “o teste falhou antes da implementação”;
- “o contrato formal não mudou entre RED e GREEN”;
- “todos os checks estavam verdes”;
- “a fonte sustentava a afirmação no momento da publicação”.

O Sinos deve fornecer esses fatos quando puder verificá-los; quando não puder, a Experience deve marcá-los como relato ou inferência, e não como fato verificado.

## Implementação incremental

### Fase 1 — schema de obligation e Experience report

- definir modelo mínimo de obligation;
- definir representação estruturada da trajectory;
- produzir Experience report para o perfil TDD já existente;
- garantir que o relatório possa ser persistido pelo WikiSkill sem reconstrução manual.

### Fase 2 — verificadores genéricos

- permitir GREEN baseado em comandos, schemas, APIs e predicados;
- separar claramente observação, verificação e inferência;
- tornar TDD apenas um perfil entre outros.

### Fase 3 — formalização Lean opcional

- representar State, Green, invariants e Step em Lean quando solicitado;
- preservar requisito natural e contrato formal juntos;
- suportar examples/counterexamples para revisar fidelidade semântica;
- congelar digests de obligation no RED;
- registrar lemas e witnesses relevantes na trajectory.

### Fase 4 — consolidação WikiSkill

- consumir múltiplas Experiences geradas pelo protocolo;
- avaliar se a estrutura comum melhora recuperação e consolidação;
- detectar padrões transversais entre diferentes domínios;
- promover padrões úteis para wiki e skills apenas com avaliação adequada.

## Critérios de aceitação da RFC

A proposta é considerada demonstrada quando for possível executar pelo menos três obligations de naturezas diferentes, por exemplo:

1. uma tarefa TDD em código;
2. uma tarefa de repositório/GitHub;
3. uma tarefa não-código baseada em requisitos verificáveis;

E, para cada uma:

- registrar RED sem confundir ausência de prova com falsidade;
- registrar trajetória estruturada;
- produzir GREEN ou uma falha explicitamente incompleta;
- gerar uma Experience WikiSkill válida;
- distinguir observação, verificação, inferência e incerteza;
- permitir ao WikiSkill comparar as três Experiences sem perder seus detalhes de domínio.

Um experimento adicional deve avaliar o modo `formal` com Lean em pelo menos uma obligation com múltiplas variáveis e invariantes.

## Questões abertas

1. O formato intermediário entre Sinos e WikiSkill deve ser o próprio tipo `Experience`, um tipo `ObligationReport`, ou ambos?
2. A evidence interna do Sinos deve ser referenciada por links/digests ou parcialmente incorporada à Experience?
3. Como versionar uma obligation quando a linguagem natural original é esclarecida durante o trabalho?
4. Quais classes de `Green` devem exigir predicados decidíveis?
5. Como medir fidelidade entre requisito natural e formalização Lean?
6. Quando uma trajetória formal deve registrar cada ação como lemma e quando basta verificar invariantes em checkpoints?
7. Quais campos da estrutura de Experience devem ser normativos e quais devem permanecer livres para relato do agente?

## Decisão proposta

Adotar Sinos como framework opcional de resolução verificável para WikiSkill, generalizando RED → GREEN de TDD para obligations de domínio geral.

O Sinos deve estruturar a trajetória e fornecer witnesses verificáveis. O agente deve produzir, a partir dessa trajetória, uma Experience padronizada em `raw/`. O WikiSkill permanece responsável por persistência, consolidação e evolução de conhecimento.

Lean deve ser tratado como nível opcional de verificação formal capaz de representar problemas com muitas variáveis, invariantes e transformações, sem restringir o framework a problemas tradicionalmente matemáticos.
