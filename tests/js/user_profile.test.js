/**
 * @jest-environment jsdom
 */

const { deleteAddressButtonInit } = require('../../static/js/user_profile.js');

// Mock Bootstrap Modal
global.bootstrap = {
  Modal: jest.fn().mockImplementation(() => ({ show: jest.fn() })),
};

describe('deleteAddressButtonInit', () => {
  let deleteForm, modalInstance;

  beforeEach(() => {
    document.body.innerHTML = `
      <button class="delete-button" data-url="/address/1/delete"></button>
      <button class="delete-button" data-url="/address/2/delete"></button>
      <div id="delete-address-modal"></div>
      <form id="delete-address-form"></form>
    `;

    deleteForm = document.getElementById('delete-address-form');

    deleteAddressButtonInit();

    // Grab the modal instance created by bootstrap.Modal
    modalInstance = bootstrap.Modal.mock.results[0].value;
  });

  test('Clicking first delete button sets form action and shows modal', () => {
    const firstButton = document.querySelectorAll('.delete-button')[0];
    firstButton.click();

    expect(deleteForm.getAttribute('action')).toBe('/address/1/delete');
    expect(modalInstance.show).toHaveBeenCalled();
  });

  test('Clicking second delete button sets form action and shows modal', () => {
    const secondButton = document.querySelectorAll('.delete-button')[1];
    secondButton.click();

    expect(deleteForm.getAttribute('action')).toBe('/address/2/delete');
    expect(modalInstance.show).toHaveBeenCalled();
  });
});