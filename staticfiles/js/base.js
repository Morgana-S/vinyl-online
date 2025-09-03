document.addEventListener('DOMContentLoaded', function () {
	toolTipInit();
	asyncSearch();
});

// Initializes tooltips
function toolTipInit() {
	const toolTipTriggerList = document.querySelectorAll(
		'[data-bs-toggle="tooltip"]'
	);
	const tooltipList = [...toolTipTriggerList].map(
		(tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
	);
}

// Enables async search results
function asyncSearch() {
	let debounceTimer;
	$('#search-input').on('input', function () {
		clearTimeout(debounceTimer);

		debounceTimer = setTimeout(function () {
			var query = $('#search-input').val();
			if (query.length < 2) {
				$('#search-results').empty();
				return;
			}

			$.ajax({
				url: '/async-search/',
				data: { q: query },
				dataType: 'json',
				success: function (data) {
					var resultsHtml = '';
					if (data.length === 0) {
						resultsHtml =
							'<div class="list-group-item"> No Results Found </div>';
					} else {
						data.forEach(function (item) {
							if (item.type == 'record') {
								resultsHtml += `<a href="/record/${item.slug}" class="list-group-item list-group-item-action">${item.name} <span class="ms-2 float-end badge rounded-pill bg-dark">Record</span></a>`;
							} else {
								resultsHtml += `<a href="/artist/${item.slug}" class="list-group-item list-group-item-action">${item.name}<span class="ms-2 float-end badge rounded-pill bg-success">Artist</span></a>`;
							}
						});
					}
					$('#search-results').html(resultsHtml);
				},
			});
		}, 200);
	});
}

// Close async search results when clicking outside the search input
$(document).on('click', function (e) {
	if (
		!$(e.target).closest('#search-input').length &&
		!$(e.target).closest('#search-results').length
	) {
		$('#search-results').empty();
	}
});
