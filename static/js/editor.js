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
                    console.error('Ошибка при получении предпросмотра:', error);
                    preview.innerHTML = "<p class='text-danger'>Ошибка при загрузке предпросмотра</p>";
                });
                return "Загрузка предпросмотра...";
            }
        });

        // Добавляем обработчик отправки формы
        const form = document.getElementById('post-form');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Синхронизируем значение редактора с textarea перед отправкой
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
                    if (response.ok) {
                        window.location.href = response.url;
                        return;
                    }
                    throw new Error('Ошибка при отправке формы');
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
            });
        }
    }
});
