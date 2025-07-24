'use client'

import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 px-4">
      <h1 className="text-4xl font-bold mb-4 text-center">Welcome to Platoro</h1>
      <p className="text-gray-600 mb-8 text-center max-w-md">
        Track your finances intelligently with smart insights and a beautiful dashboard.
      </p>
      <div className="flex space-x-4">
        <button
          onClick={() => router.push('/login')}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
        >
          Log In
        </button>
        <button
          onClick={() => router.push('/signup')}
          className="bg-gray-200 text-gray-800 px-6 py-2 rounded hover:bg-gray-300 transition"
        >
          Create Account
        </button>
      </div>
    </div>
  )
}
