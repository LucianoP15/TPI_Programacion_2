"""
Pantallas de consola: piden datos, llaman a los servicios y muestran resultados.
Todas tienen la misma firma: (servicios: Servicios, sesion: Usuario) -> None.
No hace falta capturar excepciones aca: Menu._ejecutar() ya captura
FoodStoreError, ValueError y OperacionCancelada y vuelve al menu.
"""
