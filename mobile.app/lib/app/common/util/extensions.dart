import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/storage/storage.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/common/values/strings.dart';
import 'package:hi_doctor_v2/app/data/api_response.dart';
import 'package:hi_doctor_v2/app/data/errors/api_error.dart';
import 'package:hi_doctor_v2/app/data/response_model.dart';
import 'package:hi_doctor_v2/app/routes/app_pages.dart';

extension FutureExt<T> on Future<Response<T>> {
  Future<ResponseModel1?> futureValue({
    Function(String? error)? onError,
    VoidCallback? retryFunction,
  }) async {
    return await timeout(
      Constants.timeout,
      onTimeout: () {
        throw ApiError(
          type: ErrorType.connectTimeout,
          error: Strings.conTimeOutMsg,
        );
      },
    ).then((value) {
      final responseBody = ApiResponse.getResponse<T>(value);
      // print('RESPONSE BODY: $responseBody');
      if (responseBody != null) {
        final responseModel1 = ResponseModel1.fromJson(responseBody as Map<String, dynamic>);
        return responseModel1;
      }
    }).catchError((e) {
      if (e == null) return null;

      final errorMessage = e is ApiError ? e.message : e.toString();

      if (e is ApiError) {
        if (e.type == ErrorType.connectTimeout) {
          Utils.showBottomSnackbar(errorMessage);
        } else if (e.type == ErrorType.noConnection) {
          Utils.showAlertDialog(errorMessage);
        } else if (e.type == ErrorType.unauthorized) {
          if (e.message == 'AUTHENTICATION_FAILED') {
            Utils.showTopSnackbar(Strings.loginFailedMsg, title: Strings.verification);
            return null;
          }
          Storage.clearStorage();
          Get.offAllNamed(Routes.LOGIN);
          // change the ROUTE to the LOGIN or SPLASH screen so that the
          // user can login again on UnauthorizeError error
        } else if (onError == null) {
          Utils.showAlertDialog(errorMessage);
        }
      }

      if (onError != null) {
        onError(errorMessage);
      }

      printError(info: 'catchError: $e\nerrorMessage: $errorMessage');
    });
  }
}

enum Gender { init, male, female, other }

List<Gender> genders = [Gender.male, Gender.female, Gender.other];

extension GenderExt on Gender {
  String get value {
    switch (this) {
      case Gender.male:
        return 'MALE';
      case Gender.female:
        return 'FEMALE';
      case Gender.init:
        return 'INIT';
      default:
        return 'OTHER';
    }
  }
}

extension GenderExt2 on Gender {
  String get label {
    switch (this) {
      case Gender.male:
        return 'Nam';
      case Gender.female:
        return 'Nữ';
      case Gender.init:
        return 'Init';
      default:
        return 'Khác';
    }
  }
}

enum AppointmentType { all, atPatientHome, atDoctorHome, contract, online }

extension AppointmentTypeExt on AppointmentType {
  String get value {
    switch (this) {
      case AppointmentType.online:
        return 'ONLINE';
      case AppointmentType.atPatientHome:
        return 'AT_PATIENT_HOME';
      case AppointmentType.atDoctorHome:
        return 'AT_DOCTOR_HOME';
      case AppointmentType.contract:
        return 'CONTRACT';
      default:
        return 'ALL';
    }
  }
}

extension AppointmentTypeExt2 on AppointmentType {
  String get label {
    switch (this) {
      case AppointmentType.online:
        return 'Online';
      case AppointmentType.atPatientHome:
        return 'Tại nhà bệnh nhân';
      case AppointmentType.atDoctorHome:
        return 'Tại nhà bác sĩ';
      case AppointmentType.contract:
        return 'Hợp đồng';
      default:
        return '';
    }
  }
}

enum AppointmentStatus { all, pending, completed, cancelled, inProgress }

extension AppointmentStatusExt on AppointmentStatus {
  String get value {
    switch (this) {
      case AppointmentStatus.pending:
        return 'PENDING';
      case AppointmentStatus.completed:
        return 'COMPLETED';
      case AppointmentStatus.cancelled:
        return 'CANCELLED';
      case AppointmentStatus.inProgress:
        return 'IN_PROGRESS';
      default:
        return 'ALL';
    }
  }
}

extension AppointmentStatusExt2 on AppointmentStatus {
  String get label {
    switch (this) {
      case AppointmentStatus.pending:
        return 'Đang chờ';
      case AppointmentStatus.completed:
        return 'Đã hoàn thành';
      case AppointmentStatus.cancelled:
        return 'Đã hủy';
      case AppointmentStatus.inProgress:
        return 'Đang tiến hành';
      default:
        return 'Tất cả';
    }
  }
}

extension StringToEnum on String {
  AppointmentType get enumType {
    switch (this) {
      case 'ONLINE':
        return AppointmentType.online;
      case 'AT_PATIENT_HOME':
        return AppointmentType.atPatientHome;
      case 'AT_DOCTOR_HOME':
        return AppointmentType.atDoctorHome;
      case 'CONTRACT':
        return AppointmentType.contract;
      default:
        return AppointmentType.all;
    }
  }

  AppointmentStatus get enumStatus {
    switch (this) {
      case 'PENDING':
        return AppointmentStatus.pending;
      case 'COMPLETED':
        return AppointmentStatus.completed;
      case 'CANCELLED':
        return AppointmentStatus.cancelled;
      case 'IN_PROGRESS':
        return AppointmentStatus.inProgress;
      default:
        return AppointmentStatus.all;
    }
  }
}

extension DebugLog on String {
  void debugLog(String title) {
    return debugPrint(
      '\n********************************** DebugLog **********************************\n'
      ' $title: $this'
      '\n********************************** DebugLog **********************************\n',
      wrapWidth: 1024,
    );
  }
}

extension DateTimeConverter on DateTime {
  static const Map<int, int> weekdays = {
    DateTime.sunday: 1,
    DateTime.monday: 2,
    DateTime.tuesday: 3,
    DateTime.wednesday: 4,
    DateTime.thursday: 5,
    DateTime.friday: 6,
    DateTime.saturday: 7,
  };
  int getWeekday() {
    return weekdays[weekday]!;
  }
}

extension StringExt on String {
  List<String> splitByLength(int length) => [substring(0, length), substring(length)];
}
