from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dttm
import getpass as gtp
import pandas as pd
import time


#definicoes de funçoes

def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.get(url)

    return driver

def login(lg_user='admin@admin.com', lg_password='password'):
    #Loga como admin (login padrao)
    email = driver.find_element_by_id("email")
    senha = driver.find_element_by_id("password")
    button = driver.find_element_by_xpath('//*[@id="login-form"]/div[2]/div[2]/button')

    email.send_keys(lg_user)
    senha.send_keys(lg_password)
    button.click()

def export():
    df_export = pd.DataFrame({'NOME' : user_export,
    'EMAIL' : email_export,
    'STATUS' : 'EXCLUÍDO',
    'EXCLUSÃO' : hr_export
    }
    )
    data = dttm.now()
    file_name = 'log_{}.xlsx'.format(data.strftime('%d_%m_%Y_%H_%M'))
    df_export.to_excel(file_name)
    print(df_export)

#leitura lista de users

arq = input("Digite o caminho do arquivo:\n")
column = []
column.append(str(input('Digite o nome da coluna que contém os emails dos usuários:\n')))

user_list = pd.DataFrame(pd.read_excel(arq)).astype('string')
print(user_list)
list_size = user_list[user_list.columns[0]].count()




url = "http://{}/settings/users".format(input("Digite o url da Wiki:\n"))
lg_user = input('Digite seu usuário:\n')
lg_password = gtp.getpass('Digite sua Senha:\n')
print(url)
driver = get_driver(url)


login(lg_user, lg_password)

user_export = []
email_export = []
hr_export = []
index = 0

driver.get(url)
while(index < list_size):
    try:
        print(user_list.loc[index, column[0]])
        email = user_list.loc[index, column[0]]
        email_export.insert(index, email)
        url_busca = '{}?search={}'.format(url, email)
        driver.get(url_busca)
        user = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/main/div[3]/div/div[1]/a')
        user_export.insert(index, user.text)
        driver.execute_script("arguments[0].click();", user)

        driver.find_element(By.XPATH, '//*[@id="main-content"]/div/section[1]/form/div[2]/a[2]').click()
        driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[2]/div/form/button').click()
        hora = dttm.now()
        hora = hora.strftime('%d/%m/%Y %H:%M:%S')
        hr_export.insert(index, hora)

        index += 1
    except:
        index += 1

export()