import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

class Cuenta:
    def __init__(self, Numero, Nombre, Saldo, Contactos):
        self.Numero = Numero
        self.Nombre = Nombre
        self.Saldo = int(Saldo)
        self.Contactos = Contactos
        self.Historial = []
    
    def historial(self):
        print(f"Saldo de {self.Nombre}: {self.Saldo}")
        print(f"Operaciones de {self.Nombre}")
        for operacion in self.Historial:
            if operacion['tipo'] == 'pago_recibido':
                print(f"Pago recibido de {operacion['origen']} de {operacion['monto']}")
            elif operacion['tipo'] == 'pago_realizado':
                print(f"Pago realizado de {operacion['monto']} a {operacion['destino']}")

    def pagar(self, numerodestino, valor):
        valor = int(valor)
        if self.Saldo >= valor:
            for cuenta in BD:
                if cuenta.Numero == numerodestino:
                    self.Saldo -= valor
                    cuenta.Saldo += valor
                    print("api:",cuenta.Saldo)
                    self.Historial.append({
                        'tipo': 'pago_realizado',
                        'monto': valor,
                        'destino': numerodestino
                    })
                    cuenta.Historial.append({
                        'tipo': 'pago_recibido',
                        'monto': valor,
                        'origen': self.Numero
                    })
                    #print(cuenta.Saldo)  # Verificar el saldo de la cuenta destino
                    return True
            return False
        else:
            return False

BD = []
BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
BD.append(Cuenta("123", "Luisa", 400, ["456"]))
BD.append(Cuenta("456", "Andrea", 300, ["21345"]))

@app.route('/')
def index():
    return "Bienvenido a yape"

@app.route('/billetera/contactos', methods=['GET'])
def getContactos():
    minumero = request.args.get('minumero')
    contactos_dict = {}
    for cuenta in BD:
        if cuenta.Numero == minumero:
            contactos = cuenta.Contactos
            for contacto in contactos:
                for cuenta in BD:
                    if cuenta.Numero == contacto:
                        contactos_dict[contacto] = cuenta.Nombre
                        print(f"{contacto}: {cuenta.Nombre}")
    return jsonify(contactos_dict)

@app.route('/billetera/pagar', methods=['GET'])
def postPagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = request.args.get('valor')
    for cuenta in BD:
        if cuenta.Numero == minumero:
            if cuenta.pagar(numerodestino, valor):
                print(f"Realizado en {datetime.datetime.now().strftime('%d/%m/%Y')}")
                return "Pago realizado exitosamente"
            else:
                print("Saldo insuficiente.")
                return "Saldo insuficiente para realizar el pago"
    return "Cuenta no encontrada"

@app.route('/billetera/historial', methods=['GET'])
def getHistorial():
    minumero = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.Numero == minumero:
            print(f"Saldo de {cuenta.Nombre}: {cuenta.Saldo}")
            print(f"Operaciones de {cuenta.Nombre}")
            for operacion in cuenta.Historial:
                if operacion['tipo'] == 'pago_recibido':
                    origen = next((cuenta_origen.Nombre for cuenta_origen in BD if cuenta_origen.Numero == operacion['origen']), None)
                    print(f"Pago recibido de {operacion['monto']} de {origen}")
                elif operacion['tipo'] == 'pago_realizado':
                    destino = next((cuenta_destino.Nombre for cuenta_destino in BD if cuenta_destino.Numero == operacion['destino']), None)
                    print(f"Pago realizado de {operacion['monto']} a {destino}")
            return "Historial obtenido exitosamente"
    return "Cuenta no encontrada"

if __name__ == '__main__':
    app.run()