from botcity.maestro import *
from botcity.plugins.email import BotEmailPlugin
from botcity.plugins.googlesheets import BotGoogleSheetsPlugin
from botcity.web import WebBot, Browser, By
from botcity.web.parsers import table_to_dict

from dotenv import load_dotenv
import os

# Desabilitando erros caso não exista conexão com o Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

CAMINHO_ARQUIVO_CREDENCIAIS = "credenciais.json"
ID_PLANILHA = "1Bho0kZb1FDRj-dA-T5qJZ-mc3q32R7KlmyN4hmJyEDc"
CEPS = ['57025070','71691181','69033615']

def main():
    load_dotenv()

    # Instanciando o Maestro SDK
    maestro = BotMaestroSDK.from_sys_args()
    
    # Este código precisa ser executado apenas se estivermos rodando o robô localmente
    # e precisamos nos conectar ao Orquestrador.
    # maestro.login(
    #     server=os.getenv('MAESTRO_SERVER'), 
    #     login=os.getenv('MAESTRO_LOGIN'), 
    #     key=os.getenv('MAESTRO_KEY')
    # )

    # Buscando os detalhes da tarefa atual sendo executada
    execution = maestro.get_execution()

    bot = WebBot()

    # Deixando o navegador visível para acompanharmos a execução
    bot.headless = False

    bot.browser = Browser.FIREFOX
    bot.driver_path = r"resources\geckodriver.exe"

    try:
        bot_planilha = BotGoogleSheetsPlugin(CAMINHO_ARQUIVO_CREDENCIAIS, ID_PLANILHA)

        for cep in CEPS:
            enderecos = consultar_ceps(cep, bot)
            for endereco in enderecos:
                bot_planilha.add_rows([[
                    endereco['logradouronome'],
                    endereco['bairrodistrito'],
                    endereco['localidadeuf'],
                    endereco['cep']
                ]])    

        # É importante finalizar o browser para evitarmos problemas.
        bot.stop_browser()

        enviar_email(maestro)

        # Este trecho de código serve para finalizar a tarefa,
        # informando que ela foi executada com sucesso.
        # Se estiver rodando local, pode deixar comentado.
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="CEPs cadastrados com sucesso."
        )
    except:
        # Este trecho de código serve para finalizar a tarefa,
        # informando que ela foi executada com falha.
        # Se estiver rodando local, pode deixar comentado.
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.FAILED,
            message="Cadastro falhou."
        )


def consultar_ceps(cep, bot: WebBot):
    bot.browse("https://buscacepinter.correios.com.br/app/endereco/index.php")

    campo_endereco = bot.find_element("endereco", By.ID)
    campo_endereco.send_keys(cep)

    botao_buscar = bot.find_element("btn_pesquisar", By.ID)
    botao_buscar.click()

    endereco = bot.find_element("resultado-DNEC", By.ID)
    endereco = table_to_dict(endereco)

    return endereco


def enviar_email(maestro: BotMaestroSDK):

    # Aqui estamos buscando as credenciais no Orquestrador por segurança às informações sensíveis.
    email_login = maestro.get_credential('ACESSO_EMAIL', 'email_login')
    senha_login = maestro.get_credential('ACESSO_EMAIL', 'email_senha')

    # Instanciar o plugin de email
    email = BotEmailPlugin()

    # Configure IMAP com o servidor Gmail
    email.configure_imap("imap.gmail.com", 993)

    # Configure SMTP com o servidor Gmail
    email.configure_smtp("imap.gmail.com", 587)

    # Faça login com uma conta de email válida
    email.login(email_login, senha_login)

    # Definindo os atributos que comporão a mensagem
    para = ["livecodingrpa@gmail.com"]
    assunto = "Olá Mundo!"
    corpo_email = "<h1>Olá!</h1> Esta é uma mensagem de teste!"

    # Enviando a mensagem de e -mail
    email.send_message(assunto, corpo_email, para, use_html=True)

    # Feche a conexão com os servidores IMAP e SMTP
    email.disconnect()


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
