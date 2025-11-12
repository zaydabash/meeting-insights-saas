import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

export default function Usage() {
  const { data, isLoading } = useQuery({
    queryKey: ['usage'],
    queryFn: async () => {
      const res = await api.get('/admin/usage')
      return res.data
    },
  })

  const { data: costs } = useQuery({
    queryKey: ['costs'],
    queryFn: async () => {
      const res = await api.get('/admin/costs')
      return res.data
    },
  })

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Usage & Costs</h1>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Usage</h2>
          <dl className="space-y-4">
            <div>
              <dt className="text-sm text-gray-500">Audio Minutes</dt>
              <dd className="text-2xl font-semibold text-gray-900">
                {data?.audio_minutes?.toFixed(1) || '0'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Tokens In</dt>
              <dd className="text-2xl font-semibold text-gray-900">
                {data?.tokens_in?.toLocaleString() || '0'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Tokens Out</dt>
              <dd className="text-2xl font-semibold text-gray-900">
                {data?.tokens_out?.toLocaleString() || '0'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Storage (MB)</dt>
              <dd className="text-2xl font-semibold text-gray-900">
                {data?.storage_mb?.toFixed(2) || '0'}
              </dd>
            </div>
          </dl>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Costs</h2>
          <dl className="space-y-4">
            <div>
              <dt className="text-sm text-gray-500">Total Cost (30 days)</dt>
              <dd className="text-2xl font-semibold text-gray-900">
                ${costs?.total_cost_usd?.toFixed(2) || '0.00'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Estimated Monthly</dt>
              <dd className="text-2xl font-semibold text-gray-900">
                ${data?.cost_estimate?.toFixed(2) || '0.00'}
              </dd>
            </div>
            {costs?.by_provider && Object.keys(costs.by_provider).length > 0 && (
              <div className="mt-4">
                <dt className="text-sm text-gray-500 mb-2">By Provider</dt>
                {Object.entries(costs.by_provider).map(([provider, stats]: [string, any]) => (
                  <div key={provider} className="text-sm">
                    <span className="font-medium">{provider}:</span> ${stats.cost.toFixed(2)}
                  </div>
                ))}
              </div>
            )}
          </dl>
        </div>
      </div>
    </div>
  )
}

