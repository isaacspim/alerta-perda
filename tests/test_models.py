import unittest
from datetime import date, timedelta

from models import Lote, RegistroPerda


class LoteTest(unittest.TestCase):
    def test_lote_with_imminent_expiry_needs_urgent_action(self):
        lote = Lote(data_validade=date.today() + timedelta(days=2), quantidade_atual=5)
        self.assertEqual(lote.status_alerta['tipo'], 'warning')

    def test_lote_without_balance_is_not_an_active_alert(self):
        lote = Lote(data_validade=date.today() + timedelta(days=10), quantidade_atual=0)
        self.assertEqual(lote.status_alerta['texto'], 'Sem saldo')

    def test_loss_record_can_reference_a_lot(self):
        lote = Lote(data_validade=date.today() + timedelta(days=10), quantidade_atual=4)
        registro = RegistroPerda(quantidade_perdida=1, motivo='Produto vencido', lote=lote)
        self.assertIs(registro.lote, lote)
