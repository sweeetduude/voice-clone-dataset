import os
import tkinter as tk
from pygame import mixer


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padx=10, pady=10)  # Add padding
        self.master = master
        self.master.title("Voice Clone Dataset")  # Set app title
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.folders = [f for f in os.listdir() if os.path.isdir(f)]
        self.folder_var = tk.StringVar(self)
        self.folder_var.set(self.folders[0])

        self.folder_label = tk.Label(self, text="Select Folder:")
        self.folder_label.grid(row=0, column=0)
        self.folder_dropdown = tk.OptionMenu(
            self, self.folder_var, *self.folders, command=self.load_files)
        self.folder_dropdown.grid(row=0, column=1, columnspan=3)

        self.file_var = tk.StringVar(self)

        self.file_var.trace('w', self.load_text)

        self.file_label = tk.Label(self, text="Select File:")
        self.file_label.grid(row=1, column=0)
        self.file_dropdown = tk.OptionMenu(self, self.file_var, ())
        self.file_dropdown.grid(row=1, column=1, columnspan=3)

        self.prev_button = tk.Button(
            self, text="Previous", command=self.prev_sound)
        self.prev_button.grid(row=2, column=0, pady=(40, 0))

        self.play_button = tk.Button(
            self, text="Play", command=self.play_sound)
        self.play_button.grid(row=2, column=1, pady=(40, 0))

        self.stop_button = tk.Button(
            self, text="Stop", command=self.stop_sound)
        self.stop_button.grid(row=2, column=2, pady=(40, 0))

        self.next_button = tk.Button(
            self, text="Next", command=self.next_sound)
        self.next_button.grid(row=2, column=3, pady=(40, 0))

        self.text_area = tk.Text(self, height=10, width=60)
        self.text_area.grid(row=3, column=0, columnspan=4, pady=10)

        self.save_button = tk.Button(
            self, text="Save text", command=self.save_text)
        self.save_button.grid(row=4, column=0, columnspan=4)

        self.load_files(self.folder_var.get())

    def load_files(self, folder):
        self.files = [f for f in os.listdir(folder) if f.endswith('.wav')]
        if self.files:
            self.file_var.set(self.files[0])
            self.file_dropdown['menu'].delete(0, 'end')
            for file in self.files:
                self.file_dropdown['menu'].add_command(
                    label=file, command=tk._setit(self.file_var, file))
        else:
            self.file_var.set('')
            self.file_dropdown['menu'].delete(0, 'end')

    def load_text(self, *args):
        try:
            file_path = os.path.join(self.folder_var.get(
            ), self.file_var.get().replace('.wav', '.txt'))
            if not os.path.exists(file_path):
                # Create an empty file if it doesn't exist
                open(file_path, 'w').close()

            with open(file_path, 'r') as f:
                text = f.read()
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, text)
        except Exception as e:
            print(e)

    def play_sound(self):
        try:
            mixer.init()
            mixer.music.load(os.path.join(
                self.folder_var.get(), self.file_var.get()))
            mixer.music.play()
        except Exception as e:
            print(e)

    def stop_sound(self):
        mixer.music.stop()

    def prev_sound(self):
        try:
            index = self.files.index(self.file_var.get())
            if index > 0:
                self.file_var.set(self.files[index - 1])
        except Exception as e:
            print(e)

    def next_sound(self):
        try:
            index = self.files.index(self.file_var.get())
            if index < len(self.files) - 1:
                self.file_var.set(self.files[index + 1])
        except Exception as e:
            print(e)

    def save_text(self):
        try:
            with open(os.path.join(self.folder_var.get(), self.file_var.get().replace('.wav', '.txt')), 'w') as f:
                f.write(self.text_area.get('1.0', tk.END))
        except Exception as e:
            print(e)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
