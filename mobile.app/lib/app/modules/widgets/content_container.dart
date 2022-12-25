import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';

class ContentContainer extends StatelessWidget {
  final Color? color;
  final Map<String, String> content;
  final double? verPadding;
  final double? hozPadding;
  final double labelWidth;
  final String? fontFamily;

  const ContentContainer({
    super.key,
    required this.labelWidth,
    required this.content,
    this.color,
    this.verPadding,
    this.hozPadding,
    this.fontFamily,
  });

  Widget _getRow(String key, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 5),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: labelWidth.sp,
            child: Text(
              key,
              style: TextStyle(
                fontWeight: FontWeight.w500,
                fontFamily: fontFamily,
              ),
            ),
          ),
          Expanded(
              child: Text(
            value,
            style: TextStyle(fontFamily: fontFamily),
          )),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.only(top: 5.sp),
      padding: EdgeInsets.symmetric(
        vertical: verPadding?.sp ?? Constants.padding.sp,
        horizontal: hozPadding?.sp ?? Constants.padding.sp,
      ),
      decoration: BoxDecoration(
        color: color ?? AppColors.grey200,
        borderRadius: BorderRadius.circular(5.sp),
      ),
      child: Column(
        children: content.entries.map((e) => _getRow(e.key, e.value)).toList(),
      ),
    );
  }
}

class ContentRow extends StatelessWidget {
  final Map<String, String> content;
  final double? verPadding;
  final double? hozPadding;
  final double labelWidth;
  final TextStyle? labelStyle;
  final TextStyle? valueStyle;
  final int? maxLines;

  const ContentRow({
    super.key,
    required this.content,
    this.verPadding,
    this.hozPadding,
    required this.labelWidth,
    this.labelStyle,
    this.valueStyle,
    this.maxLines,
  });

  Widget _getRow(String key, String value) {
    return Padding(
      padding: EdgeInsets.only(bottom: 10.sp),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: labelWidth.sp,
            child: Text(
              key,
              style: labelStyle,
            ),
          ),
          Expanded(
            child: Text(
              value,
              maxLines: maxLines ?? 2,
              overflow: TextOverflow.ellipsis,
              style: valueStyle,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(
        vertical: verPadding?.sp ?? 20.sp,
        horizontal: hozPadding?.sp ?? Constants.padding.sp,
      ),
      child: Column(
        children: content.entries.map((e) => _getRow(e.key, e.value)).toList(),
      ),
    );
  }
}

class ContentTitle1 extends StatelessWidget {
  final String title;
  final double? leftPadding;
  final double? topPadding;
  final double? bottomPadding;

  const ContentTitle1({
    super.key,
    required this.title,
    this.leftPadding,
    this.topPadding,
    this.bottomPadding,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        top: topPadding?.sp ?? 20.sp,
        left: leftPadding?.sp ?? 5.sp,
        bottom: bottomPadding?.sp ?? 0,
      ),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 15.sp,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }
}
