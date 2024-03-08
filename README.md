# Descrição do projeto
Neste repositório, temos um exemplo de projeto de uma automação RPA desenvolvida em Python com o framework da BotCity. Essa automação lê os CEPs recebidos, consulta no site dos Correios do Brasil, salva as informações em uma planilha do Google Sheets e faz o envio de e-mail para avisar que o cadastro funcionou.

Este projeto foi desenvolvido junto com a comunidade durante live coding que ficou salva [neste link](https://www.youtube.com/live/VCOYDfLRhoY?si=wCNjWrsjSLgacqIJ). Caso queira acompanhar as próximas lives, basta acompanhar as novidades no [canal no YouTube](https://www.youtube.com/@botcity_br) ou ainda por [esta página no LinkedIn](https://www.linkedin.com/company/botcity).

# Preparar o ambiente
Para executar este projeto, você deverá fazer a etapa de [pré-requisitos desta documentação](https://documentation.botcity.dev/pt/getting-started/prerequisites/), que basicamente são os itens abaixo.

## Pré-requisitos:
- [Conta BotCity](https://developers.botcity.dev/app/signup);
- [BotCity Studio SDK](https://documentation.botcity.dev/pt/getting-started/botcity-studio-sdk/);
- [Python 3.7 ou superior](https://www.python.org/downloads/);
- Ter uma IDE instalada, por exemplo: [Visual Studio Code](https://code.visualstudio.com/download) ou [PyCharm](https://www.jetbrains.com/pycharm/download/).

Ao instalar o BotCity Studio SDK, caso aconteça algum problema, você pode usar a ferramenta de diagnóstico para validar o que pode ter acontecido. Para acessar essa ferramenta, verifique [este link](https://documentation.botcity.dev/pt/getting-started/botcity-studio-sdk/#ferramenta-de-diagnostico) da documentação.

# Antes de executar
Atenção aos passos que deve seguir após fazer o fork e clone do projeto em seu computador.

## 01. Crie ambiente virtual
Você pode utilizar ambiente virtual com o Python, se preferir. E para criá-lo, execute o seguinte comando:
```
python -m venv venv
```

Após a criação, é necessário ativá-lo. Para isso, execute o comando abaixo:
```
venv\Scripts\activate
```

## 02. Instale as dependências do `requirements.txt`
Para fazer a instalação das dependências do projeto, você deve executar no terminal da sua IDE o comando abaixo, a partir da pasta do projeto:
```
pip install --upgrade -r requirements.txt
```

## 03. Crie a credencial para acesso ao e-mail no BotCity Orquestrador
Para acesso ao e-mail de maneira mais segura, criamos a credencial na plataforma do Orquestrador. O nome dado durante o desenvolvimento do projeto foi ``. Você pode ajustar isso, mas é importante lembrar de ajustar também no código. Para orientações de como criar a credencial, você pode seguir [este passo-a-passo](https://documentation.botcity.dev/pt/maestro/features/credentials/).

## 04. Faça a configuração da API do Google Sheets
No projeto criado, estamos utilizando a planilha do Google Sheets. Para seguir o mesmo modelo, você deverá configurar corretamente a API do Google Sheets com os seus acessos, conforme descrito no [passo-a-passo da documentação](https://documentation.botcity.dev/pt/plugins/google/sheets/).

## 05. Faça a configuração do Plugin de E-mail
No projeto criado, estamos utilizando o plugin de e-mail para envio de mensagens pelo Gmail. Caso você queira ajustar para outro tipo de e-mail, siga a [documentação e as orientações descritas](https://documentation.botcity.dev/pt/plugins/email/).

## 06. Ajuste o login do Orquestrador
Quando estamos executando o robô localmente e queremos acessar o Orquestrador para buscar alguma informação, por exemplo, o caso das credenciais para acesso ao e-mail, precisamos fazer login na ferramenta, para que a conexão aconteça da maneira correta. Para isso, observe o arquivo `.env_example`. Você deverá renomeá-lo para `.env` e preencher as informações com o seu acesso. Para descobrir as suas informações, verifique a tela "Amb. de Desenvolvedor", ou ainda, siga as [orientações da documentação](https://documentation.botcity.dev/pt/maestro/features/dev-environment/).

O arquivo deverá ter as seguintes informações:
```
MAESTRO_LOGIN = "coloque o login aqui"
MAESTRO_KEY = "coloque a key aqui"
MAESTRO_SERVER = "coloque o server aqui"
```

## 07. Valide permissionamento
Para executar no seu computador ou máquina virtual, garanta que você tem permissão para rodar scripts, códigos etc.

## 08. Crie a sua planilha no Google Sheets e verifique os CEPs para consulta
Após criar a sua planilha, substitua a constante no código:
```
ID_PLANILHA = "insira o id da planilha aqui"
```

Ajuste também os CEPs que você deseja consultar e ajuste na constante no código:
```
CEPS = ['cep1','cep2','cep3']
```

## 09. Adicione os e-mails que deseja enviar
Na função `enviar_email(maestro: BotMaestroSDK)` você deve identificar a linha `para = ["email1", "email2"]` e adicionar para quais e-mails deseja enviar a mensagem.

# Para executar local
Se você quiser testar primeiramente no seu computador ou máquina virtual, você deverá:

## 01. Deixar o código de login descomentado
Identifique no código principal, o trecho para fazer login no BotCity Orquestrador com o SDK do Maestro. Ao identificá-lo, deixe o código para ser executado, ou seja, sem comentário.
```
    maestro.login(
        server=os.getenv('MAESTRO_SERVER'), 
        login=os.getenv('MAESTRO_LOGIN'), 
        key=os.getenv('MAESTRO_KEY')
    )
```

## 02. Comente os códigos que usam o `execution`
Quando estamos executando o robô localmente, não temos uma tarefa criada. Sendo assim, precisamos comentar os códigos que tenham relação com isso para evitar erros. São eles:
```
...
# execution = maestro.get_execution()
...
try:
    ...
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="CEPs cadastrados com sucesso."
    # )
except:
    ...
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.FAILED,
    #     message="Cadastro falhou."
    # )
```

## 03. Execute o robô
Você pode executar clicando no botão de play ou de execução da sua IDE favorita, ou ainda executar o comando abaixo no seu terminal:
```
python bot.py
```

# Para executar no BotCity Orquestrador
Quando estamos executando o robô no Orquestrador, a tarefa será criada, então não precisamos deixar os códigos do item anterior comentados. Tire os comentários para que os códigos possam ser executados corretamente. O único código que você deverá comentar neste caso é o do login. Uma outra forma de lidar com essa questão de ambiente, seria fazer uma validação, demonstrada neste artigo: [Como identificar se a automação está executando localmente ou no BotCity Orquestrador?](https://dev.to/botcitydev/como-identificar-se-a-automacao-esta-executando-localmente-ou-no-botcity-orquestrador-3kh8)

Lembre-se de seguir as orientações da [documentação](https://documentation.botcity.dev/pt/tutorials/orchestrating-your-automation/) para fazer o deploy da sua automação no Orquestrador e executar com apoio do Runner.

# Próximos passos
Há diversas possibilidades de melhorias neste projeto e deixo à disponibilidade da comunidade para explorarmos essas melhorias e implementarmos. Algumas sugestões:
- Receber o ID da planilha como parâmetro na execução do robô;
- Receber o CEP de consulta como parâmetro na execução do robô ou ainda consumir de uma planilha;
- Ajustar a separação de ambiente para saber se estamos executando local ou no Orquestrador;
- Refatorar o código para melhor separação de responsabilidades;
- Criar mensagem de e-mail com mais detalhes e informações e formatá-la com apoio da [biblioteca Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#quick-start);
- Entre outros.

  Fiquem à vontade de mandar sugestões e correções pelas issues do projeto.
