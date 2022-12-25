import 'dart:convert';

import 'package:hi_doctor_v2/app/models/patient.dart';

// ignore_for_file: public_member_api_docs, sort_constructors_first
class HealthRecord {
  final int? patient;
  final int? doctor;
  final Map<String, dynamic>? detail;
  final List<dynamic>? prescriptions;
  final List<dynamic>? instructions;

  HealthRecord({
    this.patient,
    this.doctor,
    this.detail,
    this.prescriptions,
    this.instructions,
  });

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'patient': patient,
      'detail': detail,
    };
  }

  factory HealthRecord.fromMap(Map<String, dynamic> map) {
    return HealthRecord(
      patient: map['patient'] != null ? map['patient'] as int : null,
      doctor: map['doctor'] != null ? map['doctor'] as int : null,
      detail: map['detail'] != null ? Map<String, dynamic>.from((map['detail'] as Map<String, dynamic>)) : null,
      prescriptions: map['prescriptions'] != null ? List<dynamic>.from((map['prescriptions'] as List<dynamic>)) : null,
      instructions: map['instructions'] != null ? List<dynamic>.from((map['instructions'] as List<dynamic>)) : null,
    );
  }

  String toJson() => json.encode(toMap());

  factory HealthRecord.fromJson(String source) => HealthRecord.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'HealthRecord(patient: $patient, doctor: $doctor, detail: $detail, prescriptions: $prescriptions, instructions: $instructions)';
  }
}
