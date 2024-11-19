import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class PhoneSecure(toga.App):
    def startup(self):
        """Configura la interfaz de usuario de la aplicación."""
        self.key = get_random_bytes(16)  # Clave de 16 bytes para AES-128
        self.contactos = {
            "Dani": "987654321",
            "Mamá": "912345678",
            "Papá": "999888555",
            "Hermana": "945520012",
            "Judas": "912134675",
            "Cuñado": "912347896",
        }

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        title_label = toga.Label(
            "PHONESECURE", style=Pack(font_size=32, alignment="center", padding=10)
        )
        main_box.add(title_label)

        contactos_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.labels_contactos = {}

        for nombre, numero in self.contactos.items():
            label = toga.Label(f"{nombre}: {numero}", style=Pack(padding=(5, 0)))
            contactos_box.add(label)
            self.labels_contactos[nombre] = label

        scroll = toga.ScrollContainer(content=contactos_box, style=Pack(height=300))
        main_box.add(scroll)

        self.mi_numero = toga.Label(
            "YO: 934131726", style=Pack(font_size=24, padding=10)
        )
        main_box.add(self.mi_numero)

        encrypt_button = toga.Button(
            "ENCRIPTAR",
            on_press=self.encriptar_contactos,
            style=Pack(padding=10),
        )
        main_box.add(encrypt_button)

        decrypt_button = toga.Button(
            "DESENCRIPTAR",
            on_press=self.desencriptar_contactos,
            style=Pack(padding=10),
        )
        main_box.add(decrypt_button)

        self.main_window = toga.MainWindow(title="PhoneSecure")
        self.main_window.content = main_box
        self.main_window.show()

    def encriptar_contactos(self, widget):
        """Encripta los números de los contactos y actualiza la interfaz."""
        try:
            for nombre, numero in self.contactos.items():
                cipher = AES.new(self.key, AES.MODE_CBC)
                ct_bytes = cipher.encrypt(pad(numero.encode(), AES.block_size))
                iv = base64.b64encode(cipher.iv).decode('utf-8')
                ct = base64.b64encode(ct_bytes).decode('utf-8')
                numero_encriptado = f"{iv}:{ct}"
                self.labels_contactos[nombre].text = f"{nombre}: {numero_encriptado}"
        except Exception as e:
            print(f"Error en la encriptación: {e}")

    def desencriptar_contactos(self, widget):
        """Desencripta los números de los contactos y actualiza la interfaz."""
        try:
            for nombre, label in self.labels_contactos.items():
                numero_encriptado = label.text.split(": ")[1]
                iv, ct = numero_encriptado.split(":")
                iv = base64.b64decode(iv)
                ct = base64.b64decode(ct)
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                numero_desencriptado = unpad(cipher.decrypt(ct), AES.block_size).decode()
                label.text = f"{nombre}: {numero_desencriptado}"
        except Exception as e:
            print(f"Error en la desencriptación: {e}")

def main():
    return PhoneSecure()
