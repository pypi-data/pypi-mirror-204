from datetime import datetime, time, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import logging
import pytz
import re
_logger = logging.getLogger(__name__)


class ProjectInstance(models.Model):
    _name = 'project.instance'
    _description = 'Project Instance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # General Information

    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Project Description')
    start_date = fields.Date(string='Start Date')
    
    project_id = fields.Many2one('project.project', string='Project', ondelete='set null')
    helpdesk_team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', ondelete='set null')    
    instance_url = fields.Char(string='Instance URL')

    client_id = fields.Many2one('res.partner', string='Client', required=True)                                
    client_contact_id = fields.Many2one(
        'res.partner', string='Client Contact', domain=[('type', '=', 'contact')])

    technician_ids = fields.Many2many(
        'res.users', string='Technicians', relation='project_instance_technician_rel')
    functional_ids = fields.Many2many(
        'res.users', string='Functional Experts', relation='project_instance_functional_rel')

    odoo_version = fields.Selection([
        ('12.0', '12.0'),
        ('13.0', '13.0'),
        ('14.0', '14.0'),
        ('15.0', '15.0'),
        ('16.0', '16.0'),
    ], string="Odoo Version", required=True)

    odoo_version_id = fields.Many2one('odoo.version', string="Odoo Version", required=True)

    state = fields.Selection([
        ('in_progress', 'In Progress'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('cancelled', 'Terminated')
    ], string='State', default='in_progress')

    # Technical Information
    
    inventory_url = fields.Char(string='Inventory URL')
    instance_type = fields.Selection([
        ('test', 'Test'),
        ('production', 'Production'),
    ], string="Instance Type", required=True)

    deploy_schedule = fields.One2many(
        'project.instance.schedule', 'instance_id', string="Deploy Schedule")
    
    unavailable_windows = fields.One2many(
        'project.instance.unavailable_schedule', 'instance_id', string='Unavailable Windows')

    deploy_event_ids = fields.One2many(
        'calendar.event', 'instance_id', string='Deploy Events')

    server_information = fields.Text(string='Server Information')
    requirements_url = fields.Char(string='Requirements URL')
    module_ids = fields.Many2many('project.instance.module', string='Modules')

    server_type = fields.Selection([
        ('cx11', 'cx11'),
        ('cpx11', 'cpx11'),
        ('cx21', 'cx21'),
        ('cpx21', 'cpx21'),
        ('cx31', 'cx31'),
        ('cpx31', 'cpx31'),
        ('cx41', 'cx41'),
        ('cpx41', 'cpx41'),
        ('cx51', 'cx51'),
        ('cpx51', 'cpx51'),
    ], string="Server Type")

    troubleshooting_ids = fields.One2many('project.instance.troubleshooting', 'instance_id', string='Troubleshooting')
    deploy_duration = fields.Float(
        string='Deploy Duration', default=1.0, help="Duration in hours")



    # Functional Information
    process_ids = fields.Many2many(
        'project.instance.process', string='Processes')

    available_windows = fields.One2many(
        'project.instance.window', 'instance_id', string='Available Windows')

    functional_requirement_ids = fields.One2many(
        'project.instance.functional_requirement', 'project_instance_id', string='Functional Requirements')


    # Commercial Information
    contact_role_id = fields.Many2one('res.partner', string='Rol de Contacto')
    maintenance_contract_ids = fields.Char(string='Contratos de Mantenimiento')
    support_contract_ids = fields.Char(string='Contratos de Soporte')
    implementation_contract_id = fields.Char(
        string='Contrato de Implementación')


    # maintenance_contract_ids = fields.Many2many('contract.contract', string='Contratos de Mantenimiento', relation='project_instance_maintenance_contract_rel')
    # support_contract_ids = fields.Many2many('contract.contract', string='Contratos de Soporte', relation='project_instance_support_contract_rel')
    # implementation_contract_id = fields.Many2one('contract.contract', string='Contrato de Implementación', relation='project_instance_implementation_contract_rel')


    # next_window = fields.Char(string="Next Window")

    def toggle_state(self):
            state_order = ['in_progress', 'running', 'paused', 'cancelled']
            next_state_index = (state_order.index(self.state) + 1) % len(state_order)
            self.state = state_order[next_state_index]

    @api.depends('state')
    def _compute_state_color(self):
        color_map = {
            'in_progress': 'o_status_warning',
            'running': 'o_status_success',
            'paused': 'o_status_secondary',
            'cancelled': 'o_status_danger',
        }
        for record in self:
            record.state_color = color_map[record.state]

    state_color = fields.Char(compute='_compute_state_color', store=True)    


    # @api.depends('unavailable_windows')
    # def _compute_next_window(self):
    #     for instance in self:
    #         now_utc = datetime.utcnow()
    #         now_utc_time = now_utc.time()
    #         user_tz = pytz.timezone(self.env.user.tz or 'UTC')
    #         now_local = now_utc.astimezone(user_tz)

    #         next_window_start = find_next_available_window(instance, now_local, instance.deploy_duration)

    #         if next_window_start:
    #             instance.next_window = next_window_start
    #         else:
    #             instance.next_window = False

    # @api.depends('deploy_schedule')
    # def _compute_next_window(self):
    #     for instance in self:
    #         now_utc = datetime.utcnow()
    #         now_utc_time = now_utc.time()
    #         user_tz = pytz.timezone(self.env.user.tz or 'UTC')
    #         now_local = now_utc.astimezone(user_tz)
    #         now_local_time = now_local.time()
    #         now_weekday = str(now_local.weekday())

    #         closest_start_time = None
    #         closest_schedule = None

    #         for schedule in instance.deploy_schedule:
    #             schedule_hour = int(schedule.start_time)
    #             schedule_minute = int((schedule.start_time % 1) * 60)
    #             schedule_time = time(schedule_hour, schedule_minute, 0)

    #             if schedule.day_of_week == now_weekday:
    #                 if schedule_time > now_local_time:
    #                     if closest_start_time is None or schedule_time < closest_start_time:
    #                         closest_start_time = schedule.start_time
    #                         closest_schedule = schedule
    #             elif int(schedule.day_of_week) > now_local.weekday():
    #                 if closest_start_time is None or schedule_time < closest_start_time:
    #                     closest_start_time = schedule.start_time
    #                     closest_schedule = schedule

    #         if closest_schedule:
    #             scheduled_hour = int(closest_start_time)
    #             scheduled_minute = int((closest_start_time % 1) * 60)
    #             scheduled_time = time(scheduled_hour, scheduled_minute, 0)
    #             scheduled_date = now_local.date()

    #             scheduled_datetime = user_tz.localize(
    #                 datetime.combine(scheduled_date, scheduled_time))
    #             instance.next_window = scheduled_datetime
    #         else:
    #             instance.next_window = False

    def download_and_process_requirements_txt(self):
        if not self.requirements_url:
            return
        response = requests.get(self.requirements_url)
        if response.status_code == 200:
            requirements_txt = response.text
            self.import_requirements_txt(requirements_txt)
        else:
            raise UserError(
                ('Error downloading requirements.txt file. Status code: %s') % response.status_code)

    def open_calendar_event_wizard(self):
        self.ensure_one()
        wizard = self.env['project.instance.calendar.event.wizard'].create({
            'instance_id': self.id,
            'date_start': self.next_window,
            'duration': self.deploy_duration,
        })

        return {
            'name': ('Create Calendar Event'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.instance.calendar.event.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def import_requirements_txt(self, file_content):
        """Parse a requirements.txt file and update the modules field."""
        Module = self.env['project.instance.module']
        ModuleVersion = self.env['project.instance.module.version']
        modules_to_link = []        

        current_versions = ModuleVersion.search([
                ('instance_ids', 'in', [self.id]),
            ], limit=1)
        for version in current_versions:
            # delete the instance in the version
            version.instance_ids = [(3, self.id)]
            # if the version is not used by any instance, delete it
            if not version.instance_ids:
                version.unlink()
        _logger.debug('current_versions: %s', current_versions)         
        for line in file_content.splitlines():
            line = line.strip()
            if not line or '==' not in line:
                continue

            module_name, version = line.split('==')
            module = Module.search(
                [('technical_name', '=', module_name)], limit=1)

            if not module:
                module_data = self.get_module_name_from_pypi(module_name)
                module = Module.create({
                    'technical_name': module_data['technical_name'],
                    'name': module_data['name'],
                    'module_type': module_data['module_type'],
                    'odoo_version_id': module_data['odoo_version_id'].id,
                    'pypi_url': f'https://pypi.org/project/{module_name}/',
                    'is_odoo_module': module_data['is_odoo_module'],
                })

            version_record = ModuleVersion.search([
                ('name', '=', version),
                ('module_id', '=', module.id),
                ('instance_ids', 'in', [self.id]),
            ], limit=1)

            if not version_record:
                version_record = ModuleVersion.create({
                    'name': version,
                    'module_id': module.id,
                })
                version_record.instance_ids |= self

            modules_to_link.append(module.id)

        self.module_ids = [(6, 0, modules_to_link)]
        ModuleVersion.archive_or_delete_unassociated_module_versions()

    def get_module_name_from_pypi(self, technical_name):
        url = f'https://pypi.org/pypi/{technical_name}/json'
        response = requests.get(url)
        module_data = {
            'technical_name': technical_name,
            'name': technical_name,
            'module_type': 'custom',
        }

        if response.status_code == 200:
            data = response.json()
            module_data['technical_name'] = data['info']['name']
            module_data['name'] = data['info']['summary']
            module_data['home_page'] = data['info']['home_page']
            module_data['is_odoo_module'] = False
            _logger.critical('technical_name: %s', technical_name)

            # Check if the module is Odoo core or OCA
            if 'oca' in module_data['home_page'].lower():
                module_data['module_type'] = 'OCA'
            if 'odoo' in module_data['technical_name'].lower():
                module_data['is_odoo_module'] = True

            # extract odoo version from version key. Example: version	"14.0.1.0.3"
            odoo_version_pattern = r"(\d{1,2}\.\d{1,2})"
            match = re.search(odoo_version_pattern, data['info']['version'])
            if match:
                module_data['odoo_version'] = match.group(1)
                module_data['odoo_version_id'] = self.env['odoo.version'].search([('name', '=', match.group(1))], limit=1)

        else:
            _logger.warning(
                f'Error fetching module name from pypi.org for {technical_name}')

        return module_data

    def compute_available_windows(self):
        for instance in self:
            # Clear existing available windows
            instance.available_windows.unlink()

            # Calculate the available windows in the next 7 days
            now_utc = datetime.utcnow()
            user_tz = pytz.timezone(self.env.user.tz or 'UTC')
            now_local = now_utc.astimezone(user_tz)

            for i in range(7):
                current_date = now_local.date() + timedelta(days=i)
                current_weekday = str(current_date.weekday())

                unavailable_periods = []
                for schedule in instance.unavailable_windows:
                    if schedule.day_of_week == current_weekday:
                        unavailable_periods.append(schedule.get_unavailable_periods(current_date, user_tz))

                unavailable_periods.sort()
                available_start_time = user_tz.localize(datetime.combine(current_date, time(0, 0)))

                for period_start, period_end in unavailable_periods:
                    if period_start > available_start_time:
                        deploy_end_time = period_start - timedelta(hours=instance.deploy_duration)
                        if deploy_end_time > available_start_time:
                            instance.available_windows.create({
                                'instance_id': instance.id,
                                'start_time': available_start_time.astimezone(pytz.utc).replace(tzinfo=None),
                                'end_time': deploy_end_time.astimezone(pytz.utc).replace(tzinfo=None),
                            })

                    available_start_time = period_end

                available_end_time = user_tz.localize(datetime.combine(current_date, time.max))
                if available_end_time > available_start_time:
                    deploy_end_time = available_end_time - timedelta(hours=instance.deploy_duration)
                    if deploy_end_time > available_start_time:
                        instance.available_windows.create({
                            'instance_id': instance.id,
                            'start_time': available_start_time.astimezone(pytz.utc).replace(tzinfo=None),
                            'end_time': deploy_end_time.astimezone(pytz.utc).replace(tzinfo=None),
                        })


    # def compute_available_windows(self):
    #     for instance in self:
    #         # Clear existing available windows
    #         instance.available_windows.unlink()

    #         # Calculate the available windows in the next 7 days
    #         now_utc = datetime.utcnow()
    #         user_tz = pytz.timezone(self.env.user.tz or 'UTC')
    #         now_local = now_utc.astimezone(user_tz)

    #         for i in range(7):
    #             current_date = now_local.date() + timedelta(days=i)
    #             current_weekday = str(current_date.weekday())

    #             unavailable_periods = []
    #             for schedule in instance.unavailable_windows:
    #                 if schedule.day_of_week == current_weekday:
    #                     unavailable_periods.append(schedule.get_unavailable_periods(current_date, user_tz))

    #             unavailable_periods.sort()
    #             available_start_time = datetime.combine(current_date, time.min).replace(tzinfo=user_tz)

    #             for period_start, period_end in unavailable_periods:
    #                 if period_start > available_start_time:
    #                     deploy_end_time = period_start - timedelta(hours=instance.deploy_duration)
    #                     if deploy_end_time > available_start_time:
    #                         instance.available_windows.create({
    #                             'instance_id': instance.id,
    #                             'start_time': available_start_time.astimezone(pytz.utc).replace(tzinfo=None),
    #                             'end_time': deploy_end_time.astimezone(pytz.utc).replace(tzinfo=None),
    #                         })

    #                 available_start_time = period_end

    #             available_end_time = datetime.combine(current_date, time.max).replace(tzinfo=user_tz)
    #             if available_end_time > available_start_time:
    #                 deploy_end_time = available_end_time - timedelta(hours=instance.deploy_duration)
    #                 if deploy_end_time > available_start_time:
    #                     instance.available_windows.create({
    #                         'instance_id': instance.id,
    #                         'start_time': available_start_time.astimezone(pytz.utc).replace(tzinfo=None),
    #                         'end_time': deploy_end_time.astimezone(pytz.utc).replace(tzinfo=None),
    #                     })


    # def find_next_available_window(instance, now_local, required_duration):
    #     user_tz = pytz.timezone(instance.env.user.tz or 'UTC')

    #     for i in range(7):
    #         current_date = now_local.date() + timedelta(days=i)
    #         current_weekday = str(current_date.weekday())

    #         unavailable_periods = []
    #         for schedule in instance.unavailable_windows:
    #             if schedule.day_of_week == current_weekday:
    #                 schedule_hour = int(schedule.start_time)
    #                 schedule_minute = int((schedule.start_time % 1) * 60)
    #                 schedule_time = time(schedule_hour, schedule_minute, 0)
    #                 schedule_end_hour = int(schedule.end_time)
    #                 schedule_end_minute = int((schedule.end_time % 1) * 60)
    #                 schedule_end_time = time(schedule_end_hour, schedule_end_minute, 0)

    #                 start_time = user_tz.localize(
    #                     datetime.combine(current_date, schedule_time))
    #                 end_time = user_tz.localize(
    #                     datetime.combine(current_date, schedule_end_time))

    #                 unavailable_periods.append((start_time, end_time))

    #         available_start_time = datetime.combine(current_date, time.min).replace(tzinfo=user_tz)
    #         available_end_time = datetime.combine(current_date, time.max).replace(tzinfo=user_tz)

    #         if not unavailable_periods:
    #             duration = (available_end_time - available_start_time).total_seconds() / 3600
    #             if duration >= required_duration:
    #                 return available_start_time.astimezone(pytz.utc).replace(tzinfo=None)

    #         unavailable_periods.sort()

    #         for period_start, period_end in unavailable_periods:
    #             if period_start > available_start_time:
    #                 duration = (period_start - available_start_time).total_seconds() / 3600
    #                 if duration >= required_duration:
    #                     return available_start_time.astimezone(pytz.utc).replace(tzinfo=None)

    #             available_start_time = period_end

    #         if available_end_time > available_start_time:
    #             duration = (available_end_time - available_start_time).total_seconds() / 3600
    #             if duration >= required_duration:
    #                 return available_start_time.astimezone(pytz.utc).replace(tzinfo=None)

    #     return None


    @api.onchange('odoo_version_id')
    def _onchange_odoo_version_id(self):
        if self.odoo_version_id:
            self.module_ids = False
            return {
                'domain': {
                    'module_ids': [('odoo_version_id', '=', self.odoo_version_id.id)]
                }
            }
        else:
            return {
                'domain': {
                    'module_ids': []
                }
            }

    def find_next_available_window(instance, now_local, required_duration):
        user_tz = pytz.timezone(instance.env.user.tz or 'UTC')
        now_utc = now_local.astimezone(pytz.utc)

        for i in range(7):
            current_date = now_utc.date() + timedelta(days=i)
            current_weekday = str(current_date.weekday())

            unavailable_periods = []
            for schedule in instance.unavailable_windows:
                if schedule.day_of_week == current_weekday:
                    schedule_hour = int(schedule.start_time)
                    schedule_minute = int((schedule.start_time % 1) * 60)
                    schedule_time = time(schedule_hour, schedule_minute, 0)
                    schedule_end_hour = int(schedule.end_time)
                    schedule_end_minute = int((schedule.end_time % 1) * 60)
                    schedule_end_time = time(schedule_end_hour, schedule_end_minute, 0)

                    start_time = user_tz.localize(
                        datetime.combine(current_date, schedule_time))
                    end_time = user_tz.localize(
                        datetime.combine(current_date, schedule_end_time))

                    unavailable_periods.append((start_time, end_time))

            available_start_time = datetime.combine(current_date, time.min).replace(tzinfo=pytz.utc)
            available_end_time = datetime.combine(current_date, time.max).replace(tzinfo=pytz.utc)

            if not unavailable_periods:
                duration = (available_end_time - available_start_time).total_seconds() / 3600
                if duration >= required_duration:
                    return available_start_time

            unavailable_periods.sort()

        for period_start, period_end in unavailable_periods:
            if period_start > available_start_time:
                duration = (period_start - available_start_time).total_seconds() / 3600
                if duration >= required_duration:
                    return available_start_time

            available_start_time = period_end

        if available_end_time > available_start_time:
            duration = (available_end_time - available_start_time).total_seconds() / 3600
            if duration >= required_duration:
                return available_start_time

        return None

    def get_available_window_from_schedule(self, schedule, current_date, user_tz):
        schedule_hour = int(schedule.start_time)
        schedule_minute = int((schedule.start_time % 1) * 60)
        schedule_time = time(schedule_hour, schedule_minute, 0)
        schedule_end_hour = int(schedule.end_time)
        schedule_end_minute = int((schedule.end_time % 1) * 60)
        schedule_end_time = time(schedule_end_hour, schedule_end_minute, 0)

        start_time = user_tz.localize(datetime.combine(current_date, schedule_time))
        end_time = user_tz.localize(datetime.combine(current_date, schedule_end_time))

        return start_time, end_time



class ProjectInstanceSchedule(models.Model):
    _name = 'project.instance.schedule'
    _description = 'Deploy Schedule'

    instance_id = fields.Many2one('project.instance', string="Instance")
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string="Day of the Week", required=True)
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    duration = fields.Float(
        string='Duration', default=1.0, help="Duration in hours")


class FunctionalRequirement(models.Model):
    _name = 'project.instance.functional_requirement'
    _description = 'Functional Requirement'

    name = fields.Char('Requirement', required=True)
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('waiting_validation', 'Waiting for Validation')
    ], string='Status', default='not_started', required=True)
    project_instance_id = fields.Many2one(
        'project.instance', string='Project Instance')


