from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

from encryption import encrypt_file_aes, encrypt_aes_key_with_rsa, generate_rsa_key_pair, generate_aes_key
from decryption_file import decrypt_file_aes, decrypt_aes_key_with_rsa

import os

class MainApp:
    def __init__(self, master):

        self.master = master
        master.title("Cloud File Manager")

        # Load background image
        background_image = Image.open("black.png")
        self.background_photo = ImageTk.PhotoImage(
            background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS))
        background_label = Label(master, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username = ""

        # Specify the path where you want to create the folders
        self.base_folder = 'C:/Users/91772/Desktop/march15'

        # Create folders for storing encrypted and decrypted files
        self.encrypted_folder = os.path.join(self.base_folder, "encrypted")
        self.decrypted_folder = os.path.join(self.base_folder, "decrypted")

        # Create the folders
        os.makedirs(self.encrypted_folder, exist_ok=True)
        os.makedirs(self.decrypted_folder, exist_ok=True)

        # Heading
        heading_label = Label(master, text=" CRYPTOGRAPHY", font=("Tahoma", 30),
                                 bg="black",fg="magenta2")
        heading_label.place(relx=0.3,rely=0.2, anchor=CENTER)

        heading_label_2 = Label(master, text="DO YOU WANT TO SECURE YOUR FILES???", font=("Tahoma", 24), bg="black", fg="cyan2")
        heading_label_2.place(relx=0.3, rely=0.5, anchor=CENTER)

        click_button = Button(master, text="Click Me", command=self.open_signup_form,  width=10, height=2, bg="blue", fg="cyan2", font=("Arial", 14))
        click_button.place(relx=0.3,rely=0.6, anchor=CENTER)


    def open_signup_form(self):
        # Create an instance of the SignupForm and open it
        root.destroy()
        import signup


    def show_file_manager(self):

        file_manager_window = Toplevel(self.master)

        file_manager_window.title("File Manager")
        file_manager_window.attributes('-fullscreen', True)
        self.master.withdraw()
        # file_manager_window.config(bg="light blue")

        image = Image.open("upload.png")  # Replace "your_image.png" with the path to your image
        image = image.resize((file_manager_window.winfo_screenwidth(), file_manager_window.winfo_screenheight()))
        image = ImageTk.PhotoImage(image)
        image_label = Label(file_manager_window, image=image)
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
        image_label.image = image

        button_width = 22
        button_height = 3

        upload_button = Button(file_manager_window, text="UPLOAD & ENCRYPT FILE", command=self.upload_file,
                               width=button_width, height=button_height, bg="blue", fg="white",
                               font=("Arial", 18))  # Specify the desired font and size
        upload_button.place(relx=0.3, rely=0.4, anchor=CENTER)

        decrypt_button = Button(file_manager_window, text="DECRYPT FILE", command=self.decrypt_button_clicked,
                                width=button_width, height=button_height, bg="green", fg="white",
                                font=("Arial", 18))  # Specify the desired font and size
        decrypt_button.place(relx=0.7, rely=0.4, anchor=CENTER)

        exit_button = Button(file_manager_window, text="EXIT", command=file_manager_window.destroy, width=button_width,
                             height=button_height, bg="red", fg="white",
                             font=("Arial", 18))  # Specify the desired font and size
        exit_button.place(relx=0.5, rely=0.6, anchor=CENTER)



       # Define a function to get file size in bytes
    def get_file_size(self, file_path):
        return os.path.getsize(file_path)


    def upload_file(self):
        max_file_size_mb = 50

        file_path = filedialog.askopenfilename()

        # Check if a file is selected
        if file_path:
            # Get file size
            file_size = os.path.getsize(file_path)

            # Check if file size exceeds the limit
            max_file_size = max_file_size_mb * 1024 * 1024  # convert MB to bytes
            if file_size > max_file_size:
                max_file_size_mb_display = max_file_size / (1024 * 1024)
                messagebox.showerror("Error", f"File size exceeds the maximum allowed size of {max_file_size_mb} MB.")
                return

            # Continue with file upload if within size limit
            # Get username
            username: str = self.username

            aes_key = generate_aes_key()
            input_file_path = file_path

            # Specify the directory where the encrypted file will be saved
            encryption_folder = os.path.join(self.base_folder, "encrypted", username)
            os.makedirs(encryption_folder, exist_ok=True)

            # File paths
            encrypted_file_name = os.path.basename(file_path) + ".enc"
            output_file_path = os.path.join(encryption_folder, encrypted_file_name)

            # Encrypt the file with AES
            encrypt_file_aes(input_file_path, aes_key, output_file_path)

            # Key storage paths
            keys_folder = os.path.join(encryption_folder, 'keys')
            os.makedirs(keys_folder, exist_ok=True)
            private_key_path = os.path.join(keys_folder, 'private.pem')
            public_key_path = os.path.join(keys_folder, 'public.pem')
            aes_key_enc_path = os.path.join(keys_folder, 'aes_key.enc')

            # Generate RSA keys and encrypt AES key
            generate_rsa_key_pair(private_key_path, public_key_path)
            encrypt_aes_key_with_rsa(aes_key, public_key_path, aes_key_enc_path)

            messagebox.showinfo("Success", "File encrypted and uploaded successfully.")
        else:
            messagebox.showerror("Error", "No file selected.")

    def decrypt_button_clicked(self):
        # Ask the user to select the encrypted file
        selected_file_path = filedialog.askopenfilename(title="Select Encrypted File")
        if not selected_file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        # Ask the user to select the encrypted AES key
        aes_key_enc_path = filedialog.askopenfilename(title="Select Encrypted AES Key")
        if not aes_key_enc_path:
            messagebox.showerror("Error", "No encrypted AES key selected.")
            return

        # Ask the user to select the RSA private key
        private_key_path = filedialog.askopenfilename(title="Select RSA Private Key")
        if not private_key_path:
            messagebox.showerror("Error", "No RSA private key selected.")
            return

        # Call the decryption functions
        aes_key = decrypt_aes_key_with_rsa(aes_key_enc_path, private_key_path)
        user_decrypted_folder = os.path.join(self.decrypted_folder, self.username)

        os.makedirs(user_decrypted_folder, exist_ok=True)
        output_file_path = os.path.join(user_decrypted_folder, os.path.basename(selected_file_path)[:-4])
        decrypt_file_aes(selected_file_path, aes_key, output_file_path)

        # Show a message indicating that decryption is complete
        messagebox.showinfo("Decryption Complete", "File decrypted successfully.")


if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()


