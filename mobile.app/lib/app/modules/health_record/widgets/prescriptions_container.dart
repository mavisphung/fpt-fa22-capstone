import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import 'package:hi_doctor_v2/app/modules/widgets/content_container.dart';

class PrescriptionContainer extends StatelessWidget {
  final List prescriptions;
  const PrescriptionContainer({super.key, required this.prescriptions});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const ContentTitle1(title: 'Đơn thuốc', leftPadding: 5, bottomPadding: 5),
        Container(
          padding: EdgeInsets.symmetric(vertical: 8.sp, horizontal: 10.sp),
          decoration: BoxDecoration(
            color: const Color(0xFFDAFFEF),
            borderRadius: BorderRadius.circular(5.sp),
          ),
          child: Column(
            children: prescriptions
                .map((e) => ContentRow(
                      verPadding: 10,
                      content: {
                        'Loại thuốc': e['medicine'],
                        'Số lượng': e['quantity'].toString(),
                        'Đơn vị': e['unit'],
                        'Cách dùng': e['usage'],
                      },
                      labelWidth: 100,
                      labelStyle: const TextStyle(fontWeight: FontWeight.w500),
                    ))
                .toList(),
          ),
        ),
      ],
    );
  }
}
