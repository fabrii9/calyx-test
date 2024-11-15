# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_credit_control = fields.Boolean(string="Has credit control?")
    credit_groups_ids = fields.Many2many(comodel_name="credit.group", string="Credit groups")
