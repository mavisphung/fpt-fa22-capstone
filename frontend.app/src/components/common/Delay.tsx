import React, { useState, useEffect } from 'react';
import { Spinner } from 'react-bootstrap';

type Props = {
  children: React.ReactElement<any, any>;
  waitBeforeShow?: number;
};

const Delayed = ({ children, waitBeforeShow = 1000 }: Props) => {
  const [isShown, setIsShown] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsShown(true);
    }, waitBeforeShow);
    return () => clearTimeout(timer);
  }, [waitBeforeShow]);

  return isShown ? children : <Spinner variant="primary" animation={'border'} />;
};

export default Delayed;
