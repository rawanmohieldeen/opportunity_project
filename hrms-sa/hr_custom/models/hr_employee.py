# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class Employees(models.Model):
    _inherit = 'hr.employee'

    cpr_no = fields.Char('CPR No.')


class Contract(models.Model):
    _inherit = 'hr.contract'

    probation_wage = fields.Char('Probation Period Wage')