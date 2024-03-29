import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/modules/message/controllers/message_controller.dart';
import 'package:hi_doctor_v2/app/modules/message/views/chat_bubble.dart';
import 'package:hi_doctor_v2/app/modules/message/views/chat_input.dart';
import 'package:hi_doctor_v2/app/modules/widgets/loading_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/my_appbar.dart';

// ignore: constant_identifier_names
enum TypeMessage { TEXT, IMAGE, FILE, VIDEO }

class ChatPageArguments {
  final int peerId;
  final int peerAccountId;
  final String peerAvatar;
  final String peerName;
  final bool hasInputWidget;

  ChatPageArguments({
    required this.peerId,
    required this.peerAccountId,
    required this.peerAvatar,
    required this.peerName,
    required this.hasInputWidget,
  });
}

class ChatPage extends StatefulWidget {
  ChatPage({Key? key}) : super(key: key);

  final arguments = Get.arguments as ChatPageArguments;

  @override
  ChatPageState createState() => ChatPageState();
}

class ChatPageState extends State<ChatPage> {
  late final MessageController _cMessage;
  late final int _userId;
  late final int _peerAccountId;

  List<QueryDocumentSnapshot> listMessage = [];
  int _limit = 20;
  final int _limitIncrement = 20;
  late final String _groupChatId;

  final _listScrollController = ScrollController();

  _scrollListener() {
    if (!_listScrollController.hasClients) return;
    if (_listScrollController.offset >= _listScrollController.position.maxScrollExtent &&
        !_listScrollController.position.outOfRange &&
        _limit <= listMessage.length) {
      setState(() {
        _limit += _limitIncrement;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _cMessage = Get.put(MessageController());
    _userId = _cMessage.userId;
    _peerAccountId = widget.arguments.peerAccountId;
    _groupChatId = '$_userId-$_peerAccountId';

    _listScrollController.addListener(_scrollListener);
  }

  @override
  void dispose() {
    Utils.unfocus();
    super.dispose();
  }

  void _onMessageSend(int type, String? imgUrl) async {
    final content = _cMessage.inputController.text.trim();
    if (type == TypeMessage.TEXT.index) {
      if (content.isEmpty) return;
      await _cMessage.sendMessage(content, type, _groupChatId, _userId, _peerAccountId);
    } else if (type == TypeMessage.IMAGE.index) {
      await _cMessage.sendMessage(imgUrl!, type, _groupChatId, _userId, _peerAccountId);
    }
    _cMessage.inputController.clear();

    await _cMessage.setDataFirestore(
      Constants.pathMessageCollection,
      _groupChatId,
      {
        Constants.supervisorId: _userId,
        Constants.doctorId: widget.arguments.peerId,
        Constants.doctorAccountId: _peerAccountId,
        Constants.lastMessage: type == TypeMessage.TEXT.index ? content : '[hình ảnh]',
        Constants.lastTimeStamp: DateTime.now().millisecondsSinceEpoch.toString(),
      },
    );

    if (_listScrollController.hasClients) {
      _listScrollController.animateTo(0, duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
    }
  }

  Widget buildListMessage() {
    return Expanded(
      child: StreamBuilder<QuerySnapshot>(
        stream: _cMessage.getChatStream(_groupChatId, _limit),
        builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
          if (snapshot.hasData) {
            listMessage = snapshot.data!.docs;
            if (listMessage.isNotEmpty) {
              return ListView.builder(
                reverse: true,
                padding: EdgeInsets.all(10.sp),
                itemBuilder: (context, index) => ChatBubble(
                  userId: _userId,
                  document: snapshot.data?.docs[index],
                  index: index,
                  listMessage: listMessage,
                  peerAvatar: widget.arguments.peerAvatar,
                ),
                itemCount: snapshot.data?.docs.length,
                controller: _listScrollController,
              );
            } else {
              return const Center(child: Text("No message here yet..."));
            }
          } else {
            return const LoadingWidget();
          }
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: MyAppBar(
        title: widget.arguments.peerName,
      ),
      body: Column(
        children: <Widget>[
          buildListMessage(),
          // if (widget.arguments.hasInputWidget) ChatInput(onMessageSend: _onMessageSend),
          ChatInput(onMessageSend: _onMessageSend),
        ],
      ),
    );
  }
}
