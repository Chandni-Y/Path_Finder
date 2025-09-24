document.addEventListener('DOMContentLoaded', () => {

    // --- Side Menu Logic ---
    const menuToggle = document.getElementById('menu-toggle');
    const sideMenu = document.getElementById('side-menu');

    menuToggle.addEventListener('click', () => {
        sideMenu.classList.toggle('active');
    });

    document.addEventListener('click', (event) => {
        const isClickInsideMenu = sideMenu.contains(event.target) || menuToggle.contains(event.target);
        if (!isClickInsideMenu && sideMenu.classList.contains('active')) {
            sideMenu.classList.remove('active');
        }
    });

    // --- Active Menu Item Highlight ---
    const currentPath = window.location.pathname.split('/').pop();
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        item.classList.remove('active');
        const href = item.getAttribute('href');
        const filename = href.split('/').pop();
        if (filename === currentPath || (currentPath === '' && filename === 'index.html')) {
            item.classList.add('active');
        }
    });

    // --- Register Button Disappearance ---
    const registerBtn = document.querySelector('.register-btn');
    if (registerBtn) {
        registerBtn.addEventListener('click', (e) => {
            // This will make the button disappear on click
            // e.preventDefault(); // Uncomment this line if you want to stop the link navigation
            registerBtn.style.display = 'none';
        });
    }

    // --- State and City Dropdowns (Registration Page) ---
    const stateSelect = document.getElementById('state');
    const citySelect = document.getElementById('city');

    const statesAndCities = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore"],
        "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat"],
        "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Jorhat"],
        "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur"],
        "Goa": ["Panaji", "Margao", "Vasco da Gama"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "Haryana": ["Faridabad", "Gurgaon", "Panipat", "Ambala"],
        "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
        "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
        "Manipur": ["Imphal", "Thoubal"],
        "Meghalaya": ["Shillong", "Tura"],
        "Mizoram": ["Aizawl"],
        "Nagaland": ["Kohima", "Dimapur"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
        "Sikkim": ["Gangtok"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
        "Tripura": ["Agartala"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Prayagraj"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur"]
    };

    if (stateSelect && citySelect) {
        // Populate states
        for (const state in statesAndCities) {
            const option = document.createElement('option');
            option.value = state;
            option.textContent = state;
            stateSelect.appendChild(option);
        }

        stateSelect.addEventListener('change', (event) => {
            const selectedState = event.target.value;
            citySelect.innerHTML = '<option value="">Select a city</option>'; // Reset cities
            citySelect.disabled = true;

            if (selectedState) {
                const cities = statesAndCities[selectedState];
                cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
                citySelect.disabled = false;
            }
        });
    }

    // --- Dashboard Pie Chart ---
    const ctx = document.getElementById('career-quiz-chart');
    if (ctx) {
        const data = {
            labels: ['Artistic', 'Realistic', 'Social', 'Enterprising', 'Conventional', 'Investigative'],
            datasets: [{
                label: 'RIASEC Scores',
                data: [35, 25, 15, 10, 8, 7], // Example data
                backgroundColor: [
                    '#4CAF50', // Artistic (Green)
                    '#2196F3', // Realistic (Blue)
                    '#FFC107', // Social (Yellow)
                    '#FF9800', // Enterprising (Orange)
                    '#9E9E9E', // Conventional (Grey)
                    '#7B1FA2'  // Investigative (Purple)
                ],
                borderWidth: 1,
            }]
        };

        const config = {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false,
                    }
                }
            },
        };

        new Chart(ctx, config);
    }
});