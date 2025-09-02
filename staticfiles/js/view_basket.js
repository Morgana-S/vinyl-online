document.addEventListener('DOMContentLoaded', function () {
	document.querySelectorAll('.basket-qty').forEach((input) => {
		input.addEventListener('change', () => {
			input.form.submit();
		});
	});
});
