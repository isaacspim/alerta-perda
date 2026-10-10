import unittest
from datetime import date, timedelta

from models import Lote


class LoteTest(unittest.TestCase):
    def test_lote_with_imminent_expiry_needs_urgent_action(self):
        lote = Lote(data_validade=date.today() + timedelta(days=2), quantidade_atual=5)
        self.assertEqual(lote.status_alerta['tipo'], 'warning')

    def test_lote_without_balance_is_not_an_active_alert(self):
        lote = Lote(data_validade=date.today() + timedelta(days=10), quantidade_atual=0)
        self.assertEqual(lote.status_alerta['texto'], 'Sem saldo')
