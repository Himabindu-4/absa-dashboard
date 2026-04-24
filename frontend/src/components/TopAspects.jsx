function TopAspects({ data }) {
  if (!data || Object.keys(data).length === 0) return <p>No Data</p>;

  return (
    <ul>
      {Object.entries(data).map(([term, count]) => (
        <li key={term}>
          {term} ({count})
        </li>
      ))}
    </ul>
  );
}

export default TopAspects;