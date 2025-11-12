import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

export default function Settings() {
  const { data } = useQuery({
    queryKey: ['providers'],
    queryFn: async () => {
      const res = await api.get('/nlp/providers')
      return res.data
    },
  })

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Settings</h1>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">LLM Provider</h2>
        <div className="space-y-2">
          <p className="text-sm text-gray-500">
            Current provider: <span className="font-medium">{data?.current || 'mock'}</span>
          </p>
          <p className="text-sm text-gray-500">
            Available: {data?.available?.join(', ') || 'mock, openai, anthropic'}
          </p>
          <p className="text-sm text-gray-400 mt-4">
            To change provider, set LLM_PROVIDER environment variable and restart the API.
          </p>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Redaction</h2>
        <p className="text-sm text-gray-500">
          PII redaction is enabled by default. To disable, set REDACTION_ENABLED=false.
        </p>
      </div>
    </div>
  )
}

