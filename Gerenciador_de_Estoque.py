#-------------------------------------------------------
# "Programa de gerenciamento de estoque simples."
# Criado por: Luiz Gabriel Magalhães Trindade.
#-------------------------------------------------------
# Esre programa é distribuído sob a Licença MIT,
# Você deve ter recebido uma cópia da licença juntamente
# com o código fonte, caso contrário visite:
# https://mit-license.org/
#-------------------------------------------------------

from customtkinter import *
from tkinter import ttk, PhotoImage as PI, filedialog
#from PySimpleGUI import popup_quick_message as alert
import sqlite3
import shutil
from os import remove
from datetime import datetime
from CTkTable import *
from plyer import notification

version = "1.9-beta"
software_name = "Gerenciador de Estoque"

set_default_color_theme("green")
set_appearance_mode("system")
set_widget_scaling(1.7)

app = CTk()
app.title("Gerenciador de Estoque")
app.geometry("1050x650")

database_file = "_internal/ESTOQUE.db"

conn = sqlite3.connect(database_file)
command = conn.cursor()
command.execute("""CREATE TABLE IF NOT EXISTS estoque
                   (id INTEGER PRIMARY KEY,
                   nome TEXT,
                   qntd INTEGER,
                   data TEXT);""")
conn.commit()


tabview = CTkTabview(master=app, text_color="white")
tabview.pack()

tab1 = tabview.add("Adicionar")
tab2 = tabview.add("Visualizar")
tab3 = tabview.add("Remover")
tab4 = tabview.add("Alterar")
tab5 = tabview.add("Banco de dados")
tab6 = tabview.add("Sobre")

estoque_icon = PI(file="_internal/estoque_icon.png")
MIT_LICENSE_QRCODE = PI(file="_internal/MIT_LICENSE_QRCODE.png")
dev_pix = PI(file="_internal/dev_pix.png")



# INSERIR
def INSERT():
    try:
        ID = int(id_tab1.get())
        NOME = str(nome_tab1.get())
        QNTD = int(qntd_tab1.get())
        DATA = datetime.now().strftime("%d-%m-%Y às %H:%M")
        command.execute(f"INSERT INTO estoque VALUES({ID}, '{NOME}', {QNTD}, '{DATA}');")
        conn.commit()
        #alert("Dados adicionados com sucesso!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Dados adicionados com sucesso!")
        tabela.add_row(values=[])
        VIEW()
    except Exception as error:
        #alert(error, font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", f"{error}")

Image = CTkLabel(master=tab1, image=estoque_icon, text=None)
Image.pack()
id_tab1 = CTkEntry(master=tab1, placeholder_text="ID", justify="center")
id_tab1.pack(pady=10, padx=10)
nome_tab1 = CTkEntry(master=tab1, placeholder_text="NOME", justify="center")
nome_tab1.pack(pady=10, padx=10)
qntd_tab1 = CTkEntry(master=tab1, placeholder_text="QNTD", justify="center")
qntd_tab1.pack(pady=10, padx=10)
Adicionar = CTkButton(master=tab1, text="Adicionar", font=("Arial", 20, "bold"), text_color="white", fg_color="green", command=INSERT)
Adicionar.pack(pady=10, padx=10)



# VISUALIZAR
def VIEW():
    command.execute(f"SELECT * FROM estoque ORDER BY id;")
    conn.commit()
    data_table = command.fetchall()
    tabela.update_values(values=data_table)

command.execute(f"SELECT * FROM estoque ORDER BY id;")
conn.commit()
data_table = command.fetchall()

scroll = CTkScrollableFrame(tab2, width=700, height=700)
scroll.pack()

Image = CTkLabel(master=scroll, image=estoque_icon, text=None)
Image.pack()

