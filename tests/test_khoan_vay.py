from datetime import datetime

class KhoanVay:
    def __init__(self, id, soTien, mucDichVay, laiSuat, ngayBatDau, ngayDenHan, trangThai="Chưa thanh toán"):
     
        self.id = id
        self.soTien = soTien
        self.mucDichVay = mucDichVay
        self.laiSuat = laiSuat
        self.ngayBatDau = ngayBatDau
        self.ngayDenHan = ngayDenHan
        self.trangThai = trangThai
        self.lichSuThanhToan = []

    def tinhLai(self):
        soNgay = (self.ngayDenHan - self.ngayBatDau).days
        lai = (self.soTien * self.laiSuat * soNgay) / (100 * 365)
        lai = round(lai, 3)
        return lai

    def themThanhToan(self, soTien, ngayThanhToan):
        self.lichSuThanhToan.append({"ngay": ngayThanhToan, "soTien": soTien})

    def capNhatTrangThai(self):
        soTienDaThanhToan = sum([tt["soTien"] for tt in self.lichSuThanhToan])
        if soTienDaThanhToan >= self.soTien + self.tinhLai():
            self.trangThai = "Đã thanh toán"
        else:
            self.trangThai = "Chưa thanh toán"

    def laySoTienConLai(self):
        tongTienPhaiTra = self.soTien + self.tinhLai()
        soTienDaThanhToan = sum([tt["soTien"] for tt in self.lichSuThanhToan])
        return max(0, tongTienPhaiTra - soTienDaThanhToan)

if __name__ == "__main__":

    khoan_vay = KhoanVay(
        id="KV001",
        soTien=1000000,
        mucDichVay="Mua sắm",
        laiSuat=5.0,
        ngayBatDau = datetime(2023, 1, 1),
        ngayDenHan = datetime(2023, 12, 31),
    )
    # Lãi suất
    print("Lãi suất phải chi trả:", khoan_vay.tinhLai())
    # Thêm thanh toán
    khoan_vay.themThanhToan(soTien = 200000, ngayThanhToan = datetime(2023, 6, 15))
    khoan_vay.themThanhToan(soTien = 850000, ngayThanhToan = datetime(2023, 6, 18))
    print("Số tiền còn lại phải trả:", khoan_vay.laySoTienConLai())
    # Cập nhật trạng thái
    khoan_vay.capNhatTrangThai()
    print("Trạng thái khoản vay:", khoan_vay.trangThai)
