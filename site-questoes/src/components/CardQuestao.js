// src/components/CardQuestao.js
import React from 'react';

const CardQuestao = ({ questao }) => {
  return (
    <div className="cartao-questao">
      <h3>{questao.titulo} (Nº {questao.numero_questao})</h3>
      <div className="meta-info">
        <span><strong>Ano:</strong> {questao.ano}</span>
        <span><strong>Fase:</strong> {questao.fase}</span>
        <span><strong>Nível:</strong> {questao.nivel}</span>
        <span><strong>Classe:</strong> {questao.classe}</span>
      </div>
      <p><strong>Enunciado:</strong> {questao.enunciado}</p>
      <p><strong>Questão:</strong> {questao.questao}</p>
      <p><strong>Alternativas:</strong> {questao.alternativas}</p>
    </div>
  );
};

export default CardQuestao;