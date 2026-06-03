## 1. Mô tả chiến lược
* Chỉ báo:
    - EMA: EMA nhanh (9 phiên) và EMA chậm (26 phiên)
    - RSI: 14 phiên
* Điều kiện đặt lệnh:
    - Long: Xu hướng ngắn hạn cắt lên trung hạn (EMA 9 > EMA 26) và động lượng tăng vẫn còn (52 < RSI < 70)
    - Short: Khi xu hướng ngắn hạn cắt xuống trung hạn (EMA 9 < EMA 26) VÀ động lượng đang giảm vẫn còn (30 < RSI < 48).
    - Nếu ko thỏa mãn cả 2 yếu tố trên thì giữ nguyên lệnh cho đến khi xuất hiện tín hiệu đảo chiều

## 2. Các chỉ số đạt được
* Winrate 53.72%: khá tốt với chiến thuật đánh theo xu hướng
* Profit factor 1.44: cho thấy hệ thống có lợi nhuận
* Sharpe (1.86) và Sortino (3.11) khá cao cho thấy P/L tăng đều ít biến động
* Maximum drawdown -16.98% mức xụt giảm tài khoản khá cao.


## 3. Điểm mạnh
* Tối ưu độ trễ: Sử dụng EMA thay vì SMA giúp hệ thống phản ứng nhanh hơn với các biến động của thị trường
* Ít fomo: sử dụng RSI để lọc các tín hiệu đảo chiều đủ mạnh, còn động lượng để tăng/giảm tiếp để vào lệnh thay vì fomo theo xu hướng


## 4. Điểm yếu & rủi ro
* Không có cơ chế đứng ngoài: khi thị trường side way cố giữa lệnh sẽ khiến tài khoản bị mất nhiều phí giao dịch
* Thiếu quản trị rủi ro chủ động (SL/TP): Hệ thống chỉ đóng lệnh khi có tín hiệu ngược chiều. Do EMA có độ trễ nhất định khi xuất hiện tín hiệu giá thường đã đi được 1 đoạn gây mất 1 phần lợi nhuận và lỗ nặng hơn khi vào sai điểm

## 5. Đề xuất cải thiện
* Thêm SL/TP: Thay vì đợi EMA cắt ngược, thoát lệnh ngay lập tức nếu giá vi phạm đường EMA 26 hoặc sử dụng ATR để dời điểm TP theo giá.
* Bổ sung Bộ lọc Biến động: Thêm chỉ báo ADX hoặc ATR. Nếu biên độ thị trường (ATR) quá thấp, không mở vị thế dù EMA có cắt nhau.
* Thay đổi cơ chế giữ lệnh: Cho phép hệ thống đưa position về 0  nếu xu hướng bắt đầu suy yếu