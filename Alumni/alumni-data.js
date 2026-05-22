// Fake Alumni Data - Can be replaced with real data from backend
const alumniData = [
    {
        id: 1,
        name: "Rahul Sharma",
        batch: "2018",
        course: "Information Technology",
        company: "Software Engineer at Google",
        photo: "https://via.placeholder.com/150"
    },
    {
        id: 2,
        name: "Priya Patel",
        batch: "2019",
        course: "Electronics",
        company: "Data Scientist at Amazon",
        photo: "https://via.placeholder.com/150"
    },
    {
        id: 3,
        name: "Amit Kumar",
        batch: "2017",
        course: "Civil Engineering",
        company: "Project Manager at L&T",
        photo: "https://via.placeholder.com/150"
    },
    {
        id: 4,
        name: "Sneha Das",
        batch: "2020",
        course: "Mechanical",
        company: "Researcher at IIT Delhi",
        photo: "https://via.placeholder.com/150"
    },
    {
        id: 5,
        name: "Vikram Singh",
        batch: "2016",
        course: "Electrical",
        company: "Senior Engineer at TCS",
        photo: "https://via.placeholder.com/150"
    },
    {
        id: 6,
        name: "Anjali Rao",
        batch: "2019",
        course: "Architecture",
        company: "Architect at Hafeez Contractor",
        photo: "https://via.placeholder.com/150"
    }
];

// Function to render alumni cards dynamically
function renderAlumniCards() {
    const alumniGrid = document.getElementById('alumniGrid');
    if (!alumniGrid) return;
    
    alumniGrid.innerHTML = alumniData.map(alumni => `
        <div class="alumni-card">
            <div class="alumni-photo">
                <img src="${alumni.photo}" alt="${alumni.name}">
            </div>
            <div class="alumni-info">
                <h3>${alumni.name}</h3>
                <p class="alumni-batch">Batch: ${alumni.batch}</p>
                <p class="alumni-course">${alumni.course}</p>
                <p class="alumni-company">${alumni.company}</p>
            </div>
        </div>
    `).join('');
}

// Call the function when DOM is ready
document.addEventListener('DOMContentLoaded', renderAlumniCards);
