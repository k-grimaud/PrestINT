import React from 'react';
import GoToLogin from "./Login/Login.tsx";

const Navbar: React.FC = () => {
  return (
    <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', alignItems: 'center' }}>
      <GoToLogin/>
    </nav>
  );
};

export default Navbar;