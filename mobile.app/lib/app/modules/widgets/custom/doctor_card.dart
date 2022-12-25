import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';

import 'package:hi_doctor_v2/app/common/util/transformation.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_card.dart';
import 'package:hi_doctor_v2/app/modules/widgets/image_container.dart';

class DoctorCard extends StatelessWidget {
  final String? avatar;
  final String? firstName;
  final String? lastName;
  final String? specialist;
  final String? address;

  const DoctorCard(
      {super.key,
      required this.avatar,
      required this.firstName,
      required this.lastName,
      required this.specialist,
      required this.address});

  @override
  Widget build(BuildContext context) {
    return CustomCard(
      child: Row(
        children: [
          ImageContainer(
            width: 120,
            height: 120,
            imgUrl: avatar,
            borderRadius: 10,
          ),
          Expanded(
            child: Container(
              padding: EdgeInsets.only(left: 15.sp),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    Tx.getDoctorName(lastName, firstName),
                    style: TextStyle(
                      fontSize: 15.sp,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  Divider(
                    color: AppColors.greyDivider,
                    thickness: 0.3.sp,
                  ),
                  Text(
                    specialist ?? '',
                    style: TextStyle(fontSize: 11.5.sp),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 5.sp),
                    child: Text(
                      address ?? '',
                      style: TextStyle(
                        fontSize: 11.5.sp,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class DoctorCard2 extends StatelessWidget {
  final String? avatar;
  final String? firstName;
  final String? lastName;
  final double? totalPoints;
  final int? ratingTurns;
  final String? address;

  const DoctorCard2({
    super.key,
    required this.avatar,
    required this.firstName,
    required this.lastName,
    required this.totalPoints,
    required this.ratingTurns,
    required this.address,
  });

  @override
  Widget build(BuildContext context) {
    return CustomCard(
      child: Row(
        children: [
          ImageContainer(
            width: 120,
            height: 120,
            imgUrl: avatar,
            borderRadius: 10,
          ),
          Expanded(
            child: Container(
              padding: EdgeInsets.only(left: 15.sp),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    Tx.getDoctorName(lastName, firstName),
                    style: TextStyle(
                      fontSize: 15.sp,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  Divider(
                    color: AppColors.greyDivider,
                    thickness: 0.3.sp,
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 5.sp),
                    child: Text(
                      address ?? '',
                      style: TextStyle(
                        fontSize: 11.5.sp,
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 8.sp),
                    child: Row(
                      children: [
                        SvgPicture.asset(
                          'assets/icons/star.svg',
                          width: 15.sp,
                          height: 15.sp,
                        ),
                        SizedBox(width: 6.sp),
                        Text(
                          '${totalPoints ?? 0.0}',
                          style: TextStyle(
                            fontSize: 12.sp,
                          ),
                        ),
                        Text(
                          ' (${ratingTurns ?? 0} bình luận)',
                          style: TextStyle(
                            fontSize: 12.sp,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
