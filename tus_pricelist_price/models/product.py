from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_pricelist_price(self):
        """
        Author: Bhavesh Jadav TechUltra Solutions
        Date: 27/07/2020
        Func: This method use for get first price list
        first price  and store in price_list_price field if price list or product not found then its set lst_price
        return: N/A
        """
        for product_tmpl_id in self:
            pricelist_item_ids = self.env['product.pricelist.item'].search(
                [('product_tmpl_id', '=', product_tmpl_id.id)])
            if pricelist_item_ids:
                product_tmpl_id.price_list_price = pricelist_item_ids[0].fixed_price
            else:
                product_tmpl_id.price_list_price = product_tmpl_id.lst_price

    price_list_price = fields.Float(string="Pricelist Price", compute='_compute_pricelist_price',
                                    help="price list price of the product", default="0.0")


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_pricelist_price(self):
        """
        Author: Bhavesh Jadav TechUltra Solutions
        Date: 27/07/2020
        Func: This method use for get first price list
        first price  and store in price_list_price field if price list or product not found then its set lst_price
        return: N/A
        """
        for product_id in self:
            pricelist_item_ids = self.env['product.pricelist.item'].search(
                [('product_id', '=', product_id.id)])
            if pricelist_item_ids:
                product_id.price_list_price = pricelist_item_ids[0].fixed_price
            else:
                product_id.price_list_price = product_id.lst_price

    price_list_price = fields.Float(string="Pricelist Price", compute='_compute_pricelist_price',
                                    help="price list price of the product if the multiple price list then its take "
                                         "first price list price",
                                    default="0.0")
