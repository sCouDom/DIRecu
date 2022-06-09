import conexionBD
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

bbdd = conexionBD.ConexionBD("/home/dam2a/PycharmProjects/examenDI/bbdd.bd")
bbdd.conectaBD()
bbdd.creaCursor()

builder_main = Gtk.Builder()
builder_main.add_from_file("/home/dam2a/PycharmProjects/examenDI/loginDI.glade")

builder_clientes = Gtk.Builder()
builder_clientes.add_from_file("/home/dam2a/PycharmProjects/examenDI/clientes.glade")

builder_servizos = Gtk.Builder()
builder_servizos.add_from_file("/home/dam2a/PycharmProjects/examenDI/servizos.glade")

class servizosVentana(Gtk.Window):

    def __init__(self):

        class HandlerServizos:

            def on_servizosWindow_destroy(self, button):
                Gtk.main_quit()

            def on_informeButton_clicked(self):
                pass
        #ganso
        builder_servizos.connect_signals(HandlerServizos())
        ventanaServizos = builder_servizos.get_object("servizosWindow")
        gridServizos = builder_servizos.get_object("servizosGrid")
        self.informar = Gtk.Button(label="Xerar informe")
        gridServizos.attach(self.informar, 0, 1, 1, 1)
        self.informar.connect("clicked", HandlerServizos.on_informeButton_clicked)
        tViewModel = Gtk.ListStore(int, str, int)
        servizos = bbdd.consultaSenParametros("select * from servizos")
        for servizo in servizos:
            tViewModel.append(servizo)
        self.view = Gtk.TreeView(model=tViewModel)
        for i, tituloColumna in enumerate(["ID", "Nome", "Número de clientes"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i)
            self.view.append_column(columna)
        gridServizos.attach(self.view, 0, 2, 1, 1)
        ventanaServizos.show_all()

class clientesVentana(Gtk.Window):

    def __init__(self):


        class HandlerClientes:

            def on_clientesWindow_destroy(self, *args):
                Gtk.main_quit()

            def on_addButton_clicked(self, selec):

                consulta = bbdd.consultaSenParametros("insert into clientes (nome, apelido, dni, correo, idade)"
                                           "values ('"+nome.get_text()+"','"+apelido.get_text()+"','"+dni.get_text()+"','"+correo.get_text()+"','"+idade.get_text()+"');")
                if consulta is not None:
                    print("hola")
                    modelo, puntero = selec.get_selected() #qué devuelve esto?
                    modelo.append([nome.get_text(), apelido.get_text(), dni.get_text(), correo.get_text(), int(idade.get_text())])

            def on_updateButton_clicked(self, selec):
                consulta = bbdd.consultaSenParametros("update clientes "
                                                      "set nome='" + nome.get_text() + "',apelido='" + apelido.get_text() + "',dni='" + dni.get_text() + "',correo='" + correo.get_text() + "',idade='" + idade.get_text() + "' "
                                                      "where dni='"+dni.get_text()+"';")
                if consulta is not None:
                    modelo, fila = selec.get_selected()
                    modelo[fila][0] = nome.get_text()
                    modelo[fila][1] = apelido.get_text()
                    modelo[fila][2] = dni.get_text()
                    modelo[fila][3] = correo.get_text()
                    modelo[fila][4] = int(idade.get_text())

            def on_deleteButton_clicked(self, selec):
                consulta = bbdd.consultaSenParametros("delete from clientes where dni ='"+dni.get_text()+"';")
                if consulta is not None:
                    modelo, puntero = selec.get_selected()
                    modelo.remove(puntero)

            def on_servizosButton_clicked(self, button):
                window.hide()
                ser_ven = servizosVentana()

            def on_tView_changed(self, selec):
                modelo, puntero = selec.get_selected()
                nome.set_text(modelo[puntero][0])
                apelido.set_text(modelo[puntero][1])
                dni.set_text(modelo[puntero][2])
                correo.set_text(modelo[puntero][3])
                idade.set_text(str(modelo[puntero][4]))

        builder_clientes.connect_signals(HandlerClientes())
        nome = builder_clientes.get_object("nome")
        apelido = builder_clientes.get_object("apelido")
        dni = builder_clientes.get_object("dni")
        correo = builder_clientes.get_object("correo")
        idade = builder_clientes.get_object("idade")
        window = builder_clientes.get_object("clientesWindow")
        window.set_title("Clientes")
        grid = builder_clientes.get_object("grid")
        box = builder_clientes.get_object("box")
        #ganso
        tViewModel = Gtk.ListStore(str, str, str, str, int)
        clientes = bbdd.consultaSenParametros("select * from clientes")
        for cliente in clientes:
            tViewModel.append(cliente)
        tView = Gtk.TreeView(model=tViewModel)
        box.pack_start(tView, False, False, 0)
        for i, tituloColumna in enumerate(["Nome", "Apelido", "DNI", "Correo", "Idade"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i)
            tView.append_column(columna)
        seleccion = tView.get_selection()
        seleccion.connect("changed", HandlerClientes.on_tView_changed, seleccion)
        self.modificar = Gtk.Button(label="Actualizar cliente")
        self.modificar.connect("clicked", HandlerClientes.on_updateButton_clicked, seleccion)
        grid.attach(self.modificar, 1, 0, 1, 1)
        self.engadir = Gtk.Button(label="Engadir cliente")
        self.engadir.connect("clicked", HandlerClientes.on_addButton_clicked, seleccion)
        grid.attach(self.engadir, 0, 0, 1, 1)
        self.borrar = Gtk.Button(label="Borrar cliente")
        self.borrar.connect("clicked", HandlerClientes.on_deleteButton_clicked, seleccion)
        grid.attach(self.borrar, 2, 0, 1, 1)
        window.show_all()


class mainWindow(Gtk.Window):

    def __init__(self):

        class Handler:

            def on_window_destroy(self, *args):
                Gtk.main_quit()

            def on_loginButton_clicked(self, button):
                userEntry = builder_main.get_object("nomeUsuario")
                userInput = userEntry.get_text()
                pwordEntry = builder_main.get_object("contrasinal")
                passwordInput = pwordEntry.get_text()
                userDB = bbdd.consultaSenParametros("select * from usuarios where usuario='" + userInput + "'")
                if passwordInput == userDB[0][1]:
                    window.hide()
                    cli_ven = clientesVentana()

        builder_main.connect_signals(Handler())
        window = builder_main.get_object("loginWindow")
        window.set_title("Login")
        window.show_all()


def main():
    m = mainWindow()
    Gtk.main()
    return 0


if __name__ == '__main__':
    main()
