document.addEventListener('DOMContentLoaded', function () {
	toolTipInit();
});

function toolTipInit() {
	const toolTipTriggerList = document.querySelectorAll(
		'[data-bs-toggle="tooltip"]'
	);
	const tooltipList = [...toolTipTriggerList].map(
		(tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
	);
}
