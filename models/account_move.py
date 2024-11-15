# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_channel_id = fields.Many2one(comodel_name="sale.channel", string="Sale Channel")
    credit_group_id = fields.Many2one(comodel_name="credit.group", string="Credit group")