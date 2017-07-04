# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import except_orm

class Project(models.Model):
    _name = 'qj.project'
    _description = "QJ - Project"
    
    name = fields.Char(string="Name",required=True)
    area = fields.Text("Area")
    number_of_portfolio= fields.Integer("Number of Portfolio")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    state = fields.Selection([('New', 'New'),
                            ('In Progress', 'In Progress'),
                            ('Done', 'Done'),
                            ('Cancel', 'Cancel'),], string="Status", default="New")
   
    product_ids=fields.Many2many('product.product', 'prod_project_rel', 'name', 'project_id', string="Product")
    
    # methods:
    # Status bar methods:
    @api.one
    def set_new(self):
        self.state = 'New'
        
    @api.one
    def set_in_progress(self):
        self.state = 'In Progress'
         
    @api.one
    def set_done(self):
        self.state = 'Done' 
         
    @api.one
    def set_cancel(self):
        self.state = 'Cancel' 
         
    
    #don't allow to delete if status not new
    @api.multi
    def unlink(self):
        for record in self: 
            if record.state not in ['New']:
                raise except_orm('Error!', 'You can delete only projects in new status!')
        return super(Project, self).unlink() 
         