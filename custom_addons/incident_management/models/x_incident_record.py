# -*- coding: utf-8 -*-

from odoo import api, fields, models


class IncidentRecord(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "x.incident.record"
    _description = "To Report Incidents"
    _order = "location"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Incident Id must be unique !'),
    ]

    # ---------------------------------------- CRUD METHODS ---------------------------------------

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code("x.incident.record")
        vals_list['state'] = 'new'
        incident = super().create(vals_list)
        # Call the send_email method
        incident.action_send_email()
        return incident

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(string="Incident Reference", default='New', readonly=True)
    inc_reported_date = fields.Date(string="Date Reported", default=lambda self: fields.Date.today(), required=True)
    inc_date_time = fields.Datetime(string="Date & Time", required=True)
    shift = fields.Many2one("x.inc.shift", required=True)
    type = fields.Many2many("x.inc.type", string="Type of Incident", required=True)
    location = fields.Many2one("x.location", string="Location of Incident", required=True)
    description = fields.Html(string="Description", required=True)
    notified_by = fields.Many2one('res.users', string="Notified By", default=lambda self: self.env.user)
    notified_by_id = fields.Integer(related="notified_by.id", string="Notified By ID")
    notified_by_type = fields.Selection(related="notified_by.employee_type")
    severity = fields.Many2one("x.inc.severity", string="Severity Classification")

    incident_person_ids = fields.One2many(
        'x.inc.person.record', 'incident_id', string='People'
    )

    incident_asset_ids = fields.One2many(
        'x.inc.asset.record', 'incident_id', string='Asset Damages'
    )
    incident_spill_ids = fields.One2many(
        'x.inc.material.spill.record', 'incident_id', string='Material Spill'
    )
    incident_mva_ids = fields.One2many(
        'x.inc.mva.record', 'incident_id', string='Motor Vehicle Accidents'
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("investigation_assigned", "Assigned"),
            ("investigation_in_progress", "In Progress"),
            ("action_review", "Action Review"),
            ("closed", "Closed"),
            ("canceled", "Canceled"),
        ],
        string="Status",

        copy=False,

    )

    def action_send_email(self):
        mail_template = self.env.ref('incident_management.email_template_incident')
        mail_template.send_mail(self.id, force_send=True)


class IncidentType(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "x.inc.type"
    _description = "Incident Type"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Incident type must be unique !'),
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Incident Type", required="True")


class IncidentShift(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "x.inc.shift"
    _description = "Working Shift"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Shift must be unique !'),
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Shift", required="True")


class IncSeverity(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "x.inc.severity"
    _description = "Severity Classification"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Severities must be unique !'),
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(string="Severity Classification")