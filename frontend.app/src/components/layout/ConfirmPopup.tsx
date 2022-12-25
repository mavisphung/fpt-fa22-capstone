import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

export const ConfirmPopup: React.FC<any> = (props) => {
  return (
    <Modal
      show={props.show}
      onHide={props.onHide}
      dialogClassName={props.dialogClassName}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">{props.titleString}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {/* <h4>Centered Modal</h4> */}
        <p>{props.msgString}</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={props.onHide}>
          Không
        </Button>
        <Button variant="primary" onClick={props.onYes}>
          Có
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
