function MateriaCard({ nombre, peso }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
      <h3>{nombre}</h3>
      <p>Peso: {peso} kg</p>
    </div>
  );
}

export default MateriaCard;
