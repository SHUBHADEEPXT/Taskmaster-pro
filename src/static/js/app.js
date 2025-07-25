// DOM Elements
const taskInput = document.getElementById('taskInput');
const taskDateTime = document.getElementById('taskDateTime');
const taskPriority = document.getElementById('taskPriority');
const addTaskBtn = document.getElementById('addTaskBtn');
const taskList = document.getElementById('taskList');
const filterButtons = document.querySelectorAll('.filter-btn');
const sortSelect = document.getElementById('sortSelect');
const clearCompletedBtn = document.getElementById('clearCompletedBtn');
const clearAllBtn = document.getElementById('clearAllBtn');
const prevPageBtn = document.getElementById('prevPageBtn');
const statusBtn = document.getElementById('statusBtn');
const pages = document.querySelectorAll('.page');
const searchInput = document.getElementById('searchInput');

// Statistics elements
const totalTasksSpan = document.getElementById('totalTasks');
const completedTasksSpan = document.getElementById('completedTasks');
const pendingTasksSpan = document.getElementById('pendingTasks');

// State management
let tasks = [];
let currentPage = 1;
let currentFilter = 'all';
let searchQuery = '';

// Theme management
const themeToggle = document.querySelector('.theme-toggle');
const themeIcon = themeToggle.querySelector('i');

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    updateStatistics();
    setupEventListeners();
    checkOverdueTasks();
});

function setupEventListeners() {
    addTaskBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });
    
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.filter;
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderTasks();
        });
    });
    
    sortSelect.addEventListener('change', renderTasks);
    clearCompletedBtn.addEventListener('click', clearCompleted);
    clearAllBtn.addEventListener('click', clearAll);
    
    // Update navigation event listeners
    prevPageBtn.addEventListener('click', () => navigatePage(-1));
    statusBtn.addEventListener('click', () => {
        if (currentPage === 1) {
            navigatePage(1); // Go to status page
        } else {
            navigatePage(-1); // Go back to add tasks
        }
    });
    
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        renderTasks();
    });

    // Theme toggle event listener
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

function addTask() {
    const text = taskInput.value.trim();
    if (!text) return;
    
    const task = {
        id: Date.now(),
        text,
        completed: false,
        createdAt: new Date().toISOString(),
        dueDate: taskDateTime.value,
        priority: taskPriority.value,
        description: '', // Added for future use
        tags: [], // Added for future use
        lastModified: new Date().toISOString()
    };
    
    tasks.push(task);
    saveTasks();
    renderTasks();
    updateStatistics();
    
    // Clear input
    taskInput.value = '';
    taskDateTime.value = '';
    taskPriority.value = 'medium';
    
    // Show success notification
    showNotification('Task added successfully!', 'success');
}

function renderTasks() {
    let filteredTasks = [...tasks];
    
    // Apply search filter
    if (searchQuery) {
        filteredTasks = filteredTasks.filter(task => 
            task.text.toLowerCase().includes(searchQuery) ||
            task.description.toLowerCase().includes(searchQuery) ||
            task.tags.some(tag => tag.toLowerCase().includes(searchQuery))
        );
    }
    
    // Apply status filter
    switch (currentFilter) {
        case 'pending':
            filteredTasks = filteredTasks.filter(task => !task.completed);
            break;
        case 'completed':
            filteredTasks = filteredTasks.filter(task => task.completed);
            break;
        case 'overdue':
            filteredTasks = filteredTasks.filter(task => 
                !task.completed && new Date(task.dueDate) < new Date()
            );
            break;
    }
    
    // Apply sorting
    const sortValue = sortSelect.value;
    filteredTasks.sort((a, b) => {
        switch (sortValue) {
            case 'priority-high':
                return getPriorityValue(b.priority) - getPriorityValue(a.priority);
            case 'priority-low':
                return getPriorityValue(a.priority) - getPriorityValue(b.priority);
            case 'date-asc':
                return new Date(a.dueDate) - new Date(b.dueDate);
            case 'date-desc':
                return new Date(b.dueDate) - new Date(a.dueDate);
            default: // priority-date
                const priorityDiff = getPriorityValue(b.priority) - getPriorityValue(a.priority);
                return priorityDiff !== 0 ? priorityDiff : new Date(a.dueDate) - new Date(b.dueDate);
        }
    });
    
    // Render tasks
    taskList.innerHTML = filteredTasks.map(task => `
        <li class="task-item ${task.completed ? 'completed' : ''} ${isOverdue(task) ? 'overdue' : ''}" data-id="${task.id}">
            <div class="task-content">
                <input type="checkbox" ${task.completed ? 'checked' : ''}>
                <div class="task-info">
                    <span class="task-text">${highlightSearchMatch(task.text)}</span>
                    ${task.description ? `<span class="task-description">${highlightSearchMatch(task.description)}</span>` : ''}
                    ${task.tags.length ? `<div class="task-tags">${task.tags.map(tag => `<span class="tag">${highlightSearchMatch(tag)}</span>`).join('')}</div>` : ''}
                </div>
                <span class="task-due-date">${formatDate(task.dueDate)}</span>
                <span class="task-priority ${task.priority}">${task.priority}</span>
            </div>
            <div class="task-actions">
                <button class="edit-btn" title="Edit task"><i class="fas fa-edit"></i></button>
                <button class="delete-btn" title="Delete task"><i class="fas fa-trash"></i></button>
            </div>
        </li>
    `).join('');
    
    // Add event listeners to new elements
    taskList.querySelectorAll('.task-item').forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');
        const editBtn = item.querySelector('.edit-btn');
        const deleteBtn = item.querySelector('.delete-btn');
        
        checkbox.addEventListener('change', () => toggleTask(item.dataset.id));
        editBtn.addEventListener('click', () => editTask(item.dataset.id));
        deleteBtn.addEventListener('click', () => deleteTask(item.dataset.id));
    });
}

