import tkinter as tk
from tkinter import ttk, messagebox, filedialog  
from datetime import date
import psycopg2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Configuração do banco de dados (ajuste conforme necessário)
DB_CONFIG = {
    'dbname': 'PontoComInformatica',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost'
}

# Classe Database
class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Classes ContaAPagar e ContaAReceber
class ContaAPagar:
    def __init__(self, descricao, valor, data_vencimento, observacoes):
        self.descricao = descricao
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.observacoes = observacoes

    def save(self, db):
        query = """
        INSERT INTO contas_a_pagar (descricao, valor, data_vencimento, observacoes)
        VALUES (%s, %s, %s, %s)
        """
        db.execute_query(query, (self.descricao, self.valor, self.data_vencimento, self.observacoes))

    @staticmethod
    def find_all(db):
        query = """
        SELECT cp.id, cp.descricao, cp.valor, cp.data_vencimento, cp.observacoes
        FROM contas_a_pagar cp
        """
        return db.fetch_query(query)

    @staticmethod
    def delete(db, conta_id):
        query = "DELETE FROM contas_a_pagar WHERE id = %s"
        db.execute_query(query, (conta_id,))

    @staticmethod
    def update(db, conta_id, descricao, valor, data_vencimento, observacoes):
        query = """
        UPDATE contas_a_pagar 
        SET descricao = %s, valor = %s, data_vencimento = %s, observacoes = %s
        WHERE id = %s
        """
        db.execute_query(query, (descricao, valor, data_vencimento, observacoes, conta_id))

class ContaAReceber:
    def __init__(self, descricao, valor, data_recebimento, observacoes):
        self.descricao = descricao
        self.valor = valor
        self.data_recebimento = data_recebimento
        self.observacoes = observacoes    

    def save(self, db):
        query = """
        INSERT INTO contas_a_receber (descricao, valor, data_recebimento, observacoes)
        VALUES (%s, %s, %s, %s)
        """
        db.execute_query(query, (self.descricao, self.valor, self.data_recebimento, self.observacoes))

    @staticmethod
    def find_all(db):
        query = """
        SELECT cr.id, cr.descricao, cr.valor, cr.data_recebimento, cr.observacoes
        FROM contas_a_receber cr
        """
        return db.fetch_query(query)

    @staticmethod
    def delete(db, conta_id):
        query = "DELETE FROM contas_a_receber WHERE id = %s"
        db.execute_query(query, (conta_id,))

    @staticmethod
    def update(db, conta_id, descricao, valor, data_recebimento, observacoes):
        query = """
        UPDATE contas_a_receber 
        SET descricao = %s, valor = %s, data_recebimento = %s, observacoes = %s
        WHERE id = %s
        """
        db.execute_query(query, (descricao, valor, data_recebimento, observacoes, conta_id))


