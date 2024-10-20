$(document).ready(_ => {
  /**
   * ===========
   * Search bars
   * ===========
   */

  $('.search-container button').on('click', event => {
    // get box
    const searchBox = $(event.currentTarget)
      .closest('.search-container')
      .find('.search-box')
    const input = searchBox.find('input')
    // change width and set active
    if (searchBox.width() === 0) {
      searchBox.animate({ width: '6em' }, 300)
      input.focus()
    } else {
      searchBox.animate({ width: '0em' }, 300)
    }
  })
})
