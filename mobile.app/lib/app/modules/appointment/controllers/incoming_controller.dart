import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/common/util/enum.dart';
import 'package:hi_doctor_v2/app/data/api_response.dart';
import 'package:hi_doctor_v2/app/data/response_model.dart';
import 'package:hi_doctor_v2/app/models/appointment.dart';
import 'package:hi_doctor_v2/app/models/paging.dart';
import 'package:hi_doctor_v2/app/modules/appointment/providers/api_appointment.dart';

class IncomingController extends GetxController {
  late final ScrollController scrollController;
  RxList<Appointment> incomingList = <Appointment>[].obs;
  Rx<Status> loadingStatus = Status.init.obs;
  int _currentPendingPage = 1;
  int _currentInprogressPage = 1;
  int _totalPendingItems = 0;
  int _totalInprogressItems = 0;
  int _pendingItemsLength = 0;
  int _inprogressItemsLength = 0;

  late ApiAppointmentImpl apiAppointment;
  TextEditingController textController = TextEditingController();
  RxString rxReason = CancelReason.item1.obs;

  void clearIncomingList() {
    _currentPendingPage = 1;
    _currentInprogressPage = 1;
    _totalPendingItems = 0;
    _totalInprogressItems = 0;
    _pendingItemsLength = 0;
    _inprogressItemsLength = 0;
    incomingList.clear();
    update();
  }

  Future<void> getPendingAppointments({int page = 1, int limit = 10}) async {
    'loading pending appointments'.debugLog('IncomingTab');
    Response result = await apiAppointment.getUserIncomingAppointments(page: page, limit: limit);
    var response = ApiResponse.getResponse(result); // Map
    PagingModel pageModel = PagingModel.fromMap(response);

    _totalPendingItems = pageModel.totalItems ?? 0;
    if (pageModel.nextPage != null) {
      _currentPendingPage = pageModel.nextPage!;
    }
    response[Constants.currentPage].toString().debugLog('Current Page');
    ResponseModel2 model = ResponseModel2.fromMap(response);
    var data = model.data as List<dynamic>;
    incomingList.value += data.map((e) => Appointment.fromMap(e)).toList();

    _pendingItemsLength += data.length;
    data.length.toString().debugLog('PENDING items in list');
    update();
  }

  Future<void> getInProgressAppointments({int page = 1, int limit = 10}) async {
    'loading in progress appointments'.debugLog('IncomingTab');
    Response result = await apiAppointment.getUserIncomingAppointments(
        page: page, limit: limit, status: AppointmentStatus.inProgress.value);
    var response = ApiResponse.getResponse(result); // Map
    PagingModel pageModel = PagingModel.fromMap(response);

    _totalInprogressItems = pageModel.totalItems ?? 0;
    if (pageModel.nextPage != null) {
      _currentInprogressPage = pageModel.nextPage!;
    }
    response[Constants.currentPage].toString().debugLog('Current Page');
    ResponseModel2 model = ResponseModel2.fromMap(response);
    var data = model.data as List<dynamic>;
    incomingList.value += data.map((e) => Appointment.fromMap(e)).toList();

    _inprogressItemsLength += data.length;
    data.length.toString().debugLog('IN_PROGRESS items in list');
    update();
  }

  Future<bool> cancelAppointment(int appId, String reason) async {
    var response = await apiAppointment.cancelAppointment(appId, reason);
    response.body.toString().debugLog('IncomingController#cancelAppointment: ');
    if (response.isOk) {
      incomingList.removeWhere((element) => element.id == appId);
      update();
    }
    return response.isOk == true;
  }

  void loadMore() {
    loadingStatus.value = Status.loading;
    update();
  }

  void complete() {
    loadingStatus.value = Status.success;
    update();
  }

  bool validateCancelReason() {
    loadMore();
    return textController.text.isNotEmpty;
  }

  void init() async {
    loadMore();
    await getPendingAppointments(page: 1, limit: 10);
    await getInProgressAppointments(page: 1, limit: 10);
    complete();
  }

  @override
  void onInit() {
    super.onInit();
    apiAppointment = Get.put(ApiAppointmentImpl());
    scrollController = ScrollController();
    scrollController.addListener(
      () async {
        if (scrollController.position.maxScrollExtent == scrollController.offset) {
          if (incomingList.length >= (_totalPendingItems + _totalInprogressItems)) return;
          loadMore();
          if (_totalPendingItems > _pendingItemsLength) {
            await getPendingAppointments(page: _currentPendingPage);
          }
          if (_totalInprogressItems > _inprogressItemsLength) {
            await getInProgressAppointments(page: _currentInprogressPage);
          }
          complete();
        }
      },
    );
    init();
  }

  @override
  void dispose() {
    incomingList.close();
    apiAppointment.dispose();
    scrollController.dispose();
    textController.dispose();
    rxReason.close();
    super.dispose();
  }
}
