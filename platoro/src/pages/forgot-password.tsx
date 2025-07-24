import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const BASE_URL = 'https://jz9dh44oaj.execute-api.us-east-1.amazonaws.com/dev';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await axios.post(`${BASE_URL}/account/request-reset`, { email });
      setSuccess('Reset code sent! Redirecting...');
      setTimeout(() => router.push('/reset-password'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Request failed.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6 text-center">Forgot Password</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            required
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
          >
            Send Reset Code
          </button>
        </form>
        {error && <p className="text-red-500 mt-4">{error}</p>}
        {success && <p className="text-green-600 mt-4">{success}</p>}
        <p className="text-sm text-gray-600 mt-4 text-center">
          <a href="/login" className="text-blue-500 hover:underline">Back to login</a>
        </p>
      </div>
    </div>
  );
} 