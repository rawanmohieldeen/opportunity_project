# -*- coding: utf-8 -*-
################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2021-TODAY Cybrosys Technologies (<https://www.cybrosys.com>)
#    Author: Hajaj Roshan(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import timedelta
from odoo import models, fields, _, api

GENDER_SELECTION = [('male', 'Male'),
                    ('female', 'Female'),
                    ('other', 'Other')]


class HrEmployeeFamilyInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.family'
    _description = 'HR Employee Family'

    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)
    #relation_id = fields.Many2one('hr.employee.relation', string="Relation", help="Relationship with the employee")
    relation_id = fields.Selection([('wife', 'Wife'), ('son', 'Son'), ('daughter', 'Daughter')], string="Relation", help="Relationship with the employee")
    member_name = fields.Char(string='Name')
    member_contact = fields.Char(string='Mobile No.')
    birth_date = fields.Date(string="Date of Birth", tracking=True)


class HrEmployeeEmergencyContact(models.Model):
    """Table for keep employee emergency contact"""

    _name = 'hr.employee.emergency.contact'
    _description = 'HR Employee Emergency Contact'

    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)
    #relation_id = fields.Many2one('hr.employee.relation', string="Relation", help="Relationship with the employee")
    contact_name = fields.Char(string='Name')
    contact_number = fields.Char(string='Mobile No.')
    relation = fields.Char(string="Relation")
    location = fields.Selection([('local', 'In Saudi Arabia'), ('home', 'In Home Country')], string="Location", help="Emergency Contact Location") 


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    origin_country_id = fields.Many2one(
        'res.country', 'Country of Origin', groups="hr.group_hr_user", tracking=True)

    def mail_reminder(self):
        """Sending expiry date notification for ID and Passport"""

        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.id_expiry_date:
                exp_date = fields.Date.from_string(i.id_expiry_date) - timedelta(days=14)
                if date_now >= exp_date:
                    mail_content = "  Hello  " + i.name + ",<br>Your ID " + i.identification_id + "is going to expire on " + \
                                   str(i.id_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('ID-%s Expired On %s') % (i.identification_id, i.id_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()
        match1 = self.search([])
        for i in match1:
            if i.passport_expiry_date:
                exp_date1 = fields.Date.from_string(i.passport_expiry_date) - timedelta(days=180)
                if date_now >= exp_date1:
                    mail_content = "  Hello  " + i.name + ",<br>Your Passport " + i.passport_id + "is going to expire on " + \
                                   str(i.passport_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('Passport-%s Expired On %s') % (i.passport_id, i.passport_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()

    personal_mobile = fields.Char(string='Mobile', related='address_home_id.mobile', store=True,
                  help="Personal mobile number of the employee")
    joining_date = fields.Date(string='Joining Date', help="Employee joining date computed from the contract start date",compute='compute_joining', store=True)
    id_expiry_date = fields.Date(string='Expiry Date', help='Expiry date of Identification ID')
    passport_expiry_date = fields.Date(string='Expiry Date', help='Expiry date of Passport ID')
    id_attachment_id = fields.Many2many('ir.attachment', 'id_attachment_rel', 'id_ref', 'attach_ref',
                                        string="Attachment", help='You can attach the copy of your Id')
    passport_attachment_id = fields.Many2many('ir.attachment', 'passport_attachment_rel', 'passport_ref', 'attach_ref1',
                                              string="Attachment",
                                              help='You can attach the copy of Passport')
    fam_ids = fields.One2many('hr.employee.family', 'employee_id', string='Family', help='Family Information')
    emergency_ids = fields.One2many('hr.employee.emergency.contact', 'employee_id', string='Contacts', help='Emergency Contact')
    first_name = fields.Char(string='First Name', store=True, readonly=False, tracking=True)
    last_name = fields.Char(string='Surname', store=True, readonly=False, tracking=True)
    driving_license_id = fields.Char(string='Driving License No.', store=True, readonly=False, tracking=True)
    phone_saudi = fields.Char(string='Phone No in Saudi', store=True, readonly=False, tracking=True)
    local_apartment = fields.Char(string='Apartment/Villa', store=True, readonly=False)
    local_building = fields.Char(string='Building', store=True, readonly=False)
    local_road = fields.Char(string='Road', store=True, readonly=False)
    local_block = fields.Char(string='Block', store=True, readonly=False)
    local_area = fields.Char(string='Area', store=True, readonly=False)
    local_sketch = fields.Binary(string='Sketch', store=True)
    home_apartment = fields.Char(string='Apartment / House', store=True, readonly=False)
    home_street = fields.Char(string='Street', store=True, readonly=False)
    home_town = fields.Char(string='Town', store=True, readonly=False)
    home_country = fields.Char(string='Country', store=True, readonly=False)
    home_phone = fields.Char(string='Phone Number', store=True, readonly=False)
    bank_name = fields.Char(string='Name Of Bank', store=True, readonly=False)
    account_name = fields.Char(string='Account Name', store=True, readonly=False)
    bank_branch = fields.Char(string='Branch', store=True, readonly=False)
    sort_code = fields.Char(string='Sort Code', store=True, readonly=False)
    account_no = fields.Char(string='Account No.', store=True, readonly=False)
    serious_illness = fields.Text(string='Any other serious illness or an illness an employer should know about', store=True, readonly=False)
    employee_no = fields.Char(string='Employee Number',required=True)


    
    @api.depends('contract_id')
    def compute_joining(self):
        if self.contract_id:
            date = min(self.contract_id.mapped('date_start'))
            self.joining_date = date
        else:
            self.joining_date = False

    @api.onchange('spouse_complete_name', 'spouse_birthdate')
    def onchange_spouse(self):
        relation = self.env.ref('hr_employee_updation.employee_relationship')
        lines_info = []
        spouse_name = self.spouse_complete_name
        date = self.spouse_birthdate
        if spouse_name and date:
            lines_info.append((0, 0, {
                'member_name': spouse_name,
                'relation_id': relation.id,
                'birth_date': date,
            })
                              )
            self.fam_ids = [(6, 0, 0)] + lines_info


class EmployeeRelationInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.relation'

    name = fields.Char(string="Relationship", help="Relationship with thw employee")
