import React from "react";

function Sidebar({ category, setCategory }) {
  const items = ["phones", "laptops", "restaurants"];

  return (
    <div className="sidebar">
      <h2 className="logo">ABSA</h2>

      {items.map((item) => (
        <button
          key={item}
          className={`nav-btn ${category === item ? "active" : ""}`}
          onClick={() => setCategory(item)}
        >
          {item.toUpperCase()}
        </button>
      ))}
    </div>
  );
}

export default Sidebar;