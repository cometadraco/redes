import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from cryptography.fernet import Fernet

class PhoneSecure(toga.App):
    def startup(self):
        # Generar clave de encriptación
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

        # Crear caja principal con estilo vertical
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Campos de texto para nombre y número del contacto
        self.name_input = toga.TextInput(placeholder='Nombre del contacto', style=Pack(padding=5))
        self.number_input = toga.TextInput(placeholder='Número del contacto', style=Pack(padding=5))

        # Botón de encriptar con evento on_press
        encrypt_button = toga.Button(
            'Encriptar', 
            on_press=self.encrypt_contact, 
            style=Pack(padding=10)
        )

        # Etiqueta para mostrar el resultado
        self.result_label = toga.Label('Resultado:', style=Pack(padding=10))

        # Añadir widgets al contenedor principal
        main_box.add(self.name_input)
        main_box.add(self.number_input)
        main_box.add(encrypt_button)
        main_box.add(self.result_label)

        # Crear y mostrar la ventana principal
        self.main_window = toga.MainWindow(title='PhoneSecure')
        self.main_window.content = main_box
        self.main_window.show()

    def encrypt_contact(self, widget):
        # Obtener valores del formulario
        name = self.name_input.value
        number = self.number_input.value

        # Verificar que no estén vacíos
        if name and number:
            contact_data = f"{name}: {number}"
            encrypted_data = self.fernet.encrypt(contact_data.encode()).decode()

            # Mostrar el resultado en la etiqueta
            self.result_label.text = f"Resultado: {encrypted_data}"
        else:
            self.result_label.text = "Por favor, ingresa ambos campos."

def main():
    return PhoneSecure()
