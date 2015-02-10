# -*- coding: utf-8 -*-
from openerp import fields, models, api

class Partner(models.Model):
    """Extends the standard partner object with inspection fields"""
    _inherit = 'res.partner'
    
    # add a list of related work orders
    wo_ids = fields.One2many('inspection_tech.work_order',
                             inverse_name = "customer",
                             limit = 10,
                             string="Work Orders", 
                             readonly=True)
    
    inspection_ids = fields.One2many('inspection_tech.work_order.task',
                             compute='_get_inspections',
                             string="Work Orders", 
                             readonly=True)

    @api.one
    @api.depends('wo_ids')
    def _get_inspections(self):
        self.inspection_ids = self.env['inspection_tech.work_order.task'].browse()
        for wo_id in self.wo_ids:
            for task in wo_id.task_ids:
                if task.task_type == 'inspection':
                    self.inspection_ids = self.inspection_ids + task
                    if len(self.inspection_ids) >= 10: 
                        return
                    
                    
            
             

    