# Classe da Aplicação
#
class App:
    def __init__(self, root, db):
        self.root = root
        self.db = db

        self.root.title("Sistema de Gestão Financeira")
        self.root.geometry("1080x700")
        self.root.resizable(False, False)

        self.setup_styles()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.side_menu = self.create_side_menu()
        self.side_menu.pack(side="left", fill="y")

        self.cadastro_conta_pagar_frame = self.create_cadastro_conta_pagar_frame()
        self.cadastro_contas_frame = self.create_cadastro_contas()
        self.cadastro_conta_receber_frame = self.create_cadastro_conta_receber_frame()
        self.visualizar_contas_pagar_frame = self.create_visualizar_contas_pagar_frame()
        self.visualizar_contas_frame = self.create_visualizar_contas_frame()
        self.visualizar_contas_receber_frame = self.create_visualizar_contas_receber_frame()
        self.relatorio_frame = self.create_relatorio_frame()

        self.show_contas()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 11), rowheight=15)

    def create_side_menu(self):
        frame = tk.Frame(self.main_frame, bg="#003785", width=200)

        inner_frame = tk.Frame(frame, bg="#003785")
        inner_frame.pack(side="top", fill="x")

        tk.Label(inner_frame, text="Menu", bg="#003785", fg="white", font=('Arial', 14, 'bold')).pack(side="left", fill="x", pady=8, padx=10)

        menu_items = [       
            ("Cadastrar Contas", self.show_contas),     
            ("Visualizar Contas", self.show_visualizar_contas),            
            ("Gerar Relatório", self.show_relatorio)
        ]
        for text, command in menu_items:
            tk.Button(frame, text=text, bg="#77c1f9", fg="white", font=('Arial', 12), width=15, anchor="w", padx=5, command=command, justify="left").pack(side="top", fill="x", pady=5)

        return frame

    def create_cadastro_contas(self):
        frame = tk.Frame(self.main_frame, bg="white", width=max, height=max)

        ttk.Button(frame, text="Cadastrar Contas a Receber", command=self.show_cadastro_conta_receber, width=30).grid(row=1, column=1, padx=10, pady=40, sticky="w")
        ttk.Button(frame, text="Cadastrar Contas a Pagar", command=self.show_cadastro_conta_pagar, width=30).grid(row=2, column=1, padx=10, pady=0, sticky="w")

        return frame
    
    def create_visualizar_contas_frame(self):
        frame = tk.Frame(self.main_frame, bg="white", width=max, height=max)

        ttk.Button(frame, text="Visualizar Contas a Receber", command=self.show_visualizar_contas_receber, width=30).grid(row=1, column=1, padx=10, pady=40, sticky="w")
        ttk.Button(frame, text="Visualizar Contas a Pagar", command=self.show_visualizar_contas_pagar, width=30).grid(row=2, column=1, padx=10, pady=0, sticky="w")

        return frame

    def create_cadastro_conta_pagar_frame(self):
        frame = tk.Frame(self.main_frame, bg="white")

        tk.Label(frame, text="Descrição:", bg="white", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.descricao_entry_cp = tk.Entry(frame, font=('Arial', 12))
        self.descricao_entry_cp.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="Valor:", bg="white", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.valor_entry_cp = tk.Entry(frame, font=('Arial', 12))
        self.valor_entry_cp.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="Data Vencimento:", bg="white", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.data_entry_cp = tk.Entry(frame, font=('Arial', 12))
        self.data_entry_cp.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="Observações:", bg="white", font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.observacoes_entry_cp = tk.Entry(frame, font=('Arial', 12))
        self.observacoes_entry_cp.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ttk.Button(frame, text="Voltar", command=self.show_contas).grid(row=4, column=1, padx=10, pady=10, sticky="w")
        ttk.Button(frame, text="Cadastrar", command=self.cadastrar_conta_pagar).grid(row=4, column=1, padx=10, pady=10, sticky="e")

        return frame

    def create_cadastro_conta_receber_frame(self):
        frame = tk.Frame(self.main_frame, bg="white")

        tk.Label(frame, text="Descrição:", bg="white", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.descricao_entry_cr = tk.Entry(frame, font=('Arial', 12))
        self.descricao_entry_cr.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="Valor:", bg="white", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.valor_entry_cr = tk.Entry(frame, font=('Arial', 12))
        self.valor_entry_cr.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="Data Recebimento:", bg="white", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.data_entry_cr = tk.Entry(frame, font=('Arial', 12))
        self.data_entry_cr.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="Observações:", bg="white", font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.observacoes_entry_cr = tk.Entry(frame, font=('Arial', 12))
        self.observacoes_entry_cr.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ttk.Button(frame, text="Voltar", command=self.show_contas).grid(row=4, column=1, padx=10, pady=10, sticky="w")
        ttk.Button(frame, text="Cadastrar", command=self.cadastrar_conta_receber).grid(row=4, column=1, padx=10, pady=10, sticky="e")

        return frame

    def create_visualizar_contas_pagar_frame(self):
        frame = tk.Frame(self.main_frame, bg="white")

        self.conta_pagar_tree = ttk.Treeview(frame, columns=("ID", "Descrição", "Valor", "Data Vencimento", "Observações"), show="headings", height=15)        
        self.conta_pagar_tree.heading("ID", text="ID")
        self.conta_pagar_tree.heading("Descrição", text="Descrição")
        self.conta_pagar_tree.heading("Valor", text="Valor")
        self.conta_pagar_tree.heading("Data Vencimento", text="Data Vencimento")
        self.conta_pagar_tree.heading("Observações", text="Observações")
        self.conta_pagar_tree.column("#0", width=0, stretch="no")
        self.conta_pagar_tree.column("ID", width=50, anchor="center")
        self.conta_pagar_tree.column("Descrição", width=200, anchor="w")
        self.conta_pagar_tree.column("Valor", width=100, anchor="center")
        self.conta_pagar_tree.column("Data Vencimento", width=150, anchor="center")
        self.conta_pagar_tree.column("Observações", width=200, anchor="w")
        self.conta_pagar_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.conta_pagar_tree.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.conta_pagar_tree.configure(yscrollcommand=scroll_y.set)

        self.load_contas_pagar()

        # Botão para excluir conta a pagar selecionada
        ttk.Button(frame, text="Voltar", command=self.show_visualizar_contas).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(frame, text="Excluir Conta a Pagar", command=self.excluir_conta_pagar).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        return frame

    def create_visualizar_contas_receber_frame(self):
        frame = tk.Frame(self.main_frame, bg="white")

        self.conta_receber_tree = ttk.Treeview(frame, columns=("ID", "Descrição", "Valor", "Data Recebimento", "Observações"), show="headings", height=15)
        self.conta_receber_tree.heading("ID", text="ID")
        self.conta_receber_tree.heading("Descrição", text="Descrição")
        self.conta_receber_tree.heading("Valor", text="Valor")
        self.conta_receber_tree.heading("Data Recebimento", text="Data Recebimento")
        self.conta_receber_tree.heading("Observações", text="Observações")
        self.conta_receber_tree.column("#0", width=0, stretch="no")
        self.conta_receber_tree.column("ID", width=50, anchor="center")
        self.conta_receber_tree.column("Descrição", width=200, anchor="w")
        self.conta_receber_tree.column("Valor", width=100, anchor="center")
        self.conta_receber_tree.column("Data Recebimento", width=150, anchor="center")
        self.conta_receber_tree.column("Observações", width=200, anchor="w")
        self.conta_receber_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.conta_receber_tree.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.conta_receber_tree.configure(yscrollcommand=scroll_y.set)

        self.load_contas_receber()

        # Botão para excluir conta a receber selecionada
        ttk.Button(frame, text="Voltar", command=self.show_visualizar_contas).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(frame, text="Excluir Conta a Receber", command=self.excluir_conta_receber).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        return frame

    def create_relatorio_frame(self):
        frame = tk.Frame(self.main_frame, bg="white")

        tk.Label(frame, text="Gerar Relatório PDF por Data:", bg="white", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.data_relatorio_entry = tk.Entry(frame, font=('Arial', 12))
        self.data_relatorio_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Button(frame, text="Selecionar Diretório", command=self.selecionar_diretorio).grid(row=0, column=2, padx=10, pady=10, sticky="e")

        ttk.Button(frame, text="Gerar Relatório", command=self.gerar_relatorio).grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return frame

    def show_cadastro_conta_pagar(self):
        self.hide_all_frames()
        self.cadastro_conta_pagar_frame.pack(fill="both", expand=True)

    def show_contas(self):
        self.hide_all_frames()
        self.cadastro_contas_frame.pack(fill="both", expand=True)

    def show_cadastro_conta_receber(self):
        self.hide_all_frames()
        self.cadastro_conta_receber_frame.pack(fill="both", expand=True)

    def show_visualizar_contas_pagar(self):
        self.hide_all_frames()
        self.visualizar_contas_pagar_frame.pack(fill="both", expand=True)

    def show_visualizar_contas(self):
        self.hide_all_frames()
        self.visualizar_contas_frame.pack(fill="both", expand=True)

    def show_visualizar_contas_receber(self):
        self.hide_all_frames()
        self.visualizar_contas_receber_frame.pack(fill="both", expand=True)

    def show_relatorio(self):
        self.hide_all_frames()
        self.relatorio_frame.pack(fill="both", expand=True)

    def hide_all_frames(self):
        self.cadastro_conta_pagar_frame.pack_forget()
        self.cadastro_conta_receber_frame.pack_forget()        
        self.visualizar_contas_pagar_frame.pack_forget()
        self.visualizar_contas_receber_frame.pack_forget()
        self.visualizar_contas_frame.pack_forget()
        self.relatorio_frame.pack_forget()
        self.cadastro_contas_frame.pack_forget()


    def cadastrar_conta_pagar(self):
        descricao = self.descricao_entry_cp.get()
        valor = self.valor_entry_cp.get()
        data_vencimento = self.data_entry_cp.get()
        observacoes = self.observacoes_entry_cp.get()

        if descricao and valor and data_vencimento:
            conta_pagar = ContaAPagar(descricao, valor, data_vencimento, observacoes)
            conta_pagar.save(self.db)
            messagebox.showinfo("Sucesso", "Conta a pagar cadastrada com sucesso.")
            self.descricao_entry_cp.delete(0, tk.END)
            self.valor_entry_cp.delete(0, tk.END)
            self.data_entry_cp.delete(0, tk.END)
            self.observacoes_entry_cp.delete(0, tk.END)
            self.load_contas_pagar()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")

    def cadastrar_conta_receber(self):
        descricao = self.descricao_entry_cr.get()
        valor = self.valor_entry_cr.get()
        data_recebimento = self.data_entry_cr.get()
        observacoes = self.observacoes_entry_cr.get()

        if descricao and valor and data_recebimento:
            conta_receber = ContaAReceber(descricao, valor, data_recebimento, observacoes)
            conta_receber.save(self.db)
            messagebox.showinfo("Sucesso", "Conta a receber cadastrada com sucesso.")
            self.descricao_entry_cr.delete(0, tk.END)
            self.valor_entry_cr.delete(0, tk.END)
            self.data_entry_cr.delete(0, tk.END)
            self.observacoes_entry_cr.delete(0, tk.END)
            self.load_contas_receber()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")

    def load_contas_pagar(self):
        for row in self.conta_pagar_tree.get_children():
            self.conta_pagar_tree.delete(row)

        contas_pagar = ContaAPagar.find_all(self.db)
        for conta in contas_pagar:
            self.conta_pagar_tree.insert("", tk.END, values=conta)

    def load_contas_receber(self):
        for row in self.conta_receber_tree.get_children():
            self.conta_receber_tree.delete(row)

        contas_receber = ContaAReceber.find_all(self.db)
        for conta in contas_receber:
            self.conta_receber_tree.insert("", tk.END, values=conta)

    def excluir_conta_pagar(self):
        selected_item = self.conta_pagar_tree.selection()
        if selected_item:
            conta_id = self.conta_pagar_tree.item(selected_item)['values'][0]
            ContaAPagar.delete(self.db, conta_id)
            self.load_contas_pagar()
            messagebox.showinfo("Sucesso", "Conta a pagar excluída com sucesso.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma conta a pagar para excluir.")

    def excluir_conta_receber(self):
        selected_item = self.conta_receber_tree.selection()
        if selected_item:
            conta_id = self.conta_receber_tree.item(selected_item)['values'][0]
            ContaAReceber.delete(self.db, conta_id)
            self.load_contas_receber()
            messagebox.showinfo("Sucesso", "Conta a receber excluída com sucesso.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma conta a receber para excluir.")

    def selecionar_diretorio(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.caminho_relatorio = selected_directory

    def gerar_relatorio(self):
        data_relatorio = self.data_relatorio_entry.get()

        if not data_relatorio:
            messagebox.showerror("Erro", "Por favor, informe a data para gerar o relatório.")
            return        

        # Recuperar os dados do banco
        contas_a_pagar = ContaAPagar.find_all(self.db)
        contas_a_receber = ContaAReceber.find_all(self.db)

        # Gerar o relatório em PDF
        nome_arquivo = f"relatorio_{data_relatorio}.pdf"
        path_arquivo = os.path.join(self.caminho_relatorio, nome_arquivo)

        c = canvas.Canvas(path_arquivo, pagesize=letter)
        largura, altura = letter
        margem_esquerda = 100
        margem_superior = 750
        espaco_linha = 15
        y_position = margem_superior

        def escrever_conteudo(conteudo):
            nonlocal y_position
            for linha in conteudo:
                c.drawString(margem_esquerda, y_position, linha)
                y_position -= espaco_linha
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = altura - 50

        # Adicionar dados de Contas a Pagar
        c.setFont("Helvetica", 12)
        c.drawString(margem_esquerda, y_position, "Contas a Pagar:")
        y_position -= espaco_linha
        conteudo_pagar = []
        for conta in contas_a_pagar:
            conteudo_pagar.append(f"Descrição: {conta[1]}")
            conteudo_pagar.append(f"Valor: {conta[2]}")
            conteudo_pagar.append(f"Data de Vencimento: {conta[3]}")
            conteudo_pagar.append(f"Observações: {conta[4]}")            
            conteudo_pagar.append("")
        escrever_conteudo(conteudo_pagar)

        # Adicionar dados de Contas a Receber
        c.drawString(margem_esquerda, y_position, "Contas a Receber:")
        y_position -= espaco_linha
        conteudo_receber = []
        for conta in contas_a_receber:
            conteudo_receber.append(f"Descrição: {conta[1]}")
            conteudo_receber.append(f"Valor: {conta[2]}")
            conteudo_receber.append(f"Data de Recebimento: {conta[3]}")
            conteudo_receber.append(f"Observações: {conta[4]}")
            conteudo_receber.append("")
        escrever_conteudo(conteudo_receber)

        c.save()

        messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso em:\n{path_arquivo}")

def main():
    root = tk.Tk()
    db = Database()
    app = App(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()