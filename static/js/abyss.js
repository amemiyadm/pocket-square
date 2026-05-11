import { Ceres } from './ceres.js';
import { el, setFloatingPosition, resizeMonitor, clickOutside } from './novella.js';

const cache = new WeakMap();
const active = { obj: null };
resizeMonitor(active);
clickOutside(active);

export class Abyss {
    container = el('ul', 'abyss-container');
    currentFocus = 0;

    constructor(input, data, limit = Infinity) {
        const list = data.list;
        this.input = input;
        this.image = data.image;
        this.root = cache.get(list) || (cache.set(list, this.root = new Ceres(list, limit)), this.root);
        this.input.addEventListener('input', () => this.handleInputInput());
        this.input.addEventListener('keydown', (e) => this.handleInputKeyDown(e));
        this.container.addEventListener('click', (e) => this.handleSuggestionClick(e));
        this.container.addEventListener('mouseover', (e) => this.handleSuggestionMouseover(e));
        document.body.appendChild(this.container);
    }

    handleInputInput() {
        const items = this.root.search(this.input.value);

        if (items.length === 0) {
            this.close();

            return;
        }

        const image = this.image;
        const suggestions = [];

        for (let i = 0; i < items.length; i++) {
            const label = items[i].label;
            const suggestion = el('li', 'abyss-suggestion', label, { value: label, index: i });

            if (image) {
                const icon = new Image(...image.size);
                icon.src = image.path + label + image.extension;
                icon.alt = label;
                Object.assign(icon.style, image.style);
                suggestion.prepend(icon);
            }

            suggestions.push(suggestion);
        }

        this.container.replaceChildren(...suggestions);
        this.currentFocus = 0;
        this.updateActiveItem();
        this.open();
    }

    handleSuggestionClick(e) {
        const target = e.target.closest('.abyss-suggestion');

        if (!target) return;

        this.input.value = target.dataset.value;
        this.close();
    }

    handleSuggestionMouseover(e) {
        const target = e.target.closest('.abyss-suggestion');

        if (!target) return;

        this.currentFocus = Number(target.dataset.index);
        this.updateActiveItem();
    }

    handleInputKeyDown(e) {
        if (this.container.dataset.abyssOpen !== 'true') return;

        const { key, isComposing } = e;

        if (key === 'Enter' && !isComposing) {
            e.preventDefault();
            this.container.children[this.currentFocus].click();

            return;
        }

        if (key === 'Escape') {
            e.preventDefault();
            this.close();

            return;
        }

        if (key === 'ArrowUp' || key === 'ArrowDown') {
            e.preventDefault();
            const len = this.container.children.length;
            this.currentFocus = (this.currentFocus + (key === 'ArrowDown' ? 1 : len - 1)) % len;
            this.updateActiveItem();
        }
    }

    open() {
        if (this.container.dataset.abyssOpen === 'true') return;

        if (active.obj) {
            active.obj.close();
        }

        this.container.dataset.abyssOpen = 'true';
        active.obj = this;
        setFloatingPosition(this.input.parentElement, this.container);
    }

    close() {
        if (this.container.dataset.abyssOpen === 'false') return;

        this.container.dataset.abyssOpen = 'false';
        active.obj = null;
    }

    updateActiveItem() {
        this.container.querySelector('[data-abyss-active="true"]')?.removeAttribute('data-abyss-active');
        this.container.children[this.currentFocus].dataset.abyssActive = 'true';
    }
}
