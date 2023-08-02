# TCC

Container engine (comunicação): Identificar uma maneira de coletar informações de uma aplicação que esteja rodando dentro do 
ambiente de container. Seguindo a segunda e terceira proposta do artigo ISCC2021 (a ideia é ficar dentro do ambiente do container). 

## Plugin que permite coletar informações/interações entre container e o container engine

### Fluentd 

#### Referencias

* https://docs.fluentd.org/container-deployment/install-by-docker
* https://docs.fluentd.org/configuration/config-file

#### Instalação e Uso (Deve ser executado antes de subir o wordpress)

Identifique o ID do container wordpress:

    sudo docker ps

Substitua o ID que esta em `./tmp/fluentd.conf`

Rode:

    sudo docker run -p 24224:24224 -v $(pwd)/tmp:/fluentd/etc fluent/fluentd:edge-debian -c /fluentd/etc/fluentd.conf

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

## Wordpress

Para subir o container:

    sudo docker-compose up -d

------------------------------------------------------

### Meu wordpress:

    Link            http://localhost:9000/wp-admin/
    Site Title      TCC
    Username        eu
    Password        TCCAnderson.

------------------------------------------------------

Para remover as imagens que estão rodando:

    sudo docker system prune && sudo docker rmi $(sudo docker images -q)
    
------------------------------------------------------

Caso as imagens sejam removidas, sera necessario algumas configurações no container. 

* Para colocar o plugin File Manager (pois ele é grande), siga os seguintes passos:

1. Acesse o container Docker do WordPress:
```
sudo docker exec -it wordpress bash
```
2. Crie o arquivo `php.ini`:
```
touch /usr/local/etc/php/php.ini
```
3. Aumente o tamanho máximo de upload de arquivos:
```
echo "upload_max_filesize = 100M" > /usr/local/etc/php/php.ini
```
4. Reinicie o container do WordPress.

* Para rodar scripts python:

1. Acesse o container Docker do WordPress:
```
sudo docker exec -it wordpress bash
```
2. Edite o arquivo `/etc/apt/sources.list`:
```
sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list
sed -i s/security.debian.org/archive.debian.org/g /etc/apt/sources.list
```
3. Atualize o sistema:
```
apt-get update
```
4. Instale o python:
```
apt-get install python3-pip
```

## Plugins vulneravei para Wordpress

Em ultimo caso:

https://wpscan.com/plugins

Wordpress: 4.9.2 

* CVE-2019-9978 - Plugin Social Warfare (Versão: < 3.5.3). Permite a execução de código arbitrário no alvo em uma funcionalidade que gerencia a importação de configurações;

    Uso comum:
    * https://www.youtube.com/watch?v=Ks2787CrqA8
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/46794
    </br></br>
* CVE-2020-25213 – O plugin File Manager (wp-file-manager) (versão: <= 6.9). Permite o upload e execução código PHP arbitrário;

    Uso comum:
    * https://www.youtube.com/watch?v=5-iZX2sUHuQ
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/51224
    </br></br>
* CVE-2020-12800 – O plugin Drag and Drop Multiple File Upload – Contact Form 7 (versão: < 1.3.3.3). Permite o upload de arquivos sem restrição, o que permite a execução de código PHP arbitrário;

    Uso comum:
    * https://www.youtube.com/watch?time_continue=16&v=eUQK7gsLevs
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/48520
    </br></br>
* Vulnerabilidade presente no plugin Simple File List (simple-file-list) (versão: < 4.2.3). Falha em validar extensões de arquivos ao renomear, permitindo o upload e execução de arquivos PHP.

    Uso comum:
    * https://simplefilelist.com/pt/
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/48979
    </br></br>
* Vulnerabilidade presente no plugin Easy Modal (versão: = 2.0.17). Injeção de SQL com escalada de privilegio.

    Uso comum:
    * https://easy-modal.com/getting-started/how-to-make-a-pop-up
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/42431
    </br></br>
* CVE-2022-3141 – O plugin Translate Multilingual sites (versão: < 2.3.3). Injeção de SQL autenticada.

    Uso comum:
    * https://www.youtube.com/watch?v=pUlYisvBm8g&t=2s
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/51043
    </br></br>
* CVE-2022-3142 – O plugin NEX-Forms (versão: < 7.9.7). Injeção de SQL autenticada.

    Uso comum:
    * https://www.youtube.com/watch?v=9qW7cZfdxQ8
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/51042
    </br></br>
*  Vulnerabilidade presente no plugin wpDiscuz (versão: 7.0.4). Upload de arquivo arbitrário, permitindo upload de arquivos PHP, e execução remota de código.

    Uso comum:
    * https://www.youtube.com/watch?v=woPqPgvkkQ8
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/49401
    </br></br>
* Vulnerabilidade presente no plugin Payments forms (versão: 2.4.6). Injeção de código arbitrario.

    Uso comum:
    * https://www.youtube.com/watch?v=gGtehIjDG3E&t=80s
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/50246
    </br></br>
* Vulnerabilidade presente no plugin Custom Global Variables (versão: 1.0.5). Injeção de código arbitrario.

    Uso comum:
    * https://br.wordpress.org/plugins/custom-global-variables/
    </br></br>

    Ataque:
    * https://www.exploit-db.com/exploits/49406

## Coleta de dados e treinamnto do modelo

0. 
    1x10 mali.  
    1x10 comp. Normais  

    uma coleta  

1. gerar trace  
open(..)  
mmap(..)  
mmap(..)  
read()  
read()  
fseek()  
exit  

2. criar janelas  
overlap = 1  

3. treinar modelo  
.csv  
ID feature1, f2, f3  
1 [open mmap mmap]  
1 [mmap read read]  
1 [read fseek exit]  
-> ML  

    ML <- f1,f2,f3  
    result = .predict()  
    result.XXX(ID)  
