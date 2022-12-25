import { Medicines } from 'models/medicines';
import Multiselect from 'multiselect-react-dropdown';
import React from 'react';
import Modal from 'react-bootstrap/Modal';
import classes from './PrescriptionModal.module.scss';

export const PrescriptionModal: React.FC<any> = (props) => {
  const initSelectedMedicines = new Array<Medicines>();
  const [selected, setSelected] = React.useState(initSelectedMedicines);
  const [selectedNote, setSelectedNote] = React.useState(null);
  const totalRef = React.useRef<HTMLInputElement>(null);
  const unitRef = React.useRef<HTMLInputElement>(null);
  const useDescriptionRef = React.useRef<HTMLInputElement>(null);
  const noteStringRef = React.useRef<HTMLInputElement>(null);
  const handleAddPrescription = (event: any) => {
    event.preventDefault();
    const enteredTotal = totalRef.current?.value;
    const enteredUnit = unitRef.current?.value;
    const enteredDescription = useDescriptionRef.current?.value;
    let enteredNoteString = '';
    if (selectedNote !== null) {
      enteredNoteString =
        enteredDescription + ' ; ' + selectedNote[0] + ' ' + noteStringRef.current?.value ?? '';
    } else {
      enteredNoteString = String(enteredDescription);
    }
    props.onCloseModal({
      id: selected[0]?.id,
      name: selected[0]?.name,
      quantity: String(enteredTotal),
      unit: enteredUnit,
      guide: enteredNoteString,
    });
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
        <div className={classes.bodyPrescriptionModal}>
          <form onSubmit={handleAddPrescription}>
            <table>
              <tbody>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Tên thuốc</span>
                  </td>
                  <td>
                    <Multiselect
                      isObject={true}
                      onKeyPressFn={function noRefCheck() {}}
                      onRemove={setSelected}
                      onSearch={(value: string) => props.searchMedicinesFunction(value)}
                      onSelect={setSelected}
                      options={props.medicinesProps}
                      displayValue="name"
                      selectedValues={null}
                      placeholder="Tìm theo tên thuốc"
                      selectionLimit={1}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Số lượng</span>
                  </td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="number"
                      placeholder="Nhập số lượng"
                      required
                      ref={totalRef}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Đơn vị</span>
                  </td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="text"
                      placeholder="Nhập đơn vị"
                      required
                      ref={unitRef}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Cách dùng</span>
                  </td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="text"
                      placeholder="Sáng: ... ; Trưa: ... ; Chiều: ... ; Tối: ..."
                      required
                      ref={useDescriptionRef}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span>Ghi chú</span>
                  </td>
                  <td>
                    <Multiselect
                      singleSelect={true}
                      isObject={false}
                      onKeyPressFn={function noRefCheck() {}}
                      onRemove={setSelectedNote}
                      onSearch={function noRefCheck() {}}
                      onSelect={setSelectedNote}
                      options={['Trước bữa ăn', 'Sau bữa ăn']}
                      selectedValues={selectedNote}
                      placeholder="Ghi chú cách dùng"
                    />
                  </td>
                </tr>
                <tr>
                  <td></td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="text"
                      placeholder="Trước hay sau bữa ăn bao lâu?"
                      ref={noteStringRef}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
            <div className={classes.buttonSubmit}>
              <button className={classes.btnSave}>Xác nhận</button>
            </div>
          </form>
        </div>
      </Modal.Body>
    </Modal>
  );
};
