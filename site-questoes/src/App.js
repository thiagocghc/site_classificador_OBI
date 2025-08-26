import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Filtros from './components/Filtros';
import ListaQuestoes from './components/ListaQuestoes';
import Classificador from './components/Classificador';
import './App.css';

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [opcoesFiltro, setOpcoesFiltro] = useState({ ano: [], fase: [], nivel: [], classe: [] });
  const [filtrosSelecionados, setFiltrosSelecionados] = useState({ ano: '', fase: '', nivel: '', classe: '' });
  const [loading, setLoading] = useState(true);

  // Busca as opções de filtro (anos, classes, etc.) uma única vez
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/filtros')
      .then(res => res.json())
      .then(data => setOpcoesFiltro(data))
      .catch(error => console.error("Erro ao buscar opções de filtro:", error));
    
    // Carrega todas as questões inicialmente
    handleFiltrarClick();
  }, []);

  // Função chamada quando um <select> muda de valor
  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltrosSelecionados(prevState => ({ ...prevState, [name]: value }));
  };
  
  // Função chamada quando o botão "Filtrar" é clicado
  const handleFiltrarClick = () => {
    setLoading(true);
    // Cria os parâmetros de busca apenas com os filtros que têm valor
    const params = new URLSearchParams(
      Object.fromEntries(Object.entries(filtrosSelecionados).filter(([_, value]) => value))
    );
    
    fetch(`http://127.0.0.1:5000/api/questoes?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        setQuestoes(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erro ao buscar questões:", error);
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <Header />
      <main className="main-content">
        <Filtros 
          opcoes={opcoesFiltro}
          filtros={filtrosSelecionados}
          onFiltroChange={handleFiltroChange}
          onFiltrar={handleFiltrarClick}
        />
        <ListaQuestoes questoes={questoes} loading={loading} />
        <Classificador />
      </main>
    </div>
  );
}

export default App;