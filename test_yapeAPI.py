import unittest
from yapeAPI import Cuenta,BD

class TestYapeAPI(unittest.TestCase):

    def setUp(self):
        self.cuenta_origen = Cuenta("123", "Luisa", 400, ["456"])
        self.cuenta_destino = Cuenta("456", "Andrea", 300, ["123"])

    def test_pago_exitoso(self):
        """
        Caso de prueba: Pago exitoso
        """
        # Realizar un pago exitoso de 100 unidades
        self.assertTrue(self.cuenta_origen.pagar(self.cuenta_destino.Numero, 100))
        self.cuenta_destino = next((cuenta for cuenta in BD if cuenta.Numero == self.cuenta_destino.Numero), None)  # Update cuenta_destino object
        self.assertEqual(self.cuenta_origen.Saldo, 300)
        self.assertEqual(self.cuenta_destino.Saldo, 400)
        self.assertEqual(len(self.cuenta_origen.Historial), 1)
        self.assertEqual(len(self.cuenta_destino.Historial), 1)

    def test_saldo_insuficiente(self):
        """
        Caso de prueba: Saldo insuficiente para realizar el pago
        """
        # Intentar realizar un pago con saldo insuficiente de 500 unidades
        self.assertFalse(self.cuenta_origen.pagar(self.cuenta_destino.Numero, 500))
        self.assertEqual(self.cuenta_origen.Saldo, 400)
        self.assertEqual(self.cuenta_destino.Saldo, 300)
        self.assertEqual(len(self.cuenta_origen.Historial), 0)
        self.assertEqual(len(self.cuenta_destino.Historial), 0)

    def test_cuenta_origen_invalida(self):
        """
        Caso de prueba: Cuenta de origen inválida
        """
        # Intentar realizar un pago con una cuenta de origen inválida
        self.assertFalse(self.cuenta_origen.pagar("789", 100))
        self.assertEqual(self.cuenta_origen.Saldo, 400)
        self.assertEqual(self.cuenta_destino.Saldo, 300)
        self.assertEqual(len(self.cuenta_origen.Historial), 0)
        self.assertEqual(len(self.cuenta_destino.Historial), 0)

    def test_cuenta_destino_invalida(self):
        """
        Caso de prueba: Cuenta de destino inválida
        """
        # Intentar realizar un pago con una cuenta de destino inválida
        self.assertFalse(self.cuenta_origen.pagar(self.cuenta_destino.Numero + "invalida", 100))
        self.assertEqual(self.cuenta_origen.Saldo, 400)
        self.assertEqual(self.cuenta_destino.Saldo, 300)
        self.assertEqual(len(self.cuenta_origen.Historial), 0)
        self.assertEqual(len(self.cuenta_destino.Historial), 0)

if __name__ == '__main__':
    unittest.main()