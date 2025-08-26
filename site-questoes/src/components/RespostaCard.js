// src/components/RespostaCard.js
import React from 'react';

// 1. Importe os ícones que vamos usar
import { BsListOl } from 'react-icons/bs'; // Para Ordenação
import { IoShapes } from "react-icons/io5"; // Para Agrupamento
import { FaPuzzlePiece, FaExclamationTriangle } from 'react-icons/fa'; // Para Outros e Erro

const RespostaCard = ({ classificacao }) => {
  // Se não houver classificação, não renderiza nada
  if (!classificacao) {
    return null;
  }

  // 2. Lógica para definir o ícone, texto e cor com base na classe
  let icone, texto, corClasse;

  switch (classificacao.toLowerCase()) {
    case 'ordenação':
      icone = <BsListOl />;
      texto = 'Ordenação';
      corClasse = 'card-ordenacao';
      break;
    case 'agrupamento':
      icone = <IoShapes />;
      texto = 'Agrupamento';
      corClasse = 'card-agrupamento';
      break;
    case 'outros':
      icone = <FaPuzzlePiece />;
      texto = 'Outros';
      corClasse = 'card-outros';
      break;
    default: // Caso de erro ou texto inesperado
      icone = <FaExclamationTriangle />;
      texto = 'Erro na Classificação';
      corClasse = 'card-erro';
      break;
  }

  // 3. Estrutura do Card em JSX
  return (
    <div className={`resposta-card ${corClasse}`}>
      <span className="resposta-card-icon">{icone}</span>
      <span className="resposta-card-texto">{texto}</span>
    </div>
  );
};

export default RespostaCard;