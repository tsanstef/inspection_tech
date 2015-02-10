'''
The Inspection Result Types module: 
what are the valid values for the inspection point result.

@author: Tzanko
'''
from openerp import models, fields, api
import random
import logging
from openerp.osv.fields import related
_logger = logging.getLogger(__name__)

class MyClass(models.Model):
    '''
    Inspection Point Result Type
    '''
    _name = "inspection_tech.inspection_result.type"

    name = fields.Char(required = True,
                        size = 64, 
                        string = "Inspection Result",
                        index = True,
                        help = "Inspection Result Value",
                        select = True)
    orderno = fields.Integer("Order")
    _order = 'orderno, id'
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Inspection Result type must be unique!'),
    ] 