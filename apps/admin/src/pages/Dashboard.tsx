import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Calendar, CheckSquare, TrendingUp, DollarSign } from 'lucide-react'

export default function Dashboard() {
  const { data: usage } = useQuery({
    queryKey: ['usage'],
    queryFn: async () => {
      const res = await api.get('/admin/usage')
      return res.data
    },
  })

  const { data: meetings } = useQuery({
    queryKey: ['meetings'],
    queryFn: async () => {
      const res = await api.get('/meetings?page_size=5')
      return res.data
    },
  })

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Calendar className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Meetings This Month
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {meetings?.total || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckSquare className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Open Tasks
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">-</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Audio Minutes
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {usage?.audio_minutes?.toFixed(1) || '0'}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DollarSign className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Estimated Cost
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    ${usage?.cost_estimate?.toFixed(2) || '0.00'}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Recent Meetings
          </h3>
          <div className="mt-5">
            {meetings?.items?.length > 0 ? (
              <ul className="divide-y divide-gray-200">
                {meetings.items.map((meeting: any) => (
                  <li key={meeting.id} className="py-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {meeting.title}
                        </p>
                        <p className="text-sm text-gray-500">
                          {new Date(meeting.occurred_at).toLocaleDateString()}
                        </p>
                      </div>
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        {meeting.status}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500">No meetings yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

