// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class Pathology {
  final int? id;
  final String? code;
  final String? otherCode;
  final String? generalName;
  final String? diseaseName;

  Pathology({
    this.id,
    this.code,
    this.otherCode,
    this.generalName,
    this.diseaseName,
  });

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'code': code,
      'otherCode': otherCode,
      'generalName': generalName,
      'diseaseName': diseaseName,
    };
  }

  factory Pathology.fromMap(Map<String, dynamic> map) {
    return Pathology(
      id: map['id'] != null ? map['id'] as int : null,
      code: map['code'] != null ? map['code'] as String : null,
      otherCode: map['otherCode'] != null ? map['otherCode'] as String : null,
      generalName: map['generalName'] != null ? map['generalName'] as String : null,
      diseaseName: map['diseaseName'] != null ? map['diseaseName'] as String : null,
    );
  }

  factory Pathology.fromMap2(Map<String, dynamic> map) {
    return Pathology(
      id: map['id'] != null ? map['id'] as int : null,
      code: map['code'] != null ? map['code'] as String : null,
      otherCode: map['otherCode'] != null ? map['otherCode'] as String : null,
      generalName: map['vGeneralName'] != null ? map['vGeneralName'] as String : null,
      diseaseName: map['vDiseaseName'] != null ? map['vDiseaseName'] as String : null,
    );
  }

  String toJson() => json.encode(toMap());

  factory Pathology.fromJson(String source) => Pathology.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'Pathology(id: $id, code: $code, otherCode: $otherCode, generalName: $generalName, diseaseName: $diseaseName)';
  }
}
