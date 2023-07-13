# TCC

Container engine (comunicação): Identificar uma maneira de coletar informações de uma aplicação que esteja rodando dentro do 
ambiente de container. Seguindo a segunda e terceira proposta do artigo ISCC2021 (a ideia é ficar dentro do ambiente do container). 

## Pluging que permite coletar informações/interações entre container e o container engine

### Fluentd 

#### Referencias

* https://docs.fluentd.org/container-deployment/install-by-docker
* https://docs.fluentd.org/configuration/config-file

#### Instalação

Identifique o ID do container wordpress:

    sudo docker ps

Substitua o ID que esta em `/wordpress/tmp/fluentd.conf`

#### Uso (Deve ser executado antes de subir o wordpress)

    sudo docker run -p 24224:24224 -v $(pwd)/tmp:/fluentd/etc fluent/fluentd:edge-debian -c /fluentd/etc/fluentd.conf

Após esse passo, inicialize o container.

Não consegui configurar um arquivo de log

### Sysdig

#### Referencias

* https://github.com/draios/sysdig
* https://github.com/draios/sysdig/wiki/Container-Enabled-Chisels

#### Instalação

    sudo apt-get install sysdig

#### Uso

Veja o uso da CPU dos processos em execução dentro do contêiner wordpress

    sudo sysdig -pc -c topprocs_cpu container.name=wordpress

Veja os processos usando a maior largura de banda da rede dentro do contêiner wordpress

    sudo sysdig -pc -c topprocs_net container.name=wordpress

Veja os arquivos superiores em termos de bytes de E / S dentro do contêiner wordpress

    sudo sysdig -pc -c topfiles_bytes container.name=wordpress

Veja as conexões de rede superiores dentro do contêiner wordpress

    sudo sysdig -pc -c topconns container.name=wordpress

Mostrar todos os comandos interativos executados dentro do contêiner wordpress

    sudo sysdig -pc -c spy_users container.name=wordpress

Mostrar todas as interações do container

    sudo sysdig -pc container.name=wordpress

## Plugins vulneravei para Wordpress

* https://blog.saninternet.com/lista-de-plugins-wordpress-com-vulnerabilidades

### Ruschel:

#### 5.1 CONJUNTO DE TESTES

Os experimentos foram realizados em um ambiente Linux 5.4.44-1-MANJARO utilizando a distribuição Manjaro 20.0.3, o ambiente de virtualização escolhido para a realização dos testes foi o Docker na versão 19.03.11-ce. Para realizar a avaliação é necessário um dataset que represente o comportamento a ser estudado, desta forma foram elaboradas duas versões de conjuntos de dados1 para serem utilizados nos testes, onde cada versão formou um dataset de comportamento normal e anormal a partir dos dados, obtidos pela captura de instâncias do Wordpress, o objeto alvo dos experimentos. Posteriormente foi aplicada a técnica de janela deslizante para gerar os modelos que são utilizados para o treinamento do classificador.

Para ambos datasets, dois grupos de testes foram elaborados, no primeiro caso todas as system calls são utilizadas, sem a aplicação de nenhum tipo de filtro, já para o segundo caso de teste chamadas classificadas como baixo nível de ameaça foram desconsideradas.

##### 5.1.1 Dataset Versão 1

Na formação do primeiro conjunto de dados utilizado nos testes, o processo de coleta ocorreu como descrito na seção 4.2, como objeto alvo um Wordpress na versão 4.9.14 executando em um contêiner com as modificações mencionadas.

A simulação de comportamento normal do Wordpress contou com um conjunto de hosts dentro da própria rede. Foi optado por utilizar variados sistemas operacionais que seriam responsáveis por interagir com o Wordpress, com diferentes hosts Windows e Linux sendo
utilizados. A simulação tentou explorar variadas rotinas e interações normais para a aplicação, como a criação de novos posts e comentários, e manutenções corriqueiras no blog de teste implantado como alvo do experimento.

Para a obtenção dos dados de comportamento anormal, foi realizada a exploração de uma vulnerabilidade identificada pelo código CVE-2019-9978. A vulnerabilidade afeta o plugin do Wordpress Social Warfare com versão menor ou igual a 3.5.3, e permite a execução de código arbitrário no alvo em uma funcionalidade que gerencia a importação de configurações. Foi capturado o comportamento de três execuções similares da exploração da vulnerabilidade para formar o conjunto de dados anormais.

Sobre esta primeira versão do conjunto de dados utilizados nos experimentos, é importante lembrar que a captura das chamadas foram realizadas a partir de execuções únicas, e salvas em arquivos únicos. O que significa que, no momento da simulação do comportamento normal, foi executado o strace para realizar a captura das chamadas e todas as simulações com o Wordpress foram realizadas a partir daquele momento, reunindo tudo em um único arquivo, e o mesmo processo aconteceu para a simulação do comportamento anômalo. Esse processo traz algumas desvantagens na qualidade e representatividade geral dos dados capturados, pois acaba gerando uma certa redundância de dados visto que muitas rotinas acabam gerando sequências de chamadas similares, e também não é o processo recomendado para a simulação destes comportamentos, pois não separa diferentes execuções.

##### 5.1.2 Dataset Versão 2

Para a formação da segunda versão do conjunto de dados utilizados nos experimentos, o processo de coleta ocorreu como descrito na seção 4.2, desta vez utilizando como objeto alvo o Wordpress na versão 4.9.2 executando em um contêiner, com as mesmas modificações citadas anteriormente. Para esta versão, a simulação dos comportamentos normais e anormais ocorreu de forma diferente. Para a simulação de comportamento normal, foram elaboradas 5 rotinas de execução envolvendo atividades normais corriqueiras de interação com o blog, e cada rotina foi executada da mesma maneira 5 vezes, onde o fluxo de chamadas de cada execução foi redirecionado para um arquivo diferente, totalizando 25 arquivos com fluxos de comportamento
normal.

A simulação do comportamento anômalo ocorreu de forma similar, onde foram exploradas 5 vulnerabilidades diferentes:

* CVE-2019-9978 – A mesma vulnerabilidade explorada na formação do comportamento anômalo da primeira versão do dataset;
* CVE-2020-25213 – O plugin File Manager (wp-file-manager) anterior à versão 6.9 permite o upload e execução código PHP arbitrário;
* CVE-2020-12800 – O plugin Drag and Drop Multiple File Upload – Contact Form 7 anterior à versão 1.3.3.3 permite o upload de arquivos sem restrição, o que permite a execução de código PHP arbitrário;
* Vulnerabilidade encontrada no plugin AIT CSV Import/Export com versão menor ou igual a 3.0.3, que permite o upload e execução de código PHP, por conta de uma falha do plugin em verificar e validar os arquivos enviados; e
* Vulnerabilidade presente no plugin Simple File List (simple-file-list) com versão anterior à 4.2.3, que falha em validar extensões de arquivos ao renomear, permitindo o upload e execução de arquivos PHP.

Cada exploração foi executada 5 vezes e em cada execução o fluxo de chamadas foi redirecionado para um arquivo diferente, totalizando 25 arquivos representando o conjunto de dados anormais.

## Wordpress

Meu wordpress:

    Link            http://localhost:9000/wp-admin/
    Site Title      TCC
    Username        eu
    Password        TCCAnderson.

Para subir o container:

    sudo docker-compose up

Para remover as imagens que estão rodando:

    sudo docker system prune && sudo docker rmi $(sudo docker images -q)
    