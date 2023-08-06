from odoo import models, fields, api

class ImportRequirementsWizard(models.TransientModel):
    _name = 'project.instance.import.requirements.wizard'
    _description = 'Import Requirements Wizard'

    requirements_txt = fields.Text(string='requirements.txt', required=True)

    def action_import(self):
        self.ensure_one()
        project_instance = self.env['project.instance'].browse(self._context.get('active_id'))
        project_instance.import_requirements_txt(self.requirements_txt)
