class Fauna {
    children = {};
    items = new Set();
}

export class Ceres {
    root = new Fauna();

    constructor(data, limit) {
        this.limit = limit;

        for (const item of data) {
            for (const word of item.keywords) {
                this.insert(word, item);
            }
        }
    }

    insert(word, item) {
        let node = this.root;

        for (const char of word) {
            let childe = node.children[char];

            if (!childe) {
                childe = new Fauna();
                node.children[char] = childe;
            }

            node = childe;
            node.items.add(item);
        }
    }

    search(query) {
        let node = this.root;

        for (const char of query) {
            const childe = node.children[char];

            if (!childe) return [];

            node = childe;
        }

        const results = [];

        for (const item of node.items) {
            results.push(item);

            if (results.length === this.limit) break;
        }

        return results;
    }
}
