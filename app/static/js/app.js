let currentPage = 1;
const perPage = 10;
let currentEmployees = []; // Глобальный массив для хранения списка сотрудников текущей страницы
let editingEmployeeId = null; // ID сотрудника в режиме редактирования (null при создании)

document.addEventListener('DOMContentLoaded', () => {
    fetchEmployees();
});

function applyFilters() {
    currentPage = 1;
    fetchEmployees();
}

function resetFilters() {
    document.getElementById('search').value = '';
    document.getElementById('gender').value = '';
    document.getElementById('age_from').value = '';
    document.getElementById('age_to').value = '';
    currentPage = 1;
    fetchEmployees();
}

// Запрос данных с бэкенда
async function fetchEmployees() {
    const search = document.getElementById('search').value;
    const gender = document.getElementById('gender').value;
    const ageFrom = document.getElementById('age_from').value;
    const ageTo = document.getElementById('age_to').value;

    let url = `/api/v1/employees/?page=${currentPage}&per_page=${perPage}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (gender) url += `&gender=${gender}`;
    if (ageFrom) url += `&age_from=${ageFrom}`;
    if (ageTo) url += `&age_to=${ageTo}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Ошибка при получении данных');
        const data = await response.json();
        
        currentEmployees = data.items; // Сохраняем полученные данные в кэш для редактирования
        renderTable(data.items);
        renderPagination(data.count);
    } catch (error) {
        console.error(error);
        const tbody = document.getElementById('employees-table-body');
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-red-500">Не удалось загрузить данные</td></tr>`;
    }
}

function renderTable(employees) {
    const tbody = document.getElementById('employees-table-body');
    tbody.innerHTML = '';

    if (employees.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-gray-500">Сотрудники не найдены</td></tr>`;
        return;
    }

    employees.forEach(emp => {
        const patronymic = emp.patronymic ? ` ${emp.patronymic}` : '';
        const fullName = `${emp.last_name} ${emp.first_name}${patronymic}`;
        const genderText = emp.gender === 'male' ? 'Мужской' : 'Женский';
        const birthDate = emp.birth_date ? emp.birth_date : '-';
        
        const avatarUrl = emp.avatar_url || '/static/files/default_user_image.png';

        tbody.innerHTML += `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-3 px-4">${emp.id}</td>
                <td class="py-3 px-4">
                    <div class="relative group inline-block cursor-pointer hover:z-50">
                        <img src="${avatarUrl}" alt="Фото" class="w-10 h-10 object-cover rounded border border-gray-300">
                        <div class="hidden group-hover:block absolute z-50 bg-white p-1 border border-gray-300 shadow-xl rounded left-full top-1/2 -translate-y-1/2 ml-3 w-max">
                            <img src="${avatarUrl}" alt="Увеличенное фото" class="w-48 h-48 object-cover rounded">
                        </div>
                    </div>
                </td>
                <td class="py-3 px-4 font-medium">${fullName}</td>
                <td class="py-3 px-4">${emp.phone}</td>
                <td class="py-3 px-4">${genderText}</td>
                <td class="py-3 px-4">${birthDate}</td>
                <td class="py-3 px-4 space-x-2">
                    <!-- Заменили вызов функции на editEmployee и передаем только ID -->
                    <button onclick="editEmployee(${emp.id})" class="text-blue-600 hover:text-blue-950 font-semibold">
                        Изменить
                    </button>
                    <button onclick="deleteEmployee(${emp.id})" class="text-red-600 hover:text-red-950 font-semibold">
                        Удалить
                    </button>
                </td>
            </tr>
        `;
    });
}

function renderPagination(totalCount) {
    document.getElementById('total-count').textContent = totalCount;
    
    const totalPages = Math.ceil(totalCount / perPage) || 1;
    const showingCount = Math.min(currentPage * perPage, totalCount);
    document.getElementById('showing-count').textContent = showingCount;

    const controls = document.getElementById('pagination-controls');
    controls.innerHTML = '';

    const prevDisabled = currentPage === 1 ? 'disabled opacity-50 cursor-not-allowed' : '';
    controls.innerHTML += `
        <button onclick="changePage(${currentPage - 1})" ${prevDisabled} class="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300">
            Назад
        </button>
    `;

    for (let i = 1; i <= totalPages; i++) {
        const activeClass = i === currentPage ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300';
        controls.innerHTML += `
            <button onclick="changePage(${i})" class="${activeClass} px-3 py-1 rounded">
                ${i}
            </button>
        `;
    }

    const nextDisabled = currentPage === totalPages ? 'disabled opacity-50 cursor-not-allowed' : '';
    controls.innerHTML += `
        <button onclick="changePage(${currentPage + 1})" ${nextDisabled} class="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300">
            Вперед
        </button>
    `;
}

