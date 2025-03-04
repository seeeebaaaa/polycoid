/*\
 * ============
 * List Details
 * ============
\*/

/**
 *
 * This document contains all scripts relted to functions of ui elements that dont rely only on style.
 *
 */

$(document).ready(_ => {
  /**
   * ===========
   * Search bars
   * ===========
   */
  $('.search-container .search-box input').on('input', event => {
    const element_container = $(event.currentTarget)
      .closest('.box')
      .find('.container .card-container')
    const search = $(event.currentTarget).val().toLocaleLowerCase()
    element_container.children().each((idx, el) => {
      const title = $(el).find('div>.text-mirror').text().toLocaleLowerCase()
      if (title.includes(search))
        $(el).show()
      else
        $(el).hide()
    })
  })


})
