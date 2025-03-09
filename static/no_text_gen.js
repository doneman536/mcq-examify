document.getElementById('no_text_form').addEventListener('submit',function() {
    setTimeout(() => {
        this.submit();
    }, 1000);
});