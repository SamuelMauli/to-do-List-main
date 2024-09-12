# To-Do List Web Application

**Desenvolvido com Flask**

## Descrição do Projeto

O objetivo deste projeto é desenvolver uma aplicação web utilizando Python, que simula as funcionalidades básicas de um sistema de gerenciamento de tarefas, semelhante ao Trello. A aplicação permite que os usuários gerenciem suas tarefas, oferecendo funcionalidades como criação, edição, exclusão e atribuição de tarefas a outros usuários, além de monitorar o status das tarefas (pendente, em andamento, concluída).

## Funcionalidades

1. **Cadastro e Autenticação de Usuários**

   - **Registro de Novos Usuários**: Permite o cadastro de novos usuários.
   - **Login e Logout**: Controle de sessão para acesso seguro às tarefas pessoais de cada usuário.
   - **Gerenciamento de Sessões**: Cada usuário pode acessar e gerenciar suas próprias tarefas individualmente.

2. **Gerenciamento de Tarefas**

   - **Criação de Tarefas**: Usuários podem adicionar novas tarefas, especificando título, descrição e status.
   - **Visualização de Tarefas**: Exibe uma lista de todas as tarefas atribuídas ao usuário.
   - **Edição de Tarefas**: Permite atualizar as informações de uma tarefa existente.
   - **Exclusão de Tarefas**: Usuários podem remover tarefas que não são mais necessárias.
   - **Atribuição de Tarefas**: As tarefas podem ser atribuídas a outros usuários, promovendo a colaboração.

3. **Status das Tarefas**

   - **Filtragem por Status**: As tarefas podem ser filtradas com base no status (pendente, em andamento, concluída) para facilitar a organização e o acompanhamento.

4. **Dashboard**
   - **Acompanhamento do Grupo**: Um painel para visualizar todas as tarefas do grupo, oferecendo uma visão geral das atividades em andamento.

## Desenvolvimento e Tecnologias

O sistema é desenvolvido utilizando o framework **Flask** para o backend e **SQLite** como banco de dados. A autenticação de usuários é implementada para garantir acesso seguro e individual às tarefas. A interface do usuário é criada com **HTML/CSS**, com um design simples e minimamente responsivo.

### Dependências

As dependências necessárias para o projeto estão listadas em `requirements.txt` e incluem:

- `Flask==2.0.1`
- `Flask-SQLAlchemy==2.5.1`
- `SQLAlchemy==1.4.47`
- `Jinja2==3.1.4`
- `MarkupSafe==2.1.5`
- `click==8.1.7`
- `itsdangerous==2.2.0`
- `bcrypt==4.0.1`

### Como Executar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/SamuelMauli/to-do-List-main
   ```

2. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o Servidor:**

   ```bash
   python app.py
   ```

4. **Acesse a Aplicação:**

- Abra um navegador e vá para http://127.0.0.1:5000/.

## Contribuidores

Este projeto foi desenvolvido pelos alunos:

- **Samuel Giuseppe Mauli**  
  RGM: 34855149

- **Luiz Eduardo Aben Athar Ribeiro**  
  RGM: 33817511

- **Pedro Ferreira Rossi**  
  RGM: 34289968
