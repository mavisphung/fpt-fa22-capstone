import 'package:flutter/material.dart';
import 'package:hi_doctor_v2/app/modules/contract/widgets/recommend_hr.dart';
import 'package:hi_doctor_v2/app/modules/widgets/content_container.dart';

class DiagnoseContainer extends StatelessWidget {
  final List diagnoses;
  const DiagnoseContainer({super.key, required this.diagnoses});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const ContentTitle1(title: 'Chẩn đoán'),
        ...diagnoses.map((e) {
          String? diseaseName;
          diseaseName = e['diseaseName'];
          diseaseName ??= e['vDiseaseName'];
          return MonitoredPathologyRow(otherCode: e['code'], diseaseName: diseaseName);
        }),
      ],
    );
  }
}
