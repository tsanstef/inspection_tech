# -*- coding: utf-8 -*-
from openerp import models, fields, api
import random
import logging

_logger = logging.getLogger(__name__)

class EquipmentSpec(models.Model):
    '''
    Each equipment has a list of specifications. 
    '''
    _name = "inspection_tech.equipment_spec"
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Specification Name",
                        index = True,
                        help = "Specification Name",
                        readonly = False)
    equipment_type_id = fields.Many2one("inspection_tech.equipment_type",
                                        string = 'Equipment Type',
                                        ondelete='cascade',
                                        select = True, 
                                        required=True)
    order_no = fields.Integer(string = "Order",
                              help = "The order in which the values appear",
                              required=True)
    
    _order = "order_no, id"
    
class InspectionPoint(models.Model):
    '''
    Each equipment has a list of specifications. 
    '''
    _name = "inspection_tech.inspection_point"
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Inspection Point Name",
                        index = True,
                        help = "Inspection Point Name",
                        readonly = False)
    point_header = fields.Boolean(string = "Header",
                                  help = "Is this a header?",
                                  default = False)
    
    equipment_type_id = fields.Many2one("inspection_tech.equipment_type",
                                        string = 'Equipment Type',
                                        ondelete='cascade',
                                        select = True, 
                                        required=True)
    order_no = fields.Integer(string = "Order",
                              help = "The order in which the values appear",
                              required=True)
    
    _order = "order_no, id"
    
class EquipmentType(models.Model):
    '''
    Capture the specifications of an equipment type
    '''
    _name = "inspection_tech.equipment_type"
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Equipment Type",
                        index = True,
                        help = "Equipment Type Name",
                        readonly = False)
    specification_line = fields.One2many('inspection_tech.equipment_spec',
                                inverse_name="equipment_type_id",         
                                string="Specifications",
                                copy=True)
    inspection_line = fields.One2many('inspection_tech.inspection_point',
                                inverse_name="equipment_type_id",         
                                string="Inspection Points",
                                copy=True)
    
    
class Equipment(models.Model):
    '''
    An equipment instance (assigned to a customer) of a given equipment type
    '''
    _name = "inspection_tech.equipment"
    
    name = fields.Char(required = True,
                        size = 64, 
                        string = "Equipment",
                        index = True,
                        help = "Equipment Name",
                        readonly = False)
    
    equipment_type_id = fields.Many2one("inspection_tech.equipment_type",
                                        string = 'Equipment Type',
                                        ondelete='cascade',
                                        index = True,
                                        select = True, 
                                        required=True)
    partner_id = fields.Many2one("res.partner",
                                        string = 'Customer',
                                        index = True,
                                        select = True, 
                                        required=True)
    photo = fields.Binary(string = "Picture",
                          help = "Upload a photo")
    notes = fields.Text(string = "Notes", 
                        help = "Enter notes about the equipment")
    equip_specification_line = fields.One2many('inspection_tech.equipment.specification',
                                inverse_name="equipment_id",         
                                string="Specifications",
                                copy=True)
    
    # onchange handler
    @api.onchange('equipment_type_id')
    def onchange_equipment_type_id(self):
        """ Recalculate the specification lines"""
        specification_ids =[]   
        for val in self.equipment_type_id.specification_line:
            specs = {
                          'name': val.name,
                          'order_no': val.order_no,                             
                    }
            specification_ids += [specs]
        self.update({'equip_specification_line': specification_ids})
        _logger.info("[TZ]: specification_ids='%s'" % str(specification_ids))
        for spec in self.equip_specification_line:
            _logger.warning("[TZ] spec line: name='{0}' order_no='{1}'".format(
                                            str(spec.name), str(spec.order_no)))
    
class EquipmentSpecification(models.Model):
    _name = 'inspection_tech.equipment.specification'

    name = fields.Char(required = True,
                        size = 64, 
                        string = "Specification",
                        index = True,
                        help = "Specification Name",
                        readonly = False)
    equipment_id = fields.Many2one("inspection_tech.equipment",
                                        string = 'Equipment',
                                        ondelete='cascade',
                                        select = True, 
                                        required=True)
    spec_value = fields.Char(required = True,
                        size = 64, 
                        string = "Value",
                        index = True,
                        help = "Specification Value",
                        readonly = False)
    order_no = fields.Integer(string = "Order",
                              help = "The order in which the values appear",
                              required=True)
    
    _order = "order_no, id"