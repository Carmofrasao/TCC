# TCC

Container engine (comunicação): Identificar uma maneira de coletar informações de uma aplicação que esteja rodando dentro do 
ambiente de container. Seguindo a segunda e terceira proposta do artigo ISCC2021 (a ideia é ficar dentro do ambiente do container). 

Tipo de informações que são interessantes, comunicação do container com o container engine (esperado), strace, e logging.

## Pluging que permite coletar informações/interações entre container e o container engine

### Logstash
https://www.elastic.co/pt/logstash/ 

https://www.elastic.co/guide/en/logstash/current/docker-config.html

    docker build -t logstash .

    docker run --name container-logstash -p 5044:5044 --link container-elasticsearch:elasticsearch logstash

talvez consegui integrar no docker compose

### Fluentd 
* https://www.fluentd.org/architecture
* https://stackoverflow.com/questions/33601843/how-to-config-fluentd-with-docker
* https://www.digitalocean.com/community/tutorials/how-to-centralize-your-docker-logs-with-fluentd-and-elasticsearch-on-ubuntu-16-04
* https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
* https://docs.fluentd.org/container-deployment/install-by-docker
* https://docs.fluentd.org/configuration/config-file

COLOCAR ISSO VVVVV PARA RODAR, DAE RODAR O WORDPRESS 

    docker run -p 24224:24224 -v $(pwd)/tmp:/fluentd/etc fluent/fluentd:edge-debian -c /fluentd/etc/fluentd.conf

mensagem de teste, @FLUENT_LOG nãoesta mais configurado (fluent.conf)

    echo '{"json":"message"}' | fluent-cat @FLUENT_LOG -p 24224

Não consegui configurar um arquivo de log

### Sysdig
* https://github.com/draios/sysdig
* https://github.com/draios/sysdig/wiki/Container-Enabled-Chisels

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

* Usei a instalação desse lugar:

https://hub.docker.com/_/wordpress/

Meu wordpress:

    Link            http://localhost:9000/wp-admin/
    Site Title      TCC
    Username        eu
    Password        TCCAnderson.

Para subir o container:

    docker compose up

Para remover as imagens que estão rodando:

    docker system prune

* Gerar novos logs