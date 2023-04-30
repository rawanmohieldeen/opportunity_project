# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class end_of_service(models.Model):
#     _name = 'end_of_service.end_of_service'
#     _description = 'end_of_service.end_of_service'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
