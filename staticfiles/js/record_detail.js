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