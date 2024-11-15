# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_channel_id = fields.Many2one(comodel_name="sale.channel", string="Sale Channel", requerid=True)
    credit_state = fields.Selection([('no_limit', 'Without credit limit'), ('available_credit', 'Available credit'),
                                    ('blocked_credit', 'Blocked credit'),], default="no_limit", compute="_get_credit_state")
    credit_group_id = fields.Many2one(comodel_name="credit.group", string="Credit group")

    #  Genero un domain dinamico para el grupo de crédito que se va a usar
    @api.onchange('partner_id', 'sale_channel_id')
    def _get_domain_credit_group(self):
        if self.partner_id and self.sale_channel_id and self.partner_id.credit_groups_ids:
            credit_groups_ids = []
            for credit_group in self.partner_id.credit_groups_ids:
                if credit_group.sale_channel_id == self.sale_channel_id and credit_group.available_credit > 0:
                    credit_groups_ids.append(credit_group.id)
            #  Si ningún grupo tiene crédito disponible lanzo una excepción
            if not credit_groups_ids:
                raise UserError (_('This partner does not have available credit with this sales channel.'))
            #  Hago que se muestren solo los grupos de crédito que tengan crédito disponible
            return {'domain': {'credit_group_id': [('id', 'in', tuple(credit_groups_ids))]}}

    @api.depends('partner_id', 'sale_channel_id', 'credit_group_id')
    def _get_credit_state(self):
        #  inicio el estado como no_limit
        self.credit_state = "no_limit"
        if self.partner_id and self.partner_id.credit_groups_ids and self.sale_channel_id and self.credit_group_id:
            #  si ya selecciono cliente, canal de venta y el cliente tiene grupos de crédito analizo los otros estados
            if self.credit_group_id.available_credit > 0:
                self.credit_state = "available_credit"
            else: 
                self.credit_state = "blocked_credit"

    @api.onchange('sale_channel_id')
    def _change_warehouse(self):
        self.warehouse_id = self.sale_channel_id.warehouse_id

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        #  agrego el diario correspondiente a la factura
        res['journal_id'] = self.sale_channel_id.journal_id.id
        #  agrego el canal de venta correspondiente
        res['sale_channel_id'] = self.sale_channel_id.id
        if self.credit_group_id:
            #  le asigno un grupo de crédito al cual descontar
            res['credit_group_id'] = self.credit_group_id.id
        return res
    