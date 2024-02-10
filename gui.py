import customtkinter
from tkinter import messagebox


class Gui:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.title("Immaculate Grid Solver")
        self.root.geometry("500x350")

        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Immaculate Grid Solver", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Enter grid URL", font=("Roboto", 18))
        self.label.pack(pady=12, padx=10)

        self.input1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Grid URL")
        self.input1.pack(pady=12, padx=10)

        self.button = customtkinter.CTkButton(master=self.frame, text="Submit", command=self.solve)
        self.button.pack(pady=12, padx=10)

        self.return_value = ""

    def solve(self):
        print('URL provided: ' + self.input1.get())
        if self.validate():
            self.return_value = self.input1.get()
            messagebox.showinfo('Immaculate Grid Solver', 'The application will now start searching for the right '
                                                          'players! \nNote: Please make sure that the Immaculate Grid '
                                                          'page is opened in your browser.')
            self.root.destroy()
        else:
            messagebox.showinfo('Alert', 'The provided URL is in incorrect format!')

    def validate(self):
        if "https://www.immaculategrid.com/basketball/mens/" in self.input1.get():
            return True
        else:
            return False
