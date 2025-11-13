const STORAGE_KEY = 'focusflow-items-v1';

const state = {
  items: [],
  filters: {
    type: 'all',
    search: '',
    tag: 'all',
  },
};

const selectors = {
  board: document.getElementById('board'),
  counts: {
    note: document.getElementById('count-note'),
    reminder: document.getElementById('count-reminder'),
    task: document.getElementById('count-task'),
  },
  lists: {
    note: document.getElementById('list-note'),
    reminder: document.getElementById('list-reminder'),
    task: document.getElementById('list-task'),
  },
  templates: {
    item: document.getElementById('item-template'),
    chip: document.getElementById('chip-template'),
  },
  form: document.getElementById('item-form'),
  editDialog: document.getElementById('edit-dialog'),
  editForm: document.getElementById('edit-form'),
  searchInput: document.getElementById('search-input'),
  typeFilters: document.getElementById('type-filters'),
  tagFilters: document.getElementById('tag-filters'),
  themeToggle: document.getElementById('toggle-theme'),
  createPanelToggle: document.getElementById('open-create-panel'),
};

const typeConfig = {
  note: { icon: '📝', label: 'Note' },
  reminder: { icon: '⏰', label: 'Reminder' },
  task: { icon: '✅', label: 'Task' },
};

init();

function init() {
  restoreTheme();
  loadItems();
  render();
  attachListeners();
}

function restoreTheme() {
  const savedTheme = localStorage.getItem('focusflow-theme');
  if (savedTheme) {
    document.body.dataset.theme = savedTheme;
    updateThemeToggle(savedTheme);
  }
}

function updateThemeToggle(theme) {
  const icon = theme === 'dark' ? '🌙' : '☀';
  selectors.themeToggle.querySelector('.icon').textContent = icon;
  selectors.themeToggle.querySelector('.label').textContent =
    theme === 'dark' ? 'Light mode' : 'Switch theme';
}

function attachListeners() {
  selectors.form.addEventListener('submit', handleCreate);
  selectors.form.addEventListener('reset', () => selectors.form.reset());

  const typeRadios = selectors.form.querySelectorAll('input[name="type"]');
  typeRadios.forEach((radio) => {
    radio.addEventListener('change', handleTypeToggle);
  });

  applyTypeUI(selectors.form.querySelector('input[name="type"]:checked').value);

  selectors.themeToggle.addEventListener('click', toggleTheme);
  selectors.createPanelToggle.addEventListener('click', focusFirstField);

  selectors.searchInput.addEventListener('input', (event) => {
    state.filters.search = event.target.value.trim().toLowerCase();
    render();
  });

  selectors.typeFilters.addEventListener('click', (event) => {
    const button = event.target.closest('.chip');
    if (!button) return;
    state.filters.type = button.dataset.type;
    setSelectedChip(selectors.typeFilters, button);
    render();
  });

  selectors.tagFilters.addEventListener('click', (event) => {
    const chip = event.target.closest('.chip');
    if (!chip || !chip.dataset.tag) return;
    state.filters.tag = chip.dataset.tag;
    setSelectedChip(selectors.tagFilters, chip);
    render();
  });

  selectors.editForm.addEventListener('submit', handleEditSubmit);
}

function toggleTheme() {
  const nextTheme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = nextTheme;
  localStorage.setItem('focusflow-theme', nextTheme);
  updateThemeToggle(nextTheme);
}

function focusFirstField() {
  selectors.form.querySelector('input[name="title"]').focus();
}

function handleTypeToggle(event) {
  const type = event.target.value;
  applyTypeUI(type);
}

