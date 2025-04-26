import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import Options

# Carregar a planilha com os não seguidores
# Altere para o nome correto da sua planilha
df = pd.read_excel("D:\\AntonioLocal\\parar_de_seguir_python\\seguindo_nao_seguem.xlsx")

# Caminho do WebDriver (ajuste conforme necessário)
chrome_driver_path = "D:\\AntonioLocal\\Python\\parar_de_seguir\\chromedriver.exe"  # Substitua pelo caminho correto do seu WebDriver

# Configuração do Selenium
options = Options()
options.add_experimental_option("detach", True)  # Mantém o navegador aberto
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Realização do login na sua conta
url = f"https://www.instagram.com"
driver.get(url)
print('')
input("Faça Login na sua conta depois aperte enter...")
print('')

#Lista para criar uma tabela.
dados = []

# Percorre cada seguidor
for index, row in df.iterrows():
    perfil = row["Não te seguem de volta"]
    driver.get(f'{url}/{perfil}')
    time.sleep(5)

    try:
        # Coletar informação se o perfil é seguido
        status_perfil = driver.find_element(By.XPATH, "//div[@class='_ap3a _aaco _aacw _aad6 _aade']").text
        time.sleep(2)

        # Coletar a informação de quantos seguidores esse perfil tem
        var_suporte = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()=' publicações']"))
        )
        qtd_seguidores_perfil = var_suporte.find_element(By.XPATH, "./following::span[@class='x5n08af x1s688f']")
        qtd_seguidores_perfil = int(qtd_seguidores_perfil.get_attribute("title").replace(".", "")) # Pega informação do atributo e retira os pontos para transformar em inteiro.

        # Verificando se o perfil é apto para a ação de parar de seguir
        if status_perfil == 'Seguindo' and qtd_seguidores_perfil <= 40000:
            # Clica no botao 'Seguindo'
            status_perfil = driver.find_element(By.XPATH, "//div[@class='_ap3a _aaco _aacw _aad6 _aade']")
            status_perfil.click()
            time.sleep(2)

            # Clina no botao "Deixar de Seguir" na segunda janela que abre
            var_suporte = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Restringir']")))
            status_perfil = var_suporte.find_element(By.XPATH, "./following::span[@class='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft']")
            status_perfil.click()
            time.sleep(2)

            # Informação do andamento do codigo e organização da planilha.
            print(f"✅ {perfil} - Deixado de seguir!")
            dados.append({"Perfil": perfil, "Parou de seguir": 'sim', "Erro?": ''})
        elif status_perfil == 'Seguir':
            print(f"🟡 {perfil} - Já não seguia mais!")
            dados.append({"Perfil": perfil, "Parou de seguir": 'Já não seguia mais!', "Erro?": ''})
        else:
            print(f"❌ {perfil} - Não foi deixado de seguir!")
            dados.append({"Perfil": perfil, "Parou de seguir": 'não', "Erro?": ''})
    
    except Exception as e:
        print(f"❌ Erro ao coletar dados de {perfil}: {e}")
        dados.append({"Perfil": perfil, "Parou de seguir": '', "Erro?": 'X'})

# Criando data frame com os dados coletados
df = pd.DataFrame(dados)

# Salvando no Excel
df.to_excel("seguidores.xlsx", index=False)