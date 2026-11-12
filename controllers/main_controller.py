
from views.main_view import MainView
from controllers.auth_controller import AuthController
from controllers.paciente_controller import PacienteController
from controllers.departamento_controller import DepartamentoController
from controllers.farmacia_controller import FarmaciaController
from services.clima_service import ClimaService
from models.usuario import Usuario


class MainController:
    def __init__(self):
        self.view = MainView()
        self.auth_controller = AuthController()
        self.paciente_controller = PacienteController()
        self.departamento_controller = DepartamentoController()
        self.farmacia_controller = FarmaciaController()
        self.clima_service = ClimaService()
        self.usuario_actual: Usuario | None = None

    def consultar_clima(self) -> None:
        print("\n--- CONSULTA DEL CLIMA (OPEN-METEO) ---")
        print("Ciudad disponible: Chillán")

        # Coordenadas de Chillán
        latitud = -36.6066
        longitud = -72.1034

        resultado = self.clima_service.consultar_clima(
            latitud, longitud
        )

        if resultado is None:
            print("[ERROR] No fue posible obtener el clima.")
            return

        print("\n--- CLIMA ACTUAL EN CHILLÁN ---")
        print(f"Temperatura: {resultado['temperatura']} °C")
        print(f"Humedad: {resultado['humedad']} %")
        print(f"Viento: {resultado['viento']} km/h")

    def ejecutar(self) -> None:
        self.usuario_actual = self.auth_controller.iniciar_sesion()

        if not self.usuario_actual:
            self.view.mostrar_mensaje(
                "El programa ha finalizado debido a credenciales inválidas."
            )
            return

        while True:
            opcion = self.view.mostrar_menu(self.usuario_actual)

            if opcion == 1:
                self.paciente_controller.ejecutar()

            elif opcion == 2:
                self.departamento_controller.ejecutar()

            elif opcion == 3:
                self.farmacia_controller.ejecutar()

            elif opcion == 4:
                self.auth_controller.ejecutar(self.usuario_actual)

            elif opcion == 5:
                self.consultar_clima()

            elif opcion == 9:
                self.view.mostrar_mensaje(
                    f"Cerrando sesión de '{self.usuario_actual.username}'..."
                )
                self.usuario_actual = self.auth_controller.iniciar_sesion()

                if not self.usuario_actual:
                    self.view.mostrar_mensaje(
                        "El programa ha finalizado debido a credenciales inválidas."
                    )
                    break

            elif opcion == 0:
                self.view.mostrar_mensaje(
                    "Gracias por usar el sistema de la Clínica. ¡Hasta luego!"
                )
                break

            else:
                self.view.mostrar_mensaje(
                    "Opción no válida. Por favor, intente nuevamente."
                )
