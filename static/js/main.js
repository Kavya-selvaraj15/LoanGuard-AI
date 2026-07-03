/* LoanGuard AI – Main JS */

// ── API Helper ──────────────────────────────────────────────
const API = {
    token: localStorage.getItem('lg_access_token'),

    headers() {
        return {
            'Content-Type': 'application/json',
            ...(this.token ? { 'Authorization': `Bearer ${this.token}` } : {})
        };
    },

    async get(url) {
        const res = await fetch(url, { headers: this.headers() });
        return res.json();
    },

    async post(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            headers: this.headers(),
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async uploadFile(url, formData) {
        const headers = this.token ? { 'Authorization': `Bearer ${this.token}` } : {};
        const res = await fetch(url, { method: 'POST', headers, body: formData });
        return res.json();
    }
};

// ── Toast notifications ─────────────────────────────────────
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const colors = {
        success: 'rgba(46,213,115,0.15)',
        error: 'rgba(255,71,87,0.15)',
        info: 'rgba(0,212,255,0.15)',
        warning: 'rgba(255,165,2,0.15)'
    };
    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
    toast.style.cssText = `
        position:fixed;bottom:24px;right:24px;z-index:9999;
        background:${colors[type]};
        border:1px solid rgba(255,255,255,0.1);
        backdrop-filter:blur(10px);
        padding:14px 20px;border-radius:10px;
        font-family:'DM Sans',sans-serif;font-size:0.875rem;
        color:#e8eaf0;max-width:320px;
        display:flex;align-items:center;gap:10px;
        animation:slideIn 0.3s ease;
    `;
    toast.innerHTML = `<span>${icons[type]}</span><span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ── Number formatting ───────────────────────────────────────
function formatPercent(val) {
    return parseFloat(val).toFixed(1) + '%';
}

// ── Risk color helper ───────────────────────────────────────
function riskColor(level) {
    return level === 'dangerous' ? '#ff4757'
         : level === 'medium'    ? '#ffa502'
         : '#2ed573';
}

// ── Confirm dialog ──────────────────────────────────────────
function confirmAction(msg, callback) {
    if (window.confirm(msg)) callback();
}

// ── Copy to clipboard ───────────────────────────────────────
function copyText(text) {
    navigator.clipboard.writeText(text).then(() => showToast('Copied!', 'success'));
}

// ── CSS animations injected ─────────────────────────────────
const style = document.createElement('style');
style.textContent = `
@keyframes slideIn { from { transform: translateX(100px); opacity:0; } to { transform: translateX(0); opacity:1; } }
@keyframes fadeOut { to { opacity:0; transform: translateY(10px); } }
`;
document.head.appendChild(style);

// ── Active nav highlight ────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.getAttribute('href') && path.startsWith(item.getAttribute('href'))) {
            item.classList.add('active');
        }
    });
});
