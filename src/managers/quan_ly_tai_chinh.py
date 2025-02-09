﻿import csv
from datetime import datetime
from typing import List
from csv import writer
from src.models.tai_khoan import TaiKhoan
from src.models.khoan_vay import KhoanVay
from src.models.giao_dich import GiaoDich
from src.models.danh_muc import DanhMuc
from src.models.phuong_phap_sau_lo import PhuongPhapSauLo

class QuanLyTaiChinh:
    def __init__(self):
        """
        Khoi tao quan ly tai chinh voi danh sach tai khoan, khoan vay va danh muc trong
        """
        self._tai_khoan: List[TaiKhoan] = []
        self._khoan_vay: List[KhoanVay] = []
        self._danh_muc: List[DanhMuc] = []
        self._phuong_phap_sau_lo = None
        self._muc_tieu_tiet_kiem = {}

    def them_tai_khoan(self, tai_khoan: TaiKhoan):
        """
        Them mot tai khoan moi vao he thong
        """
        for tk in self._tai_khoan:
            if tk._id == tai_khoan._id:
                return False
        self._tai_khoan.append(tai_khoan)
        return True

    def xoa_tai_khoan(self, id_tai_khoan: str):
        """
        Xoa tai khoan theo ID
        """
        self._tai_khoan = [tk for tk in self._tai_khoan if tk._id != id_tai_khoan]

    def them_giao_dich(self, giao_dich: GiaoDich):
        """
        Them mot giao dich moi vao tai khoan
        """
        for tai_khoan in self._tai_khoan:
            if tai_khoan._id == giao_dich._id_tai_khoan:
                tai_khoan.them_giao_dich(giao_dich)
                tai_khoan.cap_nhat_so_du()
                return True
        return False
    
    def xoa_giao_dich(self, id_tai_khoan: str, id_giao_dich: str):
        """
        Xoa giao dich o mot tai khoan
        """
        for tai_khoan in self._tai_khoan:
            if tai_khoan._id == id_tai_khoan:
                for giao_dich in tai_khoan._giao_dich:
                    if giao_dich._id == id_giao_dich:
                        tai_khoan.xoa_giao_dich(giao_dich)
                tai_khoan.cap_nhat_so_du()
                return True
        return False

    def them_khoan_vay(self, khoan_vay: KhoanVay):
        """
        Them mot khoan vay moi vao he thong
        """
        for kv in self._khoan_vay:
            if kv._id == khoan_vay._id:
                return False
        self._khoan_vay.append(khoan_vay)
        return True
    
    def xoa_khoan_vay(self, id_khoan_vay: str):
        """
        Xoa mot khoan vay
        """
        self._khoan_vay = [kv for kv in self._khoan_vay if kv._id != id_khoan_vay]
        
    def them_danh_muc(self, danh_muc: DanhMuc):
        """
        Them mot danh muc moi vao he thong
        """
        for dm in self._danh_muc:
            if dm._id == danh_muc._id:
                return False
        self._danh_muc.append(danh_muc)
        return True
    
    def xoa_danh_muc(self, id_danh_muc: str):
        """
        Xoa mot danh muc
        """
        self._danh_muc = [dm for dm in self._danh_muc if dm._id != id_danh_muc]
    
    def xuat_csv(self):
        """
        Xuất dữ liệu của các đối tượng ra các file CSV tương ứng
        """
        # Xuất tài khoản
        with open('taikhoan.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Tên', 'Số Dư', 'Loại'])
            for tai_khoan in self._tai_khoan:
                writer.writerow([
                    tai_khoan._id, 
                    tai_khoan._ten, 
                    tai_khoan.lay_so_du(), 
                    tai_khoan._loai
                ])

        # Xuất giao dịch
        with open('giaodich.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'ID Tài Khoản', 'Số Tiền', 'Loại', 'Danh Mục', 'Ngày', 'Ghi Chú'])
            for tai_khoan in self._tai_khoan:
                for giao_dich in tai_khoan.lay_giao_dich():
                    writer.writerow([
                        giao_dich._id,
                        giao_dich._id_tai_khoan, 
                        giao_dich.lay_so_tien(),
                        giao_dich.lay_loai(),
                        giao_dich._danh_muc,
                        giao_dich._ngay.strftime('%Y-%m-%d %H:%M:%S'),  # Chuyển đổi datetime thành chuỗi
                        giao_dich._ghi_chu
                    ])

        # Xuất danh mục
        with open('danhmuc.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Tên', 'Loại', 'Mô Tả'])
            for danh_muc in self._danh_muc:
                writer.writerow([
                    danh_muc._id, 
                    danh_muc._ten, 
                    danh_muc._loai, 
                    danh_muc._mo_ta
                ])

        # Xuất phương pháp sáu lọ
        if self._phuong_phap_sau_lo:
            with open('phuongphapsaulo.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Lọ', 'Số Tiền'])
                for ten_lo, so_tien in self._phuong_phap_sau_lo._lo.items():
                    writer.writerow([ten_lo, so_tien])

        # Xuất khoản vay
        with open('khoanvay.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Số Tiền', 'Người Cho Vay', 'Người Vay', 'Lãi Suất', 'Ngày Bắt Đầu', 'Ngày Đến Hạn', 'Trạng Thái'])
            for khoan_vay in self._khoan_vay:
                writer.writerow([
                    khoan_vay._id,
                    khoan_vay._so_tien, 
                    khoan_vay._nguoi_cho_vay,
                    khoan_vay._nguoi_vay,
                    khoan_vay._lai_suat,
                    khoan_vay._ngay_bat_dau.strftime('%Y-%m-%d %H:%M:%S'),  # Chuyển đổi datetime thành chuỗi
                    khoan_vay._ngay_den_han.strftime('%Y-%m-%d %H:%M:%S'),  # Chuyển đổi datetime thành chuỗi
                    khoan_vay._trang_thai
                ])

    def nhap_csv(self):
        """
        Đọc dữ liệu từ các file CSV và nạp vào các danh sách đối tượng
        """
        # Xóa sạch dữ liệu hiện tại trước khi nhập
        self._tai_khoan.clear()
        self._danh_muc.clear()
        self._khoan_vay.clear()
        self._phuong_phap_sau_lo = None
    
        # Nhập tài khoản
        try:
            with open('taikhoan.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Bỏ qua dòng tiêu đề
                for row in csv_reader:
                    tai_khoan = TaiKhoan(row[0], row[1], float(row[2]), row[3])
                    self.them_tai_khoan(tai_khoan)
        except FileNotFoundError:
            print("Không tìm thấy file taikhoan.csv")
        except Exception as e:
            print(f"Lỗi khi đọc file taikhoan.csv: {e}")

        # Nhập danh mục
        try:
            with open('danhmuc.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Bỏ qua dòng tiêu đề
                for row in csv_reader:
                    danh_muc = DanhMuc(row[0], row[1], row[2], row[3])
                    self.them_danh_muc(danh_muc)
        except FileNotFoundError:
            print("Không tìm thấy file danhmuc.csv")
        except Exception as e:
            print(f"Lỗi khi đọc file danhmuc.csv: {e}")

        # Nhập khoản vay
        try:
            with open('khoanvay.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Bỏ qua dòng tiêu đề
                for row in csv_reader:
                    khoan_vay = KhoanVay(
                        row[0],  # id
                        float(row[1]),  # so_tien
                        row[2],  # nguoi_cho_vay
                        row[3],  # nguoi_vay
                        float(row[4]),  # lai_suat
                        datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),  # ngay_bat_dau
                        datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')  # ngay_den_han
                    )
                    khoan_vay._trang_thai = row[7]  # Trạng thái
                    self.them_khoan_vay(khoan_vay)
        except FileNotFoundError:
            print("Không tìm thấy file khoanvay.csv")
        except Exception as e:
            print(f"Lỗi khi đọc file khoanvay.csv: {e}")

        # Nhập giao dịch
        try:
            with open('giaodich.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Bỏ qua dòng tiêu đề
                for row in csv_reader:
                    giao_dich = GiaoDich(
                        row[0],  # id
                        row[1],  # id_tai_khoan
                        float(row[2]),  # so_tien
                        row[3],  # loai
                        row[4],  # danh_muc
                        datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),  # ngay
                        row[6]  # ghi_chu
                    )
                    self.them_giao_dich(giao_dich)
        except FileNotFoundError:
            print("Không tìm thấy file giaodich.csv")
        except Exception as e:
            print(f"Lỗi khi đọc file giaodich.csv: {e}")

        # Nhập phương pháp sáu lọ
        try:
            with open('phuongphapsaulo.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Bỏ qua dòng tiêu đề
        
                # Tính tổng thu nhập để khởi tạo phương pháp sáu lọ
                tong_thu_nhap = sum(float(row[1]) for row in csv_reader)
        
                # Reset về đầu file để đọc lại
                file.seek(0)
                next(csv_reader)
        
                # Thiết lập phương pháp sáu lọ
                self.thiet_lap_phuong_phap_sau_lo(tong_thu_nhap)
        
                # Cập nhật số tiền cho từng lọ
                for row in csv_reader:
                    self._phuong_phap_sau_lo.cap_nhat_so_tien_lo(row[0], float(row[1]))
        except FileNotFoundError:
            print("Không tìm thấy file phuongphapsaulo.csv")
        except Exception as e:
            print(f"Lỗi khi đọc file phuongphapsaulo.csv: {e}")
    
    def tinh_tong_thu_nhap(self) -> float:
        """
        Tính tổng thu nhập từ tất cả các tài khoản
    
        :return: Tổng số tiền thu nhập
        """
        tong_thu_nhap = 0
    
        for tai_khoan in self._tai_khoan:
            # Chỉ tính thu nhập cho các tài khoản có số dư dương
            if tai_khoan.lay_so_du() > 0:
                tong_thu_nhap += tai_khoan.lay_so_du()
    
        return tong_thu_nhap
            
    def tao_bao_cao_tai_chinh(self, ngay_bat_dau: datetime, ngay_ket_thuc: datetime) -> dict:
        """
        Tao bao cao tai chinh trong khoang thoi gian
        """
        bao_cao = {
            "tong_so_du": sum(tk.lay_so_du() for tk in self._tai_khoan),
            "tong_no": sum(kv.lay_so_tien_con_lai() for kv in self._khoan_vay),
            "giao_dich_theo_danh_muc": {},
            "chi_tiet_tai_khoan": []
        }
        
        # Chi tiet giao dich theo danh muc trong khoang thoi gian
        for tai_khoan in self._tai_khoan:
            chi_tiet_tai_khoan = {
                "id": tai_khoan._id,
                "ten": tai_khoan._ten,
                "so_du": tai_khoan.lay_so_du(),
                "giao_dich": []
            }
            
            for giao_dich in tai_khoan.lay_giao_dich():
                if ngay_bat_dau <= giao_dich._ngay <= ngay_ket_thuc:
                    chi_tiet_tai_khoan["giao_dich"].append({
                        "so_tien": giao_dich.lay_so_tien(),
                        "loai": giao_dich.lay_loai(),
                        "ngay": giao_dich._ngay,
                        "danh_muc": giao_dich._danh_muc
                    })
                    
                    # Thong ke giao dich theo danh muc
                    if giao_dich._danh_muc not in bao_cao["giao_dich_theo_danh_muc"]:
                        bao_cao["giao_dich_theo_danh_muc"][giao_dich._danh_muc] = {
                            "tong_thu": 0,
                            "tong_chi": 0
                        }
                    
                    if giao_dich.lay_loai() == "thu nhập":
                        bao_cao["giao_dich_theo_danh_muc"][giao_dich._danh_muc]["tong_thu"] += giao_dich.lay_so_tien()
                    elif giao_dich.lay_loai() == "chi tiêu":
                        bao_cao["giao_dich_theo_danh_muc"][giao_dich._danh_muc]["tong_chi"] += giao_dich.lay_so_tien()
            
            bao_cao["chi_tiet_tai_khoan"].append(chi_tiet_tai_khoan)
        
        return bao_cao

    def dat_muc_tieu_tiet_kiem(self, id_tai_khoan: str, so_tien: float):
        """
        Dat muc tieu tiet kiem cho mot tai khoan cu the
        """
        for tai_khoan in self._tai_khoan:
            if tai_khoan._id == id_tai_khoan:
                self._muc_tieu_tiet_kiem[id_tai_khoan] = so_tien
                return True
        return False

    def du_bao_xu_huong_tai_chinh(self) -> dict:    
        """
        Du bao xu huong tai chinh dua tren du lieu lich su
        """
        du_bao = {
            "xu_huong_chi_tieu": {},
            "du_bao_tiet_kiem": {},
            "canh_bao_no": []
        }
        
        # Xu huong chi tieu theo danh muc
        for tai_khoan in self._tai_khoan:
            danh_muc_chi_tieu = {}
            for giao_dich in tai_khoan.lay_giao_dich():
                if giao_dich.lay_loai() == "chi tiêu":
                    if giao_dich._danh_muc not in danh_muc_chi_tieu:
                        danh_muc_chi_tieu[giao_dich._danh_muc] = []
                    danh_muc_chi_tieu[giao_dich._danh_muc].append(giao_dich.lay_so_tien())
            
            for danh_muc, chi_tieu in danh_muc_chi_tieu.items():
                du_bao["xu_huong_chi_tieu"][danh_muc] = {
                    "trung_binh": sum(chi_tieu) / len(chi_tieu) if chi_tieu else 0,
                    "tong_chi": sum(chi_tieu)
                }
        
        # Du bao tiet kiem
        for id_tai_khoan, muc_tieu in self._muc_tieu_tiet_kiem.items():
            du_bao["du_bao_tiet_kiem"][id_tai_khoan] = {
                "muc_tieu": muc_tieu,
                "so_du_hien_tai": next((tk.lay_so_du() for tk in self._tai_khoan if tk._id == id_tai_khoan), 0)
            }
        
        # Canh bao no
        for khoan_vay in self._khoan_vay:
            canh_bao = {
                "id": khoan_vay._id,
                "so_tien_con_lai": khoan_vay.lay_so_tien_con_lai(),
                "nguoi_cho_vay": khoan_vay._nguoi_cho_vay,
                "ngay_den_han": khoan_vay._ngay_den_han
            }
            du_bao["canh_bao_no"].append(canh_bao)
        
        return du_bao

    def thiet_lap_phuong_phap_sau_lo(self, tong_thu_nhap: float):
        """
        Thiet lap phuong phap quan ly tai chinh 6 lo
        """
        self._phuong_phap_sau_lo = PhuongPhapSauLo(tong_thu_nhap)
        self._phuong_phap_sau_lo.phan_bo_thu_nhap()

    def lay_thong_ke_tong_quat(self) -> dict:
        """
        Lay thong ke tong quat ve tinh hinh tai chinh
        """
        return {
            "so_tai_khoan": len(self._tai_khoan),
            "so_khoan_vay": len(self._khoan_vay),
            "tong_tai_san": sum(tk.lay_so_du() for tk in self._tai_khoan),
            "tong_no": sum(kv.lay_so_tien_con_lai() for kv in self._khoan_vay)
        }