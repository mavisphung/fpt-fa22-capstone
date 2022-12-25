import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/modules/appointment/models/filter_model.dart';
import 'package:hi_doctor_v2/app/modules/appointment/providers/api_appointment.dart';

class AppointmentController extends GetxController {
  List<AppointmentType> types = AppointmentType.values;
  List<AppointmentStatus> statuses = AppointmentStatus.values;

  Rx<FilterModel> filterModel = FilterModel(
    type: AppointmentType.all.value,
    status: AppointmentStatus.all.value,
    isTypeChosen: false,
    isStatusChosen: false,
  ).obs;
  RxBool isOnline = true.obs;
  Rx<AppointmentType> selectedTypeObx = AppointmentType.all.obs;
  Rx<AppointmentStatus> selectedStatusObx = AppointmentStatus.all.obs;
  // scroll controller

  late ApiAppointmentImpl apiAppointment;

  void setFilterType(String type) {
    filterModel.value.type = type;
  }

  FilterModel get filter => filterModel.value;

  AppointmentType get selectedType => selectedTypeObx.value;

  void setAppointmentType(AppointmentType type) {
    selectedTypeObx.value = type;
    update();
  }

  AppointmentStatus get selectedStatus => selectedStatusObx.value;

  void setAppointmentStatus(AppointmentStatus status) {
    selectedStatusObx.value = status;
    update();
  }

  @override
  void onInit() {
    super.onInit();
    apiAppointment = Get.put(ApiAppointmentImpl());
  }

  @override
  void dispose() {
    filterModel.close();
    selectedTypeObx.close();
    selectedStatusObx.close();
    apiAppointment.dispose();
    super.dispose();
  }
}
