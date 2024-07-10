# toolbox
Projeto pessoal, feito em python com intuito de melhorar minhas habilidades na linguagem e criar uma experiência de uso no terminal do Linux.

Em um primeiro momento a caixa de ferramentas irá realizar requisições usando métodos .get e .post em algumas api's. Portanto, além de instalar a biblioteca requests, você necessitará das chaves de acesso para utilizar as api's, que em geral são gratuitas.

Na versão atual do código em relação as "tarefas" salvas, só é possível criar uma nova tarefa ou listar as existentes de acordo com uma data. Esta no road-map incluor funções para editar ou apagar uma tarefa.

Vale a pena lembrar que essas requisições são feitas na api do Google Firebase, ou seja, essas tarefas estão sinconizadas em tempo real.

Você pode criar sua conta no Firebase através deste caminho: https://firebase.google.com/
Obs.: Lembre-se de mudar as regras do banco.
E pode criar sua conta no weatherpi aqui: https://www.weatherbit.io/

----------------------------------------------------------------------------------


Nesta versão é possível criar uma nova tarefa, listar as tarefas por data, bem como listar todas as tarefas não realizadas. Também é possível editar suas tarefas, em todos os campos disponíveis, que são: data, nome, tarefa e status. Também é possível verificar as condições climáticas de um determinado local.

Por se tratar de uma versão muito recente, ainda não foram implementadas todas as funções, como por exemplo para deletar tarefas, que já está na rota para ser criada.
Um ponto importante é que você pode voltar para o menu inicial a qualquer momento que possa dar algum input, basta escrever 'q' sem aspas, alguns campos também possuem alguns atalhos que ainda precisam ser melhor definidos, como por exemplo escrever 'now' para colocar a data atual para criar uma nova tarefa, bom, decidi em não deixar nada disso explicíto na aplicação para não poluir ainda mais o ambiente, bom, fica como easter egg.
