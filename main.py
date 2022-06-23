import gi
import os
import sys
import glob
import shutil
from datetime import date
gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
HOME = os.path.expanduser('~')
date = date.today()

class Dialog_notinstalled(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(transient_for=parent, use_header_bar=True)
        self.parent = parent

        self.set_title(title='scrcpy is not installed')
        self.use_header_bar = True
        self.set_modal(modal=True)
        self.connect('response', self.dialog_response)

        # Criando os botões.
        self.add_buttons(
            '_Cancel', Gtk.ResponseType.CANCEL,
            '_OK', Gtk.ResponseType.OK,
        )

        # Adicionando class action nos botões.
        btn_ok = self.get_widget_for_response(
            response_id=Gtk.ResponseType.OK,
        )
        btn_ok.get_style_context().add_class(class_name='suggested-action')
        btn_cancel = self.get_widget_for_response(
            response_id=Gtk.ResponseType.CANCEL,
        )
        btn_cancel.get_style_context().add_class(class_name='destructive-action')

        # Acessando o box do dialogo.
        content_area = self.get_content_area()
        content_area.set_orientation(orientation=Gtk.Orientation.VERTICAL)
        content_area.set_spacing(spacing=12)
        content_area.set_margin_top(margin=12)
        content_area.set_margin_end(margin=12)
        content_area.set_margin_bottom(margin=12)
        content_area.set_margin_start(margin=12)

        label = Gtk.Label()
        label.set_markup("<b>scrcpy</b> is not installed on your operating system. Please install scrcpy from <a href='https://github.com/Genymobile/scrcpy'>Github</a>.       ")
        content_area.append(child=label)

        self.show()

    def dialog_response(self, dialog, response):
        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.OK:
            print('Button {OK} is clicked.')
            #self.parent.label.set_text(str=f'Botão CANCELAR pressionado')

            dialog.close()

        elif response == Gtk.ResponseType.CANCEL:
            print('Button {CANCEL} is clicked.')
            #self.parent.label.set_text(str=f'Botão CANCELAR pressionado')

            dialog.close()

    def get_entry_text(self):
        return self.entry.get_text()

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 400)
        self.set_title("scrcpy")
        # Things will go here
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box1)
        
        self.img = Gtk.Image()
        self.img.set_from_file("logo.jpg")
        self.img.set_pixel_size(300)
        self.box1.append(self.img)
        
        self.label = Gtk.Label()
        self.label.set_markup("<big><b>Instructions for using</b></big>\n 1. Connect your Android device via USB cable to your computer.\n 2. Click on button bellow.")
        self.box1.append(self.label)
        
        self.buttonR = Gtk.Button(label="I got it!")
        self.buttonR.connect("clicked", self.on_buttonR_clicked)
        self.box1.append(self.buttonR)
        
    def on_buttonR_clicked(self, widget, *args):
        self.start()
    def start(self):
        os.system("scrcpy")
        if not os.path.exists("/usr/bin/scrcpy"):
            dialog_n = Dialog_notinstalled(self)
            response_e = dialog_n.run()

            if response_n == Gtk.ResponseType.OK:
                print("The OK button was clicked")
            elif response_n == Gtk.ResponseType.CANCEL:
                print("The Cancel button was clicked")

            dialog_n.destroy()
        
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()
app = MyApp(application_id="com.github.Genymobile.scrcpy")
app.run(sys.argv)
