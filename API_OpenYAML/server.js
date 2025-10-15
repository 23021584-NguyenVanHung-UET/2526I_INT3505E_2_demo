const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
app.use(bodyParser.json());

// Load OpenAPI YAML
const swaggerDocument = YAML.load(path.join(__dirname, 'openapi_book_api.yaml'));

// Serve Swagger UI at /docs
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Very simple in-memory mock for /books endpoints to demo
let books = [
    { id: '1', title: 'Example Book', authors: [{ id: 'a1', name: 'Author A' }], published_date: '2020-01-01' }
];

app.get('/v1/books', (req, res) => {
    const { page = 1, per_page = 20, title } = req.query;
    let items = books;
    if (title) items = items.filter(b => b.title.toLowerCase().includes(title.toLowerCase()));
    res.json({ page: Number(page), per_page: Number(per_page), total: items.length, items });
});

app.post('/v1/books', (req, res) => {
    // In real app check auth. Here just accept payload.
    const body = req.body;
    const newBook = {
        id: (books.length + 1).toString(),
        title: body.title || 'Untitled',
        authors: body.author_ids ? body.author_ids.map((id) => ({ id, name: `Author ${id}` })) : [],
        published_date: body.published_date || null
    };
    books.push(newBook);
    res.status(201).json(newBook);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT} - Swagger UI: http://localhost:${PORT}/docs`));
