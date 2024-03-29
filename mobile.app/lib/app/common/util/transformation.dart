import 'package:intl/intl.dart';

import 'package:hi_doctor_v2/app/models/user_info.dart';
import 'package:hi_doctor_v2/app/common/values/strings.dart';

class Tx {
  static String getFullName(String? lastName, String? firstName) {
    return '$lastName $firstName';
  }

  static String getDoctorName(String? lastName, String? firstName) {
    return '${Strings.doctor} $lastName $firstName';
  }

  static String getPathologyString(String? code, String? name) {
    return '$code - $name';
  }

  static List<String> getPathologyCodeName(String codeName) {
    return codeName.split(' - ');
  }

  static String getAge(String ymd) {
    try {
      final dob = DateFormat('yyyy-MM-dd').parse(ymd);
      final now = DateTime.now();

      if (dob.year == now.year) {
        return '${now.month - dob.month} tháng';
      } else if (dob.month > now.month || (dob.month == now.month && dob.day > now.day)) {
        return '${now.year - dob.year - 1}';
      } else {
        return '${now.year - dob.year}';
      }
    } catch (e) {
      return '';
    }
  }

  static String getDateString(DateTime date) {
    final String day = date.day < 10 ? '0${date.day}' : '${date.day}';
    final String month = date.month < 10 ? '0${date.month}' : '${date.month}';
    return 'ngày $day tháng $month, năm ${date.year}';
  }

  static String getGender(String gender) {
    final index = userGender.indexWhere((e) => e['value'] == gender);
    if (index > -1) {
      return userGender[index]['label'] ?? '';
    }
    return '';
  }

  static String getParsedDateString(String? date) {
    if (date == null) return '';
    final parsedDate = DateTime.tryParse(date);
    if (parsedDate == null) return '';
    return DateFormat('dd-MM-yyyy').format(parsedDate);
  }

  static String formatPrice(double price) {
    return NumberFormat.decimalPattern('vi,VN').format(price);
  }
}
