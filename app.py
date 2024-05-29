
#Universidade Estácio de Sá
#Fabíola Dutra dos Santos - 202302198521

import customtkinter as ctk
from tkinter import PhotoImage
from tkinter import *
from tkinter.messagebox import *
import ctypes
import hashlib
import sqlite3
import customtkinter
from CTkTable import *

class BackEnd():
    def cria_db(self):
        self.conn=sqlite3.connect("cadastros_pets.db")
        self.cursor=self.conn.cursor()
        #print("O banco de dados foi criado")

    def encerra_db(self):
        self.conn.close()
        #print("Banco de dados encerrado")

    def cria_tabela(self):
        self.cria_db()

        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Email TEXT NOT NULL,
                Password TEXT NOT NULL
            )
        """)
        
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Pets(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Id_Usuario integer,
                CONSTRAINT fk_usuario_pets FOREIGN KEY (Id_Usuario) REFERENCES Usuarios (Id)
            )
        """)

        self.conn.commit()
        #print("Tabela criada")
        self.encerra_db()

    def cadastrar_usuario(self):
        self.name_cadastro=self.name_cadastro_entry.get()
        self.email_cadastro=self.email_cadastro_entry.get()
        self.password_cadastro=self.password_cadastro_entry.get()

        self.cria_db()

        select_user_query = """SELECT * FROM Usuarios WHERE Email='""" + self.email_cadastro + """';"""
        self.cursor.execute(select_user_query)
        existing_user = self.cursor.fetchone()

        if existing_user:
            self.encerra_db()
            return False
   
        hash_object = hashlib.sha256()
        hash_object.update(self.password_cadastro.encode())
        hash_password = hash_object.hexdigest()

        self.cria_db()

        self.cursor.execute("""INSERT INTO Usuarios (Name, Email, Password) VALUES (?, ?, ?)""", (self.name_cadastro, self.email_cadastro, hash_password))
        
        self.conn.commit()
        self.encerra_db()
        return True           

    def logar_usuario(self, email, password):
        self.cria_db() 
        sqlite_select_query = """SELECT * FROM Usuarios WHERE Email='""" + email + """';"""
        self.cursor.execute(sqlite_select_query)
        existing_user = self.cursor.fetchone()
        self.encerra_db()
        
        if not existing_user:
            return False
        else:
            hash_object = hashlib.sha256()
            hash_object.update(password.encode())
            hash_password = hash_object.hexdigest()
            if hash_password == existing_user[3]:
                return existing_user[0]
            else:
                return False

    def buscar_pets(self, id_usuario):
        self.cria_db()
        sqlite_select_query = """SELECT * FROM Pets WHERE Id_Usuario='""" + str(id_usuario) + """';"""
        self.cursor.execute(sqlite_select_query)
        pets = self.cursor.fetchall()
        self.encerra_db()
        return pets
    
    def criar_pet(self, pet_name, id_usuario):
        pet_name_encoded = pet_name.encode()
        self.cria_db()
        self.cursor.execute("""INSERT INTO Pets (Name,Id_Usuario) VALUES (?, ?)""", (pet_name_encoded, id_usuario))
        self.conn.commit()
        self.encerra_db()
        return True
    
    def editar_pet(self, pet_new_name, pet_id):
        self.cria_db()
        self.cursor.execute("""UPDATE Pets SET Name = ? WHERE Id = ?;""", (pet_new_name, pet_id))
        self.conn.commit()
        self.encerra_db()
        return True
    
    def deletar_pet(self, pet_id):
        self.cria_db()
        self.cursor.execute("""DELETE FROM Pets WHERE Id = ?;""",(pet_id,))
        self.conn.commit()
        self.encerra_db()
        return True

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()

    #configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x500")
        self.title("sistema de Login")
        self.resizable(False, False)

    #imagem
    def tela_de_login(self):
       self.img = PhotoImage(file="pet_grooming.png", width=600, height=195)
       self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
       self.lb_img.place(x=-100, y=150)

       #titulo
       self.title = ctk.CTkLabel(self, text="Faça seu login ou\n Cadastre-se na nossa plataforma:" , font=("Lucida Sans", 18), corner_radius=15)
       self.title.place(x=20, y=30)

       #frame formulario e login
       self.frame_login=ctk.CTkFrame(self, width=350, height=380)
       self.frame_login.place(x=350, y=10)

       #widget no frame - formulario login
       self.lb_title=ctk.CTkLabel(self.frame_login, text="Faça seu login: ", font=("Century Gothic bold", 22))
       self.lb_title.grid(row=0, column=0, padx= 10, pady=10)

       self.name_login_entry=ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Email", font=("Century Gothic bold", 15), corner_radius=15)
       self.name_login_entry.grid(row=1, column=0, padx=10, pady=10)

       self.password_login_entry=ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", font=("Century Gothic bold", 15), corner_radius=15, show="*")
       self.password_login_entry.grid(row=2, column=0, padx=10, pady=10)

       self.ver_senha=ctk.CTkCheckBox(self.frame_login, text="Clique para ver sua senha: ", font=("Century Gothic bold", 12), command=self.exibir_senha)
       self.ver_senha.grid(row=3, column=0, padx=10, pady=10)
       
       self.btn_login=ctk.CTkButton(self.frame_login, width=300, text="Login", font=("Century Gothic bold", 16), corner_radius=15, command=self.logar)
       self.btn_login.grid(row=4, column=0, padx=10, pady=10)

       self.spam=ctk.CTkLabel(self.frame_login, text="Não é cadastrado? Clique no botão", font=("Century Gothic", 10))
       self.spam.grid(row=5, column=0, padx=10, pady=10)

       self.btn_cadastro=ctk.CTkButton(self.frame_login, width=300, text="Fazer cadastro", font=("Century Gothic", 16), corner_radius=15, command=self.tela_de_cadastro)
       self.btn_cadastro.grid(row=6, column=0, padx=10, pady=10)
       
    def exibir_senha(self):
        if self.password_login_entry.cget('show')=="":
            self.password_login_entry.configure(show="*")
        else:
            self.password_login_entry.configure(show="")
            
    def exibir_senha_cadastro(self):  

        if self.password_cadastro_entry.cget('show')=="":
            self.password_cadastro_entry.configure(show="*")
        else:
            self.password_cadastro_entry.configure(show="")
            
        if self.confirma_senha_entry.cget('show')=="":
            self.confirma_senha_entry.configure(show="*")
        else:
            self.confirma_senha_entry.configure(show="")

    def tela_principal(self):
       #Frame meu pets
       self.frame_ver_pets=ctk.CTkFrame(self, width=740, height=450)
       self.frame_ver_pets.place(x=10, y=10)

       self.title_meus_pets = ctk.CTkLabel(self.frame_ver_pets, text="Meus Pets" , font=("Lucida Sans", 18), corner_radius=15)
       self.title_meus_pets.grid(row=1, column=0, padx=10, pady=10)

       self.btn_ver_pets=ctk.CTkButton(self.frame_ver_pets, width=660, text="Ver", font=("Century Gothic", 16), corner_radius=15, command=self.mostrar_meus_pets)
       self.btn_ver_pets.grid(row=3, column=0, padx=10, pady=10)

       #Frame cadastrar
       self.frame_criar_pet=ctk.CTkFrame(self, width=350, height=500)
       self.frame_criar_pet.place(x=10, y=120)

       self.title_cadastrar_pet = ctk.CTkLabel(self.frame_criar_pet, text="Cadastrar Pet" , font=("Lucida Sans", 18), corner_radius=15)
       self.title_cadastrar_pet.grid(row=1, column=0, padx=10, pady=10)

       self.new_pet_entry=ctk.CTkEntry(self.frame_criar_pet, width=300, placeholder_text="Nome:", font=("Century Gothic bold", 15), corner_radius=15)
       self.new_pet_entry.grid(row=3, column=0, padx=0, pady=10)

       self.btn_create_pet=ctk.CTkButton(self.frame_criar_pet, width=300, text="Criar", font=("Century Gothic", 16), corner_radius=15, command=self.cadastrar_pet)
       self.btn_create_pet.grid(row=4, column=0, padx=10, pady=10)

       #Frame editar
       self.frame_editar_pet=ctk.CTkFrame(self, width=350, height=380)
       self.frame_editar_pet.place(x=370, y=120)

       self.title_editar_pet = ctk.CTkLabel(self.frame_editar_pet, text="Editar Pet" , font=("Lucida Sans", 18), corner_radius=15)
       self.title_editar_pet.grid(row=1, column=1, padx=10, pady=10)

       self.edit_pet_id_entry=ctk.CTkEntry(self.frame_editar_pet, width=300, placeholder_text="ID:", font=("Century Gothic bold", 15), corner_radius=15)
       self.edit_pet_id_entry.grid(row=3, column=1, padx=10, pady=10)

       self.edit_pet_entry=ctk.CTkEntry(self.frame_editar_pet, width=300, placeholder_text="Novo nome:", font=("Century Gothic bold", 15), corner_radius=15)
       self.edit_pet_entry.grid(row=4, column=1, padx=10, pady=10)

       self.btn_edit_pet=ctk.CTkButton(self.frame_editar_pet, width=300, text="Editar", font=("Century Gothic", 16), corner_radius=15, command=self.editar_meu_pet)
       self.btn_edit_pet.grid(row=5, column=1, padx=10, pady=10)

       #Frame deletar
       self.frame_deletar_pet=ctk.CTkFrame(self, width=300, height=380)
       self.frame_deletar_pet.place(x=10, y=330)

       self.title_editar_pet = ctk.CTkLabel(self.frame_deletar_pet, text="Deletar Pet" , font=("Lucida Sans", 18), corner_radius=15)
       self.title_editar_pet.grid(row=1, column=0, padx=10, pady=10)

       self.delete_pet_id_entry=ctk.CTkEntry(self.frame_deletar_pet, width=300, placeholder_text="ID:", font=("Century Gothic bold", 15), corner_radius=15)
       self.delete_pet_id_entry.grid(row=12, column=0, padx=10, pady=10)

       self.btn_delete_pet=ctk.CTkButton(self.frame_deletar_pet, width=300, text="Deletar", font=("Century Gothic", 16), corner_radius=15, command=self.deletar_meu_pet)
       self.btn_delete_pet.grid(row=13, column=0, padx=10, pady=10)

       #Frame sair
       self.frame_logout=ctk.CTkFrame(self, width=350, height=380)
       self.frame_logout.place(x=370, y=380)

       self.btn_logout=ctk.CTkButton(self.frame_logout, width=300, text="Sair", font=("Century Gothic", 16), corner_radius=15, command=self.ir_para_login, fg_color="red")
       self.btn_logout.grid(row=2, column=1, padx=10, pady=10)

    def editar_meu_pet(self):
        pet_novo_nome = self.edit_pet_entry.get()
        pet_id = self.edit_pet_id_entry.get()
        if bool(pet_novo_nome) & bool(pet_id):
            self.editar_pet(pet_novo_nome,pet_id)
            self.exibir_mensagem("Pet atualizado com sucesso!")
            self.edit_pet_entry.delete(0, END)
            self.edit_pet_id_entry.delete(0, END)

    def deletar_meu_pet(self):        
        pet_id = self.delete_pet_id_entry.get()
        if pet_id:
            self.deletar_pet(pet_id)
            self.exibir_mensagem("Pet deletado com sucesso!")
            self.delete_pet_id_entry.delete(0, END)

    def mostrar_meus_pets(self):
        self.pets=self.buscar_pets(self.id_usuario_logado)
        root = customtkinter.CTk()

        value = [["ID", "NOME"]]

        for pet in enumerate(self.pets):
           value.append([pet[1][0], pet[1][1]])

        table = CTkTable(master=root, row=len(value), column=2, values=value)
        table.pack(expand=False, fill="both", padx=20, pady=20)

        root.mainloop()

    def tela_de_cadastro(self):
        #remover formulario de login
        self.frame_login.place_forget()

        #frame formulario cadastro
        self.frame_cadastro=ctk.CTkFrame(self, width=450, height=380)
        self.frame_cadastro.place(x=350, y=10)
        
        #titulo tela de cadastro
        self.lb_title=ctk.CTkLabel(self.frame_cadastro, text="Faça seu cadastro: ", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx= 10, pady=5)

        #criando widgets de tela de cadastro
        self.name_cadastro_entry=ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Cadastre o nome do responsável: ", font=("Century Gothic bold", 15), corner_radius=15)
        self.name_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entry=ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="E-mail para cadastro: ", font=("Century Gothic bold", 15), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.password_cadastro_entry=ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Cadastre uma senha com 6 dígitos: ", font=("Century Gothic bold", 15), corner_radius=15, show= "*")
        self.password_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)
        
        self.confirma_senha_entry=ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirme sua senha: ", font=("Century Gothic bold", 15), corner_radius=15, show="*")
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=5)
        
        self.ver_senha=ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver sua senha: ", font=("Century Gothic bold", 12), command=self.exibir_senha_cadastro)
        self.ver_senha.grid(row=5, column=0, padx=10, pady=5)

        self.btn_cadastrar_user=ctk.CTkButton(self.frame_cadastro, width=300, text="Fazer cadastro", font=("Century Gothic", 14), corner_radius=15, command=self.cadastrar)
        self.btn_cadastrar_user.grid(row=6, column=0, padx=5)
        
        self.btn_login_back=ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar ao login", font=("Century Gothic bold", 14), corner_radius=15, command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, padx=10, pady=5)
        
    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.petname_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.password_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.petname_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

    def limpar_elementos_login(self):
        self.frame_login.destroy()
        self.img.blank()
        self.title.destroy()
        self.lb_title.destroy()
        self.name_login_entry.destroy()
        self.password_login_entry.destroy()
        self.ver_senha.destroy()
        self.btn_login.destroy()
        self.spam.destroy()
        self.btn_cadastro.destroy()

    def limpar_elementos_principal(self):
        self.frame_criar_pet.destroy()
        self.frame_logout.destroy()
        self.frame_ver_pets.destroy()
        self.frame_editar_pet.destroy()
        self.frame_deletar_pet.destroy()
        self.new_pet_entry.destroy()
        self.btn_create_pet.destroy()
        self.btn_ver_pets.destroy()
        self.edit_pet_id_entry.destroy()
        self.edit_pet_entry.destroy()
        self.btn_edit_pet.destroy()
        self.delete_pet_id_entry.destroy()
        self.btn_delete_pet.destroy()
        self.btn_logout.destroy()

    def cadastrar(self):
        nome=self.name_cadastro_entry.get()
        email=self.email_cadastro_entry.get()
        if not nome:
            self.exibir_mensagem("Informe um nome de usuário")
            return
        
        if not email:
            self.exibir_mensagem("Informe um e-mail para cadastro")
            return
        
        password=self.password_cadastro_entry.get()
        password_confirmation=self.confirma_senha_entry.get()
        if len(password) <6:
            self.exibir_mensagem("Senha precisa ter 6 dígitos")
            return
        
        if password != password_confirmation:
            self.exibir_mensagem("As senhas não são iguais")
            return
        
        cadastro_sucesso = self.cadastrar_usuario()
        if not cadastro_sucesso:
            self.exibir_mensagem("Email já cadastrado!")
            return
        
        self.exibir_mensagem("Usuário cadastrado com sucesso!")
        self.tela_de_login()            

    def logar(self):
        resultado_login=self.logar_usuario(self.name_login_entry.get(), self.password_login_entry.get())
        if resultado_login:
            self.id_usuario_logado=resultado_login
            # self.exibir_mensagem('Login OK')
            self.pets=self.buscar_pets(self.id_usuario_logado)
            self.limpar_elementos_login()            
            self.tela_principal()
        else:
            self.exibir_mensagem('Login inválido')
        
    def exibir_mensagem(self,text):
        return ctypes.windll.user32.MessageBoxW(0, text,'Cadastro de pets', 0)

    def cadastrar_pet(self):
        pet_name = self.new_pet_entry.get()
        if pet_name:
            self.criar_pet(pet_name, self.id_usuario_logado)
            self.pets=self.buscar_pets(self.id_usuario_logado)
            self.new_pet_entry.delete(0, END)
            self.exibir_mensagem("Pet cadastrado com sucesso!")
        else:
            self.exibir_mensagem("Informe o nome do seu Pet!")

    def ir_para_login(self):
        self.limpar_elementos_principal()
        self.tela_de_login()

if __name__=="__main__":
    app = App()
    app.mainloop()
