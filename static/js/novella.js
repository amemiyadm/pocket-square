export const el = (tag, className = '', textContent = '', dataset = {}) => {
    const element = document.createElement(tag);
    Object.assign(element, { className, textContent });
    Object.assign(element.dataset, dataset);

    return element;
}

export const setFloatingPosition = (anchor, target) => {
    const rect = anchor.getBoundingClientRect();
    target.style.top = (rect.bottom + window.scrollY) + 'px';
    target.style.left = (rect.left + window.scrollX) + 'px';
    target.style.width = rect.width + 'px';
}

export const resizeMonitor = (active) => {
    window.addEventListener('resize', () => {
        const target = active.obj;

        if (!target) return;

        setFloatingPosition(target.input, target.container);
    });
}

export const clickOutside = (active) => {
    document.addEventListener('click', (e) => {
        const activeObj = active.obj;

        if (!activeObj || (e.target === activeObj.inputEl) || activeObj.container.contains(e.target)) return;

        activeObj.close();
    });
}

export const removeEmptyParams = () => {
    const currentUrl = new URL(window.location.href);
    const nextUrl = new URL(currentUrl.href);
    const nextParams = new URLSearchParams();

    for (const [key, value] of currentUrl.searchParams.entries()) {
        if (value !== '') {
            nextParams.append(key, value);
        }
    }

    nextUrl.search = nextParams.toString();

    if (nextUrl.href !== currentUrl.href) {
        window.history.replaceState(null, '', nextUrl.href);
    }
}

export const kataToHira = (str) => {
    return str.replace(/[\u30A1-\u30F6]/g, (match) => {
        return String.fromCharCode(match.charCodeAt(0) - 0x60);
    });
}
