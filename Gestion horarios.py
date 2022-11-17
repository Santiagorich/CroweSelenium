from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import ctypes

import datetime
dt = datetime.datetime.today()
today = datetime.datetime.today().strftime('%d/%m/%y')
message2 = "Hora agregada exitosamente!"
script = "document.getElementById('vGPGT_REGISTROHORAS_TAREAS_HORAINICIO_0001').value = '"+sys.argv[1]+"';document.getElementById('vGPGT_REGISTROHORAS_TAREAS_HORAFIN_0001').value = '"+sys.argv[2]+"';"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')  # Last I checked this was necessary.
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://apps.moyal.com.uy/GestionProyectos/servlet/seg_login")

username = driver.find_element_by_id("vUSUARIOID")
password = driver.find_element_by_id("vUSUARIOPASSWORD")

username.send_keys(sys.argv[3])
password.send_keys(sys.argv[4])

buttonlog = driver.find_element_by_css_selector("[name='BUTTON1']")

buttonlog.click()

print("Entrando a la cuenta...")

current_url = driver.current_url


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#IMAGETIEMPOS")))

#driver.find_element_by_id('IMAGETIEMPOS')

driver.get("https://apps.moyal.com.uy/GestionProyectos/servlet/gpgt_registrohoras_registro")



mes = Select(driver.find_element_by_id("vFMESACTIVIDAD"))
#anio = Select(driver.find_element_by_id("vFANIOACTIVIDAD"))

#anio.select_by_visible_text()
mes.select_by_value(str(int(dt.month)))
#insert = driver.find_element_by_id("INSERT")

#driver.implicitly_wait(3)

#insert.click()


#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vDIACOMBO")))

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#GridcabezalContainerRow_0001")))

print("Buscando horas...")

grid = driver.find_element_by_id('GridcabezalContainerDiv')
rows = grid.find_elements(By.TAG_NAME,'tr')

if len(rows) < 2:
    ctypes.windll.user32.MessageBoxW(0, "No se han encontrado registros, porfavor agregar uno", "Gestion Horarios", 0)
    driver.quit()
    sys.exit()
for row in rows:
    columns = row.find_elements(By.TAG_NAME,'td')
    for col in columns:
        if today in col.get_attribute('textContent'):
            print("Ya existe un registro para hoy, eliminando...")
            driver.get(row.find_element(By.CSS_SELECTOR,'[title="Eliminar"]').find_element(By.XPATH,"./..").get_attribute('href'))
            driver.execute_script("gx.evt.setGridEvt(32,null);gx.evt.execEvt('EENTER.',this)")
            message2 = "Hora modificada exitosamente!"
            break

driver.get("https://apps.moyal.com.uy/GestionProyectos/servlet/gpgt_registrohoras_ingreso?INS,0,230,,"+str(int(dt.month))+","+str(int(dt.year)))
print("Agregando registro...")
dia = Select(driver.find_element_by_id("vDIACOMBO"))
buttonag = driver.find_element_by_css_selector("[name='NUEVAFILA']")

dia.select_by_value(str(int(dt.day)))

buttonag.click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vGPGT_REGISTROHORAS_TAREAS_PROYECTOID_0001")))
proyecto = Select(driver.find_element_by_id("vGPGT_REGISTROHORAS_TAREAS_PROYECTOID_0001"))
tarea = Select(driver.find_element_by_id("vGPGT_REGISTROHORAS_TAREAS_TAREASNEGOCIOSID_0001"))

proyecto.select_by_visible_text(sys.argv[5])
tarea.select_by_visible_text(sys.argv[6])
#inicio = driver.find_element_by_id("vGPGT_REGISTROHORAS_TAREAS_HORAINICIO_0001")
#final = driver.find_element_by_id("vGPGT_REGISTROHORAS_TAREAS_HORAFIN_0001")

driver.execute_script(script)

#inicio.send_keys("0900")
#final.send_keys("1500")

buttonconf = driver.find_element_by_css_selector("[name='CONFIRMAR']")

buttonconf.click()

print("Consiguiendo registro...")

driver.get("https://apps.moyal.com.uy/GestionProyectos/servlet/gpgt_registrohoras_registro")
mes = Select(driver.find_element_by_id("vFMESACTIVIDAD"))
mes.select_by_value(str(int(dt.month)))
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#GridcabezalContainerRow_0001")))
grid2 = driver.find_element_by_id('GridcabezalContainerDiv')
rows2 = grid2.find_elements(By.TAG_NAME,'tr')
message = ""
for row2 in rows2:
    message +="\n"+row2.get_attribute('innerText').strip()

jsg = driver.execute_script("const lines = document.getElementsByClassName('GridOdd');var sumaextras = 0;if(lines.length>1){for (i=0;i<lines.length;i++){var trabajado = parseFloat(lines[i].getElementsByTagName('td')[7].innerText.replaceAll(',','.'));sumaextras+=trabajado-6;}return 'Horas extra: ' + sumaextras;   }    else {        return 'Sin Horas';    }")
message+="\n"+jsg

print("Hecho!")
ctypes.windll.user32.MessageBoxW(0, message2, "Gestion Horarios", 0)
ctypes.windll.user32.MessageBoxW(0, message, "Horas", 0)
driver.quit()

sys.exit()

