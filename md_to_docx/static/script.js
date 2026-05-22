let selectedFile = null;

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    document.getElementById(`${tab}-tab`).classList.add('active');
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    selectedFile = file;
    const fileNameEl = document.getElementById('fileName');
    fileNameEl.textContent = `✓ ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    fileNameEl.hidden = false;
}

function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.currentTarget.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
    const file = event.dataTransfer.files[0];
    if (file && (file.name.endsWith('.md') || file.name.endsWith('.markdown'))) {
        selectedFile = file;
        const fileNameEl = document.getElementById('fileName');
        fileNameEl.textContent = `✓ ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        fileNameEl.hidden = false;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    if (dropZone) {
        dropZone.addEventListener('dragover', handleDragOver);
        dropZone.addEventListener('dragleave', handleDragLeave);
        dropZone.addEventListener('drop', handleDrop);
    }
});

async function convert() {
    const convertBtn = document.getElementById('convertBtn');
    const statusEl = document.getElementById('status');
    const btnText = convertBtn.querySelector('.btn-text');
    const btnLoader = convertBtn.querySelector('.btn-loader');

    convertBtn.disabled = true;
    btnText.textContent = 'جاري التحويل...';
    btnLoader.hidden = false;
    statusEl.hidden = true;

    try {
        const formData = new FormData();
        let hasContent = false;

        const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
        if (activeTab === 'upload' && selectedFile) {
            formData.append('file', selectedFile);
            hasContent = true;
        } else if (activeTab === 'paste') {
            const text = document.getElementById('markdownInput').value;
            if (text.trim()) {
                formData.append('text', text);
                hasContent = true;
            }
        }

        if (!hasContent) {
            showStatus('الرجاء رفع ملف أو لصق نص Markdown', 'error');
            resetButton();
            return;
        }

        formData.append('dir', document.getElementById('dirSelect').value);
        formData.append('cover_style', document.getElementById('coverStyle').value);
        formData.append('font_arabic', document.getElementById('fontArabic').value);
        formData.append('font_latin', document.getElementById('fontLatin').value);
        formData.append('page_number_format', document.getElementById('pageNumberFormat').value);
        formData.append('heading_numbering', document.getElementById('headingNumbering').checked);
        formData.append('toc', document.getElementById('tocCheck').checked);
        formData.append('lof', document.getElementById('lofCheck').checked);
        formData.append('lot', document.getElementById('lotCheck').checked);
        formData.append('diagrams', document.getElementById('diagramsCheck').checked);

        const title = document.getElementById('coverTitle').value;
        const author = document.getElementById('coverAuthor').value;
        const date = document.getElementById('coverDate').value;
        if (title || author || date) {
            const metadata = {
                title: title,
                author: author,
                date: date,
                dir: document.getElementById('dirSelect').value,
                cover_style: document.getElementById('coverStyle').value,
                fonts: {
                    arabic: document.getElementById('fontArabic').value,
                    latin: document.getElementById('fontLatin').value,
                }
            };
            const yaml = '---\n' + Object.entries(metadata)
                .filter(([k,v]) => v)
                .map(([k,v]) => {
                    if (typeof v === 'object') {
                        return k + ':\n' + Object.entries(v)
                            .map(([sk, sv]) => `  ${sk}: "${sv}"`).join('\n');
                    }
                    return `${k}: "${v}"`;
                }).join('\n') + '\n---\n';
            if (activeTab === 'paste') {
                formData.set('text', yaml + document.getElementById('markdownInput').value);
            } else {
                formData.set('text', yaml);
            }
        }

        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error || 'فشل التحويل');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const filename = selectedFile
            ? selectedFile.name.replace(/\.(md|markdown)$/i, '.docx')
            : 'converted.docx';
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);

        showStatus(`✓ تم التحويل بنجاح! تم تحميل ${filename}`, 'success');
    } catch (error) {
        showStatus(`✗ خطأ: ${error.message}`, 'error');
    } finally {
        resetButton();
    }
}

function showStatus(message, type) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = message;
    statusEl.className = `status ${type}`;
    statusEl.hidden = false;
}

function resetButton() {
    const convertBtn = document.getElementById('convertBtn');
    convertBtn.disabled = false;
    convertBtn.querySelector('.btn-text').textContent = 'تحويل وتحميل';
    convertBtn.querySelector('.btn-loader').hidden = true;
}