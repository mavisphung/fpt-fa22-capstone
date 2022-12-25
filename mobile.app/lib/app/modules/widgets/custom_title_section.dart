import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import 'package:hi_doctor_v2/app/common/values/colors.dart';

class CustomTitleSection extends StatelessWidget {
  final String title;
  final double paddingTop;
  final double paddingLeft;
  final double paddingBottom;
  final String? suffixText;
  final VoidCallback? suffixAction;
  final TextStyle? suffixTextStyle;
  final bool? withAsterisk;

  const CustomTitleSection({
    Key? key,
    required this.title,
    this.paddingTop = 15,
    this.paddingLeft = 5,
    this.paddingBottom = 5,
    this.suffixText,
    this.suffixAction,
    this.suffixTextStyle,
    this.withAsterisk,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: paddingLeft.sp,
        top: paddingTop.sp,
        bottom: paddingBottom.sp,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Row(
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 15.sp,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(width: 5),
              if (withAsterisk ?? false) Text('*', style: TextStyle(color: AppColors.error)),
            ],
          ),
          suffixText != null
              ? Padding(
                  padding: EdgeInsets.only(right: 8.sp),
                  child: GestureDetector(
                    onTap: suffixAction,
                    child: Text(
                      suffixText!,
                      style: TextStyle(
                        color: AppColors.primary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                )
              : const SizedBox.shrink(),
        ],
      ),
    );
  }
}
