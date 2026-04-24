import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ResponsiveContainer
} from "recharts";

const colors = {
  positive: "#22c55e",
  negative: "#ef4444",
  neutral: "#eab308"
};

function AspectBarChart({ data }) {
  if (!data || data.length === 0) return <p>No Data</p>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="term" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value">
          {data.map((entry, index) => (
            <Cell key={index} fill={colors[entry.sentiment]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export default AspectBarChart;