function applyTypeUI(type) {
  const datetimeField = document.getElementById('datetime-field');
  const detailsField = document.getElementById('details-field');

  if (type === 'note') {
    datetimeField.style.display = 'none';
    detailsField.querySelector('textarea').placeholder = 'Capture thoughts, ideas, or quick sketches.';
  } else {
    datetimeField.style.display = 'flex';
    detailsField.querySelector('textarea').placeholder = 'Add context or next steps.';
  } else {
    datetimeField.style.display = 'flex';
    detailsField.querySelector('textarea').placeholder = 'Add context or next steps.';
  }

  if (type === 'note') {
    datetimeField.querySelector('input').value = '';
  }
}

function handleCreate(event) {
  event.preventDefault();
  const formData = new FormData(selectors.form);
  const type = formData.get('type');
  const title = formData.get('title').trim();
  const details = formData.get('details').trim();
  const datetime = formData.get('datetime');
  const tags = parseTags(formData.get('tags'));

  if (!title) {
    alert('Please add a title before saving.');
    return;
  }

  const item = {
    id: crypto.randomUUID(),
    type,
    title,
    details,
    tags,
    datetime: datetime || null,
    completed: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  state.items.push(item);
  persistItems();
  selectors.form.reset();
  render();
}

function handleEditSubmit(event) {
  event.preventDefault();
  const formData = new FormData(selectors.editForm);
  const id = formData.get('id');
  const title = formData.get('title').trim();
  const details = formData.get('details').trim();
  const datetime = formData.get('datetime');
  const tags = parseTags(formData.get('tags'));

  if (!title) {
    alert('Title is required.');
    return;
  }

  const item = state.items.find((entry) => entry.id === id);
  if (!item) {
    selectors.editDialog.close();
    return;
  }

  item.title = title;
  item.details = details;
  item.datetime = datetime || null;
  item.tags = tags;
  item.updatedAt = new Date().toISOString();
  persistItems();
  selectors.editDialog.close();
  render();
}

function parseTags(value) {
  return value
    ? value
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean)
        .map((tag) => tag.toLowerCase())
    : [];
}

function loadItems() {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
    state.items = Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('Failed to load saved items', error);
    state.items = [];
  }
}

function persistItems() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.items));
}

function render() {
  updateCounts();
  renderLists();
  renderTags();
}

function updateCounts() {
  const counts = state.items.reduce(
    (acc, item) => {
      acc[item.type] += 1;
      return acc;
    },
    { note: 0, reminder: 0, task: 0 }
  );

  selectors.counts.note.textContent = counts.note;
  selectors.counts.reminder.textContent = counts.reminder;
  selectors.counts.task.textContent = counts.task;
}

function renderLists() {
  Object.entries(selectors.lists).forEach(([type, container]) => {
    container.innerHTML = '';
    const filtered = getFilteredItems().filter((item) => item.type === type);

    if (filtered.length === 0) {
      container.append(createEmptyState());
      return;
    }

    filtered
      .sort((a, b) => new Date(a.datetime || a.createdAt) - new Date(b.datetime || b.createdAt))
      .forEach((item) => {
        container.append(renderItem(item));
      });
  });
}

function getFilteredItems() {
  return state.items.filter((item) => {
    if (state.filters.type !== 'all' && item.type !== state.filters.type) {
      return false;
    }

    if (state.filters.tag !== 'all' && !item.tags.includes(state.filters.tag)) {
      return false;
    }

    if (state.filters.search) {
      const searchIn = `${item.title} ${item.details}`.toLowerCase();
      if (!searchIn.includes(state.filters.search)) {
        return false;
      }
    }

    return true;
  });
}

