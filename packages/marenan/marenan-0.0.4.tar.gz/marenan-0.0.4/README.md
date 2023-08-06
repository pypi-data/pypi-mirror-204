# marenan

Pacote para simbolizar o amor entre Mari e Renan.

## Início

Instalação:

```shell
pip install marenan
```

Execute um dos comandos:

```shell
marenan
python -m marenan
```

Ou importe em um módulo Python:

```python
from marenan import marenanDay

print(marenanDay().strftime("%d/%m/%Y"))
```

## Desenvolvimento

Este pacote foi desenvolvido com o gerenciador de pacotes PDM, assim é necessário instalá-lo:

```shell
pip install pdm
```

Pra fazer as principais operações de desenvolvimento com ele é preciso apenas usar seus comandos:

```shell
pdm install      #Para instalar as dependências
pdm build        #Para gerar a build do projeto
pdm publish      #Para gerar o build e publicar o projeto
```

E para testar o pacote em desenvolvimento, existem as opções:

```shell
pdm cli          #Roda a versão CLI do programa
pdm interactive  #Roda um shell python interativo com o módulo importado
```
