import conexionBD

bbdd = conexionBD.ConexionBD("/home/dam2a/PycharmProjects/examenDI/bbdd.bd")
bbdd.conectaBD()
bbdd.creaCursor()


bbdd.consultaSenParametros("insert into servizos (id, nome, numClientes)"
                           "values('1', 'tapicería', 1)")

