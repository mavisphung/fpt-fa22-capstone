import React, { SetStateAction, useEffect, useState } from 'react';
import '../appointment/page.scss';
import { AppointmentFilter } from './filter';
import { useSelector } from 'react-redux';
import {
  AppointmenDisplayListSelector,
  appointmentAction,
} from 'features/appointment/appointmentSlice';
import { IAppointment, IAppointmentFilter } from 'models/appointment';
import { useAppDispatch } from 'app/hooks';
import { AppointmentSummaryCard } from 'features/appointment/layout/common';
import { useHistory } from 'react-router-dom';

export const DummyComponent = (props: {
  appointments: IAppointment[];
  viewDetail: (id: number) => void;
}) => {
  let appointments = props.appointments;
  const history = useHistory();
  const showAppointmentDetail = (id: number) => {
    console.log(id);
    localStorage.setItem('selectedAppointment', id.toString());
    history.push('/doctor/detailAppointment');
  };
  return (
    <>
      <div className="filter">
        <AppointmentFilter />
      </div>
      <div className="result">
        {appointments.map((appointment) => {
          return (
            <div
              onClick={(e) => {
                showAppointmentDetail(appointment.id);
              }}
            >
              <AppointmentSummaryCard
                appointment={appointment}
                showDetail={showAppointmentDetail}
              />
            </div>
          );
        })}
        <div className="pagination"></div>
      </div>
    </>
  );
};

export const Appointments = () => {
  const appointments = useSelector(AppointmenDisplayListSelector);
  const dispatch = useAppDispatch();
  const showAppointmentDetails = (id: number) => {
    dispatch(appointmentAction.viewAppointment(id));
  };
  useEffect(() => {
    let defaultFilter: IAppointmentFilter = {
      bookedAt__lte: new Date().toISOString(),
      bookedAt__gte: new Date('2022-01-01').toISOString(),
      page: 1,
      limit: 10,
      patient__pk: null,
    };
    dispatch(appointmentAction.loadFilter(defaultFilter));
  }, []);
  return (
    <>
      <div className="content">
        <DummyComponent appointments={appointments} viewDetail={showAppointmentDetails} />
      </div>
    </>
  );
};
