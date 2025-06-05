'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'

const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/about' },
  { label: 'Blog', href: '/blog' },
  { label: 'Contact', href: '/contact' },
  { label: 'Sign Up', href: '/signup' },
  {label: 'Login', href: '/login' },
]

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="light:bg-white dark:bg-gray-800 border-b shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="text-xl font-semibold light:text-stone-900 dark:text-stone-50">
            MyApp
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex space-x-6">
            {navLinks.map(link => (
              <Link
                key={link.href}
                href={link.href}
                className="light:text-gray-700 dark:text-stone-50 hover:text-sky-400 transition"
              >
                {link.label}
              </Link>
            ))}
            
          </div>

          {/* Mobile Menu Toggle */}
          <button
            className="md:hidden light:text-gray-700 dark:text-stone-50 hover:text-sky-400 transition"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle Menu"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {isOpen && (
        <div className="md:hidden px-4 pb-4 space-y-2 ">
          {navLinks.map(link => (
            <Link
              key={link.href}
              href={link.href}
              className="block light:text-gray-700 dark:text-stone-50 hover:bg-gray-900 hover:bg-gray-100 transition rounded-md px-2 py-2"
              onClick={() => setIsOpen(false)}
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
