import React, { useEffect, useState } from 'react';
import MaterialCard from './components/MaterialCard';

function App() {
  const [materiales, setMateriales] = useState([]);

  useEffect(() => {
    fetch('/materiales.json')
      .then(res => res.json())
      .then(data => setMateriales(data))
      .catch(err => console.error("Error cargando JSON", err));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Materiales Reciclados</h1>
      {materiales.map((mat, i) => (
        <MaterialCard key={i} nombre={mat.nombre} peso={mat.peso} />
      ))}
    </div>
  );
}

export default App;

