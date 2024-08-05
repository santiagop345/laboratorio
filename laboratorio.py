import json

class CuentaBancaria:
    def __init__(self, numero_cuenta, titular, saldo=0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo

    def depositar(self, cantidad):
        self.saldo += cantidad
        print(f"Deposito de {cantidad} realizado. Nuevo saldo: {self.saldo}")

    def retirar(self, cantidad):
        if cantidad > self.saldo:
            print("Fondos insuficientes")
        else:
            self.saldo -= cantidad
            print(f"Retiro de {cantidad} realizado. Nuevo saldo: {self.saldo}")

class CuentaBancariaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo=0, sobregiro=0):
        super().__init__(numero_cuenta, titular, saldo)
        self.sobregiro = sobregiro

    def retirar(self, cantidad):
        if cantidad > self.saldo + self.sobregiro:
            print("Fondos insuficientes incluso con sobregiro")
        else:
            self.saldo -= cantidad
            print(f"Retiro de {cantidad} realizado. Nuevo saldo: {self.saldo}")

class CuentaBancariaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo=0, tasa_interes=0.01):
        super().__init__(numero_cuenta, titular, saldo)
        self.tasa_interes = tasa_interes

    def aplicar_interes(self):
        interes = self.saldo * self.tasa_interes
        self.saldo += interes
        print(f"Interes de {interes} aplicado. Nuevo saldo: {self.saldo}")

class Banco:
    def __init__(self):
        self.cuentas = []

    def crear_cuenta(self, cuenta):
        self.cuentas.append(cuenta)
        print(f"Cuenta creada para {cuenta.titular}")

    def leer_cuentas(self):
        for cuenta in self.cuentas:
            print(f"Numero de cuenta: {cuenta.numero_cuenta}, Titular: {cuenta.titular}, Saldo: {cuenta.saldo}")

    def actualizar_cuenta(self, numero_cuenta, nuevo_saldo):
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                cuenta.saldo = nuevo_saldo
                print(f"Saldo actualizado para la cuenta {numero_cuenta}. Nuevo saldo: {nuevo_saldo}")
                return
        print(f"No se encontro cuenta con numero {numero_cuenta}")

    def eliminar_cuenta(self, numero_cuenta):
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                self.cuentas.remove(cuenta)
                print(f"Cuenta eliminada para el numero {numero_cuenta}")
                return
        print(f"No se encontro cuenta con numero {numero_cuenta}")

    def guardar_datos(self, archivo):
        try:
            with open(archivo, 'w') as f:
                json.dump([cuenta.__dict__ for cuenta in self.cuentas], f)
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def cargar_datos(self, archivo):
        try:
            with open(archivo, 'r') as f:
                cuentas_data = json.load(f)
                self.cuentas = [self.crear_cuenta_desde_dict(data) for data in cuentas_data]
            print("Datos cargados correctamente")
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def crear_cuenta_desde_dict(self, data):
        if 'sobregiro' in data:
            return CuentaBancariaCorriente(data)
        elif 'tasa_interes' in data:
            return CuentaBancariaAhorro(data)
        else:
            return CuentaBancaria(data)