tabela_id = CTkTable(master=scroll, column=4, values=[["id", "nome", "qntd", "data de adição"]], font=("Arial", 8, "bold"), hover_color="green").pack(expand=True, fill="both", padx=10)
tabela = CTkTable(master=scroll, column=4, values=data_table, font=("Arial", 8, "bold"), hover_color="green")
tabela.pack(expand=True, fill="both", pady=10)



# REMOVER
def REMOVE():
    try:
        ID = int(id_tab3.get())
        command.execute(f"DELETE FROM estoque WHERE id={ID}")
        conn.commit()
        #print("Dados deletados com sucesso!")
        #alert("Dados removidos com sucesso!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Dados removidos com sucesso!")
        VIEW()
    except Exception as error:
        #print(error)
        #alert(error, font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", f"{error}")

Image = CTkLabel(master=tab3, image=estoque_icon, text=None)
Image.pack()
id_tab3 = CTkEntry(master=tab3, placeholder_text="ID", justify="center")
id_tab3.pack(pady=10, padx=10)
Remover = CTkButton(master=tab3, text="Remover", font=("Arial", 20, "bold"), text_color="white", fg_color="red", command=REMOVE)
Remover.pack(pady=10, padx=10)



# ALTERAR
def alter_nome():
    nome_radio.deselect()
    qntd_radio.deselect()
    ID = int(id_tab4.get())
    value = str(valor.get())
    try:
        value = int(value)
        #alert("Não coloque número onde deveria ser um texto!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Não coloque número onde deveria ser um texto!")
    except:
        try:
            command.execute(f"UPDATE estoque SET nome='{value}' WHERE id={ID};")
            conn.commit()
            VIEW()
            #alert("Dado alterado com sucesso!", font=("Arial", 20))
            notification.notify("Gerenciador de Estoque", "Dado alterado com sucesso!")
        except Exception as error:
            #alert(error, font=("Arial", 20))
            notification.notify("Gerenciador de Estoque", f"{error}")

def alter_qntd():
    nome_radio.deselect()
    qntd_radio.deselect()
    ID = int(id_tab4.get())
    value = int(valor.get())
    try:
        command.execute(f"UPDATE estoque SET qntd={value} WHERE id={ID};")
        conn.commit()
        VIEW()
        #alert("Dado alterado com sucesso!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Dado alterado com sucesso!")
    except Exception as error:
        #alert(error, font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", f"{error}")

Image = CTkLabel(master=tab4, image=estoque_icon, text=None)
Image.pack()
id_tab4 = CTkEntry(master=tab4, placeholder_text="ID", justify="center")
id_tab4.pack(pady=10, padx=10)
valor = CTkEntry(master=tab4, placeholder_text="VALOR", justify="center")
valor.pack(pady=10, padx=10)
nome_radio = CTkRadioButton(master=tab4, text="NOME", command=alter_nome)
nome_radio.pack(pady=10, padx=10)
qntd_radio = CTkRadioButton(master=tab4, text="QNTD", command=alter_qntd)
qntd_radio.pack(pady=10, padx=10)



# BANCO DE DADOS
def SELECT_DATABASE():
    global database_file, conn, command
    file = filedialog.askopenfilename()
    if file:
        database_file = file
        conn = sqlite3.connect(file)
        command = conn.cursor()
        alert("Banco de dados selecionado com sucesso!", font=("Arial", 20))
        VIEW()
    else:
        pass

def IMPORT_DATABASE():
    alert("Selecone o banco de dados!", font=("Arial", 20))
    file = filedialog.askopenfilename()
    if file:
        #alert("Banco de dados selecionado!", font=("Arial", 20))
        #alert("Selecione o local!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Banco de dados selecionado!")
        notification.notify("Gerenciador de Estoque", "Selecione o local!")
        local = filedialog.askdirectory()
        if local:
            #alert("Local selecionado!", font=("Arial", 20))
            notification.notify("Gerenciador de Estoque", "Local selecionado!")
            shutil.copy(file, local)
            #alert("Banco de dados importado com sucesso!", font=("Arial", 20))
            notification.notify("Gerenciador de Estoque", "Banco de dados importado com sucesso!")
        else:
            pass
    else:
        pass

