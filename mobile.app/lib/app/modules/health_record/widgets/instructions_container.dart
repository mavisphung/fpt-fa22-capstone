import 'package:flutter/material.dart';
import 'package:flutter_phosphor_icons/flutter_phosphor_icons.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:hi_doctor_v2/app/modules/widgets/content_container.dart';

class InstructionContainer extends StatelessWidget {
  final List instructions;
  const InstructionContainer({super.key, required this.instructions});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const ContentTitle1(title: 'Y lệnh', leftPadding: 5, bottomPadding: 5),
        Container(
          padding: EdgeInsets.symmetric(vertical: 8.sp, horizontal: 10.sp),
          decoration: BoxDecoration(
            color: const Color(0xFFFFE4E4),
            borderRadius: BorderRadius.circular(5.sp),
          ),
          child: Column(
            children: instructions
                .map((e) => Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(e['category'], style: const TextStyle(fontWeight: FontWeight.w500)),
                            Icon(
                              PhosphorIcons.folder_notch_plus_light,
                              color: Colors.pink.shade700,
                              size: 32.sp,
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text('Trạng thái', style: TextStyle(fontWeight: FontWeight.w500)),
                            Text(e['status'] == 'COMPLETED' ? 'Đã hoàn thành' : 'Chưa hoàn thành'),
                          ],
                        ),
                      ],
                    ))
                .toList(),
          ),
        ),
      ],
    );
  }
}
