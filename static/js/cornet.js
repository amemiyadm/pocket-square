import { el } from './novella.js';

export class Cornet {
    constructor() {
        this.showArea = el('div', 'cornet-show-area');
        document.body.append(this.showArea);
    }

    show(message, duration = 2500) {
        const motion = el('div', 'cornet-motion');
        const spacer = el('div', 'cornet-spacer');
        const surface = el('div', 'cornet-surface');
        const text = el('span', '', message)
        const closeBtn = el('button', 'cornet-close-btn', '✕');
        closeBtn.type = 'button';
        let timerId;
        const hideMotion = () => {
            clearTimeout(timerId);
            this.#hide(motion);
        };
        surface.append(text, closeBtn);
        spacer.append(surface);
        motion.append(spacer);
        this.showArea.append(motion);
        motion.offsetHeight;
        motion.style.maxHeight = motion.scrollHeight + 'px';

        if (duration > 0) {
            timerId = setTimeout(hideMotion, duration);
        }

        closeBtn.addEventListener('click', hideMotion);
        return { hide: () => hideMotion }
    }

    #hide(motion) {
        if (motion.dataset.closed === 'true') return;

        motion.dataset.closed = 'true';
        motion.style.opacity = '0';
        motion.addEventListener('transitionend', function handler(e) {
            if (e.target !== motion || e.propertyName !== 'opacity') return;

            motion.removeEventListener('transitionend', handler);
            motion.style.maxHeight = '0px';
            motion.addEventListener('transitionend', function handler(e) {
                if (e.target !== motion || e.propertyName !== 'max-height') return;

                motion.removeEventListener('transitionend', handler);
                motion.remove();
            });
        });
    }

    destroy() {
        this.showArea.remove();
    }
}
