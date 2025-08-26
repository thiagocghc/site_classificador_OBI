// src/components/Logo.js
import React from 'react';
// 1. Importe a sua imagem do caminho relativo
import logoImagem from '../assets/logo_obi.png'; // <-- ATENÇÃO: Mude o nome do arquivo se for diferente

const Logo = () => (
  // 2. Use a tag <img> em vez do <svg>
  <img 
    src={logoImagem} // A variável importada vai no 'src'
    alt="Logo do Classificador OBI" // Texto alternativo é importante para acessibilidade
    className="app-logo" // Mantemos a classe para poder estilizar
  />
);

export default Logo;