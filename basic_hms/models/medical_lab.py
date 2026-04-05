# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime
# classes under  menu of laboratry 

class medical_lab(models.Model):

    _name = 'medical.lab'
    _description = 'Medical Lab'
 

    name = fields.Char(string="Name", readonly=True, default='/')
    test_id = fields.Many2one('medical.test_type', 'Test Type', required = True)
    date_analysis =  fields.Datetime('Date of the Analysis' , default = datetime.now())
    patient_id = fields.Many2one('medical.patient','Patient', required = True) 
    date_requested = fields.Datetime('Date requested',  default = datetime.now())
    medical_lab_physician_id = fields.Many2one('medical.physician','Pathologist')
    requestor_physician_id = fields.Many2one('medical.physician','Physician', required = True)
    critearea_ids = fields.One2many('medical_test.critearea','medical_lab_id', 'Critearea')
    results= fields.Text('Results')
    diagnosis = fields.Text('Diagnosis')
    is_invoiced = fields.Boolean(copy=False,default = False)

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('ltest_seq') or '/'

        records = super(medical_lab, self).create(vals_list)

        for rec in records:
            if rec.test_id:
                criterea_ids = self.env['medical_test.critearea'].search([
                    ('test_id', '=', rec.test_id.id)
                ])
                criterea_ids.write({'medical_lab_id': rec.id})

        return records
   

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
