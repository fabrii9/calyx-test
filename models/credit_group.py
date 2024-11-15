from odoo import tools
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class CreditGroup(models.Model):
    _name = 'credit.group'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code", required=True)
    sale_channel_id = fields.Many2one(comodel_name="sale.channel", required=True)
    global_credit = fields.Integer(string="Global credit", required=True)
    used_credit = fields.Integer(string="Used credit", compute="_get_used_credit")
    available_credit = fields.Integer(string="Available credit", compute="_get_available_credit")

    def _get_used_credit(self):
        for rec in self:
            used_credit = 0
            #  busco los clientes que estén agregados a este grupo de crédito
            partners = rec.env['res.partner'].search([('credit_groups_ids', 'in', (rec.id))])
            if partners:
                partner_ids = []
                for partner in partners:
                    partner_ids.append(partner.id)
                #  obtengo las ordenes de venta que tengan asignado un grupo de crédito
                sale_order_list = rec.env['sale.order'].search([('partner_id', 'in', tuple(partner_ids)), 
                                            ('state', 'in', ('sale', 'done')), 
                                            ('invoice_status', 'in', ('to invoice', 'no')),
                                            ('credit_group_id', '=', rec.id)])
                #  obtengo las facturas de venta que tengan asignado un grupo de crédito
                invoices = rec.env['account.move'].search([('partner_id', 'in', tuple(partner_ids)), 
                                                                 ('state', '=', 'posted'), 
                                                                 ('move_type', '=', 'out_invoice'), 
                                                                 ('payment_state', '=', 'not_paid'),
                                                                 ('credit_group_id', '=', rec.id)])
                #  faltaría conseguir aquellas que estén parcialmente pagadas
                for order in sale_order_list:
                    used_credit += order.amount_total
                for invoice in invoices:
                    used_credit += invoice.amount_total
                rec.used_credit = used_credit
            else:
                rec.used_credit = 0

    def _get_available_credit(self):
        for rec in self:
            rec.available_credit = rec.global_credit - rec.used_credit

    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if '026' in record.code:
                raise ValidationError("El codigo no puede contener la secuencia '026'.")