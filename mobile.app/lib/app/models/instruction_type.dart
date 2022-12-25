// ignore_for_file: public_member_api_docs, sort_constructors_first
class InstructionType {
  final int? id;
  final String? name;

  InstructionType({
    this.id,
    this.name,
  });

  factory InstructionType.fromMap(Map<String, dynamic> map) {
    return InstructionType(
      id: map['id'] != null ? map['id'] as int : null,
      name: map['name'] != null ? map['name'] as String : null,
    );
  }

  @override
  String toString() => 'InstructionType(id: $id, name: $name)';
}
