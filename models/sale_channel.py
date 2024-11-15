from odoo import tools
from odoo import fields, models, api, _

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Canales de venta'
    _inherit = ['mail.thread', 'mail.activity.mixin']                                           #con estos mixins heredo funcionalidades de mensajeria y actividades para habilitar el chatter


    name = fields.Char(string="Name", requerid=True, tracking=True)                             #habilito el seguimiento del campo para registros de cambios en el chatter
    code = fields.Char(string="Code", default=lambda self: _('New'))
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse")
    journal_id = fields.Many2one(comodel_name="account.journal")



    #  creo el codigo para la secuencia de de code
    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'sale.channel') or _('New')
        res = super(SaleChannel, self).create(vals)
        return res