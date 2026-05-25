import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import type { CityItem } from '../../types/dashboard'

interface Props {
  data: CityItem[]
}

export default function ComprasPorCiudad({ data }: Props) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 className="mb-4 text-sm font-semibold text-gray-700">Compras por Ciudad</h3>
      {data.length === 0 ? (
        <p className="py-8 text-center text-sm text-gray-400">Sin datos</p>
      ) : (
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis type="number" tick={{ fontSize: 12 }} />
            <YAxis dataKey="city" type="category" tick={{ fontSize: 12 }} width={90} />
            <Tooltip />
            <Bar dataKey="total" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
