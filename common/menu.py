import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from .files import HtmlFile
from tkinter import font


class Menu:
    """
    This class provides the interface wrapper of tkinter to display all the buttons and labels.
    Created with the purpose to simply the need of control over the interface.
    """

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

        self.write_to_logger_scripts_label = None
        self.write_to_logger_scripts_checkbox = None
        self.write_to_logger_scripts_checkbox_var = None

        self.frame = None
        self.bg_img_reference = None

        self.read_me_button = None

        self.decorate_menu()

    def run_loop(self) -> None:
        self.root.mainloop()

    def decorate_menu(self) -> None:
        """
        Decorate all the window with the necessary elements (buttons, labels, frame).
        """
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
        self.write_to_logger_scripts_checkbox_var = tk.IntVar()

        # Creating the checkbox
        self.convert_checkbox = tk.Checkbutton(self.frame, text="Check", variable=self.convert_checkbox_var,
                                               command=self.on_check_abs_to_rel,  font=("Arial", 11), bg='lightblue')
        self.convert_checkbox.place(x=340, y=120)

        # Creating the label for writing to logger
        self.write_to_logger_label = tk.Label(self.frame, text="Write to logger all hrefs", anchor="w",
                                      bg='lightblue', font=("Arial", 11))
        self.write_to_logger_label.place(x=100, y=180)

        # Creating the label for writing to logger the scrips
        self.write_to_logger_scripts_label = tk.Label(self.frame, text="Write to logger information about scripts", anchor="w",
                                      bg='lightblue', font=("Arial", 11))
        self.write_to_logger_scripts_label.place(x=100, y=240)

        # Creating the checkbox for writing to logger
        self.write_to_logger_checkbox = tk.Checkbutton(self.frame, text="Check", variable=self.write_to_logger_checkbox_var,
                                               command=self.on_check_logger,  font=("Arial", 11), bg='lightblue')
        self.write_to_logger_checkbox.place(x=280, y=180)

        # Creating the checkbox for writing to logger for scrips
        self.write_to_logger_scripts_checkbox = tk.Checkbutton(self.frame, text="Check", variable=self.write_to_logger_scripts_checkbox_var,
                                               command=self.on_check_logger_scripts,  font=("Arial", 11), bg='lightblue')
        self.write_to_logger_scripts_checkbox.place(x=380, y=240)
        button_font = font.Font(family="Helvetica", size=11, weight="bold")
        stylish_button = tk.Button(
            self.frame,
            text="ReadMe!",
            command=self.open_read_me,
            font=button_font,
            bg="#4CAF50",  # Button background color
            fg="white",  # Text color
            activebackground="#45a049",  # Background color when clicked
            activeforeground="white",  # Text color when clicked
            relief="raised",  # Raised appearance
            bd=5,  # Border width
            padx=10,  # Horizontal padding
            pady=4  # Vertical padding
        )

        # Place the button in the window
        stylish_button.place(x=180, y=290)

    def open_file(self, file_label: tk.Label) -> None:
        """
        This method is meant to open the file given by the user and perform the checked options from the
        interface. Based on the actions some popup messages will appear.
        """
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:

            translate_to_rel = True if self.convert_checkbox_var.get() == 1 else False
            write_to_log = True if self.write_to_logger_checkbox_var.get() == 1 else False
            write_to_log_script = True if self.write_to_logger_scripts_checkbox_var.get() == 1 else False

            HtmlFile(file_path, translate_to_rel, write_to_log, write_to_log_script)

            # translate local references from absolute to relative path
            if translate_to_rel:
                messagebox.showinfo("Popup", "The tool will format the local references to relative!")

            # write the output to the logger
            if write_to_log:
                messagebox.showinfo("Popup", "The tool will write to the logger all the information!")

    def on_check_abs_to_rel(self) -> None:
        """
        Method to check the state of the checkbox for relative paths
        """
        if self.convert_checkbox_var.get() == 1:
            messagebox.showinfo("Popup", "The paths will be set to relative!")
        else:
            messagebox.showinfo("Popup", "The paths will remain unchanged!")

    def on_check_logger(self) -> None:
        """
        Method to check the state of the checkbox for logger
        """
        if self.write_to_logger_checkbox_var.get() == 1:
            messagebox.showinfo("Popup", "The logger will be written!")
        else:
            messagebox.showinfo("Popup", "The logger won't be written!")

    def on_check_logger_scripts(self) -> None:
        """
        Method to check the state of the checkbox for scripts to be written to logger
        """
        if self.write_to_logger_scripts_checkbox_var.get() == 1:
            messagebox.showinfo("Popup", "The information about scripts will be written!")
        else:
            messagebox.showinfo("Popup", "The information about scripts will not be written!")

    def open_read_me(self) -> None:
        """
        Will open a new window to show some basic info about the application.
        """
        readMeObj = ReadMe()


class ReadMe:
    """
    This class is used to display the readme window where the user can read the needed information.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("ReadMe")
        self.root.geometry("518x200")
        self.root.resizable(False, False)

        self.decorate()

    def decorate(self) -> None:
        """
        Is meant to decorate the window with the necessary elements (buttons, labels, frames)
        """
        self.label0 = tk.Label(self.root, text="Select an html file to format it. The current functionalities are:\n"
                                               "translating from absolute paths to relative paths\n"
                                               "writing to logger all the hrefs from the all html tree (even its children)\n"
                                               "writing to logger the scripts paths if they exist in the html tree (even its children)\n"
                                               "the logger file has an default value which can be changed from settings file\n"
                                                "first check the desired options and then select the specific html file\n"
                                                "the formatting will happen right before after", anchor="w",
                                              bg='lightblue', font=("Arial", 11))
        self.label0.place(x=0, y=40)
