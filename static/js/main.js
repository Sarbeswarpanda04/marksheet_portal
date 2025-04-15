// This is the main JavaScript file for the Marksheet Portal
// It contains the code to handle the functionality of the portal

// This function will be called when the document is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Marksheet Portal Loaded ✅");
});


  document.addEventListener("DOMContentLoaded", function () {
    // ==== Mobile Navbar Toggle ====
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
  
    if (hamburger && navLinks) {
      hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
      });
    }
  
    const themeToggle = document.querySelector('.theme-toggle');
const body = document.body;

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark');
    localStorage.setItem('theme', body.classList.contains('dark') ? 'dark' : 'light');
  });

  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark');
  }
}

      
    // ==== Back-to-Top Button ====
    const backToTopBtn = document.getElementById('back-to-top');
  
    if (backToTopBtn) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
          backToTopBtn.style.display = 'block';
        } else {
          backToTopBtn.style.display = 'none';
        }
      });
  
      backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }
  });
  


  
  window.addEventListener("load", () => {
    document.body.classList.add("loaded");
  });
  



  const revealElements = document.querySelectorAll('.reveal');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
    }
  });
});

revealElements.forEach(el => observer.observe(el));

