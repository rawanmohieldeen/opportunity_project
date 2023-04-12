# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class HrApplicantInh(models.Model):
    _inherit = "hr.applicant"
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name ")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],string="Gender")
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')],string="Marital Status")
    date_of_birth = fields.Date(string="Date of Birth")
    nationality = fields.Many2one('res.country' ,string="Nationality")
    id_iqama_passport = fields.Char(string="ID/Iqama / Passport No.")
    id_iqama_passport_valid = fields.Date(string="ID/Iqama / Passport Valid till")
    current_residence_address = fields.Text(string="Current Residence Address")
    partner_phone = fields.Char("Telephone Number", size=32, compute='_compute_partner_phone_email',
        inverse='_inverse_partner_phone', store=True)
    partner_mobile = fields.Char("Mobile Number", size=32, compute='_compute_partner_phone_email',
        inverse='_inverse_partner_mobile', store=True)

    # qualifications_acquired_line_ids = fields.One2many('qualifications.acquired.line','applicant_id')

    # courses_attended_line_ids = fields.One2many('courses.attended.line','courses_attended_id')

    # courses_programmes_line_ids = fields.One2many('courses.programmes.line','courses_programmes_id')

    # computer_software_packages_line_ids = fields.One2many('computer.software.packages.line','computer_software_packages_id')

    # previous_employment_line_ids = fields.One2many('previous.employment.line','previous_employment_id')

    # languages_line_ids = fields.One2many('languages.line','languages_id')

    # references_line_ids = fields.One2many('references.line','references_id')

    qualifications_acquired_line_ids = fields.One2many('qualifications.acquired.line','applicants_id')

    courses_attended_line_ids = fields.One2many('courses.attended.line','courses_attended_id')

    courses_programmes_line_ids = fields.One2many('courses.programmes.line','courses_programmes_id')

    computer_software_packages_line_ids = fields.One2many('computer.software.packages.line','computer_software_packages_id')

    previous_employment_line_ids = fields.One2many('previous.employment.line','previous_employment_id')

    languages_line_ids = fields.One2many('languages.line','languages_id')

    references_line_ids = fields.One2many('references.line','references_id')


    if_offered_employment_when_will_you_be_available_to_start_work =fields.Char(string="If offered employment, when will you be available to start work? ") 
    

    # please_provide_any_other_information_that_you_identify_as_being_pertinent_to_this_application = fields.Char(string="Please provide any other information that you identify as being pertinent to this application?") 

    if_you_are_currently_in_saudi_arabia = fields.Selection([('yes', 'Yes'), ('no', 'No')],string="If you are currently in Saudi Arabia (SA), do you have a driving license that is valid in SA?")
    
    hobbies_and_interests =fields.Text(string="Hobbies and Interests") 


class QualificationsAcquiredLine(models.Model):
    _name = "qualifications.acquired.line"
    applicants_id = fields.Many2one('hr.applicant','qualifications_acquired_line_ids')
    qualification_title = fields.Char(string="Qualification Title")
    institution_training_provider = fields.Char(string="Institution/Training provider")

    year_from = fields.Selection(selection='years_selection', string="Years From")
    year_to = fields.Selection(selection='years_selection', string="Years To")

    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year-100, datetime.now().year + 10):
            year_str = str(y)
            year_list.append((year_str, year_str))
        return year_list


class CoursesAttendedLine(models.Model):
    _name = 'courses.attended.line'
    courses_attended_id = fields.Many2one('hr.applicant')
    course_training_name = fields.Char(string="Course/Training Name")



class CoursePprogrammesLine(models.Model):
    _name = 'courses.programmes.line'
    courses_programmes_id = fields.Many2one('hr.applicant')
    course_programme_mame = fields.Char(string="Course / Programme Name")
    institution_training_provider = fields.Char(string="Institution/Training provider")
    full_time = fields.Boolean(string="Full Time")
    distance = fields.Boolean(string="Distance")
    notes = fields.Char(string="Notes")


class computersoftwarepackagesLine(models.Model):
    _name = 'computer.software.packages.line'
    computer_software_packages_id = fields.Many2one('hr.applicant')
    package = fields.Char(string="Package")
    proficiency_level = fields.Selection([('basic', 'Basic'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],string="Proficiency Level")


class PreviousEmploymentLine(models.Model):
    _name = 'previous.employment.line'
    previous_employment_id = fields.Many2one('hr.applicant')
    employer_name = fields.Char(string="Employer Name")
    period_from = fields.Date(string="Period From")
    period_to = fields.Date(string="Period To")
    position_held = fields.Char(string="Position held")
    reason_for_leaving = fields.Char(string="Reason for leaving")


class LanguagesLine(models.Model):
    _name = 'languages.line'
    languages_id = fields.Many2one('hr.applicant')
    languages = fields.Char(string="Languages ")
    cpability = fields.Selection([('speak', 'Speak'), ('read', 'Read'), ('write', 'Write')],string="Capability")
    rating = fields.Selection([('fluent', 'Fluent'), ('good', 'Good'), ('fair', 'Fair')],string="Rating")


class ReferencesLine(models.Model):
    _name = 'references.line'
    references_id = fields.Many2one('hr.applicant')
    name = fields.Char(string="Name")
    contact_number = fields.Char(string="Contact Number")
    business_profession = fields.Char(string="Business Profession")