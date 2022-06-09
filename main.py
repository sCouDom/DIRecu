import gi, conexionBD

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class VentanaPerfis(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Perfís Usuarios")
        self.set_size_request(400, 300)

        CajaP = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        CajaCmb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        CajaTV = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        bbdd = conexionBD.ConexionBD("bbdd.bd")
        bbdd.conectaBD()
        bbdd.creaCursor()

        modelo = Gtk.ListStore(str, str, str)
        self.filtrado_usuario = 0
        filtro=modelo.filter_new()
        filtro.set_visible_func(self.filtro_usuario)

        vista = Gtk.TreeView(model=filtro)

        for i, titulo in enumerate (["Nome", "DNI", "Departamento"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(titulo, celda, text = 1)
            vista.append_column(columna)

        self.lblUsuario = Gtk.Label(label="Nome Usuario")
        self.cmbNomeU = Gtk.ComboBoxText()
        self.btnInforme = Gtk.Button(label="Informe")
        self.cmbNomeU.connect("changed", self.on_cmbNomeU_changed, filtro, modelo)
        self.btnInforme.connect("clicked", self.on_btnInforme_clicked, bbdd)

        nomePerfis = bbdd.consultaSenParametros("select * from perfis")

        for nome in nomePerfis:
            print(str(nome))
            self.cmbNomeU.append_text(str(nome[1]))

        datosUsuario = bbdd.consultaSenParametros("select nome, dni, departamento from usuarios where dni in "
                                                  "(select dniUsuario from perfisUsuario where idPerfil in (select idPerfil from perfis))")

        for dUsuario in datosUsuario:
            print(dUsuario)
            modelo.append(dUsuario)

        CajaCmb.pack_start(self.lblUsuario, False, False, 5)
        CajaCmb.pack_start(self.cmbNomeU, False, False, 5)
        CajaTV.pack_start(vista, True, True, 5)

        CajaP.pack_start(CajaCmb, False, False, 5)
        CajaP.pack_start(CajaTV, False, False, 5)
        CajaP.pack_start(self.btnInforme, False, False, 5)

        self.add(CajaP)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def filtro_usuario(self, modelo, fila, datos):
        if (self.filtrado_usuario is None or self.filtrado_usuario==0):
            return True
        else:
            return modelo[fila][0] == self.filtrado_usuario

    def on_cmbNomeU_changed(self, combo, filtro, modelo):
        seleccion = combo.get_active_iter()
        if seleccion is not None:
            cmbModelo = combo.get_model()
            numero = cmbModelo[seleccion][0]
            self.filtrado_usuario = str(numero)

        if seleccion is None:
            self.filtrado_usuario = 0
        filtro.refilter()

    def on_btnInforme_clicked(self, button, bd):
        pass

if __name__ == '__main__':
    VentanaPerfis()
    Gtk.main()

