import 'package:flutter/material.dart';
import 'package:flutter_phosphor_icons/flutter_phosphor_icons.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/modules/contract/controllers/create_contract_controller.dart';
import 'package:hi_doctor_v2/app/modules/contract/widgets/recommend_hr_extendable_row.dart';
import 'package:hi_doctor_v2/app/modules/contract/widgets/record_type_dropdown.dart';
import 'package:hi_doctor_v2/app/modules/health_record/controllers/health_record_controller.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_elevate_btn_widget.dart';

class RecommendOtherWidget extends StatefulWidget {
  final void Function(List<int>) setChosenList;
  const RecommendOtherWidget({super.key, required this.setChosenList});

  @override
  State<RecommendOtherWidget> createState() => _RecommendOtherWidgetState();
}

class _RecommendOtherWidgetState extends State<RecommendOtherWidget> {
  final _c = Get.find<CreateContractController>();
  final _cHealthRecord = Get.find<HealthRecordController>();

  final List<Map<String, dynamic>> _lOtherRecord = [];
  int _chosenLength = 0;

  void _getOtherTicket() {
    for (var hr in _cHealthRecord.allList) {
      if (hr.record!['isPatientProvided'] == true) {
        final pList = hr.detail!['pathologies'] as List;
        late int pIndex;
        for (var pItem in _c.lMonitoredPathology) {
          pIndex = pList.indexWhere((e) => e['id'] == pItem.id);
          if (pIndex == -1) {
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

              final typeItem = _lOtherRecord.firstWhere((e) => e['typeName'] == i['category'], orElse: () {
                isTypeGenerated = true;
                return {
                  'typeName': i['category'],
                  'details': tmp1,
                };
              });
              if (isTypeGenerated) {
                _lOtherRecord.add(typeItem);
                continue;
              }

              final lDetails = typeItem['details'] as List;
              final recordItem = lDetails.firstWhereOrNull((e) => e['record']['id'] == hr.record!['id']);
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

    // final othherList = _cHealthRecord.otherList;
    // if (othherList.isNotEmpty) {
    //   for (var hr in othherList) {
    //     final otherTicketList = hr.detail?['otherTickets'] as List?;
    //     if (otherTicketList?.isNotEmpty ?? false) {
    //       for (var t in otherTicketList!) {
    //         _lOtherRecord.add({
    //           'record': hr.record,
    //           'recordName': hr.detail?['name'],
    //           'ticketId': t['id'],
    //           'typeName': t['type'],
    //           'tickets': (t['tickets'] as List).map((e) => {'info': e, 'isChosen': false}).toList(),
    //         });
    //       }
    //     }
    //   }
    // }
  }

  void _showModalBottom(BuildContext ctx) {
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
              const Text('Danh sách phiếu khác'),
              Expanded(
                child: FutureBuilder(
                  future: _cHealthRecord.getInstructionType(),
                  builder: (_, AsyncSnapshot<bool> snapshot) {
                    if (snapshot.hasData && snapshot.data == true) {
                      if (_cHealthRecord.lInstructionType.isNotEmpty) {
                        return ObxValue<RxInt>(
                          (data) {
                            final chosenInstruction =
                                _cHealthRecord.lInstructionType.firstWhere((e) => e.id == data.value);
                            final typeItem =
                                _lOtherRecord.firstWhereOrNull((e) => e['typeName'] == chosenInstruction.name);
                            final hrList = typeItem?['details'] as List?;
                            return Column(
                              children: [
                                RecordTypeDropDown(
                                  recordId: data.value,
                                  setRecordId: (value) => data.value = value ?? -1,
                                  list: _cHealthRecord.lInstructionType,
                                ),
                                const SizedBox(height: 15),
                                if (typeItem != null && hrList?.isNotEmpty == true)
                                  Expanded(
                                    child: ListView.separated(
                                      itemBuilder: (_, index) {
                                        return ReccommendHrExtendableRow(
                                          map: hrList![index],
                                          instructionType: typeItem['typeName'],
                                        );
                                      },
                                      separatorBuilder: (_, __) => const Divider(),
                                      itemCount: hrList!.length,
                                    ),
                                  ),
                              ],
                            );
                          },
                          _c.rxRecordId,
                        );
                      } else {
                        return const SizedBox.shrink();
                      }
                    } else if (snapshot.hasData && snapshot.data == false) {
                      return const SizedBox.shrink();
                    } else if (snapshot.connectionState == ConnectionState.none) {
                      return const SizedBox.shrink();
                    }
                    return const SizedBox.shrink();
                  },
                ),
              ),
              CustomElevatedButtonWidget(
                textChild: 'Xong',
                onPressed: () {
                  _chosenLength = 0;
                  final chosenList = <int>[];
                  for (var o in _lOtherRecord) {
                    final toChooseList = o['details'] as List;
                    for (var c in toChooseList) {
                      final instructions = c['instructions'] as List;
                      for (var t in instructions) {
                        if (t['isChosen'] == true) {
                          chosenList.add(t['info']['id']);
                          ++_chosenLength;
                        }
                      }
                    }
                  }
                  widget.setChosenList(chosenList);
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
    _getOtherTicket();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('Phiếu khác'),
            GestureDetector(
              onTap: () => _showModalBottom(context),
              child: Icon(
                PhosphorIcons.folder_notch_plus_light,
                color: AppColors.primary,
                size: 27.sp,
              ),
            ),
          ],
        ),
        const SizedBox(height: 5),
        Container(
          padding: EdgeInsets.symmetric(vertical: 5.sp, horizontal: 8.sp),
          decoration: BoxDecoration(
            color: AppColors.blue100,
            borderRadius: BorderRadius.circular(Constants.textFieldRadius.sp),
          ),
          child: Text('$_chosenLength phiếu đã chọn'),
        ),
      ],
    );
  }
}
