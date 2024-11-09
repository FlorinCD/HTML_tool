import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from .files import HtmlFile


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

        self.write_to_logger_label = None
        self.write_to_logger_checkbox = None
        self.write_to_logger_checkbox_var = None
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
        self.write_to_logger_checkbox_var = tk.IntVar()

        # Creating the checkbox
        self.convert_checkbox = tk.Checkbutton(self.frame, text="Check", variable=self.convert_checkbox_var,
                                               command=self.on_check_abs_to_rel,  font=("Arial", 11), bg='lightblue')
        self.convert_checkbox.place(x=340, y=120)

        # Creating the label for writing to logger
        self.write_to_logger_label = tk.Label(self.frame, text="Write to logger all hrefs", anchor="w",
                                      bg='lightblue', font=("Arial", 11))
        self.write_to_logger_label.place(x=100, y=180)

        # Creating the checkbox for writing to logger
        self.write_to_logger_checkbox = tk.Checkbutton(self.frame, text="Check", variable=self.write_to_logger_checkbox_var,
                                               command=self.on_check_logger,  font=("Arial", 11), bg='lightblue')
        self.write_to_logger_checkbox.place(x=340, y=180)

    # Method to open file dialog and get the file and format the html file
    def open_file(self, file_label: tk.Label) -> None:
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:

            translate_to_rel = True if self.convert_checkbox_var.get() == 1 else False
            write_to_log = True if self.write_to_logger_checkbox_var.get() == 1 else False

            HtmlFile(file_path, translate_to_rel, write_to_log)

            # translate local references from absolute to relative path
            if translate_to_rel:
                messagebox.showinfo("Popup", "The tool will format the local references to relative!")

            # write the output to the logger
            if write_to_log:
                messagebox.showinfo("Popup", "The tool will write to the logger all the information!")

    # Method to check the state of the checkbox for relative paths
    def on_check_abs_to_rel(self) -> None:
        if self.convert_checkbox_var.get() == 1:
            messagebox.showinfo("Popup", "The paths will be set to relative!")
        else:
            messagebox.showinfo("Popup", "The paths will remain unchanged!")

    # Method to check the state of the checkbox for logger
    def on_check_logger(self) -> None:
        if self.write_to_logger_checkbox_var.get() == 1:
            messagebox.showinfo("Popup", "The logger will be written!")
        else:
            messagebox.showinfo("Popup", "The logger won't be written!")
