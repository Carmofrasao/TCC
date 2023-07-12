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

* https://nvd.nist.gov/vuln/search
* https://blog.saninternet.com/lista-de-plugins-wordpress-com-vulnerabilidades

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
