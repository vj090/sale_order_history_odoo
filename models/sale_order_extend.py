from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderHistory(models.Model):
    _inherit = 'sale.order'
    _description = "Extended sale.order and added History"

    all_order_hist = fields.Many2one('sale.order',string="added")
    all_order_hist_lien = fields.One2many('sale.order','all_order_hist',string="hist line")

    added_history_o = fields.One2many('sale.order.history','added_history_m',string="hist O2m")
    bool_field = fields.Boolean(string='Same text', default=False)

    c_limit = fields.Integer(string="Limit",store=True)

    # This is the function which write the data to sale order line
    @api.onchange('partner_id')
    def get_own_order_hist_line(self):
        orderr_line = [(5, 0, 0)]
        print("In function limit",self.c_limit)
        settings_partner = self.env['ir.config_parameter'].sudo().get_param('sale_history.counting_in')
        s = int(settings_partner)
        all_order = self.env['sale.order'].search([('partner_id.name','=',self.partner_id.name)],limit=s)
        for rec in all_order:
            print("Order id==>",rec)
            for lines in rec.order_line:
                print("order line ids==>",lines)
                # if lines.product_id.id in orderr_line:
                #     print("find duplicate")
                #     pass

                line = (0,0, {
                'product_id': rec.name,
                'name': lines.product_id.name,
                'description': lines.name,
                'product_qty': lines.product_uom_qty,
                'unit_price': lines.price_unit,
                'price_subtotal': lines.price_subtotal,
                })
                orderr_line.append(line)
                print("Appended list==>",orderr_line)
        self.write({'added_history_o': orderr_line})


    # 1st ==> Function which write all the history order to the sale order line(implemented a list method which append not existing record in the list )
    # def add_all_history(self):
    #     # self.bool_field = True
    #     orderr_line = []
    #     filtered_list = []
    #     # Get all record form the sale order line:
    #     get_curr_order_line = self.env['sale.order.line'].search([('order_id','=',self.id)])
    #     print("get_curr_order_line==>",get_curr_order_line)
    #     x = len(filtered_list)
    #
    #     for each in get_curr_order_line:
    #         x = len(filtered_list)
    #         print(each.name)
    #
    #         for rec in self.added_history_o:
    #             print("each x",x)
    #             # print(rec.description)
    #             if x == 0:
    #                 if each.name != rec.description:
    #                     filtered_list.append(rec)
    #                 print("filtered_list",filtered_list)
    #             else:
    #                 for a in filtered_list:
    #                     if each.name == a.description:
    #                         filtered_list.remove(a)

        # Now this filtered list having that element which is not in the already
        # print("Final not existing product:",filtered_list)
        # orderr_line = filtered_list
        # print("now append this",orderr_line)
        # get_pro_id = self.env['product.product'].search([('name', '=', rec.name)])
        # g_id = get_pro_id.id
        #
        # line = (0, 0, {
        #     'product_id': g_id,
        #     'name': rec.description,
        #     'product_uom_qty': rec.product_qty,
        #     'price_subtotal': rec.price_subtotal,
        # })
        # orderr_line.append(line)
        #
        # self.write({'order_line': orderr_line})

    # 2nd==> ?????????????(implemented a inner for loop which get the order line for each iteration of the history)
    def add_all_history(self):
        get_hist_list = self.env['sale.order.history'].search([('added_history_m','=',self.id)])
        print("get_hist_list=>",get_hist_list)

        for each in get_hist_list:
            print("curr Hist:============>",each.description)
            get_order_line = self.env['sale.order.line'].search([('order_id', '=', self.id)])
            print("updated order line==>", get_order_line)

            for l in get_order_line:
                print("curr line==>",l)
                if each.description == l.name and each.product_qty == l.product_uom_qty:
                    # print("Match found",each)
                    print("Match found==>")
                    break
            else:
                get_pro_id = self.env['product.product'].search([('name', '=', each.name)])
                g_id = get_pro_id.id

                vals = {
                    'product_id': g_id,
                    'order_id': self.id,
                    'name': each.description,
                    'product_uom_qty': each.product_qty,
                    'price_subtotal': each.price_subtotal,
                }
                print("vals", vals)
                self.env['sale.order.line'].create(vals)

            # Using write method to create record in sale order line:
            # else:
            #     print("No match found So Create this record")
            #     get_pro_id = self.env['product.product'].search([('name', '=', each.name)])
            #     g_id = get_pro_id.id
            #
            #     line = (0, 0, {
            #         'product_id': g_id,
            #         'name': each.description,
            #         'product_uom_qty': each.product_qty,
            #         'price_subtotal': each.price_subtotal,
            #     })
            #     orderr_line.append(line)
            #     print("final order line", orderr_line)
            #     self.write({'order_line': orderr_line})
            #     break


    # 3rd==>
    def test_config(self):
        self.bool_field = True
        get_order_line = self.env['sale.order.line'].search([('order_id', '=', self.id)])
        x = len(get_order_line)
        if x == 0:
            print("x===>",x)
            single_pro = self.env['sale.order.history'].search([('added_history_m', '=', self.id)])[0]
            print("get_hist_list=>", single_pro)
            get_pro_id = self.env['product.product'].search([('name', '=', single_pro.name)])
            g_id = get_pro_id.id

            vals = {
                'product_id': g_id,
                'order_id': self.id,
                'name': single_pro.description,
                'product_uom_qty': single_pro.product_qty,
                'price_subtotal': single_pro.price_subtotal,
            }
            print("vals", vals)
            self.env['sale.order.line'].create(vals)
        # ------
        get_hist_list = self.env['sale.order.history'].search([('added_history_m', '=', self.id)])
        print("get_hist_list=>", get_hist_list)

        for each in get_hist_list:
            print("curr Hist:============>", each.description)
            get_order_line = self.env['sale.order.line'].search([('order_id', '=', self.id)])
            print("updated order line==>", get_order_line)

            for l in get_order_line:
                print("curr line==>", l)
                if each.description == l.name and each.product_qty == l.product_uom_qty:
                    # print("Match found",each)
                    print("Match found==>")
                    break
            else:
                get_pro_id = self.env['product.product'].search([('name', '=', each.name)])
                g_id = get_pro_id.id

                vals = {
                    'product_id': g_id,
                    'order_id': self.id,
                    'name': each.description,
                    'product_uom_qty': each.product_qty,
                    'price_subtotal': each.price_subtotal,
                }
                print("vals", vals)
                self.env['sale.order.line'].create(vals)









# # Function which write all the history order to the sale order line
# def add_all_history(self):
#     self.bool_field = True
#     # print(self.added_history_o)
#     orderr_line = []
#     for rec in self.added_history_o:
#         print(rec.name)
#         get_pro_id = self.env['product.product'].search([('name', '=', rec.name)])
#         g_id = get_pro_id.id
#         # print("type",type(get_pro_id))
#
#         line = (0, 0, {
#             'product_id': g_id,
#             'name': rec.description,
#             'product_uom_qty': rec.product_qty,
#             'price_subtotal': rec.price_subtotal,
#         })
#         orderr_line.append(line)
#
#     self.write({'order_line': orderr_line})
