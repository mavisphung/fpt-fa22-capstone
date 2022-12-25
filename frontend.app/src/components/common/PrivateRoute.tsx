import { Redirect, RouteProps, Route } from 'react-router-dom';

export function ManagerRoute(props: RouteProps) {
  const isLoggedIn = Boolean(localStorage.getItem('access_token') !== null);
  const typeLoggedIn = localStorage.getItem('type');
  if (!isLoggedIn) return <Redirect to="/login" />;
  else if (typeLoggedIn === 'DOCTOR') return <Redirect to="/doctor/home" />;

  return <Route {...props} />;
}

export function DoctorRoute(props: RouteProps) {
  const isLoggedIn = Boolean(localStorage.getItem('access_token') !== null);
  const typeLoggedIn = localStorage.getItem('type');
  if (!isLoggedIn) return <Redirect to="/login" />;
  else if (typeLoggedIn === 'MANAGER') return <Redirect to="/manager/home" />;

  return <Route {...props} />;
}
