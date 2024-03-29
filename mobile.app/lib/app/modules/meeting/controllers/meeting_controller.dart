import 'package:get/get.dart';
import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/util/extensions.dart';

import 'package:hi_doctor_v2/app/models/appointment.dart';
import 'package:hi_doctor_v2/app/modules/meeting/providers/api_meeting.dart';

class MeetingController extends GetxController {
  final infoStr = <String>[].obs;
  final isLocalUserJoined = false.obs;
  final remoteId = RxnInt();
  final isMuted = false.obs;
  final isVideoDisabled = false.obs;

  final isAppointmentLoaded = false.obs;

  late Appointment _appointment;
  Appointment get appointment => _appointment;

  late ApiMeeting _provider;

  Future<bool?> getAppointmentDetail(int id) async {
    isAppointmentLoaded.value = false;
    final response = await _provider.getAppointmentWithId(id).futureValue();
    if (response != null && response.isSuccess && response.statusCode == Constants.successGetStatusCode) {
      _appointment = Appointment.fromMap(response.data);
      isAppointmentLoaded.value = true;
      return true;
    } else if (response != null && !response.isSuccess) {
      return false;
    }
    return null;
  }

  Future<Map<String, String>?> getChannelEntry() async {
    final response = await _provider.getAgoraChannelToken().futureValue();
    if (response != null && response.isSuccess && response.statusCode == Constants.successGetStatusCode) {
      response.data.toString().debugLog('MeetingController');
      final String? channelName = response.data['channel'];
      final String? token = response.data['token'];
      if (channelName != null && token != null) {
        return {
          'channelId': channelName,
          'token': token,
        };
      }
    }
    return null;
  }

  @override
  void onInit() {
    super.onInit();
    _provider = Get.put(ApiMeeting());
  }

  @override
  void dispose() {
    infoStr.close();
    isLocalUserJoined.close();
    remoteId.close();
    isMuted.close();
    isVideoDisabled.close();
    isAppointmentLoaded.close();
    _provider.dispose();
    super.dispose();
  }
}
