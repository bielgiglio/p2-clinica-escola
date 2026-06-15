# Sistema de Agendamento | Clínica-Escola (P2)

**Link da Aplicação em Produção:** `https://p2-clinica-escola.onrender.com`


## 1. Descrição do Problema e Solução
Clínicas universitárias que oferecem atendimento psicológico à comunidade enfrentam o desafio de conciliar a fila de pacientes com a disponibilidade fragmentada dos alunos-terapeutas (que dependem das grades de aulas). Além disso, os atendimentos possuem durações matemáticas diferentes (ex: Triagens duram 30 minutos, Psicoterapia dura 50 minutos). 

**Solução:** Este sistema de software resolve o problema permitindo agendamentos em horários não sequenciais/irregulares. Ele calcula dinamicamente o horário de término com base na modalidade escolhida, bloqueia agendamentos retroativos e previne sobreposição de horários para o mesmo terapeuta.

## 2. Divisão em Microsserviços
A solução completa foi idealizada em microsserviços para garantir escalabilidade:
* **Triage Service:** Gerencia fila e prontuários (Simulado/Escopo futuro).
* **Schedule Service (Este repositório):** Microsserviço central responsável pela orquestração das regras de tempo, disponibilidade e confirmação de sessões. 

## 3. Arquitetura Limpa (Clean Architecture)
O projeto respeita as fronteiras arquiteturais para que a regra de negócio não dependa de frameworks web ou bancos de dados externos.
* `src/domain/`: Contém as regras puras (Entities, Factories, Strategies e Interfaces).
* `src/application/`: Contém os Casos de Uso (Use Cases) que ditam o fluxo do sistema.
* `src/infrastructure/`: Contém a implementação do FastAPI e a simulação do Banco de Dados em memória.

## 4. Princípios SOLID Aplicados
* **SRP (Responsabilidade Única):** A entidade `Session` apenas mantém o estado. O cálculo de tempo foi movido para as *Strategies*, e a persistência para os *Repositories*.
* **OCP (Aberto/Fechado):** É possível adicionar novos tipos de atendimento (ex: Plantão Psicológico) criando uma nova `DurationStrategy`, sem modificar o código existente.
* **DIP (Inversão de Dependência):** O `CreateSessionUseCase` depende da abstração `SessionRepositoryInterface`, e não da implementação de banco de dados diretamente.

## 5. Design Patterns Utilizados (4 Aplicados)
1. **Strategy (`strategies.py`):** Define algoritmos intercambiáveis para o cálculo de duração da sessão (`TriagemStrategy` e `PsicoterapiaStrategy`).
2. **Factory Method (`factories.py`):** O `SessionFactory` centraliza a criação de sessões, embutindo regras críticas (como barrar datas no passado e aplicar a *Strategy* de tempo).
3. **Repository (`repositories.py`):** Oculta a complexidade de acesso a dados.
4. **Singleton (`repositories.py`):** A classe `DatabaseConnection` garante que o repositório em memória mantenha uma única instância global durante o ciclo de vida da aplicação.

## 6. Evidências de Clean Code
O código backend prioriza a legibilidade. Funções são curtas e possuem responsabilidades claras. Optou-se por não utilizar comentários excessivos (estilo focado na expressividade da linguagem), usando nomes de variáveis e métodos que documentam o comportamento real (ex: `find_overlapping`, `is_valid_duration`).

## 7. BDD (Behavior Driven Development)
O sistema foi desenhado mapeando o comportamento do usuário real da clínica. 
**Cenário Principal (Fuso e Conflito):**
* **Dado que** o terapeuta "T1" possui um atendimento agendado para o dia atual às 14:00,
* **Quando** a recepção tentar marcar outro paciente para o mesmo terapeuta às 14:15,
* **Então** o sistema recusa a solicitação por sobreposição, retornando erro claro para a interface.

## 8. TDD (Test Driven Development)
Os testes foram estruturados antes do fechamento das lógicas no Use Case. 
No arquivo `tests/test_schedule.py`, foram mapeados os cenários vitais:
* Validação de horários irregulares.
* Identificação de conflito de tempo (mesmo terapeuta em horários que se cruzam).
* Bloqueio rígido de datas retroativas (past dates).
Para rodar os testes: `python -m unittest discover tests`

## 9. Docker, Configuração e Deploy Cloud
A aplicação está empacotada utilizando um `Dockerfile` leve (`python:3.10-slim`). Para ambiente de desenvolvimento, o orquestrador `docker-compose.yml` foi configurado. 
O deploy da aplicação foi realizado na plataforma **Render**, onde o FastAPI também se encarrega de servir o frontend (`index.html`) estático na rota raiz, consumindo a porta dinâmica injetada via variável de ambiente `$PORT`.

## 10. Justificativa Técnica
A adoção do padrão *Strategy* aliada ao *Factory* foi a decisão arquitetural de maior impacto, pois resolve diretamente a dor do ambiente clínico universitário: a variação constante de modalidades de atendimento. Optar por servir o frontend desacoplado da lógica de backend no mesmo container reduziu o custo de infraestrutura no deploy, mantendo a experiência do usuário final rica, dinâmica e com validação de fusos horários (Timezones) tratada diretamente no cliente.