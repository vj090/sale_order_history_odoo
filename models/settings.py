from odoo import models, fields, api

class PurchasdeSettingExt(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'This is the settings defined for the module my_mod'

    # counting = fields.Integer(string="Enter Count")
    counting_ch = fields.Char(string="Enter Count_ch")
    counting_in = fields.Integer(string="Enter Count_ch")
    # sample_ch = fields.Char(string="Enter Count")

    # This is the get param and set param for the transient model:
    def set_values(self):
        res = super(PurchasdeSettingExt, self).set_values()
        self.env['ir.config_parameter'].set_param('sale_history.counting_in', self.counting_in)
        self.env['sale.order'].search([]).write({'c_limit':self.counting_in})
        return res

    @api.model
    def get_values(self):
        res = super(PurchasdeSettingExt, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        # notes = ICPSudo.get_param('sale_history.counting_in')
        res.update(
            counting_in=int(ICPSudo.get_param('sale_history.counting_in', default=4)),
        )
        return res

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     ICPSudo = self.env['ir.config_parameter'].sudo()
    #     res.update(
    #         default_quote_valid_to=int(ICPSudo.get_param('quote.default_quote_valid_to', default=30)),
    #     )
    #     return res