function renderItem(item) {
  const node = selectors.templates.item.content.cloneNode(true);
  const article = node.querySelector('.item');
  article.dataset.id = item.id;
  article.classList.toggle('completed', item.completed);

  node.querySelector('.item__type .icon').textContent = typeConfig[item.type].icon;
  node.querySelector('.item__type-label').textContent = typeConfig[item.type].label;
  node.querySelector('.item__title').textContent = item.title;
  node.querySelector('.item__details').textContent = item.details || 'No additional details.';

  const timeElement = node.querySelector('.item__time');
  if (item.datetime) {
    timeElement.textContent = formatDate(item.datetime);
  } else {
    timeElement.textContent = `Added ${formatRelative(item.createdAt)}`;
  }

  const tagContainer = node.querySelector('.item__tags');
  tagContainer.innerHTML = '';
  if (item.tags.length > 0) {
    item.tags.forEach((tag) => {
      const chip = selectors.templates.chip.content.cloneNode(true);
      chip.querySelector('.tag').textContent = `#${tag}`;
      tagContainer.append(chip);
    });
  }

  node.querySelector('[data-action="toggle-complete"]').addEventListener('click', () => toggleComplete(item.id));
  node.querySelector('[data-action="delete"]').addEventListener('click', () => deleteItem(item.id));
  node.querySelector('[data-action="edit"]').addEventListener('click', () => openEditDialog(item));

  return node;
}

function renderTags() {
  const container = selectors.tagFilters;
  const existingSelection = state.filters.tag;
  container.innerHTML = '';

  const tags = Array.from(
    new Set(
      state.items.flatMap((item) => item.tags).filter((tag) => tag && tag.trim().length > 0)
    )
  ).sort();

  if (tags.length === 0) {
    const placeholder = document.createElement('p');
    placeholder.className = 'chips-placeholder';
    placeholder.textContent = 'Tags appear as you add items.';
    container.append(placeholder);
    state.filters.tag = 'all';
    return;
  }

  const allChip = createChip('All tags', 'all');
  container.append(allChip);

  tags.forEach((tag) => {
    const chip = createChip(`#${tag}`, tag);
    container.append(chip);
  });

  const selectedChip =
    Array.from(container.querySelectorAll('.chip')).find((chip) => chip.dataset.tag === existingSelection) ||
    allChip;
  setSelectedChip(container, selectedChip);
  state.filters.tag = selectedChip.dataset.tag;
}

function createChip(label, value) {
  const button = document.createElement('button');
  button.className = 'chip';
  button.type = 'button';
  button.dataset.tag = value;
  button.textContent = label;
  return button;
}

function setSelectedChip(container, selected) {
  container.querySelectorAll('.chip').forEach((chip) => chip.classList.remove('selected'));
  selected.classList.add('selected');
}

function createEmptyState() {
  const placeholder = document.createElement('div');
  placeholder.className = 'empty-state';
  placeholder.textContent = 'Nothing here yet. Add something to keep this list active.';
  return placeholder;
}

function toggleComplete(id) {
  const item = state.items.find((entry) => entry.id === id);
  if (!item) return;
  item.completed = !item.completed;
  item.updatedAt = new Date().toISOString();
  persistItems();
  render();
}

function deleteItem(id) {
  const confirmed = confirm('Delete this item? This cannot be undone.');
  if (!confirmed) return;

  state.items = state.items.filter((entry) => entry.id !== id);
  persistItems();
  render();
}

function openEditDialog(item) {
  if (!selectors.editDialog.open) {
    selectors.editDialog.showModal();
  }
  selectors.editForm.elements.id.value = item.id;
  selectors.editForm.elements.title.value = item.title;
  selectors.editForm.elements.details.value = item.details || '';
  selectors.editForm.elements.datetime.value = item.datetime || '';
  selectors.editForm.elements.tags.value = item.tags.join(', ');
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return 'No date';
  return date.toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
}

function formatRelative(value) {
  const date = new Date(value);
  const formatter = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' });
  const diff = date - new Date();
  const minutes = Math.round(diff / (1000 * 60));
  const hours = Math.round(diff / (1000 * 60 * 60));
  const days = Math.round(diff / (1000 * 60 * 60 * 24));

  if (Math.abs(minutes) < 60) {
    return formatter.format(minutes, 'minute');
  }
  if (Math.abs(hours) < 24) {
    return formatter.format(hours, 'hour');
  }
  return formatter.format(days, 'day');
}

