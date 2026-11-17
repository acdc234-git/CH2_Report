/**
 * Todo List
 * 기능: 추가(Create) / 조회(Read, 필터) / 수정(Update) / 삭제(Delete) / 완료 토글
 * 저장: localStorage (새로고침해도 목록이 남는다)
 */

// ===== 화면 요소 =====
const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const emptyMessage = document.querySelector("#empty-message");
const countText = document.querySelector("#todo-count");
const filterButtons = document.querySelectorAll(".filter-btn");

// ===== 상태 =====
const STORAGE_KEY = "todos";
let todos = loadTodos();      // [{ id, text, done }]
let currentFilter = "all";    // all | active | completed
let editingId = null;         // 지금 수정 중인 항목 id

// ===== 저장소 =====
function loadTodos() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (error) {
        return [];
    }
}

function saveTodos() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
    } catch (error) {
        // 저장이 안 돼도 화면 동작은 계속된다
    }
}

// ===== 추가 =====
form.addEventListener("submit", function (event) {
    event.preventDefault();

    const text = input.value.trim();
    if (text === "") return;          // 빈 값은 추가하지 않는다

    todos.push({ id: Date.now(), text: text, done: false });
    input.value = "";
    saveTodos();
    render();
});

// ===== 조회(필터) =====
filterButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        currentFilter = button.dataset.filter;

        filterButtons.forEach(function (other) {
            other.classList.remove("active");
        });
        button.classList.add("active");

        editingId = null;             // 필터를 바꾸면 수정 중이던 건 취소
        render();
    });
});

// ===== 완료 토글 =====
list.addEventListener("change", function (event) {
    if (!event.target.classList.contains("toggle")) return;

    const id = Number(event.target.closest("li").dataset.id);
    const todo = todos.find(function (item) { return item.id === id; });
    if (!todo) return;

    todo.done = event.target.checked;
    saveTodos();
    render();
});

// ===== 수정 / 삭제 =====
list.addEventListener("click", function (event) {
    const button = event.target.closest("button");
    if (!button) return;

    const id = Number(button.closest("li").dataset.id);
    const action = button.dataset.action;

    if (action === "edit") {
        editingId = id;
        render();
    } else if (action === "save") {
        applyEdit(id);
    } else if (action === "cancel") {
        editingId = null;
        render();
    } else if (action === "delete") {
        todos = todos.filter(function (item) { return item.id !== id; });
        saveTodos();
        render();
    }
});

// 수정 중 Enter = 저장, Esc = 취소
list.addEventListener("keydown", function (event) {
    if (!event.target.classList.contains("edit-input")) return;

    const id = Number(event.target.closest("li").dataset.id);

    if (event.key === "Enter") {
        applyEdit(id);
    } else if (event.key === "Escape") {
        editingId = null;
        render();
    }
});

function applyEdit(id) {
    const field = list.querySelector("li[data-id='" + id + "'] .edit-input");
    if (!field) return;

    const text = field.value.trim();
    if (text === "") return;          // 빈 값으로는 수정하지 않는다

    const todo = todos.find(function (item) { return item.id === id; });
    if (todo) todo.text = text;

    editingId = null;
    saveTodos();
    render();
}

// ===== 그리기 =====
function getVisibleTodos() {
    if (currentFilter === "active") {
        return todos.filter(function (item) { return !item.done; });
    }
    if (currentFilter === "completed") {
        return todos.filter(function (item) { return item.done; });
    }
    return todos;
}

function render() {
    const visible = getVisibleTodos();

    list.innerHTML = "";

    visible.forEach(function (todo) {
        const li = document.createElement("li");
        li.dataset.id = todo.id;
        li.className = "todo-item";
        if (todo.done) li.classList.add("done");

        if (todo.id === editingId) {
            // 수정 모드
            const field = document.createElement("input");
            field.type = "text";
            field.className = "edit-input";
            field.value = todo.text;

            const saveButton = document.createElement("button");
            saveButton.type = "button";
            saveButton.dataset.action = "save";
            saveButton.textContent = "저장";

            const cancelButton = document.createElement("button");
            cancelButton.type = "button";
            cancelButton.dataset.action = "cancel";
            cancelButton.textContent = "취소";

            li.append(field, saveButton, cancelButton);
        } else {
            // 일반 모드
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.className = "toggle";
            checkbox.checked = todo.done;

            const text = document.createElement("span");
            text.className = "text";
            text.textContent = todo.text;

            const editButton = document.createElement("button");
            editButton.type = "button";
            editButton.dataset.action = "edit";
            editButton.textContent = "수정";

            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.dataset.action = "delete";
            deleteButton.textContent = "삭제";

            li.append(checkbox, text, editButton, deleteButton);
        }

        list.appendChild(li);
    });

    // 수정 모드면 입력칸에 커서를 둔다
    const editing = list.querySelector(".edit-input");
    if (editing) {
        editing.focus();
        editing.setSelectionRange(editing.value.length, editing.value.length);
    }

    // 빈 목록 안내
    emptyMessage.style.display = visible.length === 0 ? "block" : "none";
    if (visible.length === 0) {
        if (currentFilter === "active") {
            emptyMessage.textContent = "진행중인 할 일이 없습니다.";
        } else if (currentFilter === "completed") {
            emptyMessage.textContent = "완료한 할 일이 없습니다.";
        } else {
            emptyMessage.textContent = "할 일이 없습니다.";
        }
    }

    // 남은 개수
    const remaining = todos.filter(function (item) { return !item.done; }).length;
    countText.textContent = remaining + "개 남음";
}

render();
