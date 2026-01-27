# Hệ Thống Quản Lý Văn Bản và Khách Hàng

[![Odoo](https://img.shields.io/badge/Odoo-15.0-875A7B?style=flat&logo=odoo&logoColor=white)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=flat&logo=ubuntu&logoColor=white)](https://ubuntu.com)

Hệ thống quản lý văn bản và khách hàng được xây dựng trên nền tảng **Odoo 15**, tuân thủ **Thông tư 30** về công tác văn thư. Hệ thống bao gồm 2 module chính:

- **Module Quản lý Văn bản** (`quan_ly_van_ban`): Quản lý văn bản đi, văn bản đến, công việc và các danh mục liên quan
- **Module Quản lý Khách hàng** (`quan_ly_khach_hang`): Quản lý khách hàng, hợp đồng và liên kết với văn bản

---

## 🎯 Tổng Quan

### Module Quản lý Văn bản (`quan_ly_van_ban`)

Module cơ sở quản lý toàn bộ hệ thống văn bản trong tổ chức:

- ✅ Quản lý văn bản đi và văn bản đến
- ✅ Quản lý công việc phát sinh từ văn bản
- ✅ Tự động tính toán trạng thái công việc
- ✅ Dashboard thống kê và báo cáo
- ✅ Quản lý danh mục: loại văn bản, độ mật, trạng thái, năm, hồ sơ

**Dependencies:** `base`, `nhan_su`

### Module Quản lý Khách hàng (`quan_ly_khach_hang`)

Module mở rộng thêm chức năng quản lý khách hàng và hợp đồng:

- ✅ Quản lý thông tin khách hàng và phân loại
- ✅ Quản lý hợp đồng với khách hàng
- ✅ Tự động tính toán trạng thái hợp đồng
- ✅ Liên kết văn bản với khách hàng
- ✅ Dashboard quản lý khách hàng và hợp đồng

**Dependencies:** `base`, `quan_ly_van_ban`

---

## 🚀 Tính Năng Chính

### 1. Quản lý Văn bản Đi/Đến

- **Tự động tạo số hiệu:** Format `{count}_{ngay_YYYYMMDD}`
- **Phân loại văn bản:** Công văn, Quyết định, Chỉ thị
- **Quản lý độ mật:** Tuyệt mật, Mật, Thường
- **Liên kết với:** Phòng ban, Nhân viên, Năm, Hồ sơ
- **Tệp đính kèm:** Hỗ trợ upload và lưu trữ file

### 2. Quản lý Công việc

- **Tự động tính trạng thái** dựa trên:
  - Ngày hoàn thành → "Hoàn thành" / "Hoàn thành quá hạn"
  - Tình trạng → "Hủy"
  - Hạn xử lý → "Đang xử lý" / "Đã nhận"
- **Gán nhiệm vụ:** Chỉ đạo và Chủ trì giải quyết
- **Theo dõi tiến độ:** Ngày tạo, hạn xử lý, ngày hoàn thành

### 3. Quản lý Khách hàng

- **Tự động tạo mã:** Format `KH{count:05d}`
- **Phân loại:** VIP, Thường, Mới
- **Thống kê:** Số lượng văn bản đi/đến, hợp đồng, công việc
- **Liên kết:** Văn bản, hợp đồng, công việc

### 4. Quản lý Hợp đồng

- **Tự động tạo số hợp đồng:** Format `HD{count:05d}_{ngay_ky_YYYYMMDD}`
- **Tự động tính trạng thái** dựa trên:
  - Tình trạng → "Hủy" / "Tạm dừng" / "Hoàn thành"
  - Ngày kết thúc → "Quá hạn" / "Sắp hết hạn" / "Đang thực hiện"
- **Quản lý giá trị:** Hỗ trợ Monetary field với đa tiền tệ
- **Cảnh báo:** Tự động phát hiện hợp đồng sắp hết hạn (≤ 30 ngày)

### 5. Dashboard

**Dashboard Văn bản:**
- Tổng văn bản đến/đi
- Tổng nhân sự
- Thống kê công việc theo trạng thái

**Dashboard Khách hàng:**
- Tổng khách hàng và hợp đồng
- Văn bản liên quan đến khách hàng
- Thống kê hợp đồng theo trạng thái

---
🖼️ Hình Ảnh Minh Họa

📊 Dashboard Quản Lý Văn Bản
<p align="center"> <img src="images/dashboard_van_ban.png" width="800"/> </p>

Hình 1. Dashboard thống kê văn bản đến/đi và tình trạng công việc

📄 Giao Diện Quản Lý Văn Bản Đến
<p align="center"> <img src="images/van_ban_den.png" width="800"/> </p>

Hình 2. Giao diện quản lý văn bản đến, liên kết công việc và khách hàng

📄 Giao Diện Quản Lý Văn Bản Đi
<p align="center"> <img src="images/van_ban_di.png" width="800"/> </p>

Hình 3. Giao diện quản lý văn bản đi với số hiệu tự động

📝 Giao Diện Quản Lý Công Việc
<p align="center"> <img src="images/cong_viec.png" width="800"/> </p>

Hình 4. Giao diện quản lý và theo dõi tiến độ công việc

👤 Giao Diện Quản Lý Khách Hàng
<p align="center"> <img src="images/khach_hang.png" width="800"/> </p>

Hình 5. Thông tin khách hàng và các dữ liệu liên kết (văn bản, hợp đồng, công việc)

📑 Giao Diện Quản Lý Hợp Đồng
<p align="center"> <img src="images/hop_dong.png" width="800"/> </p>

Hình 6. Giao diện quản lý hợp đồng và trạng thái hợp đồng

📈 Dashboard Quản Lý Khách Hàng & Hợp Đồng
<p align="center"> <img src="images/dashboard_khach_hang.png" width="800"/> </p>

Hình 7. Dashboard thống kê khách hàng và hợp đồng

## 💻 Cài Đặt

### Yêu Cầu Hệ Thống

- **OS:** Ubuntu 22.04 hoặc tương đương
- **Python:** 3.10+
- **PostgreSQL:** 13+
- **Odoo:** 15.0

### 1. Clone Project

```bash
git clone https://github.com/trungduc4804/TTDN_16-06_N8.git
cd odoo-fitdnu
git checkout cntt15_04
```

### 2. Cài Đặt Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    python3.10-distutils \
    python3.10-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    python3.10-venv \
    libpq-dev \
    docker-compose
```

### 3. Khởi Tạo Môi Trường Ảo

```bash
python3.10 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 4. Setup Database

```bash
sudo docker-compose up -d
```

### 5. Cấu Hình Odoo

Tạo file `odoo.conf`:

```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

### 6. Chạy Hệ Thống

```bash
# Kích hoạt môi trường ảo
source venv/bin/activate

# Khởi động database
sudo docker-compose up -d

# Chạy Odoo và cài đặt modules
python3 odoo-bin.py -c odoo.conf -u all
python3 odoo-bin.py -c odoo.conf -u quan_ly_van_ban,quan_ly_khach_hang,nhan_su --dev=all
```

### 7. Truy Cập Hệ Thống

Mở trình duyệt và truy cập: **http://localhost:8069**

---

## ⚙️ Cấu Hình

### Cài Đặt Modules

1. Đăng nhập vào Odoo với quyền Administrator
2. Vào **Apps** → Tìm kiếm và cài đặt:
   - `nhan_su` (Module quản lý nhân sự - bắt buộc)
   - `quan_ly_van_ban` (Module quản lý văn bản)
   - `quan_ly_khach_hang` (Module quản lý khách hàng)

### Cấu Hình Danh Mục

Sau khi cài đặt, hệ thống sẽ tự động load dữ liệu mẫu. Bạn có thể cấu hình thêm:

**Module Quản lý Văn bản:**
- **Trạng thái:** Hoàn thành, Hoàn thành quá hạn, Đã nhận, Đang xử lý, Hủy
- **Loại văn bản:** Công văn, Quyết định, Chỉ thị
- **Độ mật:** Tuyệt mật, Mật, Thường
- **Năm:** Quản lý theo năm
- **Hồ sơ:** Quản lý hồ sơ văn bản

**Module Quản lý Khách hàng:**
- **Loại khách hàng:** VIP, Thường, Mới
- **Trạng thái hợp đồng:** Đang thực hiện, Sắp hết hạn, Quá hạn, Hoàn thành, Hủy, Tạm dừng

---

## 📖 Sử Dụng

### Quy Trình Quản Lý Văn Bản

1. **Tạo Văn bản Đến:**
   - Vào menu **QLVB → Quản lý văn bản đến**
   - Click **Tạo** và điền thông tin
   - Hệ thống tự động tạo số hiệu

2. **Tạo Công việc:**
   - Từ văn bản đến, click **Tạo công việc**
   - Điền thông tin: tên, yêu cầu, hạn xử lý
   - Gán Chỉ đạo và Chủ trì giải quyết
   - Hệ thống tự động tính trạng thái

3. **Theo dõi Công việc:**
   - Vào **Bảng điều khiển công việc**
   - Xem thống kê theo trạng thái
   - Cập nhật ngày hoàn thành để tự động chuyển trạng thái

### Quy Trình Quản Lý Khách Hàng

1. **Tạo Khách hàng:**
   - Vào menu **QLKH → Quản lý khách hàng**
   - Click **Tạo** và điền thông tin
   - Hệ thống tự động tạo mã khách hàng

2. **Tạo Hợp đồng:**
   - Từ form khách hàng, tab **Hợp đồng** → **Tạo**
   - Điền thông tin hợp đồng
   - Hệ thống tự động tính trạng thái và cảnh báo hết hạn

3. **Liên kết Văn bản:**
   - Khi tạo văn bản đi/đến, chọn **Khách hàng liên quan**
   - Văn bản sẽ tự động hiển thị trong form khách hàng
   - Công việc từ văn bản đến sẽ tự động liên kết với khách hàng

### Dashboard

- **Dashboard Văn bản:** Menu **QLVB → Dashboard**
- **Dashboard Khách hàng:** Menu **QLKH → Dashboard**

Dashboard tự động cập nhật và cung cấp các nút **Xem thêm** để xem chi tiết.

---

## 🏗️ Kiến Trúc Module

### Cấu Trúc Module Quản lý Văn bản

```
quan_ly_van_ban/
├── models/
│   ├── van_ban_di.py          # Văn bản đi
│   ├── van_ban_den.py         # Văn bản đến
│   ├── cong_viec.py           # Công việc
│   ├── trang_thai.py          # Trạng thái
│   ├── loai_van_ban.py        # Loại văn bản
│   ├── do_mat.py              # Độ mật
│   ├── nam.py                 # Năm
│   ├── ho_so.py               # Hồ sơ
│   └── dashboard.py           # Dashboard
├── views/
│   ├── van_ban_di.xml
│   ├── van_ban_den.xml
│   ├── cong_viec.xml
│   ├── dashboard.xml
│   └── menu.xml
├── data/
│   └── van_ban_data.xml       # Dữ liệu mẫu
└── __manifest__.py
```

### Cấu Trúc Module Quản lý Khách hàng

```
quan_ly_khach_hang/
├── models/
│   ├── khach_hang.py          # Khách hàng
│   ├── hop_dong.py            # Hợp đồng
│   ├── van_ban_ext.py         # Mở rộng văn bản
│   ├── cong_viec_ext.py       # Mở rộng công việc
│   ├── loai_khach_hang.py     # Loại khách hàng
│   ├── trang_thai_hop_dong.py # Trạng thái hợp đồng
│   └── dashboard.py           # Dashboard
├── views/
│   ├── khach_hang.xml
│   ├── hop_dong.xml
│   ├── dashboard.xml
│   └── menu.xml
├── data/
│   └── khach_hang_data.xml    # Dữ liệu mẫu
└── __manifest__.py
```

---

## 🔗 Mối Quan Hệ Giữa Các Module

### Dependency

```
quan_ly_khach_hang → depends on → quan_ly_van_ban → depends on → nhan_su
```

### Inheritance (Kế thừa)

Module `quan_ly_khach_hang` mở rộng các model của `quan_ly_van_ban`:

- **van_ban_di** → Thêm field `id_khach_hang`
- **van_ban_den** → Thêm field `id_khach_hang`
- **cong.viec** → Thêm field `khach_hang_id` (computed từ văn bản đến)

### Data Relationships

```
Khách hàng (1) ←→ (N) Văn bản đi/đến
Khách hàng (1) ←→ (N) Hợp đồng
Khách hàng (1) ←→ (N) Công việc
Văn bản đến (1) ←→ (N) Công việc
```

### Luồng Dữ liệu

```
Văn bản đến (có id_khach_hang)
    ↓
Công việc (van_ban_den_id)
    ↓
Tự động tính toán khach_hang_id từ van_ban_den_id.id_khach_hang
```

---

## ⭐ Tính Năng Nổi Bật

### 1. Tự Động Hóa

- ✅ **Tự động tạo số hiệu:** Văn bản, hợp đồng, khách hàng
- ✅ **Tự động tính trạng thái:** Công việc và hợp đồng
- ✅ **Tự động liên kết:** Công việc với khách hàng
- ✅ **Tự động cảnh báo:** Hợp đồng sắp hết hạn

### 2. Dashboard Thông Minh

- ✅ Tự động cập nhật thống kê
- ✅ Liên kết trực tiếp đến danh sách chi tiết
- ✅ Hiển thị trực quan với cards và buttons

### 3. Quản Lý Tập Trung

- ✅ Tất cả thông tin liên quan hiển thị trong một form
- ✅ Tab navigation dễ sử dụng
- ✅ Action buttons để xem chi tiết

### 4. Tính Năng Mở Rộng

- ✅ Module khách hàng mở rộng module văn bản mà không thay đổi code gốc
- ✅ Dễ dàng thêm tính năng mới thông qua inheritance
- ✅ Tách biệt chức năng, dễ bảo trì

---

## 📝 Ghi Chú

- Hệ thống tuân thủ **Thông tư 30** về công tác văn thư
- Tất cả trạng thái được tính toán tự động, không cần nhập thủ công
- Dashboard cần được mở để tính toán statistics
- Module `nhan_su` là bắt buộc cho module `quan_ly_van_ban`

---

## 👥 Tác Giả

- **Module Quản lý Văn bản:** Nhóm 2 - CNTT 1504
- **Module Quản lý Khách hàng:** Nhóm 8 - CNTT 16-06