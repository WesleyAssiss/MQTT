# MQTT

SISTEMAS DISTRIBUÍDOS

Você foi contratado para desenvolver a comunicação em um jogo de movimentação de bolas em um campo.

Seu chefe está convicto que a melhor abordagem de comunicação nesse jogo distribuído é um estilo arquitetônico baseado em eventos. Assim, ele definiu as seguintes tarefas a serem seguidas:
Criar um servidor MQTT que permita intermediar a comunicação entre todos os jogadores;
Para cada jogador:
Criar um cliente publicador, que após o jogador fazer um movimento, este movimento deve ser publicado no servidor MQTT;
Criar um cliente assinante, que recebe os movimentos de todos os jogadores e atualiza a jogada em sua interface gráfica.
Cada jogador deve utilizar uma máquina física diferente, mas um servidor MQTT pode estar executando em background em uma mesma máquina de um cliente (para simplificar o desenvolvimento);
Não a limitação de jogadores nesse jogo.


