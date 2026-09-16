# DATA-333 — Auto Thần Long debug/tool knowledge base

Repository này lưu **tri thức đã materialize từ bộ Debug của tool auto**, theo hướng tương tự DATA-2222 nhưng tập trung vào **tool-side behavior** thay vì client-side runtime.

Nguồn phân tích ban đầu: bộ Debug chứa executable .NET/WPF, PDB, KAutoHelper, OpenCV/EmguCV, Tesseract, ADB libraries và các template ảnh điều khiển UI.

## Mục tiêu

- lập bản đồ class/module và dependency;
- mô tả đường kết nối emulator/device;
- mô tả primitive điều khiển ADB/Win32;
- mô tả pipeline capture -> image matching/OCR -> action;
- materialize feature/state/config của tool;
- tạo cầu nối giữa behavior của auto (DATA-333) và semantic client knowledge (DATA-2222);
- giữ provenance/evidence level để tránh suy luận bị nâng thành fact.

> Không commit credential/token/license key lấy từ Debug vào repository. Chỉ lưu schema, fingerprint và fact đã được redaction.
