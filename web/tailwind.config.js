/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'primary': '#25d1f4',
                'primary-dim': '#1e8da5',
                'background-light': '#f5f8f8',
                'background-dark': '#101f22',
                'surface-dark': '#16262a',
                'border-color': '#283639',
            },
            fontFamily: {
                'display': ['Space Grotesk', 'sans-serif'],
                'mono': ['monospace'],
            },
            borderRadius: {
                DEFAULT: '0.25rem',
                'lg': '0.5rem',
                'xl': '0.75rem',
            },
            boxShadow: {
                'glow': '0 0 10px rgba(37, 209, 244, 0.3)',
            },
        },
    },
    plugins: [],
}