function changePage(page) {
    currentPage = page;
    fetchEmployees();
}

async function deleteEmployee(id) {
    if (confirm("Вы уверены, что хотите удалить сотрудника?")) {
        try {
            const response = await fetch(`/api/v1/employees/${id}`, { method: 'DELETE' });
            if (response.ok) {
                fetchEmployees();
            } else {
                alert('Не удалось удалить сотрудника');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    }
}

// Открытие формы в режиме создания нового сотрудника
function openModal() {
    document.getElementById('employee-id').value = '';

    document.getElementById('employee-avatar-url').value = '';
    
    document.getElementById('avatar-preview-container').classList.add('hidden');
    document.getElementById('avatar-preview').src = '';

    const modalTitle = document.getElementById('modal-title');
    const submitBtn = document.getElementById('modal-submit-btn');
    if (modalTitle) modalTitle.textContent = 'Новый сотрудник';
    if (submitBtn) submitBtn.textContent = 'Создать';

    document.getElementById('add-employee-form').reset();
    document.getElementById('add-employee-modal').classList.remove('hidden');
}

// Открытие формы в режиме изменения существующего сотрудника
function editEmployee(id) {
    const employee = currentEmployees.find(emp => emp.id === id);
    if (!employee) return;

    document.getElementById('add-employee-form').reset();

    // Записываем ID и текущий URL аватара в скрытые поля
    document.getElementById('employee-id').value = id;
    document.getElementById('employee-avatar-url').value = employee.avatar_url || '';

    // Управляем превью картинки
    const previewContainer = document.getElementById('avatar-preview-container');
    const previewImg = document.getElementById('avatar-preview');
    
    if (employee.avatar_url) {
        previewImg.src = employee.avatar_url;
        previewContainer.classList.remove('hidden');
    } else {
        previewImg.src = '';
        previewContainer.classList.add('hidden');
    }

    // Тексты модального окна
    const modalTitle = document.getElementById('modal-title');
    const submitBtn = document.getElementById('modal-submit-btn');
    if (modalTitle) modalTitle.textContent = 'Изменить данные сотрудника';
    if (submitBtn) submitBtn.textContent = 'Сохранить изменения';

    // Заполнение остальных полей
    document.getElementById('new-last-name').value = employee.last_name || '';
    document.getElementById('new-first-name').value = employee.first_name || '';
    document.getElementById('new-patronymic').value = employee.patronymic || '';
    document.getElementById('new-phone').value = employee.phone || '';
    document.getElementById('new-gender').value = employee.gender || '';
    document.getElementById('new-birth-date').value = employee.birth_date || '';

    document.getElementById('add-employee-modal').classList.remove('hidden');

}

function closeModal() {
    document.getElementById('add-employee-modal').classList.add('hidden');
    document.getElementById('add-employee-form').reset();
    editingEmployeeId = null;
}

async function addEmployee(event) {
    event.preventDefault();

    const employeeId = document.getElementById('employee-id').value;
    // Считываем текущий url аватара из скрытого поля
    const currentAvatarUrl = document.getElementById('employee-avatar-url').value;

    const employeeData = {
        last_name: document.getElementById('new-last-name').value.trim(),
        first_name: document.getElementById('new-first-name').value.trim(),
        patronymic: document.getElementById('new-patronymic').value.trim() || null,
        phone: document.getElementById('new-phone').value.trim(),
        gender: document.getElementById('new-gender').value,
        birth_date: document.getElementById('new-birth-date').value || null,
    };
    if (currentAvatarUrl) {
        employeeData.avatar_url = currentAvatarUrl;
    }   
    const formData = new FormData();
    formData.append('form_data', JSON.stringify(employeeData));

    const fileInput = document.getElementById('new-file');
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    const isEditing = employeeId !== '';
    const url = isEditing ? `/api/v1/employees/${employeeId}` : '/api/v1/employees/';
    const method = isEditing ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'accept': 'application/json'
            },
            body: formData
        });

        if (response.ok) {
            closeModal();
            fetchEmployees();
        } else {
            const errData = await response.json().catch(() => ({}));
            alert(errData.detail || 'Произошла ошибка при сохранении данных сотрудника');
        }
    } catch (error) {
        console.error('Ошибка отправки запроса:', error);
        alert('Не удалось связаться с сервером');
    }
}