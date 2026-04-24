import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function TrendChart({ data }) {
  if (!data || data.length === 0) return <p>No Data</p>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="count" stroke="#22c55e" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default TrendChart;