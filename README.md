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

Wordpress: 4.9.2 

* CVE-2019-9978 - Plugin Social Warfare (Versão: < 3.5.3). Permite a execução de código arbitrário no alvo em uma funcionalidade que gerencia a importação de configurações;

    Ataque:
    * https://www.exploit-db.com/exploits/46794
    </br></br>
* CVE-2020-25213 – O plugin File Manager (wp-file-manager) (versão: <= 6.9). Permite o upload e execução código PHP arbitrário;

    Ataque:
    * https://www.exploit-db.com/exploits/51224
    </br></br>
* Vulnerabilidade presente no plugin Simple File List (simple-file-list) (versão: < 4.2.3). Falha em validar extensões de arquivos ao renomear, permitindo o upload e execução de arquivos PHP.

    Ataque:
    * https://www.exploit-db.com/exploits/48979
    </br></br>
* Vulnerabilidade presente no plugin Payments forms (versão: 2.4.6). Injeção de código arbitrario.

    Ataque:
    * https://www.exploit-db.com/exploits/50246
    </br></br>
* CVE-2022-3142 – O plugin NEX-Forms (versão: < 7.9.7). Injeção de SQL autenticada.

    Ataque:
    * https://www.exploit-db.com/exploits/51042
    </br></br>
* Vulnerabilidade presente no plugin Mail Masta (versão: 1.0). Permite inclusão de arquivo, geralmente explorando um mecanismo de "inclusão dinâmica de arquivos" implementado no aplicativo de destino.

    Ataque:
    * https://www.exploit-db.com/exploits/40290
    </br></br>
* Vulnerabilidade presente no plugin Really Simple Guest Post (versão: 1.0.6). Local File Inclusion.

    Ataque:
    * https://www.exploit-db.com/exploits/37209
        </br></br>
* CVE: 2015-5065 – O plugin Paypal Currency Converter Basic For WooCommerce - File Read (versão: < 1.4). Download remoto de arquivos.

    Ataque:
    * https://www.exploit-db.com/exploits/37253
    </br></br>
* Vulnerabilidade presente no plugin LeagueManager (versão: 3.9.11). SQL Injection .

    Ataque:
    * https://www.exploit-db.com/exploits/37182
    </br></br>
* Vulnerabilidade presente no plugin CodeArt Google MP3 Player. File Disclosure Download.

    Ataque:
    * https://www.exploit-db.com/exploits/35460
    
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

### Tratamento dos dados

* Retirando cabeçalho e linha em branco dos logs do sysdig
```
sed -i".bak" '1,2d' *
```

* O arquivo `trata.py` retira as chamadas que não são syscall e faz a contagem de cada syscall que é feita no log

### Treinamento

* Erro atual (Com janela de tamanho 15)

```
Traceback (most recent call last):
  File "/usr/lib/python3.9/multiprocessing/pool.py", line 212, in __init__
    self._repopulate_pool()
  File "/usr/lib/python3.9/multiprocessing/pool.py", line 303, in _repopulate_pool
    return self._repopulate_pool_static(self._ctx, self.Process,
  File "/usr/lib/python3.9/multiprocessing/pool.py", line 326, in _repopulate_pool_static
    w.start()
  File "/usr/lib/python3.9/multiprocessing/dummy/__init__.py", line 51, in start
    threading.Thread.start(self)
  File "/usr/lib/python3.9/threading.py", line 874, in start
    _start_new_thread(self._bootstrap, ())
RuntimeError: can't start new thread

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/bcc/aacf20/TCC/main.py", line 386, in <module>
    ada_boost(base_normal, base_exec)
  File "/home/bcc/aacf20/TCC/main.py", line 227, in ada_boost
    abc.fit(X_train, y_train)
  File "/usr/lib/python3/dist-packages/sklearn/ensemble/_weight_boosting.py", line 443, in fit
    return super().fit(X, y, sample_weight)
  File "/usr/lib/python3/dist-packages/sklearn/ensemble/_weight_boosting.py", line 130, in fit
    sample_weight, estimator_weight, estimator_error = self._boost(
  File "/usr/lib/python3/dist-packages/sklearn/ensemble/_weight_boosting.py", line 503, in _boost
    return self._boost_real(iboost, X, y, sample_weight, random_state)
  File "/usr/lib/python3/dist-packages/sklearn/ensemble/_weight_boosting.py", line 515, in _boost_real
    y_predict_proba = estimator.predict_proba(X)
  File "/usr/lib/python3/dist-packages/sklearn/ensemble/_forest.py", line 682, in predict_proba
    Parallel(n_jobs=n_jobs, verbose=self.verbose,
  File "/usr/lib/python3/dist-packages/joblib/parallel.py", line 1051, in __call__
    if self.dispatch_one_batch(iterator):
  File "/usr/lib/python3/dist-packages/joblib/parallel.py", line 867, in dispatch_one_batch
    self._dispatch(tasks)
  File "/usr/lib/python3/dist-packages/joblib/parallel.py", line 785, in _dispatch
    job = self._backend.apply_async(batch, callback=cb)
  File "/usr/lib/python3/dist-packages/joblib/_parallel_backends.py", line 252, in apply_async
    return self._get_pool().apply_async(
  File "/usr/lib/python3/dist-packages/joblib/_parallel_backends.py", line 407, in _get_pool
    self._pool = ThreadPool(self._n_jobs)
  File "/usr/lib/python3.9/multiprocessing/pool.py", line 927, in __init__
    Pool.__init__(self, processes, initializer, initargs)
  File "/usr/lib/python3.9/multiprocessing/pool.py", line 216, in __init__
    p.terminate()
AttributeError: 'DummyProcess' object has no attribute 'terminate'

```