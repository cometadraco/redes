from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from cryptography.fernet import Fernet

class PhoneSecure(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Generar clave y objeto Fernet para encriptación
        self.clave = Fernet.generate_key()
        self.fernet = Fernet(self.clave)

        # Estructura vertical para alinear los widgets
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Título de la aplicación
        self.add_widget(Label(
            text='PHONESECURE', font_size=32, size_hint=(1, 0.1),
            bold=True, color=(1, 1, 1, 1)
        ))

        # ScrollView para la lista de contactos
        scroll = ScrollView(size_hint=(1, 0.6))
        contactos_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        contactos_layout.bind(minimum_height=contactos_layout.setter('height'))

        # Lista de contactos de ejemplo
        self.contactos = {
            "Dani": "987654321",
            "Mamá": "912345678",
            "Papá": "999888555",
            "Hermana": "945520012",
            "Judas": "912134675",
            "Cuñado": "912347896",
        }

        # Añadir contactos en el ScrollView
        self.labels_contactos = {}
        for nombre, numero in self.contactos.items():
            label = Label(text=f"{nombre}: {numero}", font_size=20, size_hint_y=None, height=40)
            contactos_layout.add_widget(label)
            self.labels_contactos[nombre] = label

        scroll.add_widget(contactos_layout)
        self.add_widget(scroll)

        # Etiqueta para el número del usuario principal
        self.mi_numero = Label(text="YO: 934131726", font_size=24, size_hint=(1, 0.1))
        self.add_widget(self.mi_numero)

        # Botón para encriptar contactos
        self.encriptar_btn = Button(
            text="ENCRIPTAR", size_hint=(1, 0.1), background_color=(0, 0.6, 0.8, 1)
        )
        self.encriptar_btn.bind(on_press=self.encriptar_contactos)
        self.add_widget(self.encriptar_btn)

        # Botón para desencriptar contactos
        self.desencriptar_btn = Button(
            text="DESENCRIPTAR", size_hint=(1, 0.1), background_color=(0, 0.8, 0.6, 1)
        )
        self.desencriptar_btn.bind(on_press=self.desencriptar_contactos)
        self.add_widget(self.desencriptar_btn)

    def encriptar_contactos(self, instance):
        # Encriptar los números de los contactos y actualizar la interfaz
        for nombre, numero in self.contactos.items():
            numero_encriptado = self.fernet.encrypt(numero.encode()).decode()
            self.labels_contactos[nombre].text = f"{nombre}: {numero_encriptado}"

    def desencriptar_contactos(self, instance):
        # Desencriptar los números de los contactos y actualizar la interfaz
        for nombre, label in self.labels_contactos.items():
            numero_encriptado = label.text.split(": ")[1]
            numero_desencriptado = self.fernet.decrypt(numero_encriptado.encode()).decode()
            label.text = f"{nombre}: {numero_desencriptado}"

class PhoneSecureApp(App):
    def build(self):
        return PhoneSecure()

if __name__ == "__main__":
    PhoneSecureApp().run()