def EXPORT_DATABASE():
    global database_file, conn, command
    local = filedialog.askdirectory()
    if local:
        shutil.copy(database_file, local)
        #alert("Banco de dados exportado com sucesso!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Banco de dados exportado com sucesso!")
    else:
        pass

def DELETE_DATABASE():
    try:
        command.execute("DROP TABLE estoque;")
        conn.commit()
        #alert("Todos os itens foram deletados com sucesso!", font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", "Todos os itens foram deletados com sucesso!")
        command.execute("""CREATE TABLE IF NOT EXISTS estoque
                   (id INTEGER PRIMARY KEY,
                   nome TEXT,
                   qntd INTEGER,
                   data TEXT);""")
        conn.commit()
        VIEW()
    except Exception as error:
        #alert(error, font=("Arial", 20))
        notification.notify("Gerenciador de Estoque", f"{error}")

Image = CTkLabel(master=tab5, image=estoque_icon, text=None)
Image.pack()
Selecionar_Database = CTkButton(master=tab5, text="Selecionar Banco de dados", font=("Arial", 20, "bold"), text_color="white", fg_color="brown", command=SELECT_DATABASE)
Selecionar_Database.pack(pady=10, padx=10)
Importar_Database = CTkButton(master=tab5, text="Importar Banco de dados", font=("Arial", 20, "bold"), text_color="white", fg_color="purple", command=IMPORT_DATABASE)
Importar_Database.pack(pady=10, padx=10)
Exportar_Database = CTkButton(master=tab5, text="Exportar Banco de dados", font=("Arial", 20, "bold"), text_color="white", fg_color="cyan", command=EXPORT_DATABASE)
Exportar_Database.pack(pady=10, padx=10)
Deletar_Database = CTkButton(master=tab5, text="Deletar Banco de dados", font=("Arial", 20, "bold"), text_color="white", command=DELETE_DATABASE)
Deletar_Database.pack(pady=10, padx=10)



# SOBRE
about = f""" 
Versão: {version}
Desenvolvido por: Luiz Gabriel Magalhães Trindade. (Estudante de Ciência da Computação)
Licença: "MIT", visite "https://mit-license.org/" para acessar a licença MIT.

Descrição:
O {software_name} é uma ferramenta de gerenciamento de estoque que oferece 
funcionalidades essenciais para ajudar no controle de seus produtos.
Com este software, você pode adicionar, visualizar,
alterar e remover produtos do seu estoque de forma eficiente.

Este software foi criado com foco na eficiência e simplicidade, e é licenciado sob
a Licença MIT, garantindo a liberdade de uso, estudo, modificação e distribuição. 
A Licença MIT é uma licença permissiva que permite que o código seja incorporado 
em um programa que pode ser distribuído sob outra licença.
Isso significa que o código deste software pode ser incorporado em outro 
software proprietário sem a necessidade de divulgar o código-fonte.
"""
scroll_about = CTkScrollableFrame(tab6, width=700, height=700)
scroll_about.pack()
Image = CTkLabel(master=scroll_about, image=estoque_icon, text=None)
Image.pack(pady=5)
sobre = CTkLabel(master=scroll_about, text=about, justify="left", font=("Arial", 12, "bold"))
sobre.pack(pady=5)
DEV_PIX_QRCODE = CTkLabel(master=scroll_about, image=dev_pix, text="Doação via PIX:  ", font=("Arial", 20, "bold"), compound="right")
DEV_PIX_QRCODE.pack(pady=10)
LICENSE_QRCODE = CTkLabel(master=scroll_about, image=MIT_LICENSE_QRCODE, text="Licença MIT via QRCODE:  ", font=("Arial", 20, "bold"), compound="right")
LICENSE_QRCODE.pack(pady=10)

app.mainloop()
