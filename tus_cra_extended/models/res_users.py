from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_menu_ids = fields.Many2many('ir.ui.menu', 'group_menu', 'menu_id', 'group_id', string="Hide Menu")

    @api.model
    def create(self, values):
        self.env['ir.ui.menu'].clear_caches()
        return super(ResUsers, self).create(values)

    def write(self, values):
        self.env['ir.ui.menu'].clear_caches()
        return super(ResUsers, self).write(values)


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user == self.env.ref('base.user_root'):
            return super(IrUiMenu, self).search(args, offset=0, limit=None, order=order, count=False)
        else:
            all_menus = super(IrUiMenu, self).search(args, offset=0, limit=None, order=order, count=False)
            if all_menus:
                menu_ids_to_rm = [menu for menu in self.env.user.group_menu_ids]
                for menu_rm in menu_ids_to_rm:
                    if menu_rm in all_menus:
                        all_menus -= menu_rm
                if limit:
                    all_menus = all_menus[:limit]
                if offset:
                    all_menus = all_menus[offset:]
            return len(all_menus) if count else all_menus