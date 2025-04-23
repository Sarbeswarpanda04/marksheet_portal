// DOM Elements
const themeToggle = document.querySelector('.theme-toggle');
const themeToggleIcon = document.getElementById('theme-toggle-icon');
const loginForm = document.getElementById('loginForm');
const toggleBtns = document.querySelectorAll('.toggle-btn');
const formHeader = document.querySelector('.form-header');
const userIdentifier = document.getElementById('userIdentifier');
const particles = document.getElementById('particles');

// Constants
const DARK_MODE_KEY = 'darkMode';
const REMEMBER_ME_KEY = 'rememberMe';
const LANGUAGE_KEY = 'preferredLanguage';

// // Translations
// const translations = {
//     en: {
//         studentLogin: 'Student Login',
//         adminLogin: 'Admin Login',
//         studentAccess: 'Access your marksheet and academic performance',
//         adminAccess: 'Manage student records and generate reports',
//         rollNumber: 'Roll Number',
//         username: 'Username',
//         password: 'Password',
//         rememberMe: 'Remember me',
//         forgotPassword: 'Forgot Password?',
//         login: 'Login',
//         orLoginWith: 'Or login with'
//     },
//     hi: {
//         studentLogin: 'छात्र लॉगिन',
//         adminLogin: 'व्यवस्थापक लॉगिन',
//         studentAccess: 'अपनी मार्कशीट और शैक्षणिक प्रदर्शन देखें',
//         adminAccess: 'छात्र रिकॉर्ड प्रबंधित करें और रिपोर्ट जनरेट करें',
//         rollNumber: 'रोल नंबर',
//         username: 'उपयोगकर्ता नाम',
//         password: 'पासवर्ड',
//         rememberMe: 'मुझे याद रखें',
//         forgotPassword: 'पासवर्ड भूल गए?',
//         login: 'लॉगिन',
//         orLoginWith: 'या इसके साथ लॉगिन करें'
//     },
//     bn: {
//         studentLogin: 'ছাত্র লগইন',
//         adminLogin: 'অ্যাডমিন লগইন',
//         studentAccess: 'আপনার মার্কশিট এবং একাডেমিক পারফরম্যান্স দেখুন',
//         adminAccess: 'ছাত্র রেকর্ড পরিচালনা করুন এবং রিপোর্ট তৈরি করুন',
//         rollNumber: 'রোল নম্বর',
//         username: 'ব্যবহারকারীর নাম',
//         password: 'পাসওয়ার্ড',
//         rememberMe: 'আমাকে মনে রাখুন',
//         forgotPassword: 'পাসওয়ার্ড ভুলে গেছেন?',
//         login: 'লগইন',
//         orLoginWith: 'অথবা এর সাথে লগইন করুন'
//     }
// };

// Add these new DOM elements at the top with other DOM elements
const loadingOverlay = document.createElement('div');
loadingOverlay.className = 'loading-overlay';
loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';
document.body.appendChild(loadingOverlay);

// Add new utility functions
function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}

// Add success/error toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div class="toast-content ${type}">
            <i class="fas ${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(() => {
        toast.style.transform = 'translateX(0)';
        toast.style.opacity = '1';
    });

    // Auto remove
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getToastIcon(type) {
    switch(type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-times-circle';
        case 'warning': return 'fa-exclamation-circle';
        default: return 'fa-info-circle';
    }
}

// Add keyboard navigation
function handleTabNavigation(e) {
    if (e.key === 'Tab') {
        const focusableElements = loginForm.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                lastElement.focus();
                e.preventDefault();
            }
        } else {
            if (document.activeElement === lastElement) {
                firstElement.focus();
                e.preventDefault();
            }
        }
    }
}

// Initialize
function initialize() {
    initializeTheme();
    // initializeLanguage();
    initializeRememberMe();
    initializeParticles();
    addInputAnimations();
    // Set default login type to "Student"
    const studentToggleBtn = document.querySelector('.toggle-btn[data-type="student"]');
    if (studentToggleBtn) {
        studentToggleBtn.click(); // Simulate a click to activate the "Student" toggle
    }
}

// Theme Management
function initializeTheme() {
    const isDarkMode = localStorage.getItem(DARK_MODE_KEY) === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        themeToggleIcon.classList.replace('fa-moon', 'fa-sun');
    }
}

// // Language Management
// function initializeLanguage() {
//     const savedLanguage = localStorage.getItem(LANGUAGE_KEY) || 'en';
//     languageSelect.value = savedLanguage;
//     updateLanguage(savedLanguage);
// }

// function updateLanguage(lang) {
//     const t = translations[lang];
//     document.querySelectorAll('[data-translate]').forEach(element => {
//         const key = element.dataset.translate;
//         if (t[key]) {
//             element.textContent = t[key];
//         }
//     });
//     localStorage.setItem(LANGUAGE_KEY, lang);
// }

// Remember Me
function initializeRememberMe() {
    const remembered = localStorage.getItem(REMEMBER_ME_KEY);
    if (remembered) {
        const { identifier, type } = JSON.parse(remembered);
        userIdentifier.value = identifier;
        rememberMeCheckbox.checked = true;
        if (type === 'admin') {
            document.querySelector('.toggle-btn[data-type="admin"]').click();
        }
    }
}

// Particles Animation
function initializeParticles() {
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        particles.appendChild(particle);
    }
}



// // Form Submission with Remember Me
// async function handleLogin(e) {
//     e.preventDefault();
    
//     const isAdmin = document.querySelector('.toggle-btn[data-type="admin"]').classList.contains('active');
//     const identifier = userIdentifier.value;
//     const password = userPassword.value;

