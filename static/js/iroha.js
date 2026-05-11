export class Iroha {
    static attachAll() {
        for (const trigger of document.querySelectorAll('.iroha-trigger')) {
            const triggerData = trigger.dataset;
            new Iroha(trigger, document.getElementById(triggerData.irohaTarget), document.getElementById(triggerData.irohaArrow));
        }
    }

    constructor(trigger, panel = null, arrow = null) {
        this.trigger = trigger;
        this.panel = panel;
        this.arrow = arrow;
        this.trigger.addEventListener('click', this.toggle);
    }

    toggle = () => {
        const triggerData = this.trigger.dataset;
        const panel = this.panel ?? document.getElementById(triggerData.irohaTarget);

        if (!panel) return;

        const arrow = this.arrow ?? document.getElementById(triggerData.irohaArrow);

        if (arrow) {
            const arrowData = arrow.dataset;
            arrowData.irohaRotate = !Boolean(arrowData.irohaRotate === 'true');
        }

        const panelStyle = panel.style;
        const panelData = panel.dataset;
        const toOpen = (panelData.irohaOpen !== 'true');
        panelStyle.maxHeight = toOpen ? '0' : panel.scrollHeight + 'px';
        panel.offsetHeight;
        panelStyle.maxHeight = toOpen ? panel.scrollHeight + 'px' : '0';
        panelData.irohaOpen = String(toOpen);

        if (toOpen) {
            panel.addEventListener('transitionend', function handler(e) {
                if (e.propertyName !== 'max-height') return;

                if (panelData.irohaOpen === 'true') {
                    panelStyle.maxHeight = 'none';
                }

                panel.removeEventListener('transitionend', handler);
            });
        }
    }
}
