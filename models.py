# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
import random
import logging
from openerp.osv.fields import related


_logger = logging.getLogger(__name__)

class WorkOrder(models.Model):
    """Represents a work order issues by a customer """
    _name = 'inspection_tech.work_order'
    
    def _getFirstState(self):
        return self._getStateValues()[0][0]

    name = fields.Char(required = True,
                        size = 64, 
                        string = "Work Order",
                        index = True,
                        help = "Work Order Name",
                        readonly = True,
                        states={'draft': [('readonly', False)], 'inprocess': [('readonly', False)]})
    purchase_order = fields.Char(size = 64,
                                string = "Purchase Order",
                                index = True,
                                help="Referring Purchase Order",
                                readonly = True,
                                states={'draft': [('readonly', False)], 
                                        'inprocess': [('readonly', False)]})
    date = fields.Date(string = "Date",
                        default = fields.Date.today,
                        index = True,
                        help="Order Date",
                        readonly = True,
                        states={'draft': [('readonly', False)], 
                                'inprocess': [('readonly', False)]})
    source = fields.Char(size = 64,
                          string = "Source Document",
                          help="Source Document",
                          readonly = True,
                          states={'draft': [('readonly', False)], 
                                  'inprocess': [('readonly', False)]})
    accepted_by = fields.Char(size = 64, 
                        string = "Accepted By (Customer)",
                        help = "The name of the customer who accepted the order",
                        readonly = True,
                        states={'draft': [('readonly', False)], 
                                'inprocess': [('readonly', False)]})
    # labor_total = fields.Float(string = "Total Labor (h)",
    #                            help = "Total labor in hours",
    #                            compute = "_getTotalLabor")
    state = fields.Selection([('draft', 'Draft'),
                                       ('inprocess', 'In Process'),
                                       ('task_completed', 'Task(s) Completed'),
                                       ('done', 'Done')], 
                              required=True,
                              readonly = True,
                              default = 'draft')
    descr = fields.Text(string = "Description",
                        help = "Description of the work order",
                        readonly = True,
                        states={'draft': [('readonly', False)], 
                                'inprocess': [('readonly', False)]})
    customer = fields.Many2one('res.partner',
                                string="Customer", 
                                index=True,
                                ondelete='set null',
                                readonly = True,
                                states={'draft': [('readonly', False)], 
                                        'inprocess': [('readonly', False)]})

    task_ids = fields.One2many('inspection_tech.work_order_task',
                               inverse_name = "wo_id",
                               copy=True,
                               string = 'Tasks')
    
    def _getTotalLabor(self):
        """ functions for the default values """
        for record in self:
            record.name = str(random.randint(1, 1e6))
     
    def _getStateValues(self, *ar, **args):
        print("TZ: models.py _getStateValue.args: ", args)
        print("TZ: models.py _getStateValue.ar: ", ar)
        return [('draft', 'Draft'),
               ('inprocess', 'In Process'),
               ('task_completed', 'Task(s) Completed'),
               ('done', 'Done'),
               ('cancel', 'Cancelled'),]
        
class work_order_task_spec(models.Model):
    """Stores the equipment specifications as of the time of creating the task.
    This data is task specific (hence the many2one to WO task). 
    """
    
    _name = "inspection_tech.wo.task.spec"
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Specification",
                        index = True,
                        help = "The name of the specification attribute")
    
    spec_value = fields.Char(required = True,
                        size = 64, 
                        string = "Value",
                        index = True,
                        help = "Specification Value",
                        readonly = False)
    order_no = fields.Integer(string = "Order",
                              help = "The order in which the values appear",
                              required=True)
    task_id = fields.Many2one("inspection_tech.work_order_task",
                                        string = 'Task ID',
                                        ondelete='cascade',
                                        select = True, 
                                        required=True)
    
class work_order_task_point(models.Model):
    """Stores the equipment inspection points as of the time of creating the task.
    This data is task specific (hence the many2one to WO task). 
    """
    
    _name = "inspection_tech.wo.task.point"
    
    @api.one
    @api.depends('image')
    def _g_image(self):
        self.image_small = tools.image_get_resized_images(
                                    self.image, 
                                    avoid_resize_medium=True)['image_small']
        _logger.debug("tz: get image executed")
    
    @api.one
    def _s_image(self):
        #self.update({'image': tools.image_resize_image_big(self.image_small)})
        self.image = tools.image_resize_image_big(self.image_small)
    
    
    task_id = fields.Many2one('inspection_tech.work_order_task',
                            string = 'Task',
                            ondelete='cascade',
                            select = True, 
                            required=True,
                            readonly = True)
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Inspection Point",
                        index = True,
                        help = "Inspection Point Name")
    
    point_value = fields.Many2one('inspection_tech.inspection_result.type', 
                                  string = 'Result',
                                  help = "Inspection Point Result")
    
    point_comment = fields.Char(string = 'Comment', 
                                size=128,
                                help = "Provide comment")
    
    order_no = fields.Integer(string = "Order",
                              help = "The order in which the values appear",
                              required=True)
    
    image = fields.Binary(string = "Image",
                          help="Holds the photo of inspection point")
    
    image_small = fields.Binary(string = "Photo",
                                compute = "_g_image",
                                inverse = "_s_image")
                                

