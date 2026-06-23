from odoo import models, fields, api


class TrangThai(models.Model):
    _name = 'trang_thai'
    _description = 'Trạng thái văn bản'
    _rec_name = "ten_trang_thai"

    # id_trang_thai = fields.Integer("ID trạng thái", required=True)
    ten_trang_thai = fields.Char("Tên trạng thái", required=True)
    mo_ta = fields.Char("Mô tả")


    