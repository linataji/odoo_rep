from openerp import models, fields, api, _
from openerp.exceptions import except_orm

class SaleOrder(models.Model):
    _inherit = 'sale.order'
  
    def action_button_confirm(self, cr, uid, ids, context=None):
        analytic_obj = self.pool.get('account.analytic.account')
        product_obj=self.pool.get('product.product')
        order = self.browse(cr, uid, ids)
        for line in order.order_line:
            if line.prod_state == 'Rent':
                # Create Analytic Account with product name
                vals = {'name': line.product_id.name, 
                        'rent_id': line.product_id.id,
                        'type': 'contract',
                        'partner_id': order.partner_id.id,
                        'recurring_invoices': True,
                        'sol_id': line.id,
                        'recurring_invoice_line_ids': [(0,0, {'product_id':line.product_id.id,
                                                              'name': line.name,
                                                              'quantity': line.product_uom_qty,
                                                              'uom_id': line.product_id.uom_id.id,
                                                              'price_unit': line.price_unit})]}
                analytic_obj.create(cr, uid, vals)
                product_obj.write(cr,uid, [line.product_id.id],{'state':'Rent'})
              
            if line.prod_state == 'Sale':
                product_obj.write(cr,uid, [line.product_id.id],{'state':'Sold'})   
                 
        res = super(SaleOrder, self).action_button_confirm(cr, uid, ids, context=context)
        return res
    
    
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    prod_state= fields.Selection([('Sale', 'Sale'),
                            ('Rent', 'Rent'),], string="Status")
    
    
    def open_project(self, cr, uid, ids, context=None):
        sol = self.browse(cr, uid, ids)[0]
        if sol.prod_state == 'Rent' and sol.product_id:
            project_ids = self.pool.get('account.analytic.account').search(cr, uid, [('sol_id','in',ids)])
            if project_ids:
                print self.pool.get('ir.model.data').get_object_reference(cr, uid, 'analytic', 'view_account_analytic_account_form')
                dummy, form_view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'analytic', 'view_account_analytic_account_form')
                dummy, tree_view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'view_account_analytic_account_tree')
                return {
                    'name': _('Product'),
                    'context': context,
                    'view_type': 'form',
                    "view_mode": 'tree,form',
                    'res_model': 'account.analytic.account',
                    'type': 'ir.actions.act_window',
                    'views': [(tree_view_id,'tree'),(form_view_id,'form')],
                    'domain': [('id', 'in', project_ids)],
                }
            else:
                raise except_orm('Error!', 'No project found!')
        else:
            raise except_orm('Error!', 'Only rented line have project!')
        
    
    
    
   