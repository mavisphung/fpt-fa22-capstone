import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/util/enum.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/common/util/validators.dart';
import 'package:hi_doctor_v2/app/common/values/strings.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/date_time_field_widget.dart';
import 'package:hi_doctor_v2/app/modules/settings/controllers/patient_profile_controller.dart';
import 'package:hi_doctor_v2/app/modules/settings/views/gender_dropdown.dart';
import 'package:hi_doctor_v2/app/modules/settings/widgets/image_picker_widget.dart';
import 'package:hi_doctor_v2/app/modules/settings/widgets/profile_skeleton.dart';
import 'package:hi_doctor_v2/app/modules/widgets/base_page.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_elevate_btn_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_textfield_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/image_container.dart';
import 'package:hi_doctor_v2/app/modules/widgets/my_appbar.dart';

class PatientProfileDetailPage extends StatelessWidget {
  final _c = Get.put(PatientProfileController());
  final _formKey = GlobalKey<FormState>();
  final _patientId = Get.arguments as int?;
  final _avtWidth = Get.width / 3;
  final _avtHeight = Get.width / 2.5;

  PatientProfileDetailPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BasePage(
      backgroundColor: Colors.white,
      appBar: MyAppBar(title: _patientId == null ? 'Thêm hồ sơ' : Strings.patientProfileDetail),
      body: FutureBuilder<bool>(
        future: _patientId == null ? _c.emptyField() : _c.getPatientWithId(_patientId!),
        builder: (ctx, snapshot) {
          if (!snapshot.hasData) {
            return const ProfileSkeleton();
          }
          if (snapshot.data == false) {
            return const Center(child: Text('System Error...'));
          }
          return Column(
            children: [
              Stack(
                children: [
                  ObxValue<RxString>(
                    (data) => ImageContainer(
                      width: _avtWidth,
                      height: _avtHeight,
                      imgUrl: data.value,
                      borderRadius: 5,
                    ),
                    _c.avatar,
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: ImagePickerWidget(
                      getImageFucntion: _c.setAvatar,
                    ),
                  ),
                ],
              ),
              SizedBox(
                height: 28.sp,
              ),
              Form(
                key: _formKey,
                child: Column(
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: CustomTextFieldWidget(
                            validator: Validators.validateEmpty,
                            focusNode: _c.firstNameFocusNode,
                            controller: _c.firstName,
                            onFieldSubmitted: (_) => FocusScope.of(context).requestFocus(_c.lastNameFocusNode),
                            labelText: Strings.firstName,
                          ),
                        ),
                        const SizedBox(
                          width: 10.0,
                        ),
                        Expanded(
                          child: CustomTextFieldWidget(
                            validator: Validators.validateEmpty,
                            focusNode: _c.lastNameFocusNode,
                            controller: _c.lastName,
                            onFieldSubmitted: (_) => FocusScope.of(context).requestFocus(_c.addressFocusNode),
                            labelText: Strings.lastName,
                          ),
                        ),
                      ],
                    ),
                    CustomTextFieldWidget(
                      validator: Validators.validateEmpty,
                      focusNode: _c.addressFocusNode,
                      controller: _c.address,
                      onFieldSubmitted: (_) => Utils.unfocus(),
                      labelText: Strings.address,
                    ),
                    MyDateTimeField(
                      dob: _c.dob,
                      formKey: _formKey,
                      extendFunc: () {
                        _c.isAdultUnder60.value = Validators.isAdultUnder60(_c.dob.text);
                      },
                    ),
                  ],
                ),
              ),
              GenderDropdown(rxGender: _c.gender),
              Row(
                children: [
                  ObxValue<RxBool>(
                    (data) => Checkbox(
                      fillColor: MaterialStateProperty.all(Theme.of(context).primaryColor),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
                      value: data.value,
                      onChanged: (_) => data.value = !data.value,
                    ),
                    _c.checkBoxStatus,
                  ),
                  Expanded(
                    child: InkWell(
                      onTap: () => _c.checkBoxStatus.value = !_c.checkBoxStatus.value,
                      child: Text(
                        Strings.trueInfoClaim,
                      ),
                    ),
                  )
                ],
              ),
              SizedBox(
                height: 20.sp,
              ),
              ObxValue<RxBool>(
                (data) => Visibility(
                  visible: data.value,
                  child: Row(
                    children: [
                      ObxValue<RxBool>(
                        (data) => Checkbox(
                          fillColor: MaterialStateProperty.all(Theme.of(context).primaryColor),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
                          value: data.value,
                          onChanged: (_) => data.value = !data.value,
                        ),
                        _c.checkBoxStatus1,
                      ),
                      Expanded(
                        child: InkWell(
                          onTap: () => _c.checkBoxStatus1.value = !_c.checkBoxStatus1.value,
                          child: Text(
                            Strings.isAdultUnder60,
                          ),
                        ),
                      )
                    ],
                  ),
                ),
                _c.isAdultUnder60,
              ),
              SizedBox(
                height: 30.sp,
              ),
              // -------------------------------------------
              SizedBox(
                width: 1.sw,
                child: ObxValue<Rx<Status>>(
                  (data) => CustomElevatedButtonWidget(
                    textChild: _patientId == null ? 'Thêm hồ sơ bệnh nhân' : Strings.saveProfile,
                    status: data.value,
                    onPressed: () {
                      _formKey.currentState?.save();
                      final isValidate = _formKey.currentState?.validate() ?? false;
                      if (!isValidate) return;
                      if (_c.avatar.value.isEmpty) {
                        Utils.showAlertDialog('Bạn cần cung cấp ảnh của bệnh nhân.');
                        return;
                      }
                      if (!_c.checkBoxStatus.value) {
                        Utils.showAlertDialog(Strings.trueInfoClaimAlertMsg);
                        return;
                      }
                      if (_c.isAdultUnder60.value && !_c.checkBoxStatus1.value) {
                        Utils.showAlertDialog(Strings.isAdultUnder60AlertMsg);
                        return;
                      }
                      if (isValidate) {
                        _patientId == null ? _c.addPatientProfile() : _c.updatePatientProfile(_patientId!);
                      }
                    },
                  ),
                  _c.status,
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
