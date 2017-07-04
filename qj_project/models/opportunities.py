from openerp import models, fields, api

class ProductTemplate(models.Model):

    _inherit = 'crm.lead'

    product_ids=fields.Many2many('product.product', string="Product")
    
    
class crm_lead_sale(models.Model):
    _inherit = "crm.make.sale"
    
    def makeOrder(self, cr, uid, ids, context=None):
        # To Review
        res = super(crm_lead_sale,self).makeOrder(cr, uid, ids, context=context)
        # to send common field from lead/oppo to sale order/quotation
        sale_obj = self.pool.get(res['res_model'])
        if context.get('active_model') and context.get('active_ids', []):
            lead_oppo = self.pool.get('crm.lead').browse(cr ,uid ,context.get('active_ids'))[0]
            if lead_oppo.product_ids:
                lines = []
                for line in lead_oppo.product_ids:
                    lines.append((0,0, {'product_id': line.id,
                                        'name': line.name,
                                        'price_unit': line.list_price}))
                if type(res['res_id']) is int:
                    sale_obj.write(cr ,uid ,res['res_id'] ,{'order_line':lines})
        return res