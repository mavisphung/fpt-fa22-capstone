import 'package:flutter/material.dart';

import 'package:hi_doctor_v2/app/modules/contract/widgets/recommend_hr.dart';
import 'package:hi_doctor_v2/app/modules/widgets/content_container.dart';

class ContractStep2 extends StatelessWidget {
  const ContractStep2({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const ContentTitle1(title: 'Chia sẻ phiếu y lệnh', topPadding: 0, bottomPadding: 8),
        RecommendHr(),
      ],
    );
  }
}
