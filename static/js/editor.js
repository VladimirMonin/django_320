function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

document.addEventListener('DOMContentLoaded', function() {
    const textArea = document.getElementById('id_text');
    if (textArea) {
        const easyMDE = new EasyMDE({
            element: textArea,
            spellChecker: false,
            autosave: {
                enabled: true,
                delay: 1000,
                uniqueId: 'post_editor'
            },
            toolbar: [
                'bold', 'italic', 'heading', '|',
                'quote', 'code', 'unordered-list', 'ordered-list', '|',
                'link', 'image', '|',
                'preview', 'side-by-side', 'fullscreen'
            ],
            previewRender: function(plainText, preview) {
                fetch('/blog/preview/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify({text: plainText})
                })
                .then(response => response.json())
                .then(data => {
                    preview.innerHTML = data.html;
                    hljs.highlightAll();
                })
                .catch(error => {
                    preview.innerHTML = "<p class='text-danger'>Ошибка при загрузке предпросмотра</p>";
                });
                return "Загрузка предпросмотра...";
            }
        });

        const form = document.getElementById('post-form');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                textArea.value = easyMDE.value();
                const formData = new FormData(form);

                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка сети');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        const toastElement = document.createElement('div');
                        toastElement.className = 'toast align-items-center text-white bg-success border-0';
                        toastElement.setAttribute('role', 'alert');
                        toastElement.setAttribute('aria-live', 'assertive');
                        toastElement.setAttribute('aria-atomic', 'true');
                        
                        toastElement.innerHTML = `
                            <div class="d-flex">
                                <div class="toast-body">
                                    ${data.message}
                                </div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                            </div>
                        `;
                        
                        document.querySelector('.toast-container').appendChild(toastElement);
                        const toast = new bootstrap.Toast(toastElement);
                        toast.show();
                        
                        if (data.redirect_url) {
                            setTimeout(() => {
                                window.location.href = data.redirect_url;
                            }, 1000);
                        }
                    }
                })
                .catch(error => {
                    const toastElement = document.createElement('div');
                    toastElement.className = 'toast align-items-center text-white bg-danger border-0';
                    toastElement.setAttribute('role', 'alert');
                    toastElement.setAttribute('aria-live', 'assertive');
                    toastElement.setAttribute('aria-atomic', 'true');
                    
                    toastElement.innerHTML = `
                        <div class="d-flex">
                            <div class="toast-body">
                                Произошла ошибка при сохранении поста
                            </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                        </div>
                    `;
                    
                    document.querySelector('.toast-container').appendChild(toastElement);
                    const toast = new bootstrap.Toast(toastElement);
                    toast.show();
                });
            });
        }
    }});