//     if (validateLogin(identifier, password, isAdmin)) {
//         showLoading();

//         try {
//             // Simulate API call
//             await new Promise(resolve => setTimeout(resolve, 1500));

//             // Handle Remember Me
//             if (rememberMeCheckbox.checked) {
//                 localStorage.setItem(REMEMBER_ME_KEY, JSON.stringify({
//                     identifier,
//                     type: isAdmin ? 'admin' : 'student'
//                 }));
//                 showToast('Login preferences saved', 'success');
//             } else {
//                 localStorage.removeItem(REMEMBER_ME_KEY);
//             }

//             // // Redirect
//             // window.location.href = isAdmin ? 'pages/admin/admin-dashboard.html' : 'pages/student/student-dashboard.html';
//         } catch (error) {
//             showToast('Login failed. Please try again.', 'error');
//         } finally {
//             hideLoading();
//         }
//     }
// }

// Login Type Toggle
function updateLoginType(type) {
    const isAdmin = type === 'admin';
    
    // Update form header
    formHeader.querySelector('.card-icon i').className = isAdmin ? 'fas fa-user-shield' : 'fas fa-user-graduate';
    formHeader.querySelector('h2').textContent = isAdmin ? 'Admin Login' : 'Student Login';
    formHeader.querySelector('p').textContent = isAdmin ? 'Manage student records and generate reports' : 'Access your marksheet and academic performance';
    
    // Update input placeholders
    userIdentifier.placeholder = isAdmin ? 'Username' : 'Roll Number';
    
    // Update validation requirements
    userPassword.setAttribute('minlength', isAdmin ? '8' : '6');
    
    // Add animation
    formHeader.style.animation = 'fadeIn 0.3s ease-out';
    setTimeout(() => formHeader.style.animation = '', 300);
}

// Form Validation
function validateLogin(identifier, password, isAdmin) {
    const validations = [
        {
            condition: !identifier || identifier.trim() === '',
            message: isAdmin ? 'Please enter your username' : 'Please enter your roll number',
            type: 'error'
        },
        {
            condition: !password,
            message: 'Please enter your password',
            type: 'error'
        },
        {
            condition: password && password.length < (isAdmin ? 8 : 6),
            message: `Password must be at least ${isAdmin ? 8 : 6} characters long`,
            type: 'error'
        },
        {
            condition: isAdmin && !/[A-Z]/.test(password),
            message: 'Admin password must contain at least one uppercase letter',
            type: 'error'
        },
        {
            condition: isAdmin && !/[0-9]/.test(password),
            message: 'Admin password must contain at least one number',
            type: 'error'
        }
    ];

    const failures = validations.filter(v => v.condition);
    
    if (failures.length > 0) {
        failures.forEach(failure => showToast(failure.message, failure.type));
        return false;
    }
    
    return true;
}


// Toggle theme
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem(DARK_MODE_KEY, isDarkMode);
    
    // Toggle icon
    if (isDarkMode) {
        themeToggleIcon.classList.replace('fa-moon', 'fa-sun');
    } else {
        themeToggleIcon.classList.replace('fa-sun', 'fa-moon');
    }

    // Add animation effect
    themeToggle.style.transform = 'scale(1.1)';
    setTimeout(() => {
        themeToggle.style.transform = 'scale(1)';
    }, 200);
}



// Input Animations
function addInputAnimations() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = 'scale(1.02)';
        });
        input.addEventListener('blur', () => {
            input.parentElement.style.transform = 'scale(1)';
        });
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', initialize);
themeToggle.addEventListener('click', toggleTheme);
// loginForm.addEventListener('submit', handleLogin);
passwordToggle.addEventListener('click', togglePasswordVisibility);
// languageSelect.addEventListener('change', (e) => updateLanguage(e.target.value));
// socialButtons.forEach(button => {
//     button.addEventListener('click', () => handleSocialLogin(button.dataset.provider));
// });

// Toggle Button Event Listeners
toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        toggleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        updateLoginType(btn.dataset.type);
    });
});

// Keyboard Shortcuts
document.addEventListener('keypress', (e) => {
    // Theme toggle: Ctrl + T
    if (e.key === 't' && e.ctrlKey) {
        toggleTheme();
    }
    // Quick login type toggle: Ctrl + Q
    if (e.key === 'q' && e.ctrlKey) {
        const currentActive = document.querySelector('.toggle-btn.active');
        const nextType = currentActive.dataset.type === 'student' ? 'admin' : 'student';
        document.querySelector(`.toggle-btn[data-type="${nextType}"]`).click();
    }
});

// Add these event listeners at the bottom with other event listeners
document.addEventListener('keydown', handleTabNavigation);

// Add touch gesture support
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipeGesture();
});

function handleSwipeGesture() {
    const SWIPE_THRESHOLD = 50;
    const swipeDistance = touchEndX - touchStartX;
    
    if (Math.abs(swipeDistance) > SWIPE_THRESHOLD) {
        const currentActive = document.querySelector('.toggle-btn.active');
        const nextType = currentActive.dataset.type === 'student' ? 'admin' : 'student';
        document.querySelector(`.toggle-btn[data-type="${nextType}"]`).click();
    }
} 
























// login.js

// Toggle password visibility
document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("userPassword");
    const toggleIcon = document.querySelector(".password-toggle");

    if (toggleIcon) {
        toggleIcon.addEventListener("click", () => {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
            toggleIcon.classList.toggle("fa-eye");
            toggleIcon.classList.toggle("fa-eye-slash");
        });
    }
});
