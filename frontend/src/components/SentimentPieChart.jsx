import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const COLORS = ["#22c55e", "#ef4444", "#eab308"];

function SentimentPieChart({ data }) {
  if (!data || data.length === 0) return <p>No Data</p>;

  const counts = { positive: 0, negative: 0, neutral: 0 };

  data.forEach(d => counts[d.sentiment]++);

  const pieData = [
    { name: "Positive", value: counts.positive },
    { name: "Negative", value: counts.negative },
    { name: "Neutral", value: counts.neutral }
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={pieData} dataKey="value" outerRadius={100}>
          {pieData.map((entry, index) => (
            <Cell key={index} fill={COLORS[index]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default SentimentPieChart;