export enum AppointmentStatus {
  CANCELLED = 'CANCELLED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  PENDING = 'PENDING',
}

export enum AppointmentType {
  OFFLINE = 'OFFLINE',
  ONLINE = 'ONLINE',
}

export const ServiceType = new Map<string, string>([
  ['AT_PATIENT_HOME', 'Đến nhà bệnh nhân'],
  ['AT_DOCTOR_HOME', 'Tại nơi làm việc của bác sĩ'],
  ['ONLINE', 'Trực tuyến'],
  ['CONTRACT', 'Hợp đồng theo dõi'],
]);

export const AppointmentStatusMap = new Map<string, string>([
  ['PENDING', 'Đang chờ'],
  ['IN_PROGRESS', 'Đang tiến hành'],
  ['COMPLETED', 'Đã hoàn thành'],
  ['CANCELLED', 'Đã hủy'],
  ['APPROVED', 'Đã duyệt'],
  ['SIGNED', 'Đã ký'],
]);

export const ServiceCategory = new Map<string, string>([
  ['Đến nhà bệnh nhân', 'AT_PATIENT_HOME'],
  ['Tại nơi làm việc của bác sĩ', 'AT_DOCTOR_HOME'],
  ['Trực tuyến', 'ONLINE'],
  ['Hợp đồng theo dõi', 'CONTRACT'],
]);

export const ContractStatusMap = new Map<string, string>([
  ['PENDING', 'Đang chờ'],
  ['IN_PROGRESS', 'Đang tiến hành'],
  ['COMPLETED', 'Đã hoàn thành'],
  ['CANCELLED', 'Đã hủy'],
  ['APPROVED', 'Đã duyệt'],
  ['SIGNED', 'Đã ký'],
]);

export const Gender = new Map<string, string>([
  ['MALE', 'Nam'],
  ['FEMALE', 'Nữ'],
  ['OTHER', 'Khác'],
]);

export const weekdayIdMap = new Map<string, string>([
  ['1', 'Chủ Nhật'],
  ['2', 'Thứ Hai'],
  ['3', 'Thứ Ba'],
  ['4', 'Thứ Tư'],
  ['5', 'Thứ Năm'],
  ['6', 'Thứ Sáu'],
  ['7', 'Thứ Bảy'],
]);
