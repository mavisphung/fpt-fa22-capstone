import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/common/util/enum.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/data/api_response.dart';
import 'package:hi_doctor_v2/app/data/custom_controller.dart';
import 'package:hi_doctor_v2/app/data/response_model.dart';
import 'package:hi_doctor_v2/app/models/patient.dart';
import 'package:hi_doctor_v2/app/models/user_info.dart';
import 'package:hi_doctor_v2/app/modules/settings/providers/api_settings_impl.dart';

class PatientProfileController extends GetxController {
  final firstNameFocusNode = FocusNode();
  final lastNameFocusNode = FocusNode();
  final addressFocusNode = FocusNode();
  final firstName = TextEditingController();
  final lastName = TextEditingController();
  final address = TextEditingController();
  final dob = TextEditingController();
  final gender = userGender.first['value']!.obs;
  final avatar = Constants.defaultAvatar.obs;
  final checkBoxStatus = false.obs;
  final checkBoxStatus1 = false.obs;
  final isAdultUnder60 = false.obs;

  RxList<Patient> patientList = <Patient>[].obs;

  final status = Status.init.obs;

  final _provider = Get.put(ApiSettingsImpl());
  final _cCustom = Get.put(CustomController());

  @override
  void onInit() {
    super.onInit();
    getPatientList();
  }

  @override
  void dispose() {
    firstNameFocusNode.dispose();
    lastNameFocusNode.dispose();
    addressFocusNode.dispose();
    firstName.dispose();
    lastName.dispose();
    address.dispose();
    dob.dispose();
    gender.close();
    avatar.close();
    checkBoxStatus.close();
    checkBoxStatus1.close();
    isAdultUnder60.close();
    patientList.clear();
    patientList.close();
    _provider.dispose();
    _cCustom.dispose();
    super.dispose();
  }

  Future<bool> emptyField() {
    firstName.text = '';
    lastName.text = '';
    dob.text = '';
    gender.value = userGender.first['value']!;
    address.text = '';
    avatar.value = Constants.defaultAvatar;
    return Future.value(true);
  }

  String? isEmpty(String? value) {
    if (value == null || value.isEmpty) {
      return null;
    }
    return null;
  }

  void setStatusLoading() {
    status.value = Status.loading;
    update();
  }

  void setStatusSuccess() {
    status.value = Status.success;
    update();
  }

  void setStatusFail() {
    status.value = Status.fail;
    update();
  }

  Future<bool?> getPatientList({int page = 1, int limit = 10}) async {
    setStatusLoading();
    final response = await _provider.getPatientList(page: page, limit: limit);

    Map<String, dynamic> result = ApiResponse.getResponse(response);
    ResponseModel2 model = ResponseModel2.fromMap(result);
    List<dynamic> data = model.data;

    if (model.success == true) {
      if (data.isNotEmpty) {
        patientList.value = data
            .map<Patient>(
              (e) => Patient(
                id: e['id'],
                firstName: e['firstName'],
                lastName: e['lastName'],
                dob: Utils.reverseDate(e['dob']),
                address: e['address'],
                gender: e['gender'],
                avatar: e['avatar'],
                supervisorId: e['supervisor_id'],
                oldOtherHealthRecords: e['old_health_records'],
              ),
            )
            .toList();
      }
      setStatusSuccess();
      return true;
    } else if (model.success == false) {
      setStatusFail();
      return false;
    }
    return null;
  }

  Future<bool> getPatientWithId(int id) async {
    final response = await _provider.getPatientProfile(id).futureValue();

    if (response != null && response.isSuccess == true) {
      final patient = Patient.fromMap(response.data);
      firstName.text = patient.firstName ?? '';
      lastName.text = patient.lastName ?? '';
      dob.text = Utils.reverseDate(patient.dob ?? '2000-10-24');
      if (patient.gender != null) {
        gender.value = patient.gender!;
      }
      address.text = patient.address ?? '';
      avatar.value = patient.avatar ?? '';
      return true;
    }
    return false;
  }

  void setAvatar(bool isFromCamera) async {
    final url = await _cCustom.getImage(isFromCamera);
    if (url != null) avatar.value = url;
  }

  void addPatientProfile() async {
    setStatusLoading();

    Patient data = Patient(
      firstName: firstName.text,
      lastName: lastName.text,
      dob: Utils.reverseDate(dob.text),
      address: address.text,
      gender: gender.value,
      avatar: avatar.value,
    );
    var response = await _provider.postPatientProfile(data).futureValue();
    if (response != null && response.isSuccess == true && response.statusCode == Constants.successPostStatusCode) {
      await getPatientList();
      setStatusSuccess();
      Get.back();
      Utils.showTopSnackbar('Thêm thành công');
    } else {
      Get.snackbar('Error ${response?.statusCode}', 'Error while adding profile', backgroundColor: Colors.red);
      setStatusFail();
    }
  }

  void updatePatientProfile(int patientId) async {
    setStatusLoading();

    Patient data = Patient(
      id: patientId,
      firstName: firstName.text,
      lastName: lastName.text,
      dob: Utils.reverseDate(dob.text),
      address: address.text,
      gender: gender.value,
      avatar: avatar.value,
    );
    var response = await _provider.putPatientProfile(patientId, data).futureValue();
    if (response != null && response.isSuccess == true) {
      await getPatientList();
      setStatusSuccess();
      Get.back();
      Utils.showTopSnackbar('Cập nhật hồ sơ thành công');
    } else {
      Get.snackbar('Error ${response?.statusCode}', 'Error while updating profile', backgroundColor: Colors.red);
      setStatusFail();
    }
  }
}
