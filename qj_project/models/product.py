from openerp import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # Fields
    number = fields.Integer("Number")
    sqm = fields.Float("SQM")
    floor = fields.Integer("Floor")
    layout = fields.Binary("Layout")
    is_property = fields.Boolean("Is Property", default=False)
    state = fields.Selection([('Available', 'Available'),
                            ('Reserved', 'Reserved'),
                            ('Sold', 'Sold'),
                            ('Rent','Rent'),
                            ('Other', 'Other'),], string="Status", default="Available")
  
    project_id = fields.Many2one('qj.project', string='Project')
    
    @api.one
    def reserve_product(self):
        if self.state not in ['Rent','Sold']:
            if self.state == 'Reserved':
                self.state = "Available"
            else:
                self.state = "Reserved"

class Productproduct(models.Model):
    _inherit = 'product.product'
    
    @api.one
    def reserve_product(self):
        print self.state
        if self.state not in ['Rent','Sold']:
            if self.state == 'Reserved':
                self.state = "Available"
            else:
                self.state = "Reserved"
            
        