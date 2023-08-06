# HeroJson

É um modúlo python criado para facilitar a manipulação de arquivos json.
Este modúlo tem como dependência o modúlo json(padrão do python).

## Funções

- **key(key : str)** -> *Traz o valor de uma determinada chave do arquivo json se esta existir e um None valor se não*.
- **update(key : str, value : any)** -> *Atualiza o valor de uma chave se esta existir e um None valor se não*.
- **drop(key : str)** -> *Deleta uma chave se esta existir*.
- **add(key : str, value : str)** -> *Adiciona um novo par chave e valor ao arquivo json*.
- **Allkeys()** -> *Retorna uma lista com todas as chaves existentes no arquivo json*.
- **AllValue()** -> *Retorna uma lista com todas os valores existentes no arquivo json*.
- **Content()** -> *Retorna o conteúdo do arquivo em formato de string*

## Página Oficial

- https://herojson.onrender.com

**Copyright Eliseu Gaspar**