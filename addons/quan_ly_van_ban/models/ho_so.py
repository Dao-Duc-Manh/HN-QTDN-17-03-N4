from odoo import models, fields, api


class HoSo(models.Model):
    _name = 'ho_so'
    _description = 'Hồ Sơ'
    _rec_name = "ho_so"

    ho_so = fields.Char("Hồ Sơ", required=True)
    mo_ta = fields.Text("Mô tả")
    thoi_gian_bat_dau = fields.Date("Ngày bắt đầu")
    thoi_gian_ket_thuc = fields.Date("Ngày kết thúc")
    van_ban_di_ids = fields.One2many('van_ban_di', 'ho_so', string="Số văn bản đi")
    van_ban_den_ids = fields.One2many('van_ban_den', 'ho_so', string="Số văn bản đến")
