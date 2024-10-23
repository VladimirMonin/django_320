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
                // Асинхронно обновляем содержимое предпросмотра
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
                    // Подсветка синтаксиса
                    hljs.highlightAll();
                })
                .catch(error => {
                    console.error('Ошибка при получении предпросмотра:', error);
                    preview.innerHTML = "<p class='text-danger'>Ошибка при загрузке предпросмотра</p>";
                });
                return "Загрузка предпросмотра..."; // Пока загружается, отображаем это сообщение
            }
        });
    }
});
