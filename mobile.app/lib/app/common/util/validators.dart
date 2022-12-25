import 'package:hi_doctor_v2/app/common/values/strings.dart';
import 'package:intl/intl.dart';

abstract class Validators {
  static String? validateEmpty(String? value) {
    if (value == null || value.isEmpty) {
      return Strings.fieldCantBeEmpty;
    }
    return null;
  }

  static String? validateEmail(String? value, bool isEmailDuplicated) {
    const pattern =
        r'^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$';
    if (value == null || value.isEmpty) {
      return Strings.emailCantBeEmpty;
    } else if (!RegExp(pattern).hasMatch(value)) {
      return Strings.enterValidEmail;
    } else if (isEmailDuplicated) {
      return Strings.duplicatedEmail;
    }
    return null;
  }

  static String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return Strings.passCantBeEmpty;
    } else if (value.length < 6) {
      return Strings.passLengthtMsg;
    }
    return null;
  }

  static String? validateConfirmPassword(String? confirmPassword, String? password) {
    if (confirmPassword == null || confirmPassword.isEmpty) {
      return Strings.confirmPassCantBeEmpty;
    } else if (confirmPassword.length < 6) {
      return Strings.confirmPassLengthtMsg;
    } else if (confirmPassword != (password ?? '')) {
      return Strings.confirmPassNotMatchMsg;
    }
    return null;
  }

  static String? validatePhone(String? value) {
    if (value == null || value.isEmpty) {
      return Strings.fieldCantBeEmpty;
    } else if (value.length != 10) {
      return Strings.enterValidPhone;
    }
    return null;
  }

  static bool isAdult(String dob) {
    final dobDate = DateFormat('dd-MM-yyyy').parse(dob);
    final now = DateTime.now();
    int yearDiff = now.year - dobDate.year;
    int monthDiff = now.month - dobDate.month;
    int dayDiff = now.day - dobDate.day;

    return yearDiff > 18 || (yearDiff == 18 && monthDiff >= 0 && dayDiff >= 0);
  }

  static bool isAdultUnder60(String dob) {
    final dobDate = DateFormat('dd-MM-yyyy').parse(dob);
    final now = DateTime.now();
    int yearDiff = now.year - dobDate.year;
    int monthDiff = now.month - dobDate.month;
    int dayDiff = now.day - dobDate.day;

    return (yearDiff > 18 || (yearDiff == 18 && monthDiff >= 0 && dayDiff >= 0)) && yearDiff < 60;
  }
}
