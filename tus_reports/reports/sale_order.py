from odoo import api, fields, models
import inflect
from translate import Translator


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def digit_to_words(self):
        return Translator(to_lang="en").translate(inflect.engine().number_to_words(str(self.amount_total)))


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def digit_to_words(self):
        return Translator(to_lang="en").translate(inflect.engine().number_to_words(str(self.amount_total)))


class AccountMove(models.Model):
    _inherit = 'account.move'

    def digit_to_words(self):
        return Translator(to_lang="en").translate(inflect.engine().number_to_words(str(self.amount_total)))