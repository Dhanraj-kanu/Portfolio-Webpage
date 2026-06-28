document.addEventListener("DOMContentLoaded", () => {
    const storedTasks = JSON.parse(localStorage.getItem('tasks'));
    if (storedTasks) {
        storedTasks.forEach((task) => tasks.push(task));
        updateTasksList();
        updateStats();
    }
});

let tasks = [];

const saveTasks = () => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
};

const addTasks = () => {
    const taskInput = document.getElementById('taskinput');
    const text = taskInput.value.trim();
    if (text) {
        tasks.push({ text: text, completed: false });
        taskInput.value = "";
        updateTasksList();
        updateStats();
        saveTasks();
    }
};

const toggleComplete = (index) => {
    tasks[index].completed = !tasks[index].completed;
    updateTasksList();
    updateStats();
    saveTasks();
};

const deleteTask = (index) => {
    tasks.splice(index, 1);
    updateTasksList();
    updateStats();
    saveTasks();
};

const editTask = (index) => {
    const taskInput = document.getElementById('taskinput');
    taskInput.value = tasks[index].text;
    tasks.splice(index, 1);
    updateTasksList();
    saveTasks();
};

const updateStats = () => {
    const completedTasks = tasks.filter((task) => task.completed).length;
    const totalTasks = tasks.length;
    const progress = (completedTasks / totalTasks) * 100;
    const progressBar = document.getElementById('progress');
    progressBar.style.width = `${progress}%`;

    document.getElementById("numbers").innerText = `${completedTasks}/${totalTasks}`;
    if (tasks.length && completedTasks === totalTasks) {
        blastConfetti();
    }
};

const updateTasksList = () => {
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = "";

    tasks.forEach((task, index) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
        <div class="taskItem">
            <div class="task ${task.completed ? 'completed' : ''}">
                <input type="checkbox" class="checkbox" ${task.completed ? "checked" : ""} />
                <p>${task.text}</p>
            </div>
            <div class="icons">
                <img src="data:image/png;base64,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" onClick="editTask(${index})" />
                <img src="data:image/png;base64,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" onClick="deleteTask(${index})" />
            </div>
        </div>
        `;
        listItem.querySelector('input').addEventListener('change', () => toggleComplete(index));
        taskList.append(listItem);
    });
};

document.getElementById("newtask").addEventListener("click", function (e) {
    e.preventDefault();
    addTasks();
});

function blastConfetti() {
    const count = 200;
    const defaults = {
        origin: { y: 0.7 },
    };

    function fire(particleRatio, opts) {
        confetti(
            Object.assign({}, defaults, opts, {
                particleCount: Math.floor(count * particleRatio),
            })
        );
    }

    fire(0.25, {
        spread: 26,
        startVelocity: 55,
    });

    fire(0.2, {
        spread: 60,
    });

    fire(0.35, {
        spread: 100,
        decay: 0.91,
        scalar: 0.8,
    });

    fire(0.1, {
        spread: 120,
        startVelocity: 25,
        decay: 0.92,
        scalar: 1.2,
    });

    fire(0.1, {
        spread: 120,
        startVelocity: 45,
    });
}
