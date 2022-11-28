import customtkinter as tk
import threading

tk.set_appearance_mode("System")
tk.set_default_color_theme("blue")

class Application(tk.CTkFrame):
    def __init__(self, master: tk.CTk):
        super().__init__(master)

        self.textvar_rfp = tk.StringVar()
        self.textvar_rfi = tk.StringVar()
        self.textvar_rfr = tk.StringVar()
        self.textvar_rff = tk.StringVar()
        self.textvar_rga = tk.StringVar()
        self.textvar_rgb = tk.StringVar()
        self.textvar_rgc = tk.StringVar()
        self.textvar_rgd = tk.StringVar()
        self.textvar_rge = tk.StringVar()
        self.textvar_rgf = tk.StringVar()
        self.textvar_rgg = tk.StringVar()
        self.textvar_rgh = tk.StringVar()

        self.label_register = tk.CTkLabel(self, text="Registers")
        self.label_screen = tk.CTkLabel(self, text="Screen")
        self.label_ramcontent = tk.CTkLabel(self, text="RAM Content")

        self.label_rfp = tk.CTkLabel(self, text="RFP", anchor="e", width=30)
        self.label_rfi = tk.CTkLabel(self, text="RFI", anchor="e", width=30)
        self.label_rfr = tk.CTkLabel(self, text="RFR", anchor="e", width=30)
        self.label_rff = tk.CTkLabel(self, text="RFF", anchor="e", width=30)
        self.label_rga = tk.CTkLabel(self, text="RGA", anchor="e", width=30)
        self.label_rgb = tk.CTkLabel(self, text="RGB", anchor="e", width=30)
        self.label_rgc = tk.CTkLabel(self, text="RGC", anchor="e", width=30)
        self.label_rgd = tk.CTkLabel(self, text="RGD", anchor="e", width=30)
        self.label_rge = tk.CTkLabel(self, text="RGE", anchor="e", width=30)
        self.label_rgf = tk.CTkLabel(self, text="RGF", anchor="e", width=30)
        self.label_rgg = tk.CTkLabel(self, text="RGG", anchor="e", width=30)
        self.label_rgh = tk.CTkLabel(self, text="RGH", anchor="e", width=30)

        self.entry_rfp = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rfp)
        self.entry_rfi = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rfi)
        self.entry_rfr = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rfr)
        self.entry_rff = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rff)
        self.entry_rga = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rga)
        self.entry_rgb = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rgb)
        self.entry_rgc = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rgc)
        self.entry_rgd = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rgd)
        self.entry_rge = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rge)
        self.entry_rgf = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rgf)
        self.entry_rgg = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rgg)
        self.entry_rgh = tk.CTkEntry(self, justify="right", state="disabled", textvariable=self.textvar_rgh)

        self.canvas = tk.CTkCanvas(self, bg="black", bd=5, width=600, height=400)
    
        self.pack_all()
        self.grid()
    
    def pack_all(self):
        self.label_register.grid(row=0, column=0, columnspan=2)
        self.label_screen.grid(row=0, column=2)
        self.label_ramcontent.grid(row=0, column=3)

        self.label_rfp.grid(row=1 , column=0, padx=0)
        self.label_rfi.grid(row=2 , column=0, padx=0)
        self.label_rfr.grid(row=3 , column=0, padx=0)
        self.label_rff.grid(row=4 , column=0, padx=0)
        self.label_rga.grid(row=5 , column=0, padx=0)
        self.label_rgb.grid(row=6 , column=0, padx=0)
        self.label_rgc.grid(row=7 , column=0, padx=0)
        self.label_rgd.grid(row=8 , column=0, padx=0)
        self.label_rge.grid(row=9 , column=0, padx=0)
        self.label_rgf.grid(row=10, column=0, padx=0)
        self.label_rgg.grid(row=11, column=0, padx=0)
        self.label_rgh.grid(row=12, column=0, padx=0)

        self.entry_rfp.grid(row=1 , column=1)
        self.entry_rfi.grid(row=2 , column=1)
        self.entry_rfr.grid(row=3 , column=1)
        self.entry_rff.grid(row=4 , column=1)
        self.entry_rga.grid(row=5 , column=1)
        self.entry_rgb.grid(row=6 , column=1)
        self.entry_rgc.grid(row=7 , column=1)
        self.entry_rgd.grid(row=8 , column=1)
        self.entry_rge.grid(row=9 , column=1)
        self.entry_rgf.grid(row=10, column=1)
        self.entry_rgg.grid(row=11, column=1)
        self.entry_rgh.grid(row=12, column=1)

        self.canvas.grid(row=1, column=2, rowspan=12, padx=5)


app = tk.CTk()
Application(app)

app.mainloop()