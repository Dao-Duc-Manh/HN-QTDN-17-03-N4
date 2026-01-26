from odoo import models, fields, api
import json
import time


class KhachHangDashboard(models.TransientModel):
    _name = 'khach_hang.dashboard'
    _description = 'Dashboard Quản lý Khách hàng'

    # Computed fields for statistics
    tong_khach_hang = fields.Integer(string="Tổng khách hàng", compute="_compute_statistics", store=False)
    tong_hop_dong = fields.Integer(string="Tổng hợp đồng", compute="_compute_statistics", store=False)
    tong_van_ban_den = fields.Integer(string="Tổng văn bản đến", compute="_compute_statistics", store=False)
    tong_van_ban_di = fields.Integer(string="Tổng văn bản đi", compute="_compute_statistics", store=False)
    hop_dong_dang_thuc_hien = fields.Integer(string="Hợp đồng đang thực hiện", compute="_compute_statistics", store=False)
    hop_dong_sap_het_han = fields.Integer(string="Hợp đồng sắp hết hạn", compute="_compute_statistics", store=False)
    hop_dong_qua_han = fields.Integer(string="Hợp đồng quá hạn", compute="_compute_statistics", store=False)

    @api.model
    def action_open_dashboard(self):
        """Tạo record dashboard và trả về action để mở form view"""
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H1",
                "location": "khach_hang/dashboard.py:action_open_dashboard",
                "message": "Opening customer dashboard",
                "data": {"uid": self.env.uid},
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion
        dashboard = self.create({})
        # Tính toán statistics ngay sau khi tạo
        dashboard._compute_statistics()
        return {
            'name': 'Dashboard Quản lý Khách hàng',
            'type': 'ir.actions.act_window',
            'res_model': 'khach_hang.dashboard',
            'res_id': dashboard.id,
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('quan_ly_khach_hang.view_khach_hang_dashboard_form').id,
        }

    @api.depends()
    def _compute_statistics(self):
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H2",
                "location": "khach_hang/dashboard.py:_compute_statistics",
                "message": "Computing statistics - start",
                "data": {},
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion
        # Tổng số lượng
        self.tong_khach_hang = self.env['khach_hang'].search_count([])
        self.tong_hop_dong = self.env['hop_dong'].search_count([])
        self.tong_van_ban_den = self.env['van_ban_den'].search_count([('id_khach_hang', '!=', False)])
        self.tong_van_ban_di = self.env['van_ban_di'].search_count([('id_khach_hang', '!=', False)])

        # Hợp đồng theo trạng thái
        trang_thai_dang_thuc_hien = self.env['trang_thai_hop_dong'].search([('ten_trang_thai', '=', 'Đang thực hiện')], limit=1)
        trang_thai_sap_het_han = self.env['trang_thai_hop_dong'].search([('ten_trang_thai', '=', 'Sắp hết hạn')], limit=1)
        trang_thai_qua_han = self.env['trang_thai_hop_dong'].search([('ten_trang_thai', '=', 'Quá hạn')], limit=1)

        self.hop_dong_dang_thuc_hien = self.env['hop_dong'].search_count([('trang_thai', '=', trang_thai_dang_thuc_hien.id)]) if trang_thai_dang_thuc_hien else 0
        self.hop_dong_sap_het_han = self.env['hop_dong'].search_count([('trang_thai', '=', trang_thai_sap_het_han.id)]) if trang_thai_sap_het_han else 0
        self.hop_dong_qua_han = self.env['hop_dong'].search_count([('trang_thai', '=', trang_thai_qua_han.id)]) if trang_thai_qua_han else 0
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H2",
                "location": "khach_hang/dashboard.py:_compute_statistics",
                "message": "Computing statistics - end",
                "data": {
                    "tong_khach_hang": self.tong_khach_hang,
                    "tong_hop_dong": self.tong_hop_dong,
                    "tong_van_ban_den": self.tong_van_ban_den,
                    "tong_van_ban_di": self.tong_van_ban_di,
                    "hop_dong": {
                        "dang_thuc_hien": self.hop_dong_dang_thuc_hien,
                        "sap_het_han": self.hop_dong_sap_het_han,
                        "qua_han": self.hop_dong_qua_han,
                    },
                },
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion


    def action_view_khach_hang(self):
        return {
            'name': 'Khách hàng',
            'type': 'ir.actions.act_window',
            'res_model': 'khach_hang',
            'view_mode': 'tree,form',
        }

    def action_view_hop_dong(self):
        return {
            'name': 'Hợp đồng',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong',
            'view_mode': 'tree,form',
        }

    def action_view_van_ban_den(self):
        return {
            'name': 'Văn bản đến',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_den',
            'view_mode': 'tree,form',
            'domain': [('id_khach_hang', '!=', False)],
        }

    def action_view_van_ban_di(self):
        return {
            'name': 'Văn bản đi',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_di',
            'view_mode': 'tree,form',
            'domain': [('id_khach_hang', '!=', False)],
        }

    def action_view_hop_dong_dang_thuc_hien(self):
        trang_thai_dang_thuc_hien = self.env['trang_thai_hop_dong'].search([('ten_trang_thai', '=', 'Đang thực hiện')], limit=1)
        domain = [('trang_thai', '=', trang_thai_dang_thuc_hien.id)] if trang_thai_dang_thuc_hien else []
        return {
            'name': 'Hợp đồng đang thực hiện',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong',
            'view_mode': 'tree,form',
            'domain': domain,
        }

    def action_view_hop_dong_sap_het_han(self):
        trang_thai_sap_het_han = self.env['trang_thai_hop_dong'].search([('ten_trang_thai', '=', 'Sắp hết hạn')], limit=1)
        domain = [('trang_thai', '=', trang_thai_sap_het_han.id)] if trang_thai_sap_het_han else []
        return {
            'name': 'Hợp đồng sắp hết hạn',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong',
            'view_mode': 'tree,form',
            'domain': domain,
        }

    def action_view_hop_dong_qua_han(self):
        trang_thai_qua_han = self.env['trang_thai_hop_dong'].search([('ten_trang_thai', '=', 'Quá hạn')], limit=1)
        domain = [('trang_thai', '=', trang_thai_qua_han.id)] if trang_thai_qua_han else []
        return {
            'name': 'Hợp đồng quá hạn',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong',
            'view_mode': 'tree,form',
            'domain': domain,
        }