class ProjectInstanceTroubleshooting(models.Model):
    _name = 'project.instance.troubleshooting'
    _description = 'Project Instance Troubleshooting'

    date = fields.Date(string='Date', default=fields.Date.context_today)
    title = fields.Char(string='Title', required=True)
    url = fields.Char(string='URL')
    type = fields.Selection([
        ('postmortem', 'Post Mortem'),
        ('config', 'Configuration'),
        ('other', 'Other')
    ], string='Type', default='config', required=True)

    instance_id = fields.Many2one('project.instance', string='Instance', ondelete='cascade')

class ProjectInstanceUnavailableSchedule(models.Model):
    _name = 'project.instance.unavailable_schedule'
    _description = 'Unavailable Deploy Schedule'

    instance_id = fields.Many2one('project.instance', string="Instance")
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string="Day of the Week", required=True)
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)

    def get_unavailable_periods(self, current_date, user_tz):
            schedule_hour = int(self.start_time)
            schedule_minute = int((self.start_time % 1) * 60)
            schedule_time = time(schedule_hour, schedule_minute, 0)
            schedule_end_hour = int(self.end_time)
            schedule_end_minute = int((self.end_time % 1) * 60)
            schedule_end_time = time(schedule_end_hour, schedule_end_minute, 0)

            start_time = user_tz.localize(datetime.combine(current_date, schedule_time))
            end_time = user_tz.localize(datetime.combine(current_date, schedule_end_time))

            return (start_time, end_time)    