function highlightSearchMatch(text) {
    if (!searchQuery) return text;
    const regex = new RegExp(`(${searchQuery})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function isOverdue(task) {
    return !task.completed && task.dueDate && new Date(task.dueDate) < new Date();
}

function checkOverdueTasks() {
    const overdueTasks = tasks.filter(isOverdue);
    if (overdueTasks.length > 0) {
        showNotification(`You have ${overdueTasks.length} overdue task(s)!`, 'warning');
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Trigger reflow
    notification.offsetHeight;
    
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function toggleTask(id) {
    const task = tasks.find(t => t.id === parseInt(id));
    if (task) {
        task.completed = !task.completed;
        task.lastModified = new Date().toISOString();
        saveTasks();
        renderTasks();
        updateStatistics();
        
        showNotification(
            task.completed ? 'Task marked as completed!' : 'Task marked as pending!',
            'success'
        );
    }
}

function editTask(id) {
    const task = tasks.find(t => t.id === parseInt(id));
    if (!task) return;
    
    const newText = prompt('Edit task:', task.text);
    if (newText !== null && newText.trim() !== '') {
        task.text = newText.trim();
        task.lastModified = new Date().toISOString();
        saveTasks();
        renderTasks();
        showNotification('Task updated successfully!', 'success');
    }
}

function deleteTask(id) {
    if (confirm('Are you sure you want to delete this task?')) {
        tasks = tasks.filter(t => t.id !== parseInt(id));
        saveTasks();
        renderTasks();
        updateStatistics();
        showNotification('Task deleted successfully!', 'success');
    }
}

function clearCompleted() {
    if (confirm('Are you sure you want to clear all completed tasks?')) {
        const completedCount = tasks.filter(task => task.completed).length;
        tasks = tasks.filter(task => !task.completed);
        saveTasks();
        renderTasks();
        updateStatistics();
        showNotification(`Cleared ${completedCount} completed task(s)!`, 'success');
    }
}

function clearAll() {
    if (confirm('Are you sure you want to clear all tasks?')) {
        const totalCount = tasks.length;
        tasks = [];
        saveTasks();
        renderTasks();
        updateStatistics();
        showNotification(`Cleared all ${totalCount} task(s)!`, 'success');
    }
}

function updateStatistics() {
    const total = tasks.length;
    const completed = tasks.filter(task => task.completed).length;
    const pending = total - completed;
    const overdue = tasks.filter(isOverdue).length;
    
    totalTasksSpan.textContent = total;
    completedTasksSpan.textContent = completed;
    pendingTasksSpan.textContent = pending;
    
    // Update overdue count in UI if element exists
    const overdueSpan = document.getElementById('overdueTasks');
    if (overdueSpan) {
        overdueSpan.textContent = overdue;
    }
}

function navigatePage(delta) {
    const newPage = currentPage + delta;
    if (newPage >= 1 && newPage <= pages.length) {
        // Remove active class from current page
        pages[currentPage - 1].classList.remove('active');
        
        // Add active class to new page
        pages[newPage - 1].classList.add('active');
        
        // Update current page
        currentPage = newPage;
        
        // Update navigation buttons
        prevPageBtn.disabled = currentPage === 1;
        
        // Update status button text and icon based on current page
        if (currentPage === 1) {
            statusBtn.innerHTML = 'Your Status <i class="fas fa-chart-line"></i>';
        } else {
            statusBtn.innerHTML = 'Add Tasks <i class="fas fa-plus"></i>';
        }
        
        // If going to status page, update statistics
        if (currentPage === 2) {
            updateStatistics();
            renderTasks();
        }
    }
}

// Utility functions
function getPriorityValue(priority) {
    const values = { high: 3, medium: 2, low: 1 };
    return values[priority] || 0;
}

function formatDate(dateString) {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    const now = new Date();
    const diff = date - now;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Tomorrow';
    if (days < 0) return `${Math.abs(days)} days ago`;
    return date.toLocaleString();
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
    }
}

function updateThemeIcon(theme) {
    themeIcon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}
