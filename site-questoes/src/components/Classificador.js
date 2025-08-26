// src/components/Classificador.js
import React, { useState } from 'react';
import RespostaCard from './RespostaCard';

const Classificador = () => {
  const [textoQuestao, setTextoQuestao] = useState(''); // Voltamos para um único estado
  const [classePredita, setClassePredita] = useState('');
  const [classificando, setClassificando] = useState(false);

  const handleClassificar = () => {
    if (!textoQuestao.trim()) {
      alert("Por favor, cole o texto da questão para classificar.");
      return;
    }
    setClassificando(true);
    setClassePredita('');

    // ATENÇÃO: A URL agora aponta para sua API FastAPI na porta 8000
    const apiUrl = 'http://127.0.0.1:8000/classificar'; 

    fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // Enviando o corpo no novo formato com apenas o campo "texto"
      body: JSON.stringify({ texto: textoQuestao }),
    })
    .then(res => {
        if (!res.ok) throw new Error('Erro de rede ou na API');
        return res.json();
    })
    .then(data => {
      // A chave da resposta é "classificacao"
      if (data.classificacao) {
        setClassePredita(data.classificacao);
      } else if (data.erro) {
        throw new Error(data.erro);
      }
    })
    .catch(error => {
      console.error("Erro ao classificar:", error);
      setClassePredita('Erro na classificação.');
    })
    .finally(() => {
        setClassificando(false);
    });
  };

  return (
    <div className="coluna-classificador">
      <h2>Classificar uma Nova Questão </h2>
      
      <textarea
        placeholder="Cole o texto completo da questão aqui..."
        value={textoQuestao}
        onChange={(e) => setTextoQuestao(e.target.value)}
      />

      <button onClick={handleClassificar} disabled={classificando}>
        {classificando ? 'Classificando...' : 'Classificar'}
      </button>
      
      <div className="resposta-classificador">
        <label>Resposta:</label>
        <RespostaCard classificacao={classePredita} />
      </div>
    </div>
  );
};

export default Classificador;
