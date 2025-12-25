document.addEventListener('DOMContentLoaded', () => {
    const switches = document.querySelectorAll('.switch');
    const nicheCounts = document.querySelectorAll('.niche-count');
    const timePicker = document.getElementById('dailyTime');
    const btnRunNow = document.getElementById('btnRunNow');
    const statusText = document.getElementById('statusText');
    const accountSwitcher = document.getElementById('accountSwitcher');

    // Switch Accounts
    accountSwitcher.addEventListener('change', async () => {
        const account = accountSwitcher.value;
        try {
            await axios.post('/api/switch_account', { account });
            showNotification('Switched to ' + account);
            location.reload(); // Reload to refresh settings
        } catch (err) {
            showNotification('Failed to switch account', 'error');
        }
    });

    // Toggle Niches
    switches.forEach(sw => {
        sw.addEventListener('click', async () => {
            sw.classList.toggle('active');
            const niche = sw.dataset.niche;
            const enabled = sw.classList.contains('active');

            await updateNicheSetting(niche, { enabled });
        });
    });

    // Update Niche Counts
    nicheCounts.forEach(input => {
        input.addEventListener('change', async () => {
            const niche = input.dataset.niche;
            const daily_count = parseInt(input.value);

            await updateNicheSetting(niche, { daily_count });
        });
    });

    // Update Schedule Time
    timePicker.addEventListener('change', async () => {
        const schedule_time = timePicker.value;
        await axios.post('/api/settings', { schedule_time });
        showNotification('Schedule updated to ' + schedule_time);
    });

    // Run All Now
    btnRunNow.addEventListener('click', async () => {
        btnRunNow.disabled = true;
        btnRunNow.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
        statusText.innerText = 'Processing...';

        try {
            await axios.post('/api/run');
            showNotification('Pipeline started successfully!');
        } catch (err) {
            showNotification('Failed to start pipeline', 'error');
        }
    });

    async function updateNicheSetting(nicheName, update) {
        try {
            const res = await axios.get('/api/settings');
            const settings = res.data;
            settings.niches[nicheName] = { ...settings.niches[nicheName], ...update };
            await axios.post('/api/settings', settings);
            showNotification(nicheName + ' updated');
        } catch (err) {
            console.error('Update failed:', err);
        }
    }

    function showNotification(msg, type = 'success') {
        const toast = document.createElement('div');
        toast.style.position = 'fixed';
        toast.style.bottom = '2rem';
        toast.style.right = '2rem';
        toast.style.padding = '1rem 2rem';
        toast.style.borderRadius = '12px';
        toast.style.background = type === 'success' ? 'var(--accent-primary)' : '#ff4444';
        toast.style.color = 'white';
        toast.style.zIndex = '1000';
        toast.style.boxShadow = 'var(--card-shadow)';
        toast.innerText = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
});
