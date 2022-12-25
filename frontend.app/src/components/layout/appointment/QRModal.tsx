import { QRCodeCanvas } from 'qrcode.react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

export const QRModal: React.FC<any> = (props) => {
  return (
    <Modal
      show={props.show}
      onHide={props.onHide}
      dialogClassName={props.dialogClassName}
      size="xl"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">{props.titleString}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <QRCodeCanvas value="https://reactjs.org/" />
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={props.actionProp}>
          Tiếp tục
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
