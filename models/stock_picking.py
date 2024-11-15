# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_channel_id = fields.Many2one(comodel_name="sale.channel", string="Sale Channel")
