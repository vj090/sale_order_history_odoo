from odoo import models, fields, api, _

class SaleOrderLineExt(models.Model):
    _inherit = 'sale.order.line'


    added_histort_m = fields.Many2one('sale.order.history',string="line M2o")



