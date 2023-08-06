# marenan

Pacote para simbolizar o amor entre Mari e Renan.

## Início

Instalação:

```
pip install marenan
```

Execute um dos comandos:

```
marenan
python -m marenan
```

Ou importe em um módulo Python:

```python
from marenan import marenanDay

print(marenanDay().strftime("%d/%m/%Y"))
```

## Desenvolvimento

Este pacote foi desenvolvido com o gerenciador de pacotes PDM, assim para fazer as principais operações de desenvolvimento é preciso apenas usar seus comandos:

```shell
pdm install   #Para
```

### Atualização da distribuição do pacote no PyPI

#### Build

```
python3 setup.py sdist bdist_wheel
```

Para os passos a seguir é preciso garantir que possui instalado o pacote `twine`. Se necessário instale com `pip install twine`.

#### Checkagem

```
twine check dist/*
```

#### Upload

Para realizar o upload é preciso ser um desenvolvedor do pacote e possuir as credenciais para upload no PyPI.

```
twine upload dist/*
```
