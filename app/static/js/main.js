document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('[role="alert"]');
    
    flashMessages.forEach(function(message) {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px)';
        message.style.transition = 'all 0.3s ease';
        setTimeout(function() {
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, 100);
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const contentTextarea = document.getElementById('content');
    
    if (contentTextarea) {
        const counter = document.createElement('div');
        counter.className = 'text-sm text-gray-500 mt-1';
        counter.id = 'char-counter';
        contentTextarea.parentNode.insertBefore(counter, contentTextarea.nextSibling);
        function updateCounter() {
            const count = contentTextarea.value.length;
            const words = contentTextarea.value.trim().split(/\s+/).filter(w => w.length > 0).length;
            counter.textContent = `Символов: ${count} | Слов: ${words}`;
        }
        contentTextarea.addEventListener('input', updateCounter);
        updateCounter();
    }
});

function confirmDelete(event, noteTitle) {
    if (!confirm(`Вы уверены, что хотите удалить заметку "${noteTitle}"?\n\nЭто действие нельзя отменить.`)) {
        event.preventDefault();
        return false;
    }
    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form[method="post"]');
    
    forms.forEach(function(form) {
        if (form.action.includes('/delete')) {
            return;
        }
        
        form.addEventListener('submit', function(event) {
            const titleInput = form.querySelector('input[name="title"]');
            const contentInput = form.querySelector('textarea[name="content"]');
            const categoryInput = form.querySelector('input[name="category"]');
            
            let errors = [];
            if (titleInput) {
                const title = titleInput.value.trim();
                if (!title) {
                    errors.push('Заголовок не может быть пустым');
                    titleInput.classList.add('border-red-500');
                } else if (title.length > 200) {
                    errors.push('Заголовок не может быть длиннее 200 символов');
                    titleInput.classList.add('border-red-500');
                } else {
                    titleInput.classList.remove('border-red-500');
                }
            }
            if (contentInput) {
                const content = contentInput.value.trim();
                if (!content) {
                    errors.push('Содержимое не может быть пустым');
                    contentInput.classList.add('border-red-500');
                } else {
                    contentInput.classList.remove('border-red-500');
                }
            }
            if (categoryInput) {
                const category = categoryInput.value.trim();
                if (!category) {
                    errors.push('Категория не может быть пустой');
                    categoryInput.classList.add('border-red-500');
                } else if (category.length > 100) {
                    errors.push('Категория не может быть длиннее 100 символов');
                    categoryInput.classList.add('border-red-500');
                } else {
                    categoryInput.classList.remove('border-red-500');
                }
            }
            if (errors.length > 0) {
                event.preventDefault();
                alert('Ошибки в форме:\n\n' + errors.join('\n'));
                return false;
            }
        });
    });
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

window.addEventListener('scroll', function() {
    const scrollButton = document.getElementById('scroll-top');
    if (scrollButton) {
        if (window.pageYOffset > 300) {
            scrollButton.classList.remove('hidden');
        } else {
            scrollButton.classList.add('hidden');
        }
    }
});
