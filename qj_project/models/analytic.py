from openerp import models, fields, api

class analytic(models.Model):
    _inherit = 'account.analytic.account'

    rent_id = fields.Many2one('product.product', string="Product")
    sol_id = fields.Many2one('sale.order.line', string="SOL")
    
    def set_close(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        analytic_account = self.browse(cr, uid, ids)
        if analytic_account.rent_id:
            product_obj.write(cr,uid, [analytic_account.rent_id.id],{'state':'Available'})   
        res = super(analytic, self).set_close(cr, uid, ids, context=context)
        return res

    def set_cancel(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        analytic_account = self.browse(cr, uid, ids)
        if analytic_account.rent_id:
            product_obj.write(cr,uid, [analytic_account.rent_id.id],{'state':'Available'}) 
        res = super(analytic, self).set_cancel(cr, uid, ids, context=context)
        return res

    def set_open(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        analytic_account = self.browse(cr, uid, ids)
        if analytic_account.rent_id:
            product_obj.write(cr,uid, [analytic_account.rent_id.id],{'state':'Rent'}) 
        res = super(analytic, self).set_open(cr, uid, ids, context=context)
        return res