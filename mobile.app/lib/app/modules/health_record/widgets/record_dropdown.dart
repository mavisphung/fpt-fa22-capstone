import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/modules/health_record/controllers/edit_health_record_controller.dart';
import 'package:hi_doctor_v2/app/modules/health_record/controllers/health_record_controller.dart';

class RecordDropDown extends StatelessWidget {
  final _cEditOtherHealthRecord = Get.put(EditOtherHealthRecordController());
  final _cHealthRecord = Get.find<HealthRecordController>();

  RecordDropDown({super.key});

  @override
  Widget build(BuildContext context) {
    final recordId = _cEditOtherHealthRecord.recordId;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: EdgeInsets.only(
            left: 19.sp,
            bottom: 1.sp,
          ),
          child: Text(
            'Loại phiếu',
            style: DefaultTextStyle.of(context).style.copyWith(
                  fontSize: 11.5.sp,
                  color: Colors.grey[600],
                ),
          ),
        ),
        FutureBuilder(
          future: _cHealthRecord.getInstructionType(),
          builder: (_, AsyncSnapshot<bool> snapshot) {
            if (snapshot.hasData && snapshot.data == true) {
              if (_cHealthRecord.lInstructionType.isNotEmpty) {
                return Container(
                  padding: EdgeInsets.symmetric(
                    vertical: 3.sp,
                    horizontal: Constants.padding.sp,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.whiteHighlight,
                    borderRadius: BorderRadius.circular(Constants.textFieldRadius.sp),
                  ),
                  child: ObxValue<RxInt>(
                    (data) => DropdownButton<int>(
                      value: data.value,
                      isExpanded: true,
                      underline: const SizedBox.shrink(),
                      hint: const Text('Loại phiếu'),
                      borderRadius: BorderRadius.circular(10.sp),
                      items: _cHealthRecord.lInstructionType.map((item) {
                        return DropdownMenuItem<int>(
                          value: item.id,
                          child: Text(item.name ?? ''),
                        );
                      }).toList(),
                      onChanged: (value) {
                        data.value = value ?? -1;
                      },
                      iconSize: 29.sp,
                      iconEnabledColor: Colors.blueGrey,
                      icon: const Icon(Icons.arrow_drop_down_rounded),
                    ),
                    recordId,
                  ),
                );
              } else {
                return const SizedBox.shrink();
              }
            } else if (snapshot.hasData && snapshot.data == false) {
              return const SizedBox.shrink();
            } else if (snapshot.connectionState == ConnectionState.none) {
              return const SizedBox.shrink();
            }
            return const SizedBox.shrink();
          },
        ),
      ],
    );
  }
}
