"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""

# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from botcity.web.util import element_as_select
from botcity.web.parsers import table_to_dict
from botcity.plugins.excel import BotExcelPlugin
# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

excel = BotExcelPlugin()
excel.add_row(['CIDADE', 'POPULAÇÃO'])

def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()
    # maestro.login(server="https://developers.botcity.dev", login="ad315e1d-e34f-4d30-be80-c170563093f4", key="AD3_NGK7WZLW6EJ5BFMFJCIF")

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path = r"C:\Users\laura.bonilha\Downloads\chromedriver-win64\chromedriver.exe"

    # Opens the BotCity website.
    bot.browse("https://buscacepinter.correios.com.br/app/faixa_cep_uf_localidade/index.php")

    drop_uf = element_as_select(bot.find_element("//select[@id='uf']", By.XPATH))
    drop_uf.select_by_value("SP")

    btn_pesquisar = bot.find_element("//button[@id='btn_pesquisar']", By.XPATH)
    btn_pesquisar.click()

    bot.wait(3000)

    table_dados = bot.find_element("//table[@id='resultado-DNEC']", By.XPATH)
    table_dados = table_to_dict(table=table_dados)

    bot.navigate_to("https://cidades.ibge.gov.br/brasil/sp/panorama")


    int_Contador = 1

    str_CidadeAnterior = ""

    for cidade in table_dados:

        str_Cidade = cidade["localidade"]

        if str_CidadeAnterior == str_Cidade:
            continue

        if int_Contador <=5:

            campo_pesquisa = bot.find_element("//input[@placeholder='O que você procura?']", By.XPATH)
            campo_pesquisa.send_keys(str_Cidade)

            opcao_cidade = bot.find_element(f"//a[span[contains(text(), '{str_Cidade}')] and span[contains(text(), 'SP')]]", By.XPATH)
            bot.wait(1000)
            opcao_cidade.click()

            bot.wait(2000)

            populacao = bot.find_element("//div[@class='indicador__valor']", By.XPATH)
            str_populacao = populacao.text

            print(str_Cidade, str_populacao)
            excel.add_row([str_Cidade, str_populacao])
            maestro.new_log_entry(activity_label="CIDADES", values={"CIDADE": f"{str_Cidade}",
                                                                    "POPULACAO": f"{str_populacao}"})


            int_Contador = int_Contador + 1
            str_CidadeAnterior = str_Cidade
        else:
            print("Número de cidades já alcançado")
            break

    excel.write("C:\Projetos Treinamento\Infos_Cidades.xlsx")
    # Implement here your logic...
    ...

    # Wait 3 seconds before closing
    bot.wait(5000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    # bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
         task_id=execution.task_id,
         status=AutomationTaskFinishStatus.SUCCESS,
         message="Task Finished OK."
     )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
