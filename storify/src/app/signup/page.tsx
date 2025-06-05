'use client'

import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import PrimaryButton from '@/components/PrimaryButton'
import { useState } from 'react'

const formSchema = z.object({
  username: z.string().min(2, 'Username is required'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type FormValues = z.infer<typeof formSchema>

export default function SignupPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
  })

  const [message, setMessage] = useState<string | null>(null)

 const onSubmit = async (data: FormValues) => {
  setMessage(null)
  try {
    const res = await fetch('http://127.0.0.1:8000/auth/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    if (!res.status.toString().startsWith('2')) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Signup failed')
    }

    const user = await res.json()

    setMessage(
      `🎉 Account created for ${user.username}. Your user ID is ${user.id}.`
    )

    // Optional: redirect to login or dashboard after a delay
    //setTimeout(() => router.push('/login'), 2000)

  } catch (err: string | any) {
    setMessage(err.message)
  }
}


  return (
    <div className="mx-auto max-w-md px-4 py-12">
      <h1 className="text-2xl font-semibold mb-6">Sign Up</h1>

      {message && (
        <div
          className={`mb-4 text-sm ${
            message.includes('success') ? 'text-green-600' : 'text-red-600'
          }`}
        >
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Username</label>
          <input
            type="text"
            {...register('username')}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
          {errors.username && (
            <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            {...register('password')}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>

        <PrimaryButton type="submit" loading={isSubmitting} className="w-full">
          Create Account
        </PrimaryButton>
      </form>
    </div>
  )
}
