/**
 * @jest-environment jsdom
 */

const $ = require('jquery');
global.$ = $;

// Mock Bootstrap Tooltip
global.bootstrap = {
	Tooltip: jest.fn(),
};

// Mock Ajax
$.ajax = jest.fn();

// Import after defining mocks
const { toolTipInit, asyncSearch } = require('../../static/js/base.js');

beforeEach(() => {
	document.body.innerHTML = `
    <input id="search-input" />
    <div id="search-results"></div>
    <button data-bs-toggle="tooltip" title="info">Hover me</button>
    `;
});
jest.clearAllMocks();

test('toolTipInit initializes Bootstrap tooltips', () => {
	// Call directly since DOMContentLoaded already fired
	toolTipInit();
	const btn = document.querySelector('[data-bs-toggle="tooltip"]');
	expect(bootstrap.Tooltip).toHaveBeenCalledWith(btn);
});

test('asyncSearch clears results if query < 2 chars', () => {
	jest.useFakeTimers();
	$('#search-input').val('a').trigger('input');

	jest.advanceTimersByTime(200);

	expect($('#search-results').html()).toBe('');
	expect($.ajax).not.toHaveBeenCalled();
});

test('asyncSearch makes AJAX call for valid query', () => {
	asyncSearch();
	jest.useFakeTimers();

	$('#search-input').val('abc').trigger('input');

	jest.advanceTimersByTime(200);

	expect($.ajax).toHaveBeenCalledWith(
		expect.objectContaining({
			url: '/async-search/',
			data: { q: 'abc' },
		})
	);
});

test('aSyncSearch renders results on success', () => {
	asyncSearch();
	jest.useFakeTimers();

	$.ajax.mockImplementation(({ success }) =>
		success([{ type: 'record', slug: 'slug1', name: 'test record' }])
	);

	$('#search-input').val('abc').trigger('input');
	jest.advanceTimersByTime(200);

	expect($('#search-results').html()).toContain('test record');
});

test('Click outside search clears results', () => {
	$('#search-results').html('<div>Result</div>');
	$(document).trigger($.Event('click', { target: document.body }));

	expect($('#search-results').html()).toBe('');
});
