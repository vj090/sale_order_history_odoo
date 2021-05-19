from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderHistory(models.Model):
    _name = 'sale.order.history'

    name = fields.Char(string='Name')
    product_id = fields.Char(string='product_id')
    description = fields.Char(string='description')
    # product_id = fields.Char(related="added_history_m.name",string='product_id')
    product_qty = fields.Float(string='quantity')
    price_subtotal = fields.Float(string='Subtotal')
    unit_price = fields.Float(string='Unit price')

    added_history_m = fields.Many2one('sale.order', string="M2o sale history")

    def add_singe_line(self):
        print("Button pressed")
        print("Current record",self)
        print("Current Product Name=>",self.description)

        check_order_line = self.env['sale.order.line'].search([('order_id','=',self.added_history_m.id)])
        # print('check_order_line',check_order_line)
        z = len(check_order_line)

        # To enter the first record in order line without any matching
        if z == 0:
            print("First record")
            orderr_line = []
            get_pro_id = self.env['product.product'].search([('name', '=', self.name)])
            g_id = get_pro_id.id

            line = (0, 0, {
                'product_id': g_id,
                'name': self.description,
                'product_uom_qty': self.product_qty,
                'price_subtotal': self.price_subtotal,
            })
            orderr_line.append(line)

            s = self.env['sale.order'].search([('id', '=', self.added_history_m.id)])

            s.write({'order_line': orderr_line})
        else:
            for each in check_order_line:
                print("Existed Product Name=>",each.name)

                if self.description == each.name and self.product_qty == each.product_uom_qty:
                    print("Already existed record")
                    return False

            orderr_line = []

            # This orm will give the current product id
            get_pro_id = self.env['product.product'].search([('name', '=', self.name)])
            g_id = get_pro_id.id

            line = (0, 0, {
                'product_id': g_id,
                'name': self.description,
                'product_uom_qty': self.product_qty,
                'price_subtotal': self.price_subtotal,
            })
            orderr_line.append(line)

            s = self.env['sale.order'].search([('id', '=', self.added_history_m.id)])

            s.write({'order_line': orderr_line})


    # This is the custom delete method
    def delete_singe_line(self):
        to_delete = self.env['sale.order.history'].search([('id', '=', self.id)]).unlink()

"""
# Working code which also show that the record is already existed 



    def add_singe_line(self):
        # print("Current record",self)
        print("Current Product Name=>",self.description)
        print("id",self.product_id)
        # print("id",self.id)

        orderr_line = []

        # ?????
        # if self.product_id in orderr_line:
        #     print("find duplicate")
        # print("line",orderr_line)
        # for rec in self.added_history_o:
        #     print(rec.name)

        # This orm will give the current product id
        get_pro_id = self.env['product.product'].search([('name','=', self.name)])
        g_id = get_pro_id.id

        # ??????
        # To get the same order line to match the product is already exist or not
        check_order_line = self.env['sale.order.line'].search([('order_id','=',self.added_history_m.id)])
        for each in check_order_line:
            print("Existed Product Name=>",each.name)
            # print("Existed Product id=>",each.id)
            if self.description == each.name:
                print("Already existed record")


        line = (0, 0, {
            'product_id': g_id,
            'name': self.description,
            'product_uom_qty': self.product_qty,
            'price_subtotal': self.price_subtotal,
        })
        orderr_line.append(line)
        print("Final orderr line==>",orderr_line)



        # s = self.env['sale.order.line'].search([('self.order_line','',self.added_history_m)])
        # s = self.env['sale.order.line'].search([('order_id.id','=',self.added_history_m.id)])
        s = self.env['sale.order'].search([('id','=',self.added_history_m.id)])

        s.write({'order_line': orderr_line})





"""