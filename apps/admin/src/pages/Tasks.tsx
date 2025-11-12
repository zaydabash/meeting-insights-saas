import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

export default function Tasks() {
  const { data, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const res = await api.get('/tasks')
      return res.data
    },
  })

  if (isLoading) {
    return <div>Loading...</div>
  }

  const tasksByStatus = {
    open: data?.filter((t: any) => t.status === 'open') || [],
    in_progress: data?.filter((t: any) => t.status === 'in_progress') || [],
    done: data?.filter((t: any) => t.status === 'done') || [],
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {['open', 'in_progress', 'done'].map((status) => (
          <div key={status} className="bg-white shadow rounded-lg p-4">
            <h2 className="text-lg font-medium text-gray-900 capitalize mb-4">
              {status.replace('_', ' ')} ({tasksByStatus[status as keyof typeof tasksByStatus].length})
            </h2>
            <div className="space-y-2">
              {tasksByStatus[status as keyof typeof tasksByStatus].map((task: any) => (
                <div
                  key={task.id}
                  className="p-3 bg-gray-50 rounded border border-gray-200"
                >
                  <p className="text-sm font-medium text-gray-900">{task.title}</p>
                  {task.due_date && (
                    <p className="text-xs text-gray-500 mt-1">
                      Due: {new Date(task.due_date).toLocaleDateString()}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

