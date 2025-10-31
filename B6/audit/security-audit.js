const fs = require('fs');
const path = require('path');

function scanDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            scanDir(fullPath);
        } else if (file.endsWith('.js')) {
            const content = fs.readFileSync(fullPath, 'utf-8');

            if (content.includes('console.log(token')) {
                console.warn(`⚠️ [${fullPath}] Log token detected!`);
            }

            if (content.includes('token=') || content.includes('Bearer ')) {
                console.info(`🔍 [${fullPath}] Token reference found.`);
            }

            if (content.includes('JWT_SECRET') && !content.includes('process.env.JWT_SECRET')) {
                console.error(`❌ [${fullPath}] Hard-coded secret detected!`);
            }
        }
    }
}

console.log('🔎 Running JWT Security Audit...');
scanDir(path.join(__dirname, '..'));
console.log('✅ Audit complete!');
