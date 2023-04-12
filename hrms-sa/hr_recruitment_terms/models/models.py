# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class HRRecruitmentTerms(models.Model):
    _name = 'hr.recruitment.terms'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin', 'utm.mixin']
    _description = 'HR Recruitment Terms and Condition'
   

    name = fields.Char(copy=False, readonly=False, index=True)
    date = fields.Date('Date',readonly=False,default=datetime.now())
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the terms without removing it.")
    terms_conditions = fields.Html('Terms and Condition')


