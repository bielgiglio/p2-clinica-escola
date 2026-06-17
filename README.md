# Sistema de Agendamento | Clínica-Escola (P2)

**Link da Aplicação em Produção:** https://p2-clinica-escola.onrender.com

## 1. Descrição do Problema e Solução
Clínicas universitárias enfrentam o desafio de conciliar a fila de pacientes com a disponibilidade fragmentada dos alunos-terapeutas. Além das durações matemáticas diferentes (Triagens vs. Psicoterapia), existe a necessidade de gerenciar o ciclo de vida da consulta (agendamentos, cancelamentos e conclusões).

**Solução:** Este sistema resolve o problema permitindo agendamentos irregulares com cálculo dinâmico de término. Ele também gerencia estados da sessão: ao cancelar um atendimento, o sistema automaticamente libera a grade de horário para um novo agendamento, prevenindo sobreposição de forma inteligente.

## 2. Divisão em Microsserviços
A solução foi desenhada como parte de uma arquitetura baseada em microsserviços:
* **Triage Service:** Gerencia fila e prontuários (Escopo futuro).
* **Schedule Service (Este repositório):** Microsserviço central que orquestra horários, bloqueio de conflitos e persistência do status das sessões.

## 3. Arquitetura Limpa (Clean Architecture)
As regras da clínica estão estritamente isoladas de tecnologias externas.
* `src/domain/`: Regras puras (Entities, Factories, Strategies, States e Interfaces).
* `src/application/`: Casos de Uso que orquestram a operação.
* `src/infrastructure/`: Framework web (FastAPI) e persistência de dados real (SQLite).

## 4. Princípios SOLID Aplicados
O sistema prova o domínio do SOLID, com destaque para:
* **SRP (Responsabilidade Única):** A entidade `Session` não calcula o tempo nem define regras de status. Isso é delegado para as *Strategies* e *States*.
* **OCP (Aberto/Fechado):** É possível adicionar novas modalidades de atendimento criando novas classes, sem modificar as existentes.
* **DIP (Inversão de Dependência) na Prática:** O projeto iniciou com um banco em memória. Posteriormente, foi plugar um `SQLiteSessionRepository` alterando apenas **uma única linha** na injeção de dependência do Use Case, sem quebrar nenhuma regra de negócio.

## 5. Design Patterns Utilizados (Mínimo de 4 Atendidos)
1. **State (`states.py`):** Modela o ciclo de vida da sessão (`ScheduledState`, `CanceledState`, `CompletedState`). Impede transições inválidas (ex: cancelar uma sessão já concluída) sem poluir o código com múltiplos comandos `if/else`.
2. **Strategy (`strategies.py`):** Define algoritmos intercambiáveis para o cálculo exato de duração (30 min ou 50 min).
3. **Factory Method (`factories.py`):** Centraliza a criação do objeto de sessão e barra agendamentos com datas no passado (validação de timezone mitigada para o Brasil).
4. **Repository (`repositories.py`):** Isola os comandos SQL e a conexão do banco de dados relacional (SQLite), protegendo as camadas superiores.

## 6. Evidências de Clean Code
A base de código adota um estilo direto e autoexplicativo. Optou-se por focar na expressividade da linguagem Python, utilizando nomenclaturas verbais claras (`find_overlapping`, `update_status`) e mantendo o código sem comentários redundantes, simulando um ambiente de desenvolvimento limpo e maduro.

## 7. BDD (Behavior Driven Development)
O sistema reflete regras reais de negócio na sua usabilidade.
**Cenário de Conflito e Cancelamento:**
* **Dado que** o terapeuta possui um atendimento às 14:00,
* **Quando** tentarem marcar outro paciente às 14:15, **Então** o sistema recusa a sobreposição.
* **Mas**, se a sessão das 14:00 for marcada como "Cancelada", **Então** o sistema libera a trava e aceita o novo agendamento no mesmo horário perfeitamente.

## 8. TDD (Test Driven Development)
Foram mapeados e testados os comportamentos vitais do sistema independentemente da internet:
* Bloqueios de horários alternados/quebrados.
* Identificação de conflito de tempo ativo.
* Bloqueio rígido de datas retroativas.
Para rodar os testes localmente: `python -m unittest discover tests`

## 9. Persistência de Dados e Banco Relacional
O projeto evoluiu para utilizar um banco de dados relacional estruturado em **SQLite**, construído com comandos `CREATE TABLE`, `INSERT`, `UPDATE` e `SELECT`. Os conflitos de horários são tratados lendo as informações consolidadas no arquivo físico `.db`.

## 10. Docker, Deploy Cloud e Justificativa Técnica
A aplicação está empacotada com um `Dockerfile` (`python:3.10-slim`) para garantir que o ambiente seja idêntico na máquina local e na nuvem. O deploy foi realizado na plataforma **Render**, servindo uma API Backend (`FastAPI`) e um Frontend interativo e responsivo no mesmo contêiner.

*(Nota sobre a nuvem: Como o Render Free utiliza discos efêmeros, o arquivo do banco de dados SQLite é reiniciado junto com as hibernações do servidor. O padrão Repository foi vital aqui para que o sistema funcione perfeitamente com as limitações da infraestrutura de nuvem, mantendo a arquitetura de software intacta).*