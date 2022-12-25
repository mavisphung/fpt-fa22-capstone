import { timeOutSeconds } from 'constants/ConstValue';
import { Toast } from 'react-bootstrap';

export const NotificationToast: React.FC<any> = (props) => {
  return (
    <Toast
      onClose={props.onClose}
      show={props.show}
      delay={timeOutSeconds}
      autohide
      animation
      style={{
        position: 'absolute',
        top: 20,
        right: 20,
        minWidth: 200,
      }}
    >
      <Toast.Header>
        <img src={props.content.icon} className="rounded me-2" alt="Error_Icon" />
        <strong className="me-auto">{props.content.title}</strong>
        <small>Ngay lúc này</small>
      </Toast.Header>
      <Toast.Body>{props.content.body}</Toast.Body>
    </Toast>
  );
};
