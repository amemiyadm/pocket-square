import { Abyss } from './abyss.js';
import { Cornet } from './cornet.js';
import { Iroha } from './iroha.js';
import { removeEmptyParams } from './novella.js';
import pokemonData from '../json/pokemons.json' with { type: 'json' };
import itemData from '../json/items.json' with { type: 'json' };
import teraTypeData from '../json/tera_types.json' with { type: 'json' };
import moveData from '../json/moves.json' with { type: 'json' };
import abilityData from '../json/abilities.json' with { type: 'json' };

const cornet = new Cornet();

function setupAbyss() {
    const listMap = {
        'pokemon': pokemonData,
        'item': itemData,
        'tera-type': teraTypeData,
        'move': moveData,
        'ability': abilityData
    };

    for (const input of document.querySelectorAll('.abyss')) {
        new Abyss(input, listMap[input.dataset.abyssType], 4);
    }
}

function setupPokemonCounter() {
    const MAX_COUNT = 6;
    const MIN_COUNT = 1;
    const addButton = document.getElementById('pokemon-add');
    const subButton = document.getElementById('pokemon-sub');
    const countInput = document.getElementById('pokemon-slots');
    let current = parseInt(countInput.value, 10);
    addButton.addEventListener('click', () => {
        if (current >= MAX_COUNT) {
            addButton.dataset.irohaTarget = '';
            return;
        }

        current++;
        addButton.dataset.irohaTarget = `pokemon-status${current}`;
        subButton.dataset.irohaTarget = `pokemon-status${current}`;
        countInput.value = current;
    });
    subButton.addEventListener('click', () => {
        if (current <= MIN_COUNT) {
            subButton.dataset.irohaTarget = '';
            return;
        }

        addButton.dataset.irohaTarget = `pokemon-status${current}`;
        subButton.dataset.irohaTarget = `pokemon-status${current}`;
        current--;
        countInput.value = current;
    });
}

function setupPairAutoFill() {
    document.addEventListener('change', (e) => {
        const source = e.target;
        const pair = document.getElementById(source.dataset.pair);

        if (!pair) return;

        if (pair.value === '') {
            pair.value = source.value;
        }
    });
}

function setupPopstateScroll() {
    if ('scrollRestoration' in window.history) {
        window.history.scrollRestoration = 'manual';
    }

    window.addEventListener('popstate', async () => {
        loadSearchResult(window.location.href);
    });
}

function setupPagenation() {
    for (const pagination of document.querySelectorAll('.pagination')) {
        const url = new URL(window.location);
        pagination.addEventListener('click', async () => {
            url.searchParams.set('page', pagination.dataset.page);
            window.history.pushState(null, '', url);
            loadSearchResult(url.href);

        });
    }
}

async function loadSearchResult(href) {
    const searchResult = document.getElementById('search-result');
    const response = await fetch(href);
    const htmlString = await response.text();
    const newSearchResult = new DOMParser().parseFromString(htmlString, 'text/html').getElementById('search-result');
    searchResult.innerHTML = newSearchResult.innerHTML;
    searchResult.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
    setupPagenation();
    setupReadLater();
}

function setupReadLater() {
    for (const button of document.querySelectorAll('.read-later-button')) {
        button.addEventListener('click', async () => {
            const formData = new FormData();
            formData.append('article_id', button.dataset.articleId);
            const response = await fetch('/toggle-read-later', { method: 'POST', body: formData });
            const result = await response.json();

            if (!response.ok) {
                cornet.show(result.message);
                return;
            }

            button.dataset.added = String(result.is_added);
            cornet.show(result.message);
        });
    }
}

function init() {
    setupAbyss();
    setupPokemonCounter();
    setupPairAutoFill();
    setupPopstateScroll();
    setupPagenation();
    setupReadLater();
    Iroha.attachAll();
    removeEmptyParams();
}

init();
