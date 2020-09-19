import os
import sys

# Editado por: Amado Rodríguez Pérez
'''
 El script hace webscrapping, en pocas palabras. Busca información en la 
 página de noticias de la UANL de acuerdo a la facultad que le proporciones,
 y el numero de pagina de noticias a iniciar y a finalizar.
 '''

# Esta funcion valida que la la entrada sea un entero y no otra cosa.
# Se usa para evitar error cuando se ingresa el inicio y final de busqueda.
def val_int (valor):
    try:
        int(valor)
        return True
    except:
        return False
    
# Este es la funcion main(), que ejecuta todo lo necesario, forzado a hacerlo así,
# pues evita que ocurra el error antes de hacer las importaciones.
def main():
    from bs4 import BeautifulSoup as bs
    import webbrowser
    import requests
    
    print("Este script navega en las páginas de noticas de la UANL")
    inicioRango = input("Pagina inicial para buscar: ")
    while val_int(inicioRango)==False:
        inicioRango = input("Pagina inicial para buscar: ")
    finRango = input("Pagina final para buscar: ")
    while val_int(finRango)==False:
        finRango = input("Pagina final para buscar: ")
    dependencia = input("Ingrese las siglas de la Facultad a buscar: ")
    if inicioRango > finRango:
        inicioRango,finRango = finRango,inicioRango
    for i in range (int(inicioRango),int(finRango),1):
        url = "https://www.uanl.mx/noticias/page/"+str(i)
        pagina = requests.get (url)
        if pagina.status_code != 200:
            raise TypeError("Pagina no encontrada")
        else:
            soup = bs(pagina.content,"html.parser")
            info = soup.select("h3 a")
            for etiqueta in info:
                url2 = etiqueta.get("href")
                pagina2 = requests.get(url2)
                if pagina2.status_code == 200:
                    soup2 = bs(pagina2.content,"html.parser")
                    parrafos = soup2.select("p")    
                    for elemento in parrafos:
                        if dependencia in elemento.getText():
                            print ("Abriendo",url2)
                            webbrowser.open(url2)
                            break

# Aquí es donde ocurre todo, primero se ejecutará el try y no el main(), por lo que
# el error se capturará antes de causar estragos.
if __name__=="__main__":
    # Aquí es donde se valida que, antes de importar, los modulos esten instalados,
    # de lo contrario se instalan y se detiene la ejecucion, para su reinico.
    try:
        main()
    except ImportError:
        print("Error en paquetes", "Instalando modulos...")
        os.system('pip install beautifulsoup4')
        os.system('pip install webbrowser')
        os.system('pip install requests')
        print("Modulos instalados", "Ejecuta de nuevo")
        exit()
