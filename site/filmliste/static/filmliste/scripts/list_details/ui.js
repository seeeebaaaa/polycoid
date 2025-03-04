/*\
 * ============
 * List Details
 * ============
\*/

/**
 *
 * This file only contains scripts relevant to the function of the ui. (Opening, Closing, resizing etc)
 *
 */

Number.prototype.clamp = function (min, max) {
  return Math.min(Math.max(this, min), max)
}
Number.prototype.round = function (decimals) {
  return Math.round(this * 10 ** decimals) / 10 ** decimals
}

$(document).ready(_ => {
  /*\
   * ===========
   * Search bars
   * ===========
  \*/
  // Hide/Show input box on button press
  $('.search-container .symbol button').on('click', event => {
    // get box
    const searchBox = $(event.currentTarget)
      .closest('.search-container')
      .find('.search-box')
    const input = searchBox.find('input')
    // change width and set active
    if (searchBox.width() === 0) {
      searchBox
        .animate({ width: '7em' }, 300)
        .find('button, input')
        .attr('tabindex', 0)
      input.focus()
    } else {
      searchBox
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
    }
  })
  //   Clear the input when X is pressed
  $('.search-container .search-box button').on('click', event => {
    const box = $(event.currentTarget).closest('.search-box')
    box.find('input').val('').focus().trigger('input') // trigger event to call search with empty value aka. reset
    box.find('button, input').attr('tabindex', -1)
  })
  // close box if empty on focus out
  $('.search-container .search-box input').on('focusout', event => {
    if ($(event.currentTarget).val() == '') {
      const searchBox = $(event.currentTarget)
        .closest('.search-container')
        .find('.search-box')
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
    }
  })
  /*\
   * ==============
   * Sorting Filter
   * ==============
  \*/
  // Hide/Show input box on button press
  $('.sort-container .symbol button').on('click', event => {
    // get box
    const sortBox = $(event.currentTarget)
      .closest('.sort-container')
      .find('.sort-box')
    const input = sortBox.find('input')
    // change width and set active
    if (sortBox.width() === 0) {
      sortBox
        .animate({ width: '7em' }, 300)
        .find('button, input')
        .attr('tabindex', 0)
      input.focus()
    } else {
      sortBox
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
      $(".dropdown").find(".dropdown-options").addClass("hidden")
    }
  })
  //   Hide Field when X is pressed
  $('.sort-container .sort-box button').on('click', event => {
    const sortBox = $(event.currentTarget)
        .closest('.sort-container')
        .find('.sort-box')
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
  })

  // dropwdown opening
  const $dropdown = $(".dropdown");
  const $selected = $dropdown.find(".dropdown-selected");
  const $options = $dropdown.find(".dropdown-options");

  // Append the options to the body
  $("body").append($options);

  // Adjust position and show options on click
  $selected.on("click", (e) => {
    const rect = $selected[0].getBoundingClientRect();
    const scrollTop = $(window).scrollTop();
    const scrollLeft = $(window).scrollLeft();
    
    const symbolWidth = $dropdown.closest(".sort-container").find(".symbol")[0].getBoundingClientRect().width
      $options.css({
          position: "absolute",
          top: `${rect.bottom+scrollTop}px`,
          left: `${rect.left+scrollLeft-symbolWidth}px`,
          width: `${rect.width+symbolWidth}px`,
          zIndex: 1000
      }).removeClass("hidden");
  });

  // Close dropdown on outside click
  $(document).on("click", (e) => {
    if (!e.target.closest(".dropdown") && !e.target.closest("button")) {
      // shrink sort box if dopdow nis already closed
      if ($options.hasClass("hidden")) {
        const sortBox = $(".sort .sort-box")
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
      } else 
      {// otherwise just close dropdown
        $options.addClass("hidden");}
        
    }
  });

  /*\
   * ===========
   * Profile Box
   * ===========
  \*/
  $('.nav>.profile>.symbol>button').on("click", event => {
    $(".profile-box").toggleClass("hidden")
    $(".bg-shadow#profile_box").toggleClass("hidden")
  })
  $('.bg-shadow#profile_box').on('click', event => {
    $('.profile-box').toggleClass('hidden')
    $(event.currentTarget).addClass('hidden')
  })
})
