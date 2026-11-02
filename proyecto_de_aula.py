
import tkinter as tk
from tkinter import ttk, messagebox
import os

class InventarioForestal:
    def __init__(self):
        self.archivoTxt = "datos_inventario.txt"

    def guardarInspeccion(self, idInspeccion, conglomerado, brigada, fustales, latizales, brinzales, muestras):
        # Muestras se guardan separadas por punto y coma, y sus atributos por coma
        muestrasStr = ";".join([f"{m[0]},{m[1]},{m[2]}" for m in muestras])

        # Formato de texto plano separado por pipes (|)
        linea = f"{idInspeccion}|{conglomerado}|{brigada}|{fustales}|{latizales}|{brinzales}|{muestrasStr}\n"

        with open(self.archivoTxt, "a", encoding="utf-8") as archivo:
            archivo.write(linea)

    def consultarInspeccion(self, idBusqueda):
        if not os.path.exists(self.archivoTxt):
            return None

        with open(self.archivoTxt, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")
                if datos[0] == idBusqueda:
                    return datos
        return None

class FrontIFN:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema IFN - IDEAM")
        self.ventana.geometry("850x650")

        self.inventario = InventarioForestal()
        self.muestrasTemporales = []

        # Crear pestañas para separar el registro de la consulta
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.pestañaRegistro = tk.Frame(self.notebook, bg="#e6f2ff")
        self.pestañaConsulta = tk.Frame(self.notebook, bg="#f2ffe6")

        self.notebook.add(self.pestañaRegistro, text="Registrar Inspección")
        self.notebook.add(self.pestañaConsulta, text="Consultar Inspección")

        self.construirInterfazRegistro()
        self.construirInterfazConsulta()

    def construirInterfazRegistro(self):
        # --- DATOS GENERALES ---
        marcoGeneral = tk.LabelFrame(self.pestañaRegistro, text="Datos del Conglomerado y Brigada", bg="#e6f2ff")
        marcoGeneral.pack(fill="x", padx=10, pady=5)

        tk.Label(marcoGeneral, text="ID Inspección:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
        self.txtIdInsp = tk.Entry(marcoGeneral)
        self.txtIdInsp.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(marcoGeneral, text="Conglomerado:", bg="#e6f2ff").grid(row=0, column=2, padx=5, pady=5)
        self.txtConglomerado = tk.Entry(marcoGeneral)
        self.txtConglomerado.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(marcoGeneral, text="Brigada:", bg="#e6f2ff").grid(row=0, column=4, padx=5, pady=5)
        self.txtBrigada = tk.Entry(marcoGeneral)
        self.txtBrigada.grid(row=0, column=5, padx=5, pady=5)

        # --- CONTEO DE ÁRBOLES ---
        marcoConteo = tk.LabelFrame(self.pestañaRegistro, text="Conteo de Árboles (Diámetro)", bg="#e6f2ff")
        marcoConteo.pack(fill="x", padx=10, pady=5)

        tk.Label(marcoConteo, text="Fustales:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
        self.txtFustales = tk.Entry(marcoConteo, width=10)
        self.txtFustales.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(marcoConteo, text="Latizales:", bg="#e6f2ff").grid(row=0, column=2, padx=5, pady=5)
        self.txtLatizales = tk.Entry(marcoConteo, width=10)
        self.txtLatizales.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(marcoConteo, text="Brinzales:", bg="#e6f2ff").grid(row=0, column=4, padx=5, pady=5)
        self.txtBrinzales = tk.Entry(marcoConteo, width=10)
        self.txtBrinzales.grid(row=0, column=5, padx=5, pady=5)

        # --- MUESTRAS VEGETALES ---
        marcoMuestras = tk.LabelFrame(self.pestañaRegistro, text="Toma de Muestras Vegetales", bg="#e6f2ff")
        marcoMuestras.pack(fill="both", expand=True, padx=10, pady=5)

        controlesMuestra = tk.Frame(marcoMuestras, bg="#e6f2ff")
        controlesMuestra.pack(fill="x", pady=5)

        tk.Label(controlesMuestra, text="Código:", bg="#e6f2ff").grid(row=0, column=0, padx=5)
        self.txtCodMuestra = tk.Entry(controlesMuestra, width=15)
        self.txtCodMuestra.grid(row=0, column=1, padx=5)

        tk.Label(controlesMuestra, text="Nombre Común:", bg="#e6f2ff").grid(row=0, column=2, padx=5)
        self.txtNombreMuestra = tk.Entry(controlesMuestra, width=15)
        self.txtNombreMuestra.grid(row=0, column=3, padx=5)

        tk.Label(controlesMuestra, text="Uso:", bg="#e6f2ff").grid(row=0, column=4, padx=5)
        self.cmbUso = ttk.Combobox(controlesMuestra, values=["medicinal", "alimenticio", "maderable"], width=10, state="readonly")
        self.cmbUso.grid(row=0, column=5, padx=5)
        self.cmbUso.current(0)

        btnAgregarMuestra = tk.Button(controlesMuestra, text="Agregar Muestra", bg="blue", fg="white", command=self.agregarMuestraTemporal)
        btnAgregarMuestra.grid(row=0, column=6, padx=10)

        self.tablaMuestras = ttk.Treeview(marcoMuestras, columns=("codigo", "nombre", "uso"), show="headings", height=5)
        self.tablaMuestras.heading("codigo", text="Código")
        self.tablaMuestras.heading("nombre", text="Nombre Común")
        self.tablaMuestras.heading("uso", text="Uso")
        self.tablaMuestras.pack(fill="both", expand=True, padx=10, pady=5)

        # --- BOTÓN GUARDAR ---
        btnGuardar = tk.Button(self.pestañaRegistro, text="GUARDAR INSPECCIÓN", bg="green", fg="white", font=("Arial", 12, "bold"), command=self.guardarInspeccionCompleta)
        btnGuardar.pack(pady=10)

    def construirInterfazConsulta(self):
        marcoBusqueda = tk.Frame(self.pestañaConsulta, bg="#f2ffe6")
        marcoBusqueda.pack(pady=15)

        tk.Label(marcoBusqueda, text="ID de Inspección a buscar:", bg="#f2ffe6", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.txtBuscar = tk.Entry(marcoBusqueda, font=("Arial", 12))
        self.txtBuscar.grid(row=0, column=1, padx=5)

        btnBuscar = tk.Button(marcoBusqueda, text="Buscar", bg="black", fg="white", command=self.buscarInspeccion)
        btnBuscar.grid(row=0, column=2, padx=5)

        # Visor de resultados
        self.txtResultados = tk.Text(self.pestañaConsulta, width=80, height=20, font=("Courier", 11), state="disabled")
        self.txtResultados.pack(pady=10)

    def agregarMuestraTemporal(self):
        cod = self.txtCodMuestra.get().strip()
        nom = self.txtNombreMuestra.get().strip()
        uso = self.cmbUso.get()

        if not cod or not nom:
            messagebox.showerror("Error", "Debe ingresar el código y el nombre de la muestra.")
            return

        self.muestrasTemporales.append((cod, nom, uso))
        self.tablaMuestras.insert("", tk.END, values=(cod, nom, uso))

        self.txtCodMuestra.delete(0, tk.END)
        self.txtNombreMuestra.delete(0, tk.END)

    def guardarInspeccionCompleta(self):
        idInsp = self.txtIdInsp.get().strip()
        cong = self.txtConglomerado.get().strip()
        brig = self.txtBrigada.get().strip()
        fust = self.txtFustales.get().strip()
        lat = self.txtLatizales.get().strip()
        brin = self.txtBrinzales.get().strip()

        if not idInsp or not cong or not brig or not fust or not lat or not brin:
            messagebox.showerror("Error", "Todos los campos de datos generales y conteo son obligatorios.")
            return

        if not fust.isdigit() or not lat.isdigit() or not brin.isdigit():
            messagebox.showerror("Error", "Los valores de conteo (fustales, latizales, brinzales) deben ser numéricos.")
            return

        # Guarda usando la lógica
        self.inventario.guardarInspeccion(idInsp, cong, brig, fust, lat, brin, self.muestrasTemporales)
        messagebox.showinfo("Éxito", "Inspección guardada en archivo de texto correctamente.")

        # Limpiar formulario
        self.txtIdInsp.delete(0, tk.END)
        self.txtConglomerado.delete(0, tk.END)
        self.txtBrigada.delete(0, tk.END)
        self.txtFustales.delete(0, tk.END)
        self.txtLatizales.delete(0, tk.END)
        self.txtBrinzales.delete(0, tk.END)
        self.muestrasTemporales.clear()
        for fila in self.tablaMuestras.get_children():
            self.tablaMuestras.delete(fila)

    def buscarInspeccion(self):
        idBusqueda = self.txtBuscar.get().strip()
        if not idBusqueda:
            messagebox.showwarning("Aviso", "Ingrese un ID para buscar.")
            return

        datos = self.inventario.consultarInspeccion(idBusqueda)

        self.txtResultados.config(state="normal")
        self.txtResultados.delete("1.0", tk.END)

        if datos:
            reporte = (
                f"=== RESULTADOS DE LA INSPECCIÓN ===\n\n"
                f"ID Inspección : {datos[0]}\n"
                f"Conglomerado  : {datos[1]}\n"
                f"Brigada       : {datos[2]}\n"
                f"-----------------------------------\n"
                f"CONTEO DE ÁRBOLES:\n"
                f"Fustales      : {datos[3]}\n"
                f"Latizales     : {datos[4]}\n"
                f"Brinzales     : {datos[5]}\n"
                f"-----------------------------------\n"
                f"MUESTRAS REGISTRADAS:\n"
            )

            muestrasPlanas = datos[6]
            if muestrasPlanas:
                muestrasLista = muestrasPlanas.split(";")
                for m in muestrasLista:
                    cod, nom, uso = m.split(",")
                    reporte += f" - [{cod}] {nom} (Uso: {uso})\n"
            else:
                reporte += " No se registraron muestras.\n"

            self.txtResultados.insert(tk.END, reporte)
        else:
            self.txtResultados.insert(tk.END, f"No se encontró ninguna inspección con el ID: {idBusqueda}")

        self.txtResultados.config(state="disabled")

if __name__ == "__main__":
    ventanaPrincipal = tk.Tk()
    app = FrontIFN(ventanaPrincipal)
    ventanaPrincipal.mainloop()

