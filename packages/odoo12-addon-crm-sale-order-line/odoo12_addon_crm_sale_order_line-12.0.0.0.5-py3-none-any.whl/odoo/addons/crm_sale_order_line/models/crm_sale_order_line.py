# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models
from odoo.tools.translate import _


class CrmSaleOrderLine(models.Model):
    _name = "crm.sale.order.line"

    crm_lead_id = fields.Many2one('crm.lead', string=_("Related lead"))
    product_id = fields.Many2one('product.product', string=_("Product"))
    price_unit = fields.Float(string="Price unit")
    partner_id = fields.Many2one(
        'res.partner',
        compute="_get_partner_id",
        store=False
    )

    @api.depends('crm_lead_id')
    def _get_partner_id(self):
        self.ensure_one()
        if self.crm_lead_id:
            self.partner_id = self.crm_lead_id.id

    @api.constrains('product_id')
    def _setup_default_price_unit(self):
        self.ensure_one()
        if self.product_id:
            if self.price_unit == 0:
                self.price_unit = self.product_id.lst_price

    @api.onchange('product_id')
    def _change_default_price_unit(self):
        for record in self:
            if record.product_id:
                record.price_unit = record.product_id.lst_price
