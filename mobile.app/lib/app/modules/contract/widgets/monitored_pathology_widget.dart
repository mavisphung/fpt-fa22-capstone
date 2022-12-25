import 'package:flutter/material.dart';
import 'package:flutter_phosphor_icons/flutter_phosphor_icons.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/models/pathology.dart';
import 'package:hi_doctor_v2/app/modules/contract/controllers/create_contract_controller.dart';
import 'package:hi_doctor_v2/app/modules/contract/widgets/pathology_extendable_row.dart';
import 'package:hi_doctor_v2/app/modules/contract/widgets/recommend_hr.dart';
import 'package:hi_doctor_v2/app/modules/health_record/controllers/health_record_controller.dart';
import 'package:hi_doctor_v2/app/modules/health_record/models/hr_res_model.dart';
import 'package:hi_doctor_v2/app/modules/health_record/widgets/pathology_textfield.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_elevate_btn_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_title_section.dart';
import 'package:hi_doctor_v2/app/modules/widgets/loading_widget.dart';

class MonitoredPathologyWidget extends StatelessWidget {
  final _cHealthRecord = Get.find<HealthRecordController>();
  final _c = Get.find<CreateContractController>();
  final _pTmpList = <Pathology>[];

  MonitoredPathologyWidget({super.key});

  final _sizedBox10 = const SizedBox(height: 10);
  final _sizedBox20 = const SizedBox(height: 20);
  final List<Map<String, dynamic>> _lCategory = [];

  void _categorizeDisease(HrResModel hr) {
    List? pList;
    if (hr.record!['isPatientProvided'] == true) {
      pList = hr.detail?['pathologies'];
    }
    if (pList?.isEmpty ?? true) return;
    for (var d in pList!) {
      final cate = _lCategory.firstWhereOrNull((e) => e['generalName'] == d['vGeneralName']);

      if (cate == null) {
        _lCategory.add({
          'generalName': d['vGeneralName'],
          'diseases': [
            {
              'id': d['id'],
              'code': d['code'],
              'otherCode': d['otherCode'],
              'generalName': d['vGeneralName'],
              'diseaseName': d['vDiseaseName'],
              'isChosen': false,
            },
          ],
        });
        continue;
      }
      final updatedCate = cate['diseases'] as List;
      final existedP = updatedCate.firstWhereOrNull((e) => e['diseaseName'] == d['vDiseaseName']);
      if (existedP == null) {
        updatedCate.add({
          'id': d['id'],
          'code': d['code'],
          'otherCode': d['otherCode'],
          'generalName': d['vGeneralName'],
          'diseaseName': d['vDiseaseName'],
          'isChosen': false,
        });
        continue;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return ObxValue<RxList<Pathology>>(
      (data) {
        if (data.isNotEmpty) {
          return Column(
            children: [
              CustomTitleSection(
                title: 'Các bệnh lý theo dõi đã chọn',
                suffixText: 'Chọn lại',
                suffixAction: () {
                  _c.lMonitoredPathology.clear();
                  _pTmpList.clear();
                  _c.rxPTmpListLength.value = 0;
                },
              ),
              ...data.map((e) => MonitoredPathologyRow(otherCode: e.otherCode, diseaseName: e.diseaseName)).toList(),
              Divider(color: AppColors.greyDivider, height: 30.sp),
            ],
          );
        }
        return GestureDetector(
          onTap: () => showModalBottomSheet(
            isScrollControlled: true,
            context: context,
            builder: (_) {
              _lCategory.clear();
              return Container(
                height: Get.height * 0.9,
                padding: EdgeInsets.symmetric(vertical: 20.sp, horizontal: Constants.padding.sp),
                decoration: BoxDecoration(
                  color: AppColors.grey200,
                  borderRadius: BorderRadius.only(topLeft: Radius.circular(8.sp), topRight: Radius.circular(8.sp)),
                ),
                child: Column(
                  children: [
                    PathologyTextField(
                      height: 60,
                      hasLabel: false,
                      onChoose: (result) {
                        _pTmpList.add(result);
                        _c.rxPTmpListLength.value = _pTmpList.length;
                        Get.back();
                      },
                    ),
                    _sizedBox10,
                    ObxValue<RxInt>(
                      (data) => data.value > 0
                          ? Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text('Danh sách bệnh lý bạn đã chọn từ khung tìm kiếm'),
                                ..._pTmpList
                                    .map((e) =>
                                        MonitoredPathologyRow(otherCode: e.otherCode, diseaseName: e.diseaseName))
                                    .toList()
                              ],
                            )
                          : const SizedBox.shrink(),
                      _c.rxPTmpListLength,
                    ),
                    _sizedBox20,
                    Expanded(
                      child: ObxValue<RxList<HrResModel>>(
                        (data) {
                          if (data.isNotEmpty) {
                            for (var hr in data) {
                              _categorizeDisease(hr);
                            }
                            if (_lCategory.isNotEmpty) {
                              return Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'Danh sách dưới đây tương ứng với những bệnh lý có trong hồ sơ từ hệ thống và hồ sơ ngoài hệ thống bạn đã thêm của bệnh nhân',
                                    textAlign: TextAlign.justify,
                                  ),
                                  Expanded(
                                    child: ListView.separated(
                                      itemBuilder: (_, index) {
                                        return PathologyExtendableRow(
                                          generalName: _lCategory[index]['generalName'],
                                          diseaseList: _lCategory[index]['diseases'] as List,
                                        );
                                      },
                                      separatorBuilder: (_, __) => const Divider(),
                                      itemCount: _lCategory.length,
                                    ),
                                  )
                                ],
                              );
                            }
                            return const SizedBox.shrink();
                          } else if (data.isEmpty) {
                            return const SizedBox.shrink();
                          }
                          return const LoadingWidget();
                        },
                        _cHealthRecord.allList,
                      ),
                    ),
                    const SizedBox(height: 20),
                    CustomElevatedButtonWidget(
                        textChild: 'Xong',
                        onPressed: () {
                          for (var c in _lCategory) {
                            final dList = c['diseases'] as List;
                            for (var d in dList) {
                              if (d['isChosen'] == true) {
                                _c.lMonitoredPathology.add(Pathology(
                                  id: d['id'],
                                  code: d['code'],
                                  otherCode: d['otherCode'],
                                  generalName: d['generalName'],
                                  diseaseName: d['diseaseName'],
                                ));
                              }
                            }
                          }
                          if (_pTmpList.isNotEmpty) _c.lMonitoredPathology.addAll(_pTmpList);
                          Get.back();
                        }),
                  ],
                ),
              );
            },
          ),
          child: Container(
            padding: EdgeInsets.all(Constants.padding.sp),
            decoration: BoxDecoration(
              color: AppColors.blue100,
              borderRadius: BorderRadius.circular(5.sp),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Chọn bệnh lý cần theo dõi',
                  style: TextStyle(
                    fontSize: 14.sp,
                    color: AppColors.primary,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Icon(PhosphorIcons.magnifying_glass_plus, color: AppColors.primary),
              ],
            ),
          ),
        );
      },
      _c.lMonitoredPathology,
    );
  }
}
