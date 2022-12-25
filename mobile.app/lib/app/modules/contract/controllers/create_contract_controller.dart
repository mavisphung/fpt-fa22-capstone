import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';

import 'package:hi_doctor_v2/app/common/util/enum.dart';
import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/models/doctor.dart';
import 'package:hi_doctor_v2/app/models/pathology.dart';
import 'package:hi_doctor_v2/app/models/patient.dart';
import 'package:hi_doctor_v2/app/modules/contract/providers/api_contract.dart';

class CreateContractController extends GetxController {
  final _apiContract = Get.put(ApiContract());
  final lMonitoredPathology = <Pathology>[].obs;
  List<int> lInstruction = [];
  List<int> lOtherInstruction = [];
  final lPrescription = <int>[].obs;

  final status = Status.init.obs;
  final rxAgreedStatus = false.obs;

  late Doctor doctor;
  final rxPatient = Rxn<Patient>();
  final rxRecordId = 1.obs;
  final rxPTmpListLength = 0.obs;

  final contractNoteController = TextEditingController();
  final startDateController = TextEditingController();
  Rx<DateTime> rxSelectedDate = DateTime.now().add(const Duration(days: 5)).obs;

  Future<bool?> createContract() async {
    status.value = Status.loading;
    final lDisease = lMonitoredPathology
        .map((e) => {
              'code': e.code,
              'generalName': e.generalName,
              'diseaseName': e.diseaseName,
            })
        .toList();
    final startDate = DateFormat('yyyy-MM-dd').format(rxSelectedDate.value);
    final endDate = DateFormat('yyyy-MM-dd').format(rxSelectedDate.value.add(const Duration(days: 7)));

    final sharedInstructions = lInstruction + lOtherInstruction;

    final reqModel = {
      "patient": rxPatient.value!.id,
      "doctor": doctor.id,
      "package": 1,
      "startedAt": startDate,
      "endedAt": endDate,
      "detail": {
        "allergies": [],
        "socialHistory": [],
        "pathologies": [],
        "diseases": lDisease,
      },
      "prescriptions": [],
      "instructions": sharedInstructions,
    };
    print('REGMODEL: ${reqModel.toString()}');
    final response = await _apiContract.postContract(reqModel).futureValue();

    if (response != null) {
      if (response.isSuccess == true) {
        status.value = Status.success;
        return true;
      } else {
        status.value = Status.fail;
        return false;
      }
    }
    status.value = Status.fail;
    return null;
  }

  @override
  void dispose() {
    lMonitoredPathology.clear();
    lMonitoredPathology.close();
    lInstruction.clear();
    lOtherInstruction.clear();
    lPrescription.clear();
    lPrescription.close();
    status.close();
    rxAgreedStatus.close();
    rxPatient.close();
    rxRecordId.close();
    rxPTmpListLength.close();
    contractNoteController.dispose();
    startDateController.dispose();
    super.dispose();
  }
}
