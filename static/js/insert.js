import { Abyss } from './abyss.js';
import pokemonData from '../json/pokemons.json' with { type: 'json' };
import itemData from '../json/items.json' with { type: 'json' };
import teraTypeData from '../json/tera_types.json' with { type: 'json' };
import moveData from '../json/moves.json' with { type: 'json' };
import abilityData from '../json/abilities.json' with { type: 'json' };
import natureData from '../json/natures.json' with { type: 'json' };

function setupAbyss() {
    const listMap = {
        'pokemon': pokemonData,
        'item': itemData,
        'tera-type': teraTypeData,
        'move': moveData,
        'ability': abilityData,
        'nature': natureData
    };

    for (const input of document.querySelectorAll('.abyss')) {
        new Abyss(input, listMap[input.dataset.abyssType], 4);
    }
}

function init() {
    setupAbyss();
}

init();