class work_order_task(models.Model):
    """Represent a task in the Work Order. A task can be of type:
    - service - for general equipment service activities
    - inspection - for equipment inspection reports"""
    
    _name = "inspection_tech.work_order_task"
    
    TASK_TYPES = [('service', 'Service'),
                  ('inspection', 'Inspection')]
    
    wo_id = fields.Many2one('inspection_tech.work_order',
                            string = 'Work Oder',
                            ondelete='cascade',
                            select = True, 
                            required=True,
                            readonly = True,
                            states={'draft': [('readonly', False)]})
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Task",
                        index = True,
                        help = "Enter Task Name")
    
    task_type = fields.Selection(TASK_TYPES,
                                string = "Type",
                                index = True,
                                help="Task Type",
                                readonly = True,
                                states={'draft': [('readonly', False)], 
                                        'inprocess': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                               ('inprocess', 'In Process'),
                               ('done', 'Done')], 
                              required=True,
                              readonly = True,
                              default = 'draft')
    
    descr = fields.Char(string = "Description",
                        size = 128,
                        help = "Short Task Decription",
                        readonly = True,
                        states={'draft': [('readonly', False)], 
                                'inprocess': [('readonly', False)]})
    
    compl_date = fields.Date(string = "Completion",
                        help="Order Date",
                        readonly = True,
                        states={'draft': [('readonly', False)], 
                                'inprocess': [('readonly', False)]})
    
    inspector =  fields.Many2one('hr.employee', 
                                 string='Performed By', 
                                 select=True)
    
    notes = fields.Text(string = "Notes",
                        help = "Notes",
                        readonly = True,
                        states={'draft': [('readonly', False)], 
                                'inprocess': [('readonly', False)]})
    
    equipment_customer_id = fields.Many2one('inspection_tech.equipment',
                            string = 'Certification', 
                            required=True,
                            readonly = True,
                            states={'draft': [('readonly', False)]})
    
    inspection_line = fields.One2many('inspection_tech.wo.task.point',
                               inverse_name = "task_id",
                               copy=True,
                               string = 'Inspection Points')
    
    spec_line = fields.One2many("inspection_tech.wo.task.spec",
                                string = "Specification Lines" ,
                                inverse_name ='task_id',
                                copy=True,
                                readonly = True,
                                states={'draft': [('readonly', False)]})
    
    
    @api.onchange('task_type', 'wo_id') 
    def _onchange_name(self):
        """compute the name of the task from the task type and wo id.
        The computed name starts with the task type followed by '(<wo id>)'.
        If the name follows a different pattern (say changed by the user) it 
        will not be recalculated. 
        """
        if self.task_type and self.wo_id.name: 
            woid_suffix = " ({})".format(self.wo_id.name)
            if (self.name and self.name.endswith(woid_suffix)) or (not self.name):
                self.name = "{}{}".format(dict(self.TASK_TYPES).get(self.task_type), 
                                           woid_suffix)
    @api.onchange('equipment_customer_id') 
    def _onchange_equipment(self):
        """Upon change of the equipment, regenerate the specification lines and
        the inspection points."""
        specification_ids =[]
        point_ids = []
        #generate the specification lines  
        for val in self.equipment_customer_id.equip_specification_line:
            specs = {
                          'name': val.name,
                          'spec_value': val.spec_value,
                          'order_no': val.order_no,                             
                    }
            specification_ids += [specs]
        self.update({'spec_line': specification_ids}) #specs updated
        # generate the inspection points
        for val in self.equipment_customer_id.equipment_type_id.inspection_line:
            point = {
                          'name': val.name,
                          'order_no': val.order_no,                             
                    }
            point_ids += [point]
        self.update({'inspection_line': point_ids}) #specs updated
        #log some data - to be deleted
        _logger.info("[TZ]: points_id='%s'" % str(point_ids))
        for spec in self.spec_line:
            _logger.warning("[TZ] spec line: name='{0}' order_no='{1}'".format(
                                            str(spec.name), str(spec.order_no)))
        
    
    def create(self, cr, uid, values, context=None):
        return super(work_order_task, self).create(cr, uid, values, context=context)
    
    @api.multi
    def write(self, vals):
        _logger.warning("[TZ] write spec line '{0}'".format(
                                            str(self.spec_line)))
        for spec in self.spec_line:
            _logger.warning("[TZ] write spec line: name='{0}' order_no='{1}'".format(
                                            str(spec.name), str(spec.order_no)))
        return models.Model.write(self, vals)
    
