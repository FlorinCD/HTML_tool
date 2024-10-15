import tkinter as tk
from tkinter import filedialog, messagebox, Canvas


class Menu:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("HTML tool")
        self.root.geometry("500x400")
        self.file_button = None
        self.file_label = None
        self.convert_label = None
        self.convert_checkbox = None
        self.convert_checkbox_var = None
        self.frame = None
        self.bg_img_reference = None

        self.decorate_menu()

    def run_loop(self) -> None:
        self.root.mainloop()

    def decorate_menu(self) -> None:
        # Disable window resizing
        self.root.resizable(False, False)

        # set the icon of the menu
        self.root.iconbitmap(r"static/icons/html_tool_icon.ico")

        self.frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Load the background image
        self.bg_img_reference = tk.PhotoImage(file=r"static/images/html_tool_main_menu.png")

        # Create Canvas
        self.canvas1 = Canvas(self.frame, width=500, height=400)
        self.canvas1.pack()
        # Display image
        self.canvas1.create_image((0, 0), image=self.bg_img_reference, anchor="nw")

        # File selection button
        self.file_label = tk.Label(self.frame, text="Please select the html file:", anchor="w", bg='lightblue', font=("Arial", 11))
        self.file_label.place(x=100, y=50)

        self.file_button = tk.Button(self.frame, text="Select", command=lambda: self.open_file(self.file_label), font=("Arial", 11), bg='lightblue')
        self.file_button.place(x=300, y=50)

        self.convert_label = tk.Label(self.frame, text="Translate to relative path all hrefs:", anchor="w", bg='lightblue', font=("Arial", 11))
        self.convert_label.place(x=100, y=120)

        # Variable to hold checkbox state (0 for unchecked, 1 for checked)
        self.convert_checkbox_var = tk.IntVar()

        # Creating the checkbox
        self.convert_checkbox = tk.Checkbutton(self.frame, text="Check", variable=self.convert_checkbox_var,
                                               command=self.on_check,  font=("Arial", 11), bg='lightblue')
        self.convert_checkbox.place(x=340, y=120)

    # Method to open file dialog and get the file
    def open_file(self, file_label: tk.Label) -> None:
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            messagebox.showinfo("Popup", "The file has been added to the tool!")

    # Method to check the state of the checkbox
    def on_check(self):
        if self.convert_checkbox_var.get() == 1:
            messagebox.showinfo("Popup", "Checkbox is checked!")
        else:
            messagebox.showinfo("Popup", "Checkbox is unchecked!")