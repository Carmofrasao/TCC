# TCC

Container engine (comunicação): Identificar uma maneira de coletar informações de uma aplicação que esteja rodando dentro do 
ambiente de container. Seguindo a segunda e terceira proposta do artigo ISCC2021 (a ideia é ficar dentro do ambiente do container). 

## Pluging que permite coletar informações/interações entre container e o container engine

### Fluentd 

#### Referencias

* https://docs.fluentd.org/container-deployment/install-by-docker
* https://docs.fluentd.org/configuration/config-file

#### Instalação e Uso (Deve ser executado antes de subir o wordpress)

Identifique o ID do container wordpress:

    sudo docker ps

Substitua o ID que esta em `./tmp/fluentd.conf`

Rode:

    sudo docker run -p 24224:24224 -v $(pwd)/../tmp:/fluentd/etc fluent/fluentd:edge-debian -c /fluentd/etc/fluentd.conf

Após esse passo, inicialize o container.

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

##### Dataset Versão 1

Wordpress: 4.9.14

* CVE-2019-9978 - Plugin Social Warfare (Versão: <= 3.5.3). Permite a execução de código arbitrário no alvo em uma funcionalidade que gerencia a importação de configurações.

##### Dataset Versão 2

Wordpress: 4.9.2 

* CVE-2019-9978 – A mesma vulnerabilidade explorada na formação do comportamento anômalo da primeira versão do dataset;
* CVE-2020-25213 – O plugin File Manager (wp-file-manager) anterior à versão 6.9 permite o upload e execução código PHP arbitrário;
* CVE-2020-12800 – O plugin Drag and Drop Multiple File Upload – Contact Form 7 anterior à versão 1.3.3.3 permite o upload de arquivos sem restrição, o que permite a execução de código PHP arbitrário;
* Vulnerabilidade encontrada no plugin AIT CSV Import/Export com versão menor ou igual a 3.0.3, que permite o upload e execução de código PHP, por conta de uma falha do plugin em verificar e validar os arquivos enviados; e
* Vulnerabilidade presente no plugin Simple File List (simple-file-list) com versão anterior à 4.2.3, que falha em validar extensões de arquivos ao renomear, permitindo o upload e execução de arquivos PHP.

## Wordpress

### Dockerfile

Buldando o container:

    docker build -t wordpress .

Para subir o container:

    docker run -p 9000:80 wordpress

------------------------------------------------------

### docker-compose

Para subir o container:

    sudo docker-compose up

------------------------------------------------------

### Meu wordpress:

    Link            http://localhost:9000/wp-admin/
    Site Title      TCC
    Username        eu
    Password        TCCAnderson.

------------------------------------------------------

Para remover as imagens que estão rodando:

    sudo docker system prune && sudo docker rmi $(sudo docker images -q)
    