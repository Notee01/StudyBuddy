/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./course/templates/*.html', 
  './quiz/templates/quiz/*.html',
  './material/templates/*.html',
  './survey/templates/*.html',
  './static/js/*.js',
  
  'templates/*.html',
  ],
  theme: {
    extend: {
      colors: {
        danger: '#dc3545', // Example color for "danger"
        success: '#28a745', // Example color for "success"
      },
    },
  },
  plugins: [
    
  ],
    
}

