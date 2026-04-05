from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    clinic_doctor = fields.Boolean(string="Doctor")
    clinic_chemist = fields.Boolean(string="Chemist")
    clinic_medical_group = fields.Boolean(string="Medical Group")
    clinic_receptionist = fields.Boolean(string="Receptionist")

    def _apply_clinic_groups(self):
        doctor_group = self.env.ref('basic_hms.bi_group_doctor', raise_if_not_found=False)
        chemist_group = self.env.ref('basic_hms.group_chemist', raise_if_not_found=False)
        medical_group = self.env.ref('basic_hms.group_medical_group', raise_if_not_found=False)
        receptionist_group = self.env.ref('basic_hms.group_receptionist', raise_if_not_found=False)

        for user in self:
            if doctor_group:
                if user.clinic_doctor:
                    user.group_ids = [(4, doctor_group.id)]
                else:
                    user.group_ids = [(3, doctor_group.id)]

            if chemist_group:
                if user.clinic_chemist:
                    user.group_ids = [(4, chemist_group.id)]
                else:
                    user.group_ids = [(3, chemist_group.id)]

            if medical_group:
                if user.clinic_medical_group:
                    user.group_ids = [(4, medical_group.id)]
                else:
                    user.group_ids = [(3, medical_group.id)]

            if receptionist_group:
                if user.clinic_receptionist:
                    user.group_ids = [(4, receptionist_group.id)]
                else:
                    user.group_ids = [(3, receptionist_group.id)]

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        users._apply_clinic_groups()
        return users

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in [
            'clinic_doctor',
            'clinic_chemist',
            'clinic_medical_group',
            'clinic_receptionist',
        ]):
            self._apply_clinic_groups()
        return res