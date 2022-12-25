import { useRef } from 'react';
import { Form } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

export const CancelModal: React.FC<any> = (props) => {
  const reasonCancelRef = useRef<HTMLInputElement>(null);

  const handleCancelAppointment = (event: any) => {
    event.preventDefault();

    props.onCloseModal(reasonCancelRef.current?.value);
  };
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
        <>
          <Form onSubmit={handleCancelAppointment}>
            <Form.Group className="mb-3" controlId="formInput">
              <Form.Control
                type="text"
                placeholder="Vui lòng nhập lý do hủy cuộc hẹn"
                required
                ref={reasonCancelRef}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Xác nhận
            </Button>
          </Form>
        </>
      </Modal.Body>
    </Modal>
  );
};
