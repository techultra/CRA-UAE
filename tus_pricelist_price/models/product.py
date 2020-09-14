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
                [('product_tmpl_id', '=', product_tmpl_id.id), ('min_quantity', '=', 0), ('date_start', '=', False),
                 ('date_end', '=', False), ('applied_on', '=', '1_product')])
            if pricelist_item_ids:
                product_tmpl_id.price_list_price = pricelist_item_ids[0].fixed_price
            else:
                product_tmpl_id.price_list_price = 0.0

    price_list_price = fields.Float(string="Public Selling Price", compute='_compute_pricelist_price',
                                    help="price list price of the product")
    product_landed_cost = fields.Float(string="Average Landed Cost", related='product_variant_ids.product_landed_cost',
                                       help="Average landed cost base on sum of all landed cost dived by the current stock")

    def set_or_create_pricelist_item(self, price_list_price, obj, tmpl=False, variant=False):
        """
        Author:Bhavesh Jadav TechUltra solutions
        :param price_list_price:USe for the public price list
        :param obj:use for the product or template object
        :param tmpl:use if call for template
        :param variant:use for call for variant
        :return:True
        """
        domain = [('min_quantity', '=', 0), ('date_start', '=', False),
                  ('date_end', '=', False)]
        if tmpl:
            domain.append(('applied_on', '=', '1_product'))
            domain.append(('product_id', '=', False))
            domain.append(('product_tmpl_id', '=', obj.id))
        elif variant:
            domain.append(('applied_on', '=', '0_product_variant'))
            domain.append(('product_id', '=', obj.id))
            domain.append((('product_tmpl_id', '=', obj.product_tmpl_id.id)))
        pricelist_item_ids = self.env['product.pricelist.item'].search(domain)
        if pricelist_item_ids:
            pricelist_item_ids[0].fixed_price = price_list_price
        else:
            pricelist_ids = self.env['product.pricelist'].search([])
            if pricelist_ids:
                pricelist_item_vals = {'pricelist_id': pricelist_ids[0].id,
                                       'min_quantity': 0,
                                       'date_start': False,
                                       'date_end': False,
                                       'categ_id': False,
                                       'fixed_price': price_list_price}
                if tmpl:
                    pricelist_item_vals.update(
                        {'product_id': False, 'applied_on': '1_product', 'product_tmpl_id': obj.id})
                elif variant:
                    pricelist_item_vals.update(
                        {'product_id': obj.id, 'applied_on': '0_product_variant',
                         'product_tmpl_id': obj.product_tmpl_id.id})
                pricelist_item_id = self.env['product.pricelist.item'].create(pricelist_item_vals)
        return True

    def write(self, vals):
        """
        Author: Bhavesh Jadav TechUltra solutions
        Date:11/07/2020
        Func: this method use for thr create price list item record if its not otherwise its update first record
        :param vals: use for the product template vals
        :return:result of super method
        """
        if vals.get('price_list_price'):
            self.set_or_create_pricelist_item(price_list_price=vals.get('price_list_price'), obj=self, tmpl=True,
                                              variant=False)
        res = super(ProductTemplate, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        """
        Author: Bhavesh Jadav TechUltra solutions
        Date:11/07/2020
        Func: this method use for thr create price list item record if its not otherwise its update first record
        :param vals: use for the create vals
        :return: result
        """
        res = super(ProductTemplate, self).create(vals)
        if vals.get('price_list_price') and float(vals.get('price_list_price')) > 0:
            self.set_or_create_pricelist_item(price_list_price=vals.get('price_list_price'), obj=res, tmpl=True,
                                              variant=False)
        return res


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
                [('product_id', '=', product_id.id), ('min_quantity', '=', 0), ('date_start', '=', False),
                 ('date_end', '=', False), ('applied_on', '=', '0_product_variant')])
            if pricelist_item_ids:
                product_id.price_list_price = pricelist_item_ids[0].fixed_price
            else:
                product_id.price_list_price = 0.0

    def _compute_product_landed_cost(self):
        """
        Author:Bhavesh Jadav TechUltra Solutions
        Date:08/07/2020
        func:Calculate landed cost base on the landed cost record
        :return:N/A
        """
        for product_id in self:
            landed_cost_lines = self.env['stock.valuation.adjustment.lines'].search(
                [('product_id', '=', product_id.id)])

            posted_landed_cost_lines = landed_cost_lines and landed_cost_lines.filtered(
                lambda l: l.cost_id.state == 'done')
            try:
                product_id.product_landed_cost = sum(posted_landed_cost_lines.mapped('additional_landed_cost')) / (
                        product_id.qty_available - product_id.outgoing_qty)
            except:
                product_id.product_landed_cost = 0.0

    price_list_price = fields.Float(string="Public Selling Price", compute='_compute_pricelist_price',
                                    help="price list price of the product if the multiple price list then its take "
                                         "first price list price",
                                    default="0.0")
    product_landed_cost = fields.Float(string="Average Landed Cost", compute='_compute_product_landed_cost',
                                       help="Average landed cost base on sum of all landed cost dived by the current stock",
                                       default="0.0")
    quantity_sellable = fields.Float(string="Quantity Sellable", compute='_compute_quantity_sellable')
    quantity_incoming = fields.Float(string="Incoming Quantity", compute='_compute_quantity_incoming')

    def _compute_quantity_sellable(self):
        for rec in self:
            rec.quantity_sellable = rec.qty_available - rec.outgoing_qty

    def _compute_quantity_incoming(self):
        for rec in self:
            rec.quantity_incoming = rec.incoming_qty

    @api.model
    def create(self, vals):
        """
        Author: Bhavesh Jadav TechUltra solutions
        Date:11/07/2020
        Func: this method use for thr create price list item record if its not otherwise its update first record
        :param vals: use for the create vals
        :return: result
        """
        res = super(ProductProduct, self).create(vals)
        if vals.get('price_list_price') and float(vals.get('price_list_price')) > 0:
            self.env['product.template'].set_or_create_pricelist_item(
                price_list_price=vals.get('price_list_price'), obj=res, tmpl=False, variant=True)
        return res

    def write(self, vals):
        """
        Author: Bhavesh Jadav TechUltra solutions
        Date:11/07/2020
        Func: this method use for thr create price list item record if its not otherwise its update first record
        :param vals: use for the product vals
        :return:result of super method
        """
        if vals.get('price_list_price'):
            self.env['product.template'].set_or_create_pricelist_item(
                price_list_price=vals.get('price_list_price'), obj=self, tmpl=False, variant=True)
        res = super(ProductProduct, self).write(vals)
        return res
