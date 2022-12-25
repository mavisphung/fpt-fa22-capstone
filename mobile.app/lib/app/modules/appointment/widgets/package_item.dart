import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/util/transformation.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/modules/appointment/controllers/booking/booking_controller.dart';

// ignore: constant_identifier_names
enum CategoryType { AT_DOCTOR_HOME, AT_PATIENT_HOME, ONLINE }

class PackageItem extends StatelessWidget {
  final int id;
  final String name;
  final String description;
  final double price;
  final String? category;

  PackageItem({
    Key? key,
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.category,
  }) : super(key: key);

  final _c = Get.find<BookingController>();

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.whiteHighlight,
        borderRadius: BorderRadius.circular(Constants.borderRadius.sp),
      ),
      margin: EdgeInsets.only(bottom: 20.sp),
      padding: EdgeInsets.symmetric(horizontal: 16.sp, vertical: 16.sp),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 14.sp,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(
                  height: 10.sp,
                ),
                Text(
                  description,
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 12.sp,
                  ),
                ),
                SizedBox(
                  height: 10.sp,
                ),
                Text(
                  category!.toString().enumType.label,
                  style: TextStyle(
                    color: AppColors.secondary,
                    fontSize: 15.sp,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
          SizedBox(
            width: 8.sp,
          ),
          Text(
            Tx.formatPrice(price),
            style: TextStyle(
              color: AppColors.primary,
              fontSize: 16.sp,
              fontWeight: FontWeight.w500,
              fontFamily: 'OpenSans',
            ),
          ),
          ObxValue<RxInt>(
            (data) => Radio(
              onChanged: (int? value) {
                if (value != null) {
                  _c.setServiceId(value);
                }
              },
              value: id,
              groupValue: data.value,
            ),
            _c.rxServiceId,
          ),
        ],
      ),
    );
  }
}
