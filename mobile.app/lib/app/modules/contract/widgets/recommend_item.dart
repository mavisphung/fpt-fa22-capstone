import 'package:flutter/material.dart';
import 'package:flutter_phosphor_icons/flutter_phosphor_icons.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/models/pathology.dart';
import 'package:hi_doctor_v2/app/modules/contract/controllers/create_contract_controller.dart';
import 'package:hi_doctor_v2/app/modules/contract/widgets/recommend_hr_extendable_row.dart';
import 'package:hi_doctor_v2/app/modules/health_record/controllers/health_record_controller.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_container.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_elevate_btn_widget.dart';

class RecommendItem extends StatefulWidget {
  final Pathology data;

  const RecommendItem({super.key, required this.data});

  @override
  State<RecommendItem> createState() => _RecommendItemState();
}

class _RecommendItemState extends State<RecommendItem> {
  final _c = Get.find<CreateContractController>();
  final _cHealthRecord = Get.find<HealthRecordController>();
  final List<Map<String, dynamic>> _lType = [];
  int _chosenLength = 0;

  void _groupRecordType() {
    for (var hr in _cHealthRecord.allList) {
      if (hr.record!['isPatientProvided'] == true) {
        print('HR: ${hr.toString()}');
        final pList = hr.detail!['pathologies'] as List;
        final pIndex = pList.indexWhere((e) => e['id'] == widget.data.id);
        if (pIndex != -1) {
          final iList = hr.detail!['instructions'] as List;
          for (var i in iList) {
            bool isTypeGenerated = false;
            final tmp1 = [];
            final tmp2 = [];
            tmp2.add({
              'info': {
                'id': i['id'],
                'content': i['submissions'],
              },
              'isChosen': false,
            });
            tmp1.add({
              'record': {
                'id': hr.record!['id'],
                'createdAt': hr.record!['createdAt'],
                'recordName': hr.record!['name'],
                'isPatientProvided': hr.record!['isPatientProvided'],
              },
              'instructions': tmp2,
            });

            final typeItem = _lType.firstWhere((e) => e['typeName'] == i['category'], orElse: () {
              isTypeGenerated = true;
              return {
                'typeName': i['category'],
                'details': tmp1,
              };
            });
            if (isTypeGenerated) {
              _lType.add(typeItem);
              continue;
            }

            final lDetails = typeItem['details'] as List;
            print('lDetails: ${lDetails.toString()}');
            final recordItem = lDetails.firstWhereOrNull((e) => e['record']['id'] == hr.record!['id']);
            print('RecordItem: ${recordItem.toString()}');
            if (recordItem == null) {
              (typeItem['details'] as List).addAll(tmp1);
              continue;
            }
            (recordItem['instructions'] as List).add({
              'info': {
                'id': i['id'],
                'content': i['submissions'],
              },
              'isChosen': false,
            });
          }
        }
      }
    }
  }

  void _showModalSheet(BuildContext ctx, Map<String, dynamic> map) {
    final details = map['details'] as List;
    showModalBottomSheet(
      isScrollControlled: true,
      context: ctx,
      builder: (_) {
        return Container(
          height: Get.height * 0.9,
          padding: EdgeInsets.symmetric(vertical: 30.sp, horizontal: Constants.padding.sp),
          decoration: BoxDecoration(
            color: AppColors.grey200,
            borderRadius: BorderRadius.only(topLeft: Radius.circular(8.sp), topRight: Radius.circular(8.sp)),
          ),
          child: Column(
            children: [
              Text('Danh sách ${map["typeName"]}'),
              Expanded(
                child: ListView.separated(
                  itemBuilder: (_, index) {
                    return ReccommendHrExtendableRow(map: details[index], instructionType: map["typeName"] as String);
                  },
                  separatorBuilder: (_, __) => const Divider(),
                  itemCount: details.length,
                ),
              ),
              CustomElevatedButtonWidget(
                textChild: 'Xong',
                onPressed: () {
                  _chosenLength = 0;
                  final chosenList = <int>[];
                  for (var item in _lType) {
                    final dList = item['details'] as List;
                    for (var d in dList) {
                      final iList = d['instructions'] as List;
                      for (var i in iList) {
                        if (i['isChosen'] == true) {
                          chosenList.add(i['info']['id']);
                          ++_chosenLength;
                        }
                      }
                    }
                  }
                  if (chosenList.isNotEmpty) _c.lInstruction = chosenList;

                  // final item5 = _lType.firstWhereOrNull((e) => e['typeId'] == 5);
                  // final dListItem5 = item5?['details'] as List?;
                  // if (dListItem5 != null) {
                  //   for (var d in dListItem5) {
                  //     final lPrescriptions = d['prescriptions'] as List?;
                  //     if (lPrescriptions != null) {
                  //       for (var p in lPrescriptions) {
                  //         if (p['isChosen'] == true) {
                  //           _c.lPrescription.add(p['id']);
                  //           ++prescriptionCount;
                  //         } else if (p['isChosen'] == false) {
                  //           _c.lPrescription.remove(p['id']);
                  //         }
                  //       }
                  //     }
                  //   }
                  // }

                  setState(() {});
                  Get.back();
                },
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  void initState() {
    _groupRecordType();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return _lType.isNotEmpty
        ? CustomContainer(
            color: AppColors.grey200,
            borderRadius: 5,
            child: Column(
              children: [
                Row(
                  children: [
                    Icon(
                      PhosphorIcons.first_aid,
                      color: AppColors.primary,
                      size: 25.sp,
                    ),
                    SizedBox(width: 5.sp),
                    Text(
                      'Mã bệnh ${widget.data.otherCode}',
                      style: TextStyle(
                        color: AppColors.primary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 15.sp),
                ..._lType.map((e) {
                  return Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text('${e["typeName"]}'),
                          GestureDetector(
                            onTap: () => _showModalSheet(context, e),
                            child: Icon(
                              PhosphorIcons.folder_notch_plus_light,
                              color: AppColors.primary,
                              size: 27.sp,
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 5.sp),
                      Container(
                          padding: EdgeInsets.symmetric(vertical: 5.sp, horizontal: 8.sp),
                          decoration: BoxDecoration(
                            color: AppColors.blue100,
                            borderRadius: BorderRadius.circular(Constants.textFieldRadius.sp),
                          ),
                          child: Text('$_chosenLength phiếu đã chọn')),
                    ],
                  );
                }).toList(),
              ],
            ),
          )
        : Padding(
            padding: EdgeInsets.only(left: 5.sp),
            child: const Text('Không có phiếu y lệnh được gợi ý.'),
          );
  }
}
