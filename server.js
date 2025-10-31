require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
app.use(express.json());

// 🧠 Tạm lưu user trong bộ nhớ (demo, chưa có database)
const users = [];

// ----------------------------
// 🔹 1. REGISTER
// ----------------------------
app.post('/register', async (req, res) => {
    const { email, password } = req.body;

    const existing = users.find(u => u.email === email);
    if (existing) return res.status(400).json({ message: 'Email already exists' });

    const hashed = await bcrypt.hash(password, 10);
    users.push({ email, password: hashed });

    res.json({ message: '✅ User registered successfully' });
});

// ----------------------------
// 🔹 2. LOGIN → Tạo token
// ----------------------------
app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    const user = users.find(u => u.email === email);
    if (!user) return res.status(404).json({ message: 'User not found' });

    const match = await bcrypt.compare(password, user.password);
    if (!match) return res.status(401).json({ message: 'Invalid password' });

    // Tạo token
    const token = jwt.sign(
        { email },
        process.env.JWT_SECRET,
        { expiresIn: process.env.JWT_EXPIRES }
    );

    res.json({ token });
});

// ----------------------------
// 🔹 Middleware kiểm tra token
// ----------------------------
function verifyToken(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader) return res.status(401).json({ message: 'Missing Authorization header' });

    const token = authHeader.split(' ')[1];
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        res.status(401).json({ message: 'Invalid or expired token' });
    }
}

// ----------------------------
// 🔹 3. Protected route
// ----------------------------
app.get('/profile', verifyToken, (req, res) => {
    res.json({
        message: '🔒 Protected route accessed!',
        user: req.user
    });
});

// ----------------------------
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
