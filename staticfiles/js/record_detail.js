$(document).ready(function () {
	// Average Rating
	const averageRating = $('#average-user-rating').data('average-rating');
	renderRatingStars('#average-user-rating', averageRating);

	// Clickable Thumbnails with preview going to main image
	$('.clickable').on('click', function () {
		const mainImage = $('#main-image');
		var tempSrc = mainImage.attr('src');
		var tempAlt = mainImage.attr('alt');
		mainImage.attr('src', $(this).attr('src'));
		mainImage.attr('alt', $(this).attr('alt'));
	});

	// Quantity Buttons
	$('.btn-outline-danger').click(function (e) {
		e.preventDefault();

		// Find the related input
		const $input = $(this).siblings('input.qty_input');
		let currentVal = parseInt($input.val());
		const min = parseInt($input.attr('min'));
		const max = parseInt($input.attr('max'));

		if ($(this).find('i').hasClass('fa-minus')) {
			if (currentVal > min) currentVal--;
		} else if ($(this).find('i').hasClass('fa-plus')) {
			if (currentVal < max) currentVal++;
		}

		$input.val(currentVal);
	});

	// Async add-to-basket function
	$(document).on('submit', '.add-to-basket-form', function (e) {
		e.preventDefault();

		const $form = $(this);
		const recordId = $form.find('input[name="record_id"]').val();
		const quantity = $form.find('input.qty_input').val();
		const csrfToken = $form.find('input[name="csrfmiddlewaretoken"]').val();

		$.ajax({
			url: $form.attr('action'),
			method: 'POST',
			data: {
				record_id: recordId,
				quantity: quantity,
				csrfmiddlewaretoken: csrfToken,
			},

			success: function (response) {
				const $badge = $('#basket-count')
				// Update basket count/visibility
				$badge.text(response.basket_count);
				if (response.basket_count > 0) {
					$badge.show();
				} else {
					$badge.hide();
				}
				// Show confirmation toast
				$('#toast-header-text').text(response.toast_header);
				$('#basket-toast-body').text(response.toast_message);
				const toastEl = document.getElementById('basket-toast');
				const toast = new bootstrap.Toast(toastEl);
				toast.show();
			},
			error: function (xhr) {
				// Show error toast
				$('#toast-header-text').text("Error");
				$('#basket-toast-body').text("Could not add item to basket.");
				const toastEl = document.getElementById('basket-toast');
				const toast = new bootstrap.Toast(toastEl);
				toast.show();
			},
		});
	});
});

// Converts user ratings to stars
function renderRatingStars(container, rating) {
	const maxStars = 5;
	let starsHtml = '';

	for (let i = 1; i <= maxStars; i++) {
		if (rating >= i) {
			starsHtml += '<i class="fa-solid fa-star text-warning"></i>';
		} else if (rating >= i - 0.5) {
			starsHtml += '<i class="fa-solid fa-star-half-stroke text-warning"></i>';
		} else {
			starsHtml += '<i class="fa-regular fa-star text-warning"></i>';
		}
	}

	$(container).html(starsHtml);
}
