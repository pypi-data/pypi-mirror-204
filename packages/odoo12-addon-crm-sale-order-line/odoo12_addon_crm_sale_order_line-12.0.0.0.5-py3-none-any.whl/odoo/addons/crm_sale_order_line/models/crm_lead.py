from odoo import api, fields, models
from odoo.tools.translate import _
from odoo import exceptions


class CrmLead(models.Model):
    _inherit = "crm.lead"

    crm_order_line_ids = fields.One2many(
        "crm.sale.order.line",
        string=_("Order lines"),
        inverse_name="crm_lead_id"
    )
    has_order_lines = fields.Boolean(
        string=_("Has order lines"), compute="_get_has_order_lines", store=False)

    # TODO: create a method to pupulate related_partner from lead
    # If no partner found we might need to create one.
    @api.depends("crm_order_line_ids")
    def _get_has_order_lines(self):
        if self.crm_order_line_ids:
            self.has_order_lines = True
        else:
            self.has_order_lines = False

    def create_quotation_from_order_line_action(self):
        self._validate_create_quotation_from_order_line()
        view_id = self._create_quotation_from_order_line()
        return view_id

    def _validate_create_quotation_from_order_line(self):
        if not self.partner_id:
            raise exceptions.ValidationError(
                _("Client must be defined")
            )
        if not self.crm_order_line_ids:
            raise exceptions.ValidationError(
                _("Can't create quotation without order lines selected")
            )

    def _create_quotation_from_order_line(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id
        })
        for crm_order_line in self.crm_order_line_ids:
            self._generate_so_order_line(sale_order, crm_order_line)
        self.action_set_won_rainbowman()
        return {
            'name': _('Quotation'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('sale.view_order_form').id,
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'self'
        }

    def _generate_so_order_line(self, sale_order, crm_order_line):
        creation_data = self._get_base_so_order_line_creation_data(
            sale_order, crm_order_line)
        self.env['sale.order.line'].create(
            creation_data
        )

    def _get_base_so_order_line_creation_data(
        self,
        sale_order,
        crm_order_line
    ):
        creation_data = {
            'product_id': crm_order_line.product_id.id,
            'order_id': sale_order.id
        }
        if crm_order_line.price_unit > 0:
            creation_data['price_unit'] = crm_order_line.price_unit
        return creation_data
