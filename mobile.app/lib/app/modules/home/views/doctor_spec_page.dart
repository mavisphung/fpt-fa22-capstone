import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:hi_doctor_v2/app/models/doctor.dart';
import 'package:hi_doctor_v2/app/modules/home/controllers/home_controller.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom/doctor_card.dart';
import 'package:hi_doctor_v2/app/modules/widgets/loading_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/my_appbar.dart';
import 'package:hi_doctor_v2/app/modules/widgets/response_status_widget.dart';

class DoctorBySpecPage extends StatelessWidget {
  final _homeController = Get.find<HomeController>();
  final specMap = Get.arguments as Map<String, dynamic>;
  DoctorBySpecPage({super.key});

  Future<bool?> getDoctorListBySpec() {
    if (specMap['id'] != null) {
      return _homeController.getDoctorListBySpecialist(specMap['id']);
    }
    return Future.value(false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const MyAppBar(title: ''),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 12.sp),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Danh sách bác sĩ chuyên khoa ${specMap["name"]}',
                style: const TextStyle(fontWeight: FontWeight.w500)),
            const SizedBox(height: 10),
            Expanded(
              child: FutureBuilder(
                future: getDoctorListBySpec(),
                builder: (_, AsyncSnapshot<bool?> snapshot) {
                  if (snapshot.hasData && snapshot.data == true) {
                    if (_homeController.doctorBySpecList.isNotEmpty) {
                      return ObxValue<RxList<Doctor>>(
                        (data) => ListView.separated(
                          itemCount: data.length,
                          itemBuilder: (_, index) {
                            var realDoctor = data[index];
                            return DoctorCard2(
                              avatar: realDoctor.avatar,
                              firstName: realDoctor.firstName,
                              lastName: realDoctor.lastName,
                              totalPoints: realDoctor.ratingPoints,
                              ratingTurns: realDoctor.ratingTurns,
                              address: realDoctor.address,
                            );
                          },
                          separatorBuilder: (_, __) => SizedBox(
                            height: 10.sp,
                          ),
                        ),
                        _homeController.doctorBySpecList,
                      );
                    } else {
                      return const NoDataWidget(message: 'Danh sách bác sĩ chuyên khoa này hiện đang trống.');
                    }
                  } else if (snapshot.hasData && snapshot.data == false) {
                    return const SystemErrorWidget();
                  } else if (snapshot.connectionState == ConnectionState.none) {
                    return const NoInternetWidget2();
                  }
                  return const LoadingWidget();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
