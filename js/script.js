document.addEventListener('DOMContentLoaded', function() {
    // Auto-fill nutrition data when typing meal name
    const nameInput = document.getElementById('name');
    if (nameInput) {
        const caloriesInput = document.getElementById('calories');
        const proteinInput = document.getElementById('protein');
        const carbsInput = document.getElementById('carbs');
        const fatInput = document.getElementById('fat');
        
        let timeout;
        nameInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const foodName = nameInput.value.trim();
                if (foodName.length > 2) {
                    fetchNutritionData(foodName);
                }
            }, 800);
        });
        
        function fetchNutritionData(foodName) {
            fetch(/api/nutrition/${encodeURIComponent(foodName)})
                .then(response => {
                    if (!response.ok) throw new Error('Nutrition data not found');
                    return response.json();
                })
                .then(data => {
                    if (!data.error) {
                        caloriesInput.value = data.calories || '';
                        proteinInput.value = data.protein || '';
                        carbsInput.value = data.carbs || '';
                        fatInput.value = data.fat || '';
                        showToast('Nutrition data auto-filled!', 'success');
                    }
                })
                .catch(error => {
                    console.log('Could not fetch nutrition data:', error);
                });
        }
    }
    
    // Show toast notifications
    function showToast(message, type) {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = toast show align-items-center text-white bg-${type};
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
