/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
<<<<<<< HEAD
    "./src/**/forms.py",
=======
    './src/**/forms.py'
>>>>>>> dev-branch
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}
