// src/components/Header.js
import React from 'react';
import Logo from './Logo'; // Reutilizando a logo que já fizemos

const Header = () => {
  return (
    <header className="app-header">
      <Logo />
      <h1>Classificador de Questões OBI</h1>
    </header>
  );
};

export default Header;