from odoo import models, fields, api


class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _description = 'Bảng chứa thông tin loại văn bản'
    _rec_name = "loai_van_ban"
    
    id = fields.Integer("id", required=True)
    loai_van_ban = fields.Char("Loại văn bản", required=True)
    mo_ta = fields.Char("Mô tả")
    van_ban_di_ids = fields.One2many('van_ban_di', 'id_loai_van_ban', string="Văn bản đi")
    van_ban_den_ids = fields.One2many('van_ban_den', 'id_loai_van_ban', string="Văn bản đến")